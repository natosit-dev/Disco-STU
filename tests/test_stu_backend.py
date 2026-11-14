"""Offline, deterministic tests; no external model and no human judgements."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from stu.contracts import (GenerationRequest, clean_semantics, canonical, digest)
from stu.fixtures import FIXTURES, DeterministicFixtureAdapter
from stu.storage import StuStore, EventJournal, atomic_json
from stu.runner import ExperimentRunner, prompt_hashes
from stu.review import HumanReview


def prepared(tmp_path, fixture_id='F01'):
    store = StuStore(tmp_path / 'data')
    fixture = FIXTURES[fixture_id]
    sample_id = 'test-sample-' + fixture_id
    source = {'packet_type': 'stu_source_v0.1', 'sample_id': sample_id,
              'source_sha256': digest(fixture['source']), 'original_text': fixture['source']}
    atomic_json(store.root / 'stu_inputs' / (sample_id + '.json'), source)
    study = store.create_study(sample_id=sample_id, source_sha256=source['source_sha256'],
        fixture_id=fixture_id, oracle_ref={'version': 1, 'explication_id': 'private-oracle-secret'},
        prompts=prompt_hashes(), schema_sha256='test-schema', implementation='deterministic-test')
    return store, study


def test_fake_is_exact_and_never_semantically_falls_back():
    fixture = FIXTURES['F01']
    source = {'packet_type': 'stu_source_v0.1', 'sample_id': 'x',
              'original_text': fixture['source'], 'source_sha256': digest(fixture['source'])}
    req = GenerationRequest(stage='decompose', condition='none', fixture_id='F01',
        model_profile='fixture', system='synthetic', user=json.dumps({'source_packet': source}),
        input_sha256=digest(fixture['source']))
    adapter = DeterministicFixtureAdapter()
    assert adapter.generate(req).content == adapter.generate(req).content
    parsed = clean_semantics(json.loads(adapter.generate(req).content))
    assert parsed['units'][0]['text'] == fixture['meaning']
    with pytest.raises(ValueError, match='Unknown deterministic fixture'):
        adapter.generate(GenerationRequest(**{**req.__dict__, 'fixture_id': 'NO_SUCH_FIXTURE'}))
    altered = {**source, 'original_text': 'ANOTHER SOURCE'}
    with pytest.raises(ValueError, match='exact known synthetic'):
        adapter.generate(GenerationRequest(**{**req.__dict__,
                 'user': json.dumps({'source_packet': altered})}))


def test_runner_keeps_exact_parent_and_isolates_branches(tmp_path):
    store, study = prepared(tmp_path)
    run = ExperimentRunner(store).run(study['study_id'])
    assert run['status'] == 'completed'
    report = store.verify_run(run['run_id'])
    assert report['valid']
    decomp = store.load_artifact(run['run_id'], 'decompose.parsed.json')
    assert [s['step'] for s in run['steps']] == ['decompose', 'neutral', 'commercial']
    for condition in ('neutral', 'commercial'):
        req = json.loads(store.load_artifact(run['run_id'], condition + '.request.json'))
        assert req['input_sha256'] == digest(decomp)
        body = json.loads(req['messages'][1]['content'])
        assert set(body) == {'decomposition'}
        assert canonical(body['decomposition']) == decomp
        assert 'private-oracle-secret' not in json.dumps(req)
        assert 'source_packet' not in json.dumps(body)
    comps = store.list_comparisons(study['study_id'])
    assert len(comps) == 8
    assert all(x['synthetic'] and x['semantic_verdict'] == 'not_evaluated' for x in comps)


@pytest.mark.parametrize('fid,expected', [('F07','incomplete'),('F08','incomplete')])
def test_invalid_json_and_incomplete_pair_remain_evidence(tmp_path, fid, expected):
    store, study = prepared(tmp_path, fid)
    run = ExperimentRunner(store).run(study['study_id'])
    assert run['status'] == expected
    assert store.verify_run(run['run_id'])['valid']
    if fid == 'F07':
        assert run['steps'][0]['status'] == 'invalid_output'
        assert store.load_artifact(run['run_id'], 'decompose.response.txt').startswith(b'{')
        assert 'decompose.parsed.json' not in run['artifacts']
    else:
        assert run['steps'][2]['status'] == 'failed'
        assert run['steps'][1]['status'] == 'completed'
        assert 'neutral.response.txt' in run['artifacts']
        assert 'commercial.error.json' in run['artifacts']


def test_event_chain_and_artifact_corruption_detected(tmp_path):
    store, study = prepared(tmp_path)
    run = ExperimentRunner(store).run(study['study_id'])
    path = store.run_path(run['run_id']) / 'artifacts' / 'neutral.response.txt'
    path.write_bytes(b'changed')
    with pytest.raises(RuntimeError, match='Corrupted artifact'):
        store.verify_run(run['run_id'])
    events = EventJournal(store.run_path(run['run_id']) / 'events.jsonl')
    assert events.read()
    with events.path.open('ab') as f:
        f.write(b'{"sequence":999}\n')
    with pytest.raises(RuntimeError, match='Event chain broken'):
        events.read()


def test_review_explanation_interval_and_explicit_no_gap(tmp_path):
    store, study = prepared(tmp_path)
    ExperimentRunner(store).run(study['study_id'])
    cid = store.list_comparisons(study['study_id'])[0]['comparison_id']
    anchor = datetime(2026, 11, 14, tzinfo=timezone.utc)
    values = iter((anchor, anchor + timedelta(seconds=12), anchor + timedelta(seconds=22),
                   anchor + timedelta(seconds=29), anchor + timedelta(seconds=42)))
    rv = HumanReview(store, clock=lambda: next(values).isoformat())
    a = rv.begin(cid)
    assert a['open_interval_since'] and a['active_seconds'] == 0
    assert rv.begin(cid)['event_count'] == 1  # duplicate click no second event
    assert rv.pause(cid)['active_seconds'] == 12
    assert rv.pause(cid)['event_count'] == 2
    assert rv.resume(cid)['status'] == 'explaining'
    rv.save(cid, 'The output changed the purpose.',
            gaps=[{'label': 'altered', 'rationale': 'Purpose shifted to maximize sales.'}])
    result = rv.complete(cid)
    assert result['active_seconds'] == 32
    assert result['status'] == 'completed'
    assert result['event_count'] == 5
    assert rv.complete(cid)['event_count'] == 5
    assert HumanReview(store).state(cid)['active_seconds'] == 32  # restart
    another = store.list_comparisons(study['study_id'])[1]['comparison_id']
    clock = iter((anchor, anchor + timedelta(seconds=2)))
    no_gap = HumanReview(store, clock=lambda: next(clock).isoformat())
    no_gap.begin(another)
    no_gap.save(another, '', no_gap=True)
    # need an additional clock value for completion
    no_gap.clock = lambda: (anchor + timedelta(seconds=3)).isoformat()
    assert no_gap.complete(another)['no_meaningful_gap'] is True


def test_long_unclosed_interval_not_silently_counted(tmp_path):
    store, study = prepared(tmp_path)
    ExperimentRunner(store).run(study['study_id'])
    cid = store.list_comparisons(study['study_id'])[0]['comparison_id']
    t = datetime(2026, 11, 14, tzinfo=timezone.utc)
    clock = iter((t, t + timedelta(hours=3)))
    review = HumanReview(store, clock=lambda: next(clock).isoformat())
    review.begin(cid)
    assert HumanReview(store).state(cid)['active_seconds'] == 0
    state = review.interrupt(cid)
    assert state['timing_uncertain']
    assert state['active_seconds'] == 0
    assert state['status'] == 'interrupted'


def test_thin_ui_static_boundary():
    root = Path(__file__).parents[1]
    for page in ['1_SERA.py','2_STU_Transform.py','3_STU_Review.py','4_STU_Results.py']:
        text = (root / 'pages' / page).read_text()
        assert 'from stu.storage import' not in text
        assert 'from stu.runner import' not in text
        assert 'from sera.storage import' not in text
        assert 'from sera.service import' not in text
        assert 'import requests' not in text
        assert 'open(' not in text
