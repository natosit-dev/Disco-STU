"""Thin SERA view: presentation and explicit application-service commands only."""
from __future__ import annotations

import json
import os
import pandas as pd
import streamlit as st
from sera.application import SeraApplication

st.set_page_config(page_title='SERA · DiScO STU', page_icon='🐟', layout='wide')
st.title('🐟 SERA — Capture human intended meaning')
app = SeraApplication(os.environ.get('SERA_DATA_DIR', 'data'))
config = app.editor_spec()


def command(fn, *args, **kwargs):
    try:
        result = fn(*args, **kwargs)
    except (ValueError, RuntimeError, OSError) as exc:
        st.error(str(exc))
        return None
    st.rerun()
    return result


def rows(frame):
    # Presentation adapter; semantic validation and canonicalization occur in backend.
    return frame.where(pd.notna(frame), '').to_dict(orient='records')


records = app.list_samples()
ids = [r['sample_id'] for r in records]
options = ['Create a new sample', *ids]
focus = st.session_state.pop('_focus_sample', None)
if focus in options:
    st.session_state['sample_selection'] = focus
with st.sidebar:
    choice = st.selectbox('Sample', options, key='sample_selection')
    st.caption('Local only · All durable state lives in Python services')

if choice == 'Create a new sample':
    with st.form('new_source'):
        original = st.text_area('Original paragraph (≤200 words)')
        title = st.text_input('Title')
        origin = st.text_input('Origin / citation')
        date = st.text_input('Original date')
        domain = st.selectbox('Domain', config['domains'])
        context = st.text_area('Private context dependencies')
        submitted = st.form_submit_button('Create sample')
    if submitted:
        try:
            rec = app.create_sample(original, title=title, origin=origin,
                                    original_date=date, domain=domain,
                                    context_dependencies=context)
            st.session_state['_focus_sample'] = rec['sample_id']
            st.rerun()
        except (ValueError, RuntimeError, OSError) as exc:
            st.error(str(exc))
    st.stop()

record = app.get_sample(choice)
source = record['source']
st.subheader(source.get('title') or 'Sample ' + choice[:8])
st.caption(f"Sample: {choice} · Version: {record['version']} · {record['status'].upper()}")

if record['status'] == 'frozen':
    st.success('Frozen private Oracle — read only')
    st.markdown('**Original paragraph**')
    st.write(source['original_text'])
    st.markdown('**Intended meaning**')
    st.write(record['intention_free_text'])
    with st.expander('Category prose'):
        for key, question in config['categories'].items():
            st.markdown('**' + question + '**')
            st.write(record['category_prose'].get(key, ''))
    with st.expander('Semantic units and relationships'):
        st.dataframe(record['units'], hide_index=True)
        st.dataframe(record['relations'], hide_index=True)
    st.download_button('Download PRIVATE Oracle', json.dumps(record, ensure_ascii=False, indent=2),
                       file_name=f'private-oracle-{choice}-v{record["version"]}.json', mime='application/json')
    packet = app.model_packet(choice)
    st.download_button('Download source-only model packet', json.dumps(packet, ensure_ascii=False, indent=2),
                       file_name=f'stu-source-{choice}.json', mime='application/json')
    if st.button('Begin amendment (new version)'):
        command(app.begin_amendment, choice)
    st.stop()

st.markdown('### 1. Source')
with st.form('source_form'):
    original = st.text_area('Original text', value=source['original_text'],
                            disabled=bool(record.get('intention_saved_at')))
    title = st.text_input('Title', value=source.get('title', ''))
    origin = st.text_input('Origin', value=source.get('origin', ''))
    date = st.text_input('Original date', value=source.get('original_date', ''))
    domain = st.selectbox('Domain', config['domains'], index=config['domains'].index(source['domain']))
    context = st.text_area('Private context', value=source.get('context_dependencies', ''))
    save_source = st.form_submit_button('Save source/provenance')
if save_source:
    command(app.save_source, choice, original_text=original, title=title,
            origin=origin, original_date=date, domain=domain, context_dependencies=context)

st.markdown('### 2. What did you intend to communicate?')
with st.form('intention'):
    intention = st.text_area('Unrestricted explanation (before categories)',
                             value=record['intention_free_text'], height=190)
    save_intention = st.form_submit_button('Save unrestricted intention')
if save_intention:
    command(app.save_intention, choice, intention)
if not record.get('intention_saved_at'):
    st.info('Save your unrestricted intention to unlock categories.')
    st.stop()

st.markdown('### 3. Category explanations')
with st.form('categories'):
    prose = {key: st.text_area(prompt, value=record['category_prose'].get(key, ''),
                               key=f'{choice}-{key}-{record["explication_id"]}')
             for key, prompt in config['categories'].items()}
    save_categories = st.form_submit_button('Save category prose')
if save_categories:
    command(app.save_categories, choice, prose)
if not record.get('categories_saved_at'):
    st.info('Save categories (empty categories are valid) to unlock semantic structure.')
    st.stop()

st.markdown('### 4. Semantic units')
unit_columns = ['unit_id','kind','text','importance','polarity','source_support','notes']
with st.form('unit_editor'):
    units = st.data_editor(pd.DataFrame(record['units'], columns=unit_columns).fillna(''),
        num_rows='dynamic', hide_index=True,
        column_config={'kind': st.column_config.SelectboxColumn(options=config['unit_kinds']),
                       'importance': st.column_config.SelectboxColumn(options=config['importance']),
                       'polarity': st.column_config.SelectboxColumn(options=config['polarity'])})
    save_units = st.form_submit_button('Save semantic units')
if save_units:
    command(app.save_units, choice, rows(units))

st.markdown('### 4b. Directed relationships')
relation_columns = ['relation_id','from_unit_id','relation_type','to_unit_id','explanation']
with st.form('relation_editor'):
    relations = st.data_editor(pd.DataFrame(record['relations'], columns=relation_columns).fillna(''),
        num_rows='dynamic', hide_index=True,
        column_config={'relation_type': st.column_config.SelectboxColumn(options=config['relation_types'])})
    save_relations = st.form_submit_button('Save directed relationships')
if save_relations:
    command(app.save_relations, choice, rows(relations))

st.markdown('### 5. Review and freeze')
with st.expander('Inspect complete draft'):
    st.json(record)
errors = app.validation_errors(choice)
for item in errors:
    st.warning(item)
with st.form('freeze'):
    confirmed = st.checkbox('I reviewed these layers and want to freeze this Oracle version.')
    freeze = st.form_submit_button('Freeze private Oracle', disabled=bool(errors))
if freeze:
    if not confirmed:
        st.error('Explicit confirmation is required.')
    else:
        command(app.freeze, choice, expected_version=record['version'])
