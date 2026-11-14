"""Thin Streamlit view: no experiment logic, artifact writes or model calls."""
from __future__ import annotations

import os
import streamlit as st
from stu.application import StuApplication

st.set_page_config(page_title='STU · Transform', layout='wide')
st.title('STU — Deterministic synthetic transformation')
st.warning('SYNTHETIC SOFTWARE TEST — No real LLM inference or empirical research findings.')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))
samples = [r for r in app.capture.list_samples() if r['status'] == 'frozen']
if not samples:
    st.info('Create and freeze a SERA sample first.')
    st.stop()

with st.form('create_study'):
    selected = st.selectbox('Frozen SERA sample', [r['sample_id'] for r in samples],
                            format_func=lambda sid: next((r['source'].get('title') or sid[:8]
                                                          for r in samples if r['sample_id'] == sid), sid))
    fixture_id = st.selectbox('Deterministic fixture', ['STRUCTURAL',
        'F01','F02','F03','F04','F05','F06','F07','F08','F09','F10'])
    st.caption('Use STRUCTURAL for ordinary writing. F01–F10 require the corresponding exact synthetic source.')
    create = st.form_submit_button('Create synthetic study')
if create:
    try:
        study = app.create_study(selected, fixture_id=fixture_id)
        st.session_state['active_study'] = study['study_id']
        st.rerun()
    except (ValueError, RuntimeError, OSError) as exc:
        st.error(str(exc))

studies = app.list_studies()
if studies:
    options = [r['study_id'] for r in studies]
    current = st.session_state.get('active_study')
    study_id = st.selectbox('Study', options, index=options.index(current) if current in options else len(options)-1)
    study = app.get_study(study_id)
    st.json({k: study[k] for k in ('study_id','mode','fixture_id','status','adapter','runs')})
    if st.button('Run deterministic experiment', type='primary'):
        try:
            result = app.run_sample(study_id)
            st.success(f"Recorded run {result['run_id']} — {result['status']}")
            st.rerun()
        except (ValueError, RuntimeError, OSError) as exc:
            st.error(str(exc))
    if study['runs']:
        st.subheader('Recorded steps')
        for run_id in study['runs']:
            for item in app.get_results(study_id)['runs']:
                if item['run_id'] == run_id:
                    st.write(run_id, item['status'])
                    st.dataframe(item['steps'], hide_index=True)
    st.caption('The runner receives the source-only packet; it does not load the private Oracle.')
