"""Actual Streamlit page startup; domain tests exercise the deeper workflows."""
from pathlib import Path

import pytest


def test_streamlit_pages_start_without_backend_exceptions(tmp_path, monkeypatch):
    pytest.importorskip('streamlit')
    from streamlit.testing.v1 import AppTest
    monkeypatch.setenv('SERA_DATA_DIR', str(tmp_path / 'data'))
    root = Path(__file__).resolve().parents[1]
    for page in ('1_SERA.py', '2_STU_Transform.py', '3_STU_Review.py',
                 '4_STU_Results.py', '5_Adaption_API_Test.py'):
        app = AppTest.from_file(str(root / 'pages' / page), default_timeout=15).run()
        assert not app.exception, f'{page}: {list(app.exception)}'

def test_results_page_renders_existing_study_and_comparison_details(tmp_path, monkeypatch):
    pytest.importorskip('streamlit')
    from streamlit.testing.v1 import AppTest
    from stu.application import StuApplication
    from stu.cli import smoke

    data_root = tmp_path / 'data'
    result = smoke(StuApplication(data_root), fixture_id='F01')
    monkeypatch.setenv('SERA_DATA_DIR', str(data_root))
    root = Path(__file__).resolve().parents[1]
    app = AppTest.from_file(str(root / 'pages' / '4_STU_Results.py'),
                            default_timeout=15).run()
    assert not app.exception, list(app.exception)
    # This tests more than startup: the page loaded a recorded study and
    # rendered an actual comparison through the application facade.
    assert any(metric.label == 'Model runs' and str(metric.value) == '1'
               for metric in app.metric)
    assert StuApplication(data_root).get_results(result['study_id'])['comparison_count'] == 10

def test_review_page_uses_source_and_final_output_as_primary_views(tmp_path, monkeypatch):
    pytest.importorskip('streamlit')
    from streamlit.testing.v1 import AppTest
    from stu.application import StuApplication
    from stu.cli import smoke

    data_root = tmp_path / 'data'
    smoke(StuApplication(data_root), fixture_id='F01')
    monkeypatch.setenv('SERA_DATA_DIR', str(data_root))
    root = Path(__file__).resolve().parents[1]
    ui = AppTest.from_file(str(root / 'pages' / '3_STU_Review.py'),
                           default_timeout=15).run()
    assert not ui.exception, list(ui.exception)
    assert len(ui.selectbox) >= 3
    assert len(ui.selectbox[2].options) == 2
    rendered = ' '.join(element.value for element in ui.markdown)
    assert 'Original writing' in rendered
    assert 'Model reconstruction' in rendered
    assert any('Frozen authorial intention' in expander.label for expander in ui.get('expander'))
    assert any('Gemma' in text.value or 'Synthetic' in text.value
               for text in ui.caption)


def test_sera_v2_existing_draft_renders_simple_authoring_screen(tmp_path, monkeypatch):
    pytest.importorskip('streamlit')
    from streamlit.testing.v1 import AppTest
    from sera.application import SeraApplication

    data_root = tmp_path / 'data'
    capture = SeraApplication(data_root)
    source = capture.create_sample('An authored sentence.', title='Human baseline')
    monkeypatch.setenv('SERA_DATA_DIR', str(data_root))
    root = Path(__file__).resolve().parents[1]
    ui = AppTest.from_file(str(root / 'pages' / '1_SERA.py'),
                           default_timeout=15).run()
    assert not ui.exception, list(ui.exception)
    # Select the existing draft rather than the default new-source form.
    ui.selectbox[0].set_value(source['sample_id']).run()
    assert not ui.exception, list(ui.exception)
    rendered = ' '.join(element.value for element in ui.markdown)
    assert 'Your intended meaning' in rendered
    assert any(button.label == 'Save draft' for button in ui.button)


def test_review_navigation_edit_pause_resume_complete_and_amend(tmp_path, monkeypatch):
    pytest.importorskip('streamlit')
    from streamlit.testing.v1 import AppTest
    from stu.application import StuApplication
    from stu.cli import smoke

    data_root = tmp_path / 'data'
    result = smoke(StuApplication(data_root), fixture_id='F01')
    monkeypatch.setenv('SERA_DATA_DIR', str(data_root))
    root = Path(__file__).resolve().parents[1]
    ui = AppTest.from_file(str(root / 'pages' / '3_STU_Review.py'),
                           default_timeout=15).run()
    assert not ui.exception, list(ui.exception)
    assert len(ui.selectbox[2].options) == 2

    def click(label):
        nonlocal ui
        button = next(b for b in ui.button if b.label == label)
        ui = button.click().run()
        assert not ui.exception, list(ui.exception)
        return ui

    first = ui.selectbox[2].value
    click('Begin timed explanation')
    assert ui.selectbox[0].disabled
    assert ui.selectbox[1].disabled
    assert ui.selectbox[2].disabled
    assert len(ui.text_area) == 1
    ui = ui.text_area[0].set_value('The line breaks were intentional.').run()
    assert not ui.exception, list(ui.exception)
    click('Pause & save draft')
    state = StuApplication(data_root).review.state(first)
    assert state['status'] == 'paused'
    assert state['explanation'] == 'The line breaks were intentional.'
    assert not ui.selectbox[2].disabled
    assert len(ui.text_area) == 0  # paused writing cannot escape the timer
    click('Resume timed editing')
    assert ui.text_area[0].value == 'The line breaks were intentional.'
    click('Save & complete')
    assert StuApplication(data_root).review.state(first)['status'] == 'completed'

    # One saved finding, not two identical Save/Complete entries.
    events = StuApplication(data_root).review._journal(first).read()
    assert [e['kind'] for e in events] == ['begin', 'save', 'pause', 'resume', 'complete']
    click('Amend completed review')
    assert len(ui.text_area) == 0  # amendment is untimed until explicit resume
    click('Resume timed amendment')
    ui = ui.text_area[0].set_value('The line breaks were intentional and independent.').run()
    click('Save & complete')
    assert StuApplication(data_root).review.state(first)['event_count'] == 8

    # Switching to the second primary comparison after completion is stable.
    second = next(c['comparison_id'] for c in StuApplication(data_root)
                  .list_review_choices(result['study_id'], result['run_id'])
                  if c['comparison_id'] != first)
    ui = ui.selectbox[2].set_value(second).run()
    assert not ui.exception, list(ui.exception)
    assert 'Begin timed explanation' in [b.label for b in ui.button]
    click('Begin timed explanation')
    assert StuApplication(data_root).active_review()['comparison_id'] == second
    assert ui.selectbox[2].disabled
