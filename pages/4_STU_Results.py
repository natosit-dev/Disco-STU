"""Results view. All analysis/export logic lives in StuApplication."""
from __future__ import annotations

import os
import streamlit as st
from stu.application import StuApplication

st.set_page_config(page_title='STU · Results', layout='wide')
st.title('Results and evidence coverage')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))
studies = app.list_studies()
if not studies:
    st.info('No studies have been created.')
    st.stop()
study_id = st.selectbox('Study', [x['study_id'] for x in studies])

with st.expander('Archived runs: add missing original-to-final comparisons'):
    st.caption('Explicit, idempotent reconciliation. Adds evidence-backed comparison records '
               'without rerunning models or changing existing reviews.')
    if st.button('Add missing comparisons for this study'):
        try:
            outcome = app.reconcile_original_final_comparisons(study_id)
            st.success(f"Added {outcome['created_count']} comparison(s). "
                       "Existing comparison IDs and review events were not changed.")
        except (ValueError, RuntimeError, OSError, KeyError) as exc:
            st.error(str(exc))

report = app.get_results(study_id)
if report['synthetic']:
    st.warning('Synthetic fixture verification only. Not empirical LLM findings.')
else:
    st.info('Live hosted inference evidence. Successful requests do not establish semantic correctness.')
st.metric('Recorded runs', report['recorded_run_count'])
st.metric('Valid paired outputs', len(report['paired_reconstructions']))
st.metric('Primary human reviews completed',
          f"{report['completed_primary_reviews']}/{report['primary_comparison_count']}")
st.caption('Review prioritizes Oracle vs neutral and Oracle vs commercial; '
           'other comparisons remain optional diagnostics.')
st.subheader('Coverage')
st.json({k: report[k] for k in ('run_status_counts','comparison_count','review_gap_labels',
                                  'completed_explanation_active_seconds')})
st.subheader('Optional reconstruction diagnostics')
with st.expander('Full decomposition vs exact model-visible reconstruction projection'):
    comparisons = [c for c in app.list_comparisons(study_id)
                   if c['kind'] in ('decomposition_vs_neutral', 'decomposition_vs_commercial')]
    if comparisons:
        diagnostic_id = st.selectbox(
            'Diagnostic comparison', [c['comparison_id'] for c in comparisons],
            format_func=lambda cid: next(
                (c['kind'] + ' · ' + c['run_id'][:8] for c in comparisons
                 if c['comparison_id'] == cid), cid),
        )
        try:
            diagnostic = app.get_comparison(diagnostic_id)
            if 'model_visible_projection_view' in diagnostic:
                left, right = st.columns(2)
                with left:
                    st.caption('Full decomposition (recorded evidence)')
                    st.json(diagnostic['reference_view']['payload'])
                with right:
                    st.caption('EXACT reconstruction input (source_support removed)')
                    projection = diagnostic['model_visible_projection_view']
                    st.json(projection['payload'])
                    st.caption('SHA-256: ' + projection['sha256'])
                st.caption('The two reconstruction branches were verified against their '
                           'recorded provider request bytes. Full decomposition remains unchanged.')
            else:
                st.info('Synthetic studies used the full decomposition; no live projection exists.')
                st.json(diagnostic['reference_view']['payload'])
            st.caption('Output from the selected comparison')
            st.write(diagnostic['target_view']['payload'])
        except (ValueError, RuntimeError, OSError, KeyError) as exc:
            st.error(str(exc))
    else:
        st.info('No completed reconstruction diagnostics are available.')

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
