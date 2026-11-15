"""Comparison coverage, review priorities and explicit historical reconciliation."""
from __future__ import annotations

import json
from zipfile import ZipFile

from stu.application import StuApplication
from stu.cli import smoke
from stu.fixtures import FIXTURES


def test_ten_comparisons_primary_first_and_source_final_correct(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app, fixture_id='F01')
    comparisons = app.list_comparisons(result['study_id'])
    assert len(comparisons) == 10
    assert [c['kind'] for c in comparisons[:2]] == [
        'oracle_vs_neutral', 'oracle_vs_commercial']
    assert all(c['review_role'] == 'primary' for c in comparisons[:2])
    assert all(c['review_role'] == 'diagnostic' for c in comparisons[2:])
    assert all(c['semantic_verdict'] == 'not_evaluated' for c in comparisons)
    assert len({c['comparison_id'] for c in comparisons}) == 10
    for condition in ('neutral', 'commercial'):
        comp = next(c for c in comparisons if c['kind'] == 'original_vs_' + condition)
        detail = app.get_comparison(comp['comparison_id'])
        assert detail['reference'] == 'source_packet.json'
        assert detail['reference_view']['payload']['original_text'] == FIXTURES['F01']['source']
        assert detail['target_view']['payload'] == FIXTURES['F01'][condition]
        assert detail['reference_view']['sha256'] == comp['reference_sha256']
        assert detail['target_view']['sha256'] == comp['target_sha256']
    summary = app.get_results(result['study_id'])
    assert summary['comparison_count'] == 10
    assert summary['primary_comparison_count'] == 2
    assert summary['diagnostic_comparison_count'] == 8
    assert summary['completed_primary_reviews'] == 0
    assert summary['validation']['valid']


def test_reconcile_archived_eight_idempotently_and_preserve_reviews(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app, fixture_id='F01')
    study_id = result['study_id']
    run_id = result['run_id']
    first = app.list_comparisons(study_id)[0]['comparison_id']
    app.begin_gap_explanation(first)
    app.save_gap_explanation(first, 'Human observation, preserved as written.',
                             gaps=[{'label': 'altered', 'rationale': 'Meaning changed.'}])
    app.complete_gap_explanation(first)
    review_path = app.store.review_path(first) / 'events.jsonl'
    original_review = review_path.read_bytes()
    study_path = app.store.study_path(study_id) / 'manifest.json'
    run_path = app.store.run_path(run_id) / 'run.json'
    study_before, run_before = study_path.read_bytes(), run_path.read_bytes()

    # Simulate the real 8-comparison archive from before this change.
    for kind in ('original_vs_neutral', 'original_vs_commercial'):
        app.store.comparison_path(run_id + '-' + kind).unlink()
    old_comparisons = app.store.list_comparisons(study_id)
    assert len(old_comparisons) == 8
    old_bytes = {c['comparison_id']: app.store.comparison_path(
        c['comparison_id']).read_bytes() for c in old_comparisons}
    assert app.get_results(study_id)['comparison_count'] == 8
    assert len(app.store.list_comparisons(study_id)) == 8  # reads do not migrate

    outcome = app.reconcile_original_final_comparisons(study_id)
    assert outcome['created_count'] == 2
    assert set(outcome['comparison_ids']) == {
        run_id + '-original_vs_neutral', run_id + '-original_vs_commercial'}
    assert app.reconcile_original_final_comparisons(study_id)['created_count'] == 0
    assert len(app.list_comparisons(study_id)) == 10
    assert app.get_results(study_id)['completed_primary_reviews'] == 1
    assert review_path.read_bytes() == original_review
    assert study_path.read_bytes() == study_before
    assert run_path.read_bytes() == run_before
    for cid, raw in old_bytes.items():
        assert app.store.comparison_path(cid).read_bytes() == raw
    with ZipFile(app.export_study(study_id)['path']) as archive:
        names = set(archive.namelist())
        for cid in outcome['comparison_ids']:
            assert 'comparisons/' + cid + '.json' in names
            record = json.loads(archive.read('comparisons/' + cid + '.json'))
            assert record['semantic_verdict'] == 'not_evaluated'
        assert 'reviews/' + first + '/events.jsonl' in names
        assert archive.read('reviews/' + first + '/events.jsonl') == original_review


def test_incomplete_run_only_compares_successful_final_outputs(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app, fixture_id='F08')
    kinds = {c['kind'] for c in app.list_comparisons(result['study_id'])}
    assert result['run_status'] == 'incomplete'
    assert 'original_vs_neutral' in kinds
    assert 'original_vs_commercial' not in kinds
    assert 'oracle_vs_neutral' in kinds
    assert 'oracle_vs_commercial' not in kinds
    assert app.reconcile_original_final_comparisons(result['study_id'])['created_count'] == 0
    assert app.get_results(result['study_id'])['primary_comparison_count'] == 1
