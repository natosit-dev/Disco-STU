"""Presentation labels are derived from pinned records and actual run timestamps."""
from __future__ import annotations

import json
from datetime import datetime
from zoneinfo import ZoneInfo

from stu.application import StuApplication
from stu.cli import smoke
from stu.presentation import display_datetime, model_name, comparison_name


def test_utc_timestamp_is_formatted_in_declared_local_timezone(monkeypatch):
    monkeypatch.setenv('STU_UI_TIMEZONE', 'America/New_York')
    # DST conversion is deliberate; original source-writing date stays separate.
    result = display_datetime('2026-11-15T18:51:00+00:00')
    assert 'Nov 15, 2026' in result
    assert '1:51 PM' in result
    assert 'EST' in result
    assert display_datetime('') == 'Time unavailable'
    assert display_datetime('2026-11-15T18:51:00') == 'Time zone unspecified'
    assert model_name('gemma-4-31b-it') == 'Gemma 4 31B'


def test_review_options_human_readable_grouped_by_run_and_pinned_oracle(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app)
    sid = result['study_id']
    options = app.list_study_options(with_runs=True)
    assert len(options) == 1
    assert 'SYNTHETIC F01' in options[0]['label']
    assert options[0]['label'].endswith(sid[:8])
    assert options[0]['pinned_oracle_version'] == 1
    runs = app.list_review_runs(sid)
    assert len(runs) == 1
    assert runs[0]['run_id'] == result['run_id']
    assert runs[0]['label'].endswith(result['run_id'][:8])
    primaries = app.list_review_choices(sid, result['run_id'])
    assert [c['kind'] for c in primaries] == [
        'original_vs_neutral', 'original_vs_commercial']
    assert all('SYNTHETIC' not in c['label'] for c in primaries)
    assert all('Not Started' in c['label'] for c in primaries)
    assert len(app.list_review_choices(sid, result['run_id'], diagnostics=True)) == 10
    view = app.get_review_context(primaries[0]['comparison_id'])
    assert view['source_title'] == 'SYNTHETIC F01'
    assert view['source_text'] == app.capture.get_sample(result['sample_id'])['source']['original_text']
    assert view['output_text']
    assert view['oracle_intention'].startswith('SYNTHETIC ORACLE')
    assert view['oracle_version'] == 1
    assert view['is_primary'] is True


def test_review_title_stays_pinned_after_sera_amendment(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app)
    sid = result['sample_id']
    original_title = app.list_study_options()[0]['source_title']
    app.capture.begin_amendment(sid)
    app.capture.save_source(sid, title='LATER NAME NOT RETROACTIVE')
    app.capture.save_intention(sid, 'Later human meaning')
    app.capture.freeze(sid)
    assert app.list_study_options()[0]['source_title'] == original_title
    comparison_id = app.list_review_choices(result['study_id'], result['run_id'])[0]['comparison_id']
    assert app.get_review_context(comparison_id)['oracle_version'] == 1
    assert app.get_review_context(comparison_id)['source_title'] == original_title
