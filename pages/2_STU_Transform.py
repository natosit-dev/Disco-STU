"""Thin Streamlit controller: explicit app-service commands, no SDK or storage access."""
from __future__ import annotations

import os
import streamlit as st
from stu.application import StuApplication
from stu.adaption_api import SUPPORTED_MODELS
from ui.adaption_credentials import render_api_key_input
from stu.presentation import model_name

st.set_page_config(page_title='STU · Transform', layout='wide')
st.title('Run a transformation')
st.caption('Choose a frozen source and model. Technical evidence is recorded automatically.')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))

with st.expander('Adaption API credential', expanded=True):
    key = render_api_key_input()
    st.caption('Key stays in this local Streamlit session; never saved to experiment artifacts.')

samples = app.capture.list_frozen_sources()
if not samples:
    st.info('Create and freeze a SERA source before running a model.')
    st.stop()

sample_options = [r['sample_id'] for r in samples]


def sample_label(sid):
    return next((r['source'].get('title') or sid[:8]
                 for r in samples if r['sample_id'] == sid), sid)


st.subheader('Create live experiment')
with st.form('new_live_study'):
    sample_id = st.selectbox('Frozen SERA source', sample_options,
                             format_func=sample_label)
    model_id = st.selectbox('Hosted model', SUPPORTED_MODELS,
                            format_func=model_name)
    create_live = st.form_submit_button('Create live study')
if create_live:
    try:
        study = app.create_study(sample_id, mode='live', model_id=model_id)
        st.session_state['active_study'] = study['study_id']
        st.rerun()
    except (ValueError, RuntimeError, OSError) as exc:
        st.error(str(exc))

with st.expander('Legacy regression fixtures — synthetic only', expanded=False):
    st.caption('Retained for repeatable testing. These are not empirical model responses.')
    with st.form('new_synthetic_study'):
        synthetic_source = st.selectbox('Frozen source', sample_options,
                                        format_func=sample_label, key='fixture_source')
        fixture_id = st.selectbox('Fixture', ['STRUCTURAL', 'F01','F02','F03','F04',
                                               'F05','F06','F07','F08','F09','F10'])
        create_synthetic = st.form_submit_button('Create synthetic test study')
    if create_synthetic:
        try:
            study = app.create_study(synthetic_source, fixture_id=fixture_id)
            st.session_state['active_study'] = study['study_id']
            st.rerun()
        except (ValueError, RuntimeError, OSError) as exc:
            st.error(str(exc))

studies = app.list_study_options()
if studies:
    st.subheader('Recorded studies')
    labels = {study['study_id']: study['label'] for study in studies}
    options = list(labels)
    current = st.session_state.get('active_study')
    selected = st.selectbox('Source and study', options,
        index=options.index(current) if current in options else 0,
        format_func=lambda sid: labels[sid])
    study = app.get_study(selected)
    live = study['mode'] == 'live'
    if live:
        st.caption('Hosted model: ' + model_name(study['model_id']))
        st.warning('One live experiment makes up to three potentially chargeable '
                   'independent API requests.')
    else:
        st.warning('Synthetic diagnostic study; outputs are not observations about an LLM.')
    disabled = live and not (key or os.environ.get('ADAPTION_API_KEY'))
    if st.button('Run model experiment' if live else 'Run synthetic regression',
                 type='primary', disabled=disabled):
        try:
            run = app.run_sample(selected, api_key=key if live else None)
            st.session_state['active_study'] = selected
            st.success('Recorded run: ' + run['status'].replace('_', ' '))
            st.rerun()
        except (ValueError, RuntimeError, OSError) as exc:
            st.error(str(exc))
    if disabled:
        st.info('Enter an API key above or configure ADAPTION_API_KEY in your local environment.')

    st.markdown('**Run history**')
    runs = app.list_review_runs(selected)
    if not runs:
        st.caption('This study has no recorded runs yet.')
    for run in runs:
        st.write('• ' + run['label'] + ' — ' + run['status'].replace('_', ' '))
    with st.expander('Technical evidence'):
        st.json({k: study.get(k) for k in
                 ('study_id', 'mode', 'model_id', 'fixture_id', 'adapter', 'runs')})
        for record in app.get_results(selected)['runs']:
            with st.expander('Stage details · ' + record['run_id'][:8]):
                st.dataframe(record['steps'], hide_index=True)
    st.caption('Inspect outputs and author judgments on Review; download evidence on Results.')
