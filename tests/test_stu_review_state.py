"""Regression suite for single-user Review lifecycle and archival timing quality."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from stu.application import StuApplication
from stu.cli import smoke
from stu.review import HumanReview
from stu.storage import EventJournal


def prepared(tmp_path):
    app = StuApplication(tmp_path / 'data')
    run = smoke(app, fixture_id='F01')
    comps = app.list_review_choices(run['study_id'], run['run_id'])
    assert [c['kind'] for c in comps] == ['original_vs_neutral', 'original_vs_commercial']
    return app, run, [c['comparison_id'] for c in comps]


def test_no_overlapping_active_review_and_restart_recovers_active(tmp_path):
    app, run, (neutral, commercial) = prepared(tmp_path)
    assert app.active_review() is None
    app.begin_gap_explanation(neutral)
    assert app.active_review()['comparison_id'] == neutral
    restarted = StuApplication(app.store.root)
    assert restarted.active_review()['comparison_id'] == neutral
    with pytest.raises(ValueError, match='Another explanation timer'):
        restarted.begin_gap_explanation(commercial)
    app.pause_gap_explanation(neutral)
    assert restarted.active_review() is None
    app.begin_gap_explanation(commercial)
    with pytest.raises(ValueError, match='Another explanation timer'):
        app.resume_gap_explanation(neutral)
    assert app.active_review()['comparison_id'] == commercial
    app.pause_gap_explanation(commercial)
    app.resume_gap_explanation(neutral)
    assert app.active_review()['comparison_id'] == neutral


def test_one_real_save_no_duplicates_paused_edits_forbidden_and_amendment_timed(tmp_path):
    app, run, (neutral, commercial) = prepared(tmp_path)
    review = app.review
    review.begin(neutral)
    saved = review.save(neutral, 'Original rhetoric was changed.')
    assert saved['event_count'] == 2
    assert review.save(neutral, 'Original rhetoric was changed.')['event_count'] == 2
    paused = review.pause(neutral)
    assert paused['status'] == 'paused'
    with pytest.raises(ValueError, match='Resume the explanation timer'):
        review.save(neutral, 'Changed while paused.')
    assert review.save(neutral, 'Original rhetoric was changed.')['event_count'] == 3
    completed = review.complete(neutral)
    assert completed['status'] == 'completed'
    review.amend(neutral)
    with pytest.raises(ValueError, match='Resume the explanation timer'):
        review.save(neutral, 'An untimed amendment')
    resumed = review.resume(neutral)
    assert resumed['status'] == 'explaining'
    modified = review.save(neutral, 'Original rhetoric was changed; amended with evidence.')
    assert modified['explanation'].endswith('evidence.')
    review.complete(neutral)
    assert review.state(neutral)['event_count'] == 8
    assert review.state(neutral)['labor_measurement_incomplete'] is False
    assert review.state(neutral)['explicit_meaningful_difference'] is True


def test_cumulative_fifteen_min_budget_independent_from_long_interval(tmp_path):
    app, run, (neutral, commercial) = prepared(tmp_path)
    t = datetime(2026, 11, 15, tzinfo=timezone.utc)
    clock = iter((t, t + timedelta(seconds=500), t + timedelta(seconds=600),
                  t + timedelta(seconds=1001)))
    review = HumanReview(app.store, clock=lambda: next(clock).isoformat())
    review.begin(neutral)
    review.pause(neutral)
    review.resume(neutral)
    final = review.pause(neutral)
    assert final['active_seconds'] == pytest.approx(901.0)
    assert final['reached_15min_budget'] is True
    assert final['timing_uncertain'] is False
    assert final['labor_measurement_incomplete'] is False

    clock2 = iter((t, t + timedelta(seconds=1000)))
    other = HumanReview(app.store, clock=lambda: next(clock2).isoformat())
    other.begin(commercial)
    uncertain = other.pause(commercial)
    assert uncertain['active_seconds'] == 0
    assert uncertain['reached_15min_budget'] is False
    assert uncertain['timing_uncertain'] is True
    assert uncertain['labor_measurement_incomplete'] is True


def test_historical_paused_save_is_flagged_without_rewriting_events(tmp_path):
    app, run, (neutral, commercial) = prepared(tmp_path)
    journal = EventJournal(app.store.review_path(commercial) / 'events.jsonl')
    t = datetime(2026, 11, 15, 20, tzinfo=timezone.utc)
    iso = lambda seconds: (t + timedelta(seconds=seconds)).isoformat()
    journal.append('begin', {}, at=iso(0))
    journal.append('pause', {}, at=iso(30))
    journal.append('save', {'explanation': 'A careful interpretation.',
                            'gaps': [], 'no_gap': False}, at=iso(421))
    journal.append('complete', {}, at=iso(425))
    original = journal.path.read_bytes()

    state = app.review.state(commercial)
    assert state['status'] == 'completed'
    assert state['active_seconds'] == 30
    assert state['timing_uncertain'] is False
    assert state['unmeasured_edit_event'] is True
    assert state['labor_measurement_incomplete'] is True
    assert state['explicit_meaningful_difference'] is True
    report = app.get_results(run['study_id'])
    assert report['free_text_findings_count'] == 1
    assert report['explicit_no_gap_reviews'] == 0
    assert report['review_gap_labels'] == {}
    assert report['reviews_with_incomplete_labor_measurement'] == 1
    assert journal.path.read_bytes() == original


def test_historical_untimed_amendment_flagged_even_if_text_unchanged(tmp_path):
    app, run, (neutral, commercial) = prepared(tmp_path)
    j = EventJournal(app.store.review_path(neutral) / 'events.jsonl')
    t = datetime(2026, 11, 15, 20, tzinfo=timezone.utc)
    iso = lambda seconds: (t + timedelta(seconds=seconds)).isoformat()
    j.append('begin', {}, at=iso(0))
    j.append('save', {'explanation': 'Same statement', 'gaps': [],
                      'no_gap': False}, at=iso(10))
    j.append('complete', {}, at=iso(12))
    j.append('amend', {}, at=iso(13))
    j.append('save', {'explanation': 'Same statement', 'gaps': [],
                      'no_gap': False}, at=iso(40))
    j.append('complete', {}, at=iso(41))
    before = j.path.read_bytes()
    state = app.review.state(neutral)
    assert state['active_seconds'] == 12
    assert state['unmeasured_edit_event']
    assert state['labor_measurement_incomplete']
    assert j.path.read_bytes() == before


def test_free_text_and_explicit_no_gap_both_reported_without_labels(tmp_path):
    app, run, (neutral, commercial) = prepared(tmp_path)
    app.begin_gap_explanation(neutral)
    app.save_gap_explanation(neutral, 'The three-line break mattered.')
    app.complete_gap_explanation(neutral)
    app.begin_gap_explanation(commercial)
    app.save_gap_explanation(commercial, '', no_gap=True)
    app.complete_gap_explanation(commercial)
    report = app.get_results(run['study_id'])
    assert report['completed_primary_reviews'] == 2
    assert report['free_text_findings_count'] == 1
    assert report['explicit_no_gap_reviews'] == 1
    assert report['review_gap_labels'] == {}
    assert report['reviews_with_incomplete_labor_measurement'] == 0
    exported = app.export_study(run['study_id'], privacy_level='safe')
    assert exported['report']['free_text_findings_count'] == 1
    assert exported['report']['explicit_no_gap_reviews'] == 1
