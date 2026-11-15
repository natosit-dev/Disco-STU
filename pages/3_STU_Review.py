"""Human-first Review page. Domain events, time and storage remain in services."""
from __future__ import annotations

import os

import streamlit as st
from stu.application import StuApplication

st.set_page_config(page_title='STU · Review', layout='wide')
st.title('Review what survived')
st.caption('Inspect the original and reconstructed output before beginning a timed explanation.')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))


def execute(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except (ValueError, RuntimeError, OSError, KeyError) as exc:
        st.error(str(exc))
        return
    st.rerun()


studies = app.list_study_options(with_runs=True)
if not studies:
    st.info('Freeze a SERA source and run a model in Transform first.')
    st.stop()

study_labels = {study['study_id']: study['label'] for study in studies}
study_id = st.selectbox('Source / study', list(study_labels),
                        format_func=lambda value: study_labels[value])
runs = app.list_review_runs(study_id)
if not runs:
    st.info('No model runs are recorded for this source.')
    st.stop()
run_labels = {run['run_id']: run['label'] for run in runs}
run_id = st.selectbox('Model run', list(run_labels),
                      format_func=lambda value: run_labels[value])

# Ten recorded comparisons are research instrumentation, not ten required
# human tasks. Only the two original-to-final outcomes are primary.
show_diagnostics = st.checkbox('Show optional diagnostic comparisons', value=False)
choices = app.list_review_choices(study_id, run_id,
                                   diagnostics=show_diagnostics)
if not choices:
    st.info('This run has no primary final-output comparisons yet. '
            'If it predates the new comparison types, use Results → Maintenance '
            'to add them from stored evidence without rerunning the model.')
    st.stop()
choice_labels = {comp['comparison_id']: comp['label'] for comp in choices}
if show_diagnostics:
    cid = st.selectbox('Comparison (diagnostics included)', list(choice_labels),
                       format_func=lambda value: choice_labels[value])
else:
    cid = st.radio('Final reconstruction', list(choice_labels),
                   format_func=lambda value: choice_labels[value],
                   horizontal=True)

try:
    view = app.get_review_context(cid)
except (ValueError, RuntimeError, OSError, KeyError) as exc:
    st.error(str(exc))
    st.stop()

st.subheader(view['source_title'])
st.caption(f"{view['run_label']} · Frozen SERA v{view['oracle_version']}")
if not view['is_primary']:
    st.info('Diagnostic comparison: optional investigation, not required author labor.')

left, right = st.columns(2, gap='large')
with left:
    st.markdown('**Original writing**')
    with st.container(border=True):
        st.markdown(view['source_text'].replace('\n', '  \n'))
with right:
    st.markdown('**Model reconstruction**')
    with st.container(border=True):
        st.markdown(view['output_text'].replace('\n', '  \n'))

with st.expander('Frozen authorial intention · optional reference'):
    st.caption('Pinned human meaning recorded before this model run. '
               'Not supplied to the model.')
    st.write(view['oracle_intention'])
    prose = {key: value for key, value in view['oracle_categories'].items()
             if value.strip()}
    if prose:
        with st.expander('Additional author notes'):
            for key, value in prose.items():
                st.markdown('**' + key.replace('_', ' ').title() + '**')
                st.write(value)
    if view['oracle_characteristics']:
        st.caption('Optional characteristics: ' +
                   ', '.join(view['oracle_characteristics']))
    with st.expander('Advanced structured annotations'):
        if view['oracle_units']:
            st.dataframe(view['oracle_units'], hide_index=True)
        if view['oracle_relations']:
            st.dataframe(view['oracle_relations'], hide_index=True)

st.divider()
state = view['review']
status = state['status']
st.subheader('Your assessment')
if status == 'completed':
    st.success('Review completed')
    st.write(state['explanation'] or 'Explicitly recorded: no meaningful gap.')
else:
    st.caption('Write what changed, what survived, or what your original failed to convey. '
               'No automated semantic judgment is made.')

if status == 'not_started':
    if st.button('Begin explanation', type='primary'):
        execute(app.begin_gap_explanation, cid)
elif status == 'explaining':
    if st.button('Pause explanation'):
        execute(app.pause_gap_explanation, cid)
elif status in ('paused', 'interrupted'):
    if st.button('Resume explanation', type='primary'):
        execute(app.resume_gap_explanation, cid)
elif status == 'completed':
    if st.button('Amend completed explanation'):
        execute(app.amend_gap_explanation, cid)

if status in ('explaining', 'paused', 'amended', 'interrupted'):
    # The typed discrepancy annotations are optional. Free-text author
    # explanation remains the primary measurement.
    options = ('preserved', 'omitted', 'altered', 'contradicted',
               'unsupported_addition', 'source_consistent_extension',
               'unresolved_ambiguous')
    prior = {g['label']: g['rationale'] for g in state['gaps']}
    labels = st.multiselect('Optional discrepancy characteristics', options,
                            default=list(prior), key='labels_' + cid)
    with st.form('assessment_' + cid):
        explanation = st.text_area('Your explanation', value=state['explanation'],
                                   height=160, key='assessment_text_' + cid)
        no_gap = st.checkbox('No meaningful gap', value=state['no_meaningful_gap'])
        rationales = {}
        if labels:
            with st.expander('Optional classification details', expanded=False):
                for label in labels:
                    rationales[label] = st.text_input(
                        label.replace('_', ' ').title() + ' — why?',
                        value=prior.get(label, ''), key='rationale_' + cid + '_' + label)
        save = st.form_submit_button('Save explanation')
        complete = st.form_submit_button('Save and complete', type='primary',
                                          disabled=status == 'interrupted')
    if save or complete:
        gaps = [{'label': label, 'rationale': rationales.get(label, '')}
                for label in labels]
        try:
            app.save_gap_explanation(cid, explanation, gaps=gaps, no_gap=no_gap)
            if complete:
                app.complete_gap_explanation(cid)
        except (ValueError, RuntimeError, OSError, KeyError) as exc:
            st.error(str(exc))
        else:
            st.rerun()

with st.expander('Timing and technical evidence'):
    st.write('Review state:', status.replace('_', ' '))
    st.write('Confirmed active explanation time:', round(state['active_seconds'], 2),
             'seconds')
    if state['open_interval_since']:
        st.caption('An interval is open; only closed intervals count toward active time.')
    if state['timing_uncertain']:
        st.warning('A long interval has uncertain duration. Timing review is required.')
    st.caption('The separate 15-minute labor-budget threshold is being handled '
               'in the Review domain contract; this display does not silently '
               'reinterpret uncertain time.')
    if status == 'explaining' and st.button('Record interruption'):
        execute(app.interrupt_gap_explanation, cid)
    with st.expander('Comparison IDs and stored artifacts'):
        st.json({
            'comparison_id': cid,
            'run_id': view['run_id'],
            'reference_artifact': view['comparison']['reference'],
            'target_artifact': view['comparison']['target'],
            'reference_sha256': view['comparison']['reference_sha256'],
            'target_sha256': view['comparison']['target_sha256'],
        })
