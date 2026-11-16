"""Human-first Results page; technical records remain available on demand."""
from __future__ import annotations

import os
import streamlit as st
from stu.application import StuApplication

st.set_page_config(page_title='STU · Results', layout='wide')
st.title('Results')
st.caption('Study completion and recorded human observations—not an automated meaning score.')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))
studies = app.list_study_options(with_runs=True)
if not studies:
    st.info('Run a study in Transform before viewing results.')
    st.stop()
labels = {study['study_id']: study['label'] for study in studies}
study_id = st.selectbox('Source / study', list(labels),
                        format_func=lambda sid: labels[sid])
report = app.get_results(study_id)
if report['synthetic']:
    st.warning('Synthetic fixture verification only; no empirical model results.')
else:
    st.info('Live hosted inference: successful execution does not prove meaning preservation.')

a, b, c = st.columns(3)
a.metric('Model runs', report['recorded_run_count'])
b.metric('Complete neutral/commercial pairs', len(report['paired_reconstructions']))
c.metric('Primary reviews completed',
         f"{report['completed_primary_reviews']} of {report['primary_comparison_count']}")
st.caption('Primary reviews are the original writing compared with each final model output. '
           'Other comparisons are optional diagnostic instruments.')
st.markdown('**Human findings and timing quality**')
x, y, z = st.columns(3)
x.metric('Reviews with written differences', report['free_text_findings_count'])
y.metric('Explicit no-meaningful-gap reviews', report['explicit_no_gap_reviews'])
z.metric('Reviews with incomplete labor measurement',
         report['reviews_with_incomplete_labor_measurement'])
st.caption("Optional discrepancy labels are separate from the author\'s free-text finding. "
           'Recorded active time does not necessarily equal total labor. '
           'A cumulative 15-minute threshold is independent of uncertain long intervals.')

st.subheader('Run history')
for run in app.list_review_runs(study_id):
    info = next((value for value in report['runs'] if value['run_id'] == run['run_id']),
                None)
    if info is None:
        continue
    st.markdown('**' + run['label'] + '**')
    st.caption('Recorded status: ' + run['status'].replace('_', ' '))
    primary = app.list_review_choices(study_id, run['run_id'])
    if primary:
        for comp in primary:
            st.write('• ' + comp['label'])
    else:
        st.caption('No primary comparisons for this run. See Maintenance if it is an older study.')

st.divider()
st.subheader('Export')
st.warning('The complete private ZIP includes source writing, frozen SERA intention, '
           'provider requests/responses and review explanations. Do not publish it unreviewed.')
col1, col2 = st.columns(2)
with col1:
    if st.button('Prepare complete private ZIP'):
        try:
            app.export_study(study_id)
            st.session_state['stu_export'] = {'study_id': study_id, 'kind': 'full'}
            st.rerun()
        except (ValueError, RuntimeError, OSError, KeyError) as exc:
            st.error(str(exc))
with col2:
    if st.button('Prepare redacted sharing summary'):
        try:
            app.export_study(study_id, privacy_level='safe')
            st.session_state['stu_export'] = {'study_id': study_id, 'kind': 'safe'}
            st.rerun()
        except (ValueError, RuntimeError, OSError, KeyError) as exc:
            st.error(str(exc))
prepared = st.session_state.get('stu_export')
if prepared and prepared['study_id'] == study_id:
    kind = prepared['kind']
    try:
        st.download_button(
            'Download ' + ('complete private ZIP' if kind == 'full' else 'redacted JSON'),
            data=app.get_export_bytes(study_id, privacy_level=kind),
            file_name=study_id + ('-full.zip' if kind == 'full' else '-safe.json'),
            mime='application/zip' if kind == 'full' else 'application/json',
        )
    except (ValueError, RuntimeError, OSError, KeyError) as exc:
        st.error(str(exc))

with st.expander('Technical evidence and coverage'):
    st.json({k: report[k] for k in ('run_status_counts', 'comparison_count',
        'diagnostic_comparison_count', 'free_text_findings_count',
        'explicit_no_gap_reviews', 'reviews_with_incomplete_labor_measurement',
        'reviews_reaching_15min_budget', 'review_gap_labels',
        'completed_explanation_active_seconds')})
    for run in report['runs']:
        with st.expander('Recorded stages · ' + run['run_id'][:8]):
            st.dataframe(run['steps'], hide_index=True)
    st.markdown('**Evidence validation**')
    st.json(report['validation'])

with st.expander('Optional reconstruction diagnostics'):
    diagnostics = [comp for comp in app.list_comparisons(study_id)
                   if comp['kind'] in ('decomposition_vs_neutral',
                                      'decomposition_vs_commercial')]
    if not diagnostics:
        st.info('No completed decomposition diagnostics are available.')
    else:
        names = {comp['comparison_id']: comp['kind'].replace('_', ' ').title()
                 + ' · ' + comp['run_id'][:8] for comp in diagnostics}
        comparison_id = st.selectbox('Recorded comparison', list(names),
                                      format_func=lambda cid: names[cid])
        try:
            detail = app.get_comparison(comparison_id)
            if 'model_visible_projection_view' in detail:
                left, right = st.columns(2)
                with left:
                    st.markdown('**Full decomposition (archived)**')
                    st.json(detail['reference_view']['payload'])
                with right:
                    st.markdown('**Exact model-visible projection**')
                    projected = detail['model_visible_projection_view']
                    st.json(projected['payload'])
                    st.caption('SHA-256: ' + projected['sha256'])
                st.caption('The two reconstruction inputs share the same frozen bytes.')
            else:
                st.info('This synthetic run used its complete decomposition.')
                st.json(detail['reference_view']['payload'])
            st.markdown('**Reconstructed output**')
            st.write(detail['target_view']['payload'])
        except (ValueError, RuntimeError, OSError, KeyError) as exc:
            st.error(str(exc))

with st.expander('Maintenance · archived comparison records'):
    st.caption('For older eight-comparison studies only. This action creates '
               'missing original-to-final comparison records from saved output, '
               'without rerunning inference or altering old review events.')
    if st.button('Add missing comparisons for this study'):
        try:
            outcome = app.reconcile_original_final_comparisons(study_id)
            st.success(f"Added {outcome['created_count']} comparison(s).")
        except (ValueError, RuntimeError, OSError, KeyError) as exc:
            st.error(str(exc))
