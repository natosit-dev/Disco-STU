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
    assert any(metric.label == 'Recorded runs' and str(metric.value) == '1'
               for metric in app.metric)
    assert StuApplication(data_root).get_results(result['study_id'])['comparison_count'] == 10
