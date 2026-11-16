"""Human Review: untimed inspection, one explicit timed explanation at a time.

Only transient widget/draft state lives here. All review events and evidence are
owned by StuApplication/HumanReview, not by Streamlit session_state.
"""
from __future__ import annotations

import os

import streamlit as st
from stu.application import StuApplication

st.set_page_config(page_title='STU · Review', layout='wide')
st.title('Review what survived')
st.caption('Read without a timer. Begin timing only when you are ready to explain.')
app = StuApplication(os.environ.get('SERA_DATA_DIR', 'data'))


def command(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except (ValueError, RuntimeError, OSError, KeyError) as exc:
        st.error(str(exc))
    else:
        st.rerun()


def remember_draft(comparison_id: str) -> None:
    # A Streamlit widget key can disappear when its branch is not rendered.
    # Keep pending text in a separate, per-comparison session-only key.
    widget_key = 'review_editor_' + comparison_id
    st.session_state['review_draft_' + comparison_id] = st.session_state.get(
        widget_key, '')


studies = app.list_study_options(with_runs=True)
if not studies:
    st.info('Freeze a SERA source and run a model in Transform first.')
    st.stop()

active = app.active_review()
if active:
    st.warning('An explanation timer is running. Pause it before switching '
               'sources, model runs, or comparisons.')
    st.session_state['review_study'] = active['study_id']
    st.session_state['review_run'] = active['run_id']
    st.session_state['review_comparison'] = active['comparison_id']

study_labels = {item['study_id']: item['label'] for item in studies}
study_options = list(study_labels)
if st.session_state.get('review_study') not in study_options:
    st.session_state['review_study'] = study_options[0]
study_id = st.selectbox('Source / study', study_options,
                        format_func=lambda value: study_labels[value],
                        key='review_study', disabled=active is not None)

runs = app.list_review_runs(study_id)
if not runs:
    st.info('No model runs are recorded for this source.')
    st.stop()
run_labels = {item['run_id']: item['label'] for item in runs}
run_options = list(run_labels)
if st.session_state.get('review_run') not in run_options:
    st.session_state['review_run'] = run_options[0]
run_id = st.selectbox('Model run', run_options,
                      format_func=lambda value: run_labels[value],
                      key='review_run', disabled=active is not None)

if active and active['run_id'] == run_id:
    # An active diagnostic must remain available if diagnostics are hidden.
    primary = app.list_review_choices(study_id, run_id, diagnostics=False)
    if active['comparison_id'] not in {c['comparison_id'] for c in primary}:
        st.session_state['review_diagnostics'] = True

diagnostics = st.checkbox('Show optional diagnostic comparisons',
                          key='review_diagnostics', disabled=active is not None)
choices = app.list_review_choices(study_id, run_id, diagnostics=diagnostics)
if not choices:
    st.info('No final-output comparison exists for this run. Older studies can '
            'add missing comparisons explicitly in Results → Maintenance.')
    st.stop()

choice_labels = {item['comparison_id']: item['label'] for item in choices}
choice_options = list(choice_labels)
if st.session_state.get('review_comparison') not in choice_options:
    st.session_state['review_comparison'] = choice_options[0]
cid = st.selectbox('Review comparison', choice_options,
                   format_func=lambda value: choice_labels[value],
                   key='review_comparison', disabled=active is not None)

try:
    view = app.get_review_context(cid)
except (ValueError, RuntimeError, OSError, KeyError) as exc:
    st.error(str(exc))
    st.stop()

st.subheader(view['source_title'])
st.caption(f"{view['run_label']} · Frozen SERA v{view['oracle_version']}")
if not view['is_primary']:
    st.info('Optional diagnostic: not a required human evaluation.')

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
    st.caption('Recorded before this model run. Never sent to the model.')
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
    with st.expander('Advanced semantic annotations'):
        if view['oracle_units']:
            st.dataframe(view['oracle_units'], hide_index=True)
        if view['oracle_relations']:
            st.dataframe(view['oracle_relations'], hide_index=True)

st.divider()
state = view['review']
status = state['status']
st.subheader('Your assessment')
st.caption('Your unrestricted explanation is the primary evidence. '
           'Optional labels do not replace it.')
if state['labor_measurement_incomplete']:
    st.warning('Timing quality is incomplete or uncertain in this review history. '
               'The original event journal remains unchanged.')

# Keep these fields separate so Streamlit's conditionally rendered widgets
# cannot cross-populate another comparison after a rerun.
draft_key = 'review_draft_' + cid
editor_key = 'review_editor_' + cid
nogap_key = 'review_no_gap_' + cid
labels_key = 'review_labels_' + cid
if draft_key not in st.session_state:
    st.session_state[draft_key] = state['explanation']
if nogap_key not in st.session_state:
    st.session_state[nogap_key] = state['no_meaningful_gap']
if labels_key not in st.session_state:
    st.session_state[labels_key] = [g['label'] for g in state['gaps']]

if status == 'not_started':
    st.info('Inspection is untimed. Click Begin when ready to write your explanation.')
    if st.button('Begin timed explanation', type='primary'):
        command(app.begin_gap_explanation, cid)

elif status in ('paused', 'interrupted'):
    st.warning('Timer paused. Editing is disabled so new work cannot be '
               'silently excluded from the recorded time.')
    if state['explanation']:
        st.write('**Saved draft**')
        st.write(state['explanation'])
    if st.button('Resume timed editing', type='primary'):
        command(app.resume_gap_explanation, cid)
    if (status == 'paused' and
            (state['explanation'].strip() or state['no_meaningful_gap'])):
        if st.button('Complete saved draft without additional editing'):
            command(app.complete_gap_explanation, cid)

elif status == 'amended':
    st.info('Amendment opened. Resume timing before changing the explanation.')
    st.write(state['explanation'])
    if st.button('Resume timed amendment', type='primary'):
        command(app.resume_gap_explanation, cid)

elif status == 'completed':
    st.success('Review completed')
    st.write(state['explanation'] or 'Explicitly recorded: no meaningful gap.')
    if st.button('Amend completed review'):
        command(app.amend_gap_explanation, cid)

elif status == 'explaining':
    st.success('Explanation timer active. The source/run/comparison selectors '
               'are locked until you pause or complete this review.')
    st.text_area('Your explanation', key=editor_key,
                 value=st.session_state[draft_key],
                 height=180, on_change=remember_draft, args=(cid,))
    st.checkbox('No meaningful gap', key=nogap_key)
    with st.expander('Optional discrepancy classifications'):
        labels = st.multiselect(
            'Classification (optional)', (
                'preserved', 'omitted', 'altered', 'contradicted',
                'unsupported_addition', 'source_consistent_extension',
                'unresolved_ambiguous'),
            key=labels_key, disabled=st.session_state[nogap_key])
        for label in labels:
            key = 'review_rationale_' + cid + '_' + label
            if key not in st.session_state:
                st.session_state[key] = next(
                    (gap['rationale'] for gap in state['gaps']
                     if gap['label'] == label), '')
            st.text_input(label.replace('_', ' ').title() + ': why?',
                          key=key)

    def save_current() -> None:
        # Read the widget's current value rather than the potentially stale
        # draft copy; keep a copy across conditional render/navigation.
        draft = st.session_state.get(editor_key, state['explanation'])
        st.session_state[draft_key] = draft
        no_gap = bool(st.session_state.get(nogap_key, False))
        selected_labels = [] if no_gap else st.session_state.get(labels_key, [])
        gaps = [
            {'label': label, 'rationale': st.session_state.get(
                'review_rationale_' + cid + '_' + label, '')}
            for label in selected_labels
        ]
        app.save_gap_explanation(cid, draft, gaps=gaps, no_gap=no_gap)

    col1, col2, col3 = st.columns([1, 1.2, 1.4])
    with col1:
        if st.button('Save draft'):
            try:
                save_current()
            except (ValueError, RuntimeError, OSError, KeyError) as exc:
                st.error(str(exc))
            else:
                st.success('Draft recorded')
    with col2:
        if st.button('Pause & save draft'):
            try:
                save_current()
                app.pause_gap_explanation(cid)
            except (ValueError, RuntimeError, OSError, KeyError) as exc:
                st.error(str(exc))
            else:
                st.rerun()
    with col3:
        if st.button('Save & complete', type='primary'):
            try:
                save_current()
                app.complete_gap_explanation(cid)
            except (ValueError, RuntimeError, OSError, KeyError) as exc:
                st.error(str(exc))
            else:
                st.rerun()

with st.expander('Timing and technical evidence'):
    st.write('Review state:', status.replace('_', ' '))
    st.write('Confirmed active explanation time:',
             round(state['active_seconds'], 2), 'seconds')
    st.write('Confirmed cumulative time reached 15 minutes:',
             state['reached_15min_budget'])
    st.write('Uncertain long interval:', state['timing_uncertain'])
    st.write('Unmeasured editing recorded in historical events:',
             state['unmeasured_edit_event'])
    if state['open_interval_since']:
        st.caption('Timer active; an open interval is not counted until closed.')
    if state['labor_measurement_incomplete']:
        st.warning('Confirmed time is not a defensible measure of total effort.')
    st.caption('Free-text explanation is recorded independently of optional labels.')
    with st.expander('Comparison IDs and saved artifacts'):
        st.json({
            'comparison_id': cid,
            'run_id': view['run_id'],
            'reference_artifact': view['comparison']['reference'],
            'target_artifact': view['comparison']['target'],
            'reference_sha256': view['comparison']['reference_sha256'],
            'target_sha256': view['comparison']['target_sha256'],
        })
    if status == 'explaining' and st.button('Record interruption'):
        command(app.interrupt_gap_explanation, cid)
