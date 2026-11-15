"""Thin Streamlit controller: explicit app-service commands, no SDK or storage access."""
from __future__ import annotations

import os
import streamlit as st
from stu.application import StuApplication
from stu.adaption_api import SUPPORTED_MODELS
from ui.adaption_credentials import render_api_key_input

st.set_page_config(page_title='STU · Transform', layout='wide')
st.title('STU — Semantic transformation')
st.caption('Hosted Adaption inference is the primary experiment. Fixtures are retained under diagnostics.')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))

with st.expander('Adaption API credential', expanded=True):
    key = render_api_key_input()
    st.caption('Key stays in this local Streamlit session; never saved to experiment artifacts.')

samples = [r for r in app.capture.list_samples() if r['status'] == 'frozen']
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
    model_id = st.selectbox('Hosted model', SUPPORTED_MODELS)
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

studies = app.list_studies()
if studies:
    st.subheader('Run and inspect recorded studies')
    options = [r['study_id'] for r in studies]
    current = st.session_state.get('active_study')
    selected = st.selectbox('Study', options,
        index=options.index(current) if current in options else len(options)-1,
        format_func=lambda sid: next((r['mode'] + ' · ' +
             (r.get('model_id') or r.get('fixture_id') or 'fixture') + ' · ' + sid[:8]
                                    for r in studies if r['study_id'] == sid), sid))
    study = app.get_study(selected)
    live = study['mode'] == 'live'
    st.json({k: study.get(k) for k in
             ('study_id', 'mode', 'model_id', 'fixture_id', 'adapter', 'runs')})
    if live:
        st.warning('Live run makes up to THREE chargeable, independent hosted requests.')
    run_label = 'Run live model experiment' if live else 'Run synthetic fixture'
    disabled = live and not (key or os.environ.get('ADAPTION_API_KEY'))
    if st.button(run_label, type='primary', disabled=disabled):
        try:
            run = app.run_sample(selected, api_key=key if live else None)
            st.session_state['active_study'] = selected
            st.success('Recorded ' + run['run_id'] + ': ' + run['status'])
            st.rerun()
        except (ValueError, RuntimeError, OSError) as exc:
            st.error(str(exc))
    if disabled:
        st.info('Enter an API key above or set ADAPTION_API_KEY to execute live inference.')
    report = app.get_results(selected)
    for record in report['runs']:
        with st.expander(record['run_id'][:8] + ' · ' + record['status']):
            st.dataframe(record['steps'], hide_index=True)
    st.caption('Review and complete private ZIP exports are on the Review / Results pages.')
