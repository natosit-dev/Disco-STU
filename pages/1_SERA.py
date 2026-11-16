"""Human-first SERA capture. Immutable v0.1 drafts/freezes remain compatible."""
from __future__ import annotations

import json
import os

import pandas as pd
import streamlit as st
from sera.application import SeraApplication
from stu.presentation import display_datetime

st.set_page_config(page_title='SERA · Write and Explain', page_icon='🐟', layout='wide')
st.title('SERA · Write → Explain')
st.caption('Your unrestricted explanation is the human reference. Structured annotations are optional for new records.')
app = SeraApplication(os.environ.get('SERA_DATA_DIR', 'data'))
spec = app.editor_spec()


def command(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except (ValueError, RuntimeError, OSError, KeyError) as exc:
        st.error(str(exc))
        return
    st.rerun()


def rows(frame):
    return frame.where(pd.notna(frame), '').to_dict(orient='records')


records = app.list_samples()
lookup = {rec['sample_id']: rec for rec in records}
choices = ['new', *lookup]


def label(value):
    if value == 'new':
        return '+ New source'
    rec = lookup[value]
    title = rec['source'].get('title') or 'Untitled source'
    return f"{title} · {rec['status'].title()} v{rec['version']} · {value[:8]}"


focus = st.session_state.pop('_focus_sample', None)
if focus in choices:
    st.session_state['sera_choice'] = focus
choice = st.selectbox('Source', choices, format_func=label, key='sera_choice')

if choice == 'new':
    st.subheader('New writing')
    with st.form('new_source'):
        title = st.text_input('Title', placeholder='A short name for this writing')
        original = st.text_area('Original source · maximum 200 words', height=130)
        with st.expander('Optional provenance'):
            origin = st.text_input('Origin / citation')
            original_date = st.text_input('Original writing date (separate from capture time)')
            domain = st.selectbox('Domain', spec['domains'])
            context = st.text_area('Private contextual notes')
        create = st.form_submit_button('Create source', type='primary')
    if create:
        try:
            rec = app.create_sample(original, title=title, origin=origin,
                original_date=original_date, domain=domain,
                context_dependencies=context, schema_version=spec['v2_schema_version'])
            st.session_state['_focus_sample'] = rec['sample_id']
            st.rerun()
        except (ValueError, RuntimeError, OSError) as exc:
            st.error(str(exc))
    st.stop()

record = app.get_sample(choice)
source = record['source']
version = record.get('schema_version', '0.1.0')
st.subheader(source.get('title') or 'Untitled source')
st.caption(f"Captured {display_datetime(record['created_at'])} · "
           f"{record['status'].title()} · SERA contract {version} · "
           f"Record {choice[:8]}")

if record['status'] == 'frozen':
    st.success('Frozen authorial baseline · immutable')
    st.markdown('**Original source**')
    st.markdown(source['original_text'].replace('\n', '  \n'))
    st.markdown('**Your intended meaning**')
    st.write(record['intention_free_text'])
    if record.get('characteristics'):
        st.caption('Optional characteristics: ' + ', '.join(
            spec['characteristics'].get(x, x) for x in record['characteristics']))
    with st.expander('Additional human evidence and provenance'):
        st.json({'title': source.get('title'), 'origin': source.get('origin'),
                 'original_date': source.get('original_date'),
                 'domain': source.get('domain'),
                 'context_dependencies': source.get('context_dependencies')})
        for key, question in spec['categories'].items():
            value = record.get('category_prose', {}).get(key, '')
            if value:
                st.markdown('**' + question + '**')
                st.write(value)
        if record.get('units'):
            st.dataframe(record['units'], hide_index=True)
        if record.get('relations'):
            st.dataframe(record['relations'], hide_index=True)
    with st.expander('Private exports and amendment'):
        st.warning('Private Oracle exports contain authorial intention. Do not publish unreviewed.')
        st.download_button('Download private frozen Oracle',
            json.dumps(record, ensure_ascii=False, indent=2),
            file_name=f'private-oracle-{choice}-v{record["version"]}.json',
            mime='application/json')
        st.download_button('Download source-only model packet',
            json.dumps(app.model_packet(choice), ensure_ascii=False, indent=2),
            file_name=f'stu-source-{choice}.json', mime='application/json')
        if st.button('Begin new amendment version'):
            command(app.begin_amendment, choice)
    st.stop()

# v0.2 drafts: one Save action, one explicit Freeze, optional advanced work.
if version == spec['v2_schema_version']:
    st.markdown('**Original source**')
    if record.get('intention_saved_at'):
        st.caption('The original source was locked when you saved your intended meaning.')
    with st.form('human_capture_' + record['explication_id']):
        original = st.text_area('Original writing', value=source['original_text'],
                                height=125, disabled=bool(record.get('intention_saved_at')))
        title = st.text_input('Title', value=source.get('title', ''))
        st.markdown('**Your intended meaning**')
        intention = st.text_area('In your words, what were you trying to communicate?',
                                 value=record['intention_free_text'], height=220)
        st.markdown('**Optional characteristics**')
        st.caption('These checkboxes help organize a review. They do NOT encode a semantic graph.')
        characteristics = [key for key, description in spec['characteristics'].items()
                           if st.checkbox(description,
                               value=key in record.get('characteristics', []))]
        with st.expander('Optional guided explanation prompts'):
            prose = {key: st.text_area(question,
                     value=record['category_prose'].get(key, ''),
                     key='v2_prose_' + record['explication_id'] + '_' + key)
                     for key, question in spec['categories'].items()}
        with st.expander('Optional source provenance'):
            origin = st.text_input('Origin', value=source.get('origin', ''))
            original_date = st.text_input('Original writing date',
                                         value=source.get('original_date', ''))
            domain = st.selectbox('Domain', spec['domains'],
                index=spec['domains'].index(source.get('domain', 'other')))
            context = st.text_area('Private context',
                                   value=source.get('context_dependencies', ''))
        save = st.form_submit_button('Save draft', type='primary')
    if save:
        command(app.save_authoring_draft, choice, original_text=original, title=title,
                origin=origin, original_date=original_date, domain=domain,
                context_dependencies=context, intention=intention,
                characteristics=characteristics, category_prose=prose)

    with st.expander('Advanced: optional semantic units and relationships'):
        st.caption('These are voluntary annotations, not required for a frozen baseline.')
        unit_cols = ['unit_id', 'kind', 'text', 'importance', 'polarity',
                     'source_support', 'notes']
        relation_cols = ['relation_id', 'from_unit_id', 'relation_type',
                         'to_unit_id', 'explanation']
        with st.form('advanced_annotations_' + record['explication_id']):
            units = st.data_editor(pd.DataFrame(record['units'], columns=unit_cols).fillna(''),
                num_rows='dynamic', hide_index=True, key='optional_units_' + choice,
                column_config={
                    'kind': st.column_config.SelectboxColumn(options=spec['unit_kinds']),
                    'importance': st.column_config.SelectboxColumn(options=spec['importance']),
                    'polarity': st.column_config.SelectboxColumn(options=spec['polarity'])})
            relations = st.data_editor(
                pd.DataFrame(record['relations'], columns=relation_cols).fillna(''),
                num_rows='dynamic', hide_index=True, key='optional_relations_' + choice,
                column_config={
                    'relation_type': st.column_config.SelectboxColumn(
                        options=spec['relation_types'])})
            save_advanced = st.form_submit_button('Save optional annotations')
        if save_advanced:
            command(app.save_optional_annotations, choice, units=rows(units),
                    relations=rows(relations))

    st.markdown('**Freeze authorial baseline**')
    errors = app.validation_errors(choice)
    for error in errors:
        st.warning(error)
    with st.form('freeze_v2_' + record['explication_id']):
        confirmed = st.checkbox('I reviewed this explanation and want to freeze it.')
        freeze = st.form_submit_button('Freeze this version', disabled=bool(errors))
    if freeze:
        if confirmed:
            command(app.freeze, choice, expected_version=record['version'])
        else:
            st.error('Confirm the freeze first.')
    st.stop()

# v0.1 drafts remain editable under their ORIGINAL strict research contract.
st.warning('Legacy SERA v0.1 draft: this version retains the original progressive '
           'category + unit requirements. Its validation has not been relaxed.')
with st.form('legacy_source'):
    original = st.text_area('Original writing', value=source['original_text'],
                            disabled=bool(record.get('intention_saved_at')))
    title = st.text_input('Title', value=source.get('title', ''))
    with st.expander('Provenance'):
        origin = st.text_input('Origin', value=source.get('origin', ''))
        original_date = st.text_input('Original date', value=source.get('original_date', ''))
        domain = st.selectbox('Domain', spec['domains'],
                               index=spec['domains'].index(source['domain']))
        context = st.text_area('Private context',
                               value=source.get('context_dependencies', ''))
    save_source = st.form_submit_button('Save source')
if save_source:
    command(app.save_source, choice, original_text=original, title=title,
            origin=origin, original_date=original_date, domain=domain,
            context_dependencies=context)

with st.form('legacy_intention'):
    intention = st.text_area('Unrestricted authorial intention',
                             value=record['intention_free_text'], height=180)
    save_intention = st.form_submit_button('Save intention')
if save_intention:
    command(app.save_intention, choice, intention)
if not record.get('intention_saved_at'):
    st.info('Save your intention to continue the legacy v0.1 explication.')
    st.stop()

with st.form('legacy_categories'):
    prose = {key: st.text_area(question, value=record['category_prose'].get(key, ''))
             for key, question in spec['categories'].items()}
    save_categories = st.form_submit_button('Save category explanations')
if save_categories:
    command(app.save_categories, choice, prose)
if not record.get('categories_saved_at'):
    st.info('Legacy v0.1 requires saving category explanations.')
    st.stop()

with st.expander('Legacy semantic units and relations', expanded=True):
    unit_cols = ['unit_id', 'kind', 'text', 'importance', 'polarity',
                 'source_support', 'notes']
    relation_cols = ['relation_id', 'from_unit_id', 'relation_type',
                     'to_unit_id', 'explanation']
    with st.form('legacy_units'):
        units = st.data_editor(pd.DataFrame(record['units'], columns=unit_cols).fillna(''),
            num_rows='dynamic', hide_index=True,
            column_config={
                'kind': st.column_config.SelectboxColumn(options=spec['unit_kinds']),
                'importance': st.column_config.SelectboxColumn(options=spec['importance']),
                'polarity': st.column_config.SelectboxColumn(options=spec['polarity'])})
        save_units = st.form_submit_button('Save units')
    if save_units:
        command(app.save_units, choice, rows(units))
    with st.form('legacy_relations'):
        relations = st.data_editor(
            pd.DataFrame(record['relations'], columns=relation_cols).fillna(''),
            num_rows='dynamic', hide_index=True,
            column_config={
                'relation_type': st.column_config.SelectboxColumn(
                    options=spec['relation_types'])})
        save_relations = st.form_submit_button('Save relations')
    if save_relations:
        command(app.save_relations, choice, rows(relations))

errors = app.validation_errors(choice)
for error in errors:
    st.warning(error)
with st.form('legacy_freeze'):
    confirmed = st.checkbox('Freeze this legacy v0.1 baseline')
    freeze = st.form_submit_button('Freeze private Oracle', disabled=bool(errors))
if freeze:
    if confirmed:
        command(app.freeze, choice, expected_version=record['version'])
    else:
        st.error('Explicit confirmation is required.')
