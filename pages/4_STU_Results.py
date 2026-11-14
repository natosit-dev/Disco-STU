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
st.metric('Recorded runs', report['planned_run_count'])
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
if st.button('Write private-safe export'):
    try:
        info = app.export_study(study_id)
        st.success('Wrote ' + info['path'])
        st.caption('Excluded private source, Oracle, raw responses and human explanations.')
    except (ValueError, RuntimeError, OSError) as exc:
        st.error(str(exc))
