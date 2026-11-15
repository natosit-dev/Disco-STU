"""Results view. All analysis/export logic lives in StuApplication."""
from __future__ import annotations

import os
import streamlit as st
from stu.application import StuApplication

st.set_page_config(page_title='STU · Results', layout='wide')
st.title('Results and evidence coverage')
st.warning('Synthetic fixture verification only. These are NOT empirical LLM findings.')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))
studies = app.list_studies()
if not studies:
    st.info('No studies have been created.')
    st.stop()
study_id = st.selectbox('Study', [x['study_id'] for x in studies])
report = app.get_results(study_id)
st.metric('Recorded runs', report['recorded_run_count'])
st.metric('Valid paired outputs', len(report['paired_reconstructions']))
st.metric('Completed human reviews', report['completed_reviews'])
st.subheader('Coverage')
st.json({k: report[k] for k in ('run_status_counts','comparison_count','review_gap_labels',
                                  'completed_explanation_active_seconds')})
st.subheader('Run lineage and stage outcomes')
for run in report['runs']:
    with st.expander(run['run_id'] + ' · ' + run['status']):
        st.dataframe(run['steps'], hide_index=True)
st.subheader('Verification')
st.json(report['validation'])
st.subheader('Export study evidence')
st.warning('The complete bundle includes original writing, private SERA intention, raw requests/responses and human explanations. Do not publish it unreviewed.')
if st.button('Create complete private ZIP bundle'):
    try:
        info = app.export_study(study_id)
        st.session_state['stu_export'] = {'study_id': study_id, 'kind': 'full'}
        st.success('Complete bundle written to ' + info['path'])
    except (ValueError, RuntimeError, OSError, KeyError) as exc:
        st.error(str(exc))
if st.button('Create redacted sharing summary (JSON)'):
    try:
        info = app.export_study(study_id, privacy_level='safe')
        st.session_state['stu_export'] = {'study_id': study_id, 'kind': 'safe'}
        st.success('Redacted summary written to ' + info['path'])
    except (ValueError, RuntimeError, OSError, KeyError) as exc:
        st.error(str(exc))
choice = st.session_state.get('stu_export')
if choice and choice['study_id'] == study_id:
    kind = choice['kind']
    extension = 'full.zip' if kind == 'full' else 'safe.json'
    st.download_button(
        label='Download ' + ('complete private bundle' if kind == 'full' else 'redacted JSON'),
        data=app.get_export_bytes(study_id, privacy_level=kind),
        file_name=study_id + '-' + extension,
        mime='application/zip' if kind == 'full' else 'application/json',
    )
