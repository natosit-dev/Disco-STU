"""Thin human Review view using the same application services as the CLI."""
from __future__ import annotations

import json
import os
import streamlit as st
from stu.application import StuApplication

st.set_page_config(page_title='STU · Human Review', layout='wide')
st.title('Review — Explain the semantic gap')
st.info('Human-written explanations are observations. Fixture outputs are synthetic, not model findings.')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))
studies = app.list_studies()
if not studies:
    st.info('Run a synthetic STU study first.')
    st.stop()
study_id = st.selectbox('Study', [x['study_id'] for x in studies])
comparisons = app.list_comparisons(study_id)
if not comparisons:
    st.info('No comparisons available; run the study.')
    st.stop()
cid = st.selectbox('Comparison', [x['comparison_id'] for x in comparisons],
                   format_func=lambda x: next((c['kind'] + ' · ' + c['run_id'][:8]
                    for c in comparisons if c['comparison_id'] == x), x))
try:
    comp = app.get_comparison(cid)
except (ValueError, RuntimeError, OSError) as exc:
    st.error(str(exc))
    st.stop()

left, right = st.columns(2)
with left:
    st.caption('REFERENCE')
    st.json(comp['reference_view']['payload'])
with right:
    st.caption('TARGET')
    st.json(comp['target_view']['payload'])
state = comp['review']
st.write('Status:', state['status'], '· recorded active seconds:', round(state['active_seconds'], 2))
if state['open_interval_since']:
    st.warning('An explanatory interval is open. Only completed intervals count toward recorded active time.')
if state['timing_uncertain']:
    st.warning('One or more long intervals have uncertain active duration. Manual review required.')


def issue(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
        st.rerun()
    except (ValueError, RuntimeError, OSError) as exc:
        st.error(str(exc))


controls = st.columns(5)
with controls[0]:
    if st.button('Begin', disabled=state['status'] != 'not_started'):
        issue(app.begin_gap_explanation, cid)
with controls[1]:
    if st.button('Pause', disabled=state['status'] != 'explaining'):
        issue(app.pause_gap_explanation, cid)
with controls[2]:
    if st.button('Resume', disabled=state['status'] not in ('paused','interrupted')):
        issue(app.resume_gap_explanation, cid)
with controls[3]:
    if st.button('Interrupt', disabled=state['status'] != 'explaining'):
        issue(app.interrupt_gap_explanation, cid)
with controls[4]:
    if st.button('Amend', disabled=state['status'] != 'completed'):
        issue(app.amend_gap_explanation, cid)

if state['status'] not in ('not_started','completed'):
    with st.form('human_explanation'):
        explanation = st.text_area('Explain what you meant and what the transformed output did',
                                   value=state['explanation'], height=180)
        no_gap = st.checkbox('Completed: no meaningful gap', value=state['no_meaningful_gap'])
        label = st.selectbox('Optional gap classification', ['(none)', 'preserved', 'omitted', 'altered',
            'contradicted', 'unsupported_addition', 'source_consistent_extension', 'unresolved_ambiguous'])
        rationale = st.text_area('Rationale for that classification')
        save = st.form_submit_button('Save human explanation')
    if save:
        gaps = [] if label == '(none)' else [{'label': label, 'rationale': rationale}]
        issue(app.save_gap_explanation, cid, explanation, gaps=gaps, no_gap=no_gap)
    if state['status'] in ('explaining', 'paused', 'amended'):
        if st.button('Complete explanation'):
            issue(app.complete_gap_explanation, cid)
