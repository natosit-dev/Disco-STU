"""Actual Streamlit page startup; domain tests exercise the deeper workflows."""
from pathlib import Path

import pytest


def test_streamlit_pages_start_without_backend_exceptions(tmp_path, monkeypatch):
    pytest.importorskip('streamlit')
    from streamlit.testing.v1 import AppTest
    monkeypatch.setenv('SERA_DATA_DIR', str(tmp_path / 'data'))
    root = Path(__file__).resolve().parents[1]
    for page in ('1_SERA.py', '2_STU_Transform.py', '3_STU_Review.py', '4_STU_Results.py'):
        app = AppTest.from_file(str(root / 'pages' / page), default_timeout=15).run()
        assert not app.exception, f'{page}: {list(app.exception)}'
