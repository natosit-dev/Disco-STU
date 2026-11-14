"""Exercises the actual SERA baseline and STU facade together on the full repo."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from stu.application import StuApplication
from stu.cli import smoke
from stu.contracts import CATEGORIES, canonical
from stu.fixtures import FIXTURES
from stu.storage import atomic_json


def test_synthetic_full_pipeline_including_actual_sera(tmp_path):
    app = StuApplication(tmp_path / 'data')
    report = smoke(app, fixture_id='F01')
    assert report['verification']['valid'] is True
    assert report['run_status'] == 'completed'
    results = report['results']
    assert results['research_verdict'] == 'NO EMPIRICAL MODEL RESULTS'
    assert len(results['paired_reconstructions']) == 1
    assert results['comparison_count'] == 8
    cmp_id = next(c['comparison_id'] for c in app.list_comparisons(report['study_id'])
                  if c['kind'] == 'oracle_vs_neutral')
    comp = app.get_comparison(cmp_id)
    assert comp['reference_view']['private']
    assert comp['reference_view']['payload']['intention_free_text'].startswith('SYNTHETIC ORACLE')
    assert comp['target_view']['payload'] == FIXTURES['F01']['neutral']
    result = app.export_study(report['study_id'])
    exported = Path(result['path']).read_text(encoding='utf-8')
    assert 'SYNTHETIC ORACLE TEST REFERENCE' not in exported
    assert FIXTURES['F01']['source'] not in exported
    assert 'raw_model_responses' in exported


def test_historical_oracle_is_pinned_after_new_amendment(tmp_path):
    app = StuApplication(tmp_path / 'data')
    report = smoke(app)
    sid = report['sample_id']
    old_oracle = app.capture.private_oracle(sid)
    edited = app.capture.begin_amendment(sid)
    assert edited['version'] == old_oracle['version'] + 1
    app.capture.save_intention(sid, 'SYNTHETIC DIFFERENT LATER INTENTION')
    app.capture.freeze(sid)
    new_oracle = app.capture.private_oracle(sid)
    assert new_oracle['version'] == 2
    assert old_oracle['intention_free_text'] != new_oracle['intention_free_text']
    cid = next(c['comparison_id'] for c in app.list_comparisons(report['study_id'])
               if c['kind'] == 'oracle_vs_original')
    pinned = app.get_comparison(cid)['reference_view']['payload']
    assert pinned['version'] == 1
    assert pinned['intention_free_text'] == old_oracle['intention_free_text']


def test_source_packet_with_private_field_fails_before_running(tmp_path):
    app = StuApplication(tmp_path / 'data')
    report = smoke(app)
    sid = report['sample_id']
    path = app.store.root / 'stu_inputs' / (sid + '.json')
    packet = json.loads(path.read_text())
    packet['intention_free_text'] = 'TOP_SECRET_ORACLE_CANARY'
    atomic_json(path, packet)
    with pytest.raises(ValueError, match='unexpected fields'):
        app.run_sample(report['study_id'])


def test_synthetic_incomplete_cannot_be_reported_as_valid_pair(tmp_path):
    app = StuApplication(tmp_path / 'data')
    report = smoke(app, fixture_id='F08')
    assert report['run_status'] == 'incomplete'
    assert report['verification']['valid'] is True  # correctly retained evidence
    assert report['results']['paired_reconstructions'] == []
    assert report['results']['run_status_counts']['incomplete'] == 1


def test_real_adapter_and_scored_modes_fail_closed(tmp_path):
    app = StuApplication(tmp_path / 'data')
    report = smoke(app)
    with pytest.raises(ValueError, match='Only deterministic synthetic'):
        app.run_sample(report['study_id'], adapter='openai')
    with pytest.raises(ValueError, match='Only deterministic synthetic'):
        app.run_sample(report['study_id'], mode='scored')
