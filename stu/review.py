"""Human gap explanation, typed observations and persisted event-derived timing."""
from __future__ import annotations

from datetime import datetime, timezone
from .contracts import now
from .storage import EventJournal, StuStore

LABELS = ('preserved', 'omitted', 'altered', 'contradicted',
          'unsupported_addition', 'source_consistent_extension', 'unresolved_ambiguous')
MAX_UNCONFIRMED_SECONDS = 15 * 60


def seconds_between(left: str, right: str) -> float:
    a = datetime.fromisoformat(left)
    b = datetime.fromisoformat(right)
    if a.tzinfo is None or b.tzinfo is None:
        raise ValueError('Clock events must have time zone offsets.')
    delta = (b - a).total_seconds()
    if delta < 0:
        raise ValueError('Nonmonotonic review event timestamps.')
    return delta


class HumanReview:
    """No LLM, no semantic inference; only explicit human judgments."""
    def __init__(self, store: StuStore, clock=now):
        self.store = store
        self.clock = clock

    def _journal(self, comparison_id: str) -> EventJournal:
        self.store.get_comparison(comparison_id)
        return EventJournal(self.store.review_path(comparison_id) / 'events.jsonl')

    def state(self, comparison_id: str) -> dict:
        events = self._journal(comparison_id).read()
        status = 'not_started'
        active = 0.0
        began = None
        explanation = ''
        gaps = []
        no_gap = False
        uncertain = False
        for event in events:
            kind, at, details = event['kind'], event['at'], event['details']
            if kind in ('begin', 'resume'):
                began = at
                status = 'explaining'
            elif kind in ('pause', 'complete', 'interrupt'):
                if began is not None:
                    interval = seconds_between(began, at)
                    if interval <= MAX_UNCONFIRMED_SECONDS:
                        active += interval
                    else:
                        uncertain = True
                    began = None
                status = {'pause': 'paused', 'complete': 'completed',
                          'interrupt': 'interrupted'}[kind]
            elif kind == 'save':
                explanation = details['explanation']
                gaps = details['gaps']
                no_gap = details['no_gap']
            elif kind == 'amend':
                status = 'amended'
        # Intentionally do NOT count unclosed intervals. Browser reload cannot inflate time.
        return {'comparison_id': comparison_id, 'status': status,
                'active_seconds': active, 'open_interval_since': began,
                'timing_uncertain': uncertain,
                'explanation': explanation, 'gaps': gaps,
                'no_meaningful_gap': no_gap,
                'event_count': len(events), 'timing_protocol': 'untimed_inspection_explicit_begin_v0.1',
                'synthetic': self.store.get_comparison(comparison_id)['synthetic']}

    def _event(self, cid: str, name: str, details: dict | None = None) -> dict:
        self._journal(cid).append(name, details or {}, at=self.clock())
        return self.state(cid)

    def begin(self, cid: str) -> dict:
        state = self.state(cid)
        if state['status'] == 'explaining':
            return state
        if state['status'] != 'not_started':
            raise ValueError('Cannot begin review in its current state.')
        return self._event(cid, 'begin')

    def pause(self, cid: str) -> dict:
        state = self.state(cid)
        if state['status'] == 'paused':
            return state
        if state['status'] != 'explaining':
            raise ValueError('Cannot pause unless explanation is active.')
        return self._event(cid, 'pause')

    def resume(self, cid: str) -> dict:
        state = self.state(cid)
        if state['status'] == 'explaining':
            return state
        if state['status'] not in ('paused', 'interrupted'):
            raise ValueError('Can only resume a paused or interrupted explanation.')
        return self._event(cid, 'resume')

    def interrupt(self, cid: str) -> dict:
        state = self.state(cid)
        if state['status'] == 'interrupted':
            return state
        if state['status'] != 'explaining':
            raise ValueError('No active interval to interrupt.')
        return self._event(cid, 'interrupt')

    def save(self, cid: str, explanation: str, gaps: list[dict] | None = None,
             no_gap: bool = False) -> dict:
        state = self.state(cid)
        if state['status'] not in ('explaining', 'paused', 'interrupted', 'amended'):
            raise ValueError('Begin the explanation before saving.')
        gaps = gaps or []
        for gap in gaps:
            if not isinstance(gap, dict) or gap.get('label') not in LABELS or not gap.get('rationale', '').strip():
                raise ValueError('Each gap requires a valid label and human rationale.')
        if no_gap and gaps:
            raise ValueError('No-gap outcome cannot also list meaningful discrepancies.')
        return self._event(cid, 'save', {'explanation': explanation, 'gaps': gaps, 'no_gap': bool(no_gap)})

    def complete(self, cid: str) -> dict:
        state = self.state(cid)
        if state['status'] == 'completed':
            return state
        if state['status'] not in ('explaining', 'paused', 'amended'):
            raise ValueError('Review must have begun before completion.')
        if not state['no_meaningful_gap'] and not state['explanation'].strip():
            raise ValueError('A meaningful-gap completion requires written explanation.')
        if state['status'] == 'amended':
            # An amendment does not silently add more active time.
            return self._event(cid, 'complete')
        return self._event(cid, 'complete')

    def amend(self, cid: str) -> dict:
        if self.state(cid)['status'] != 'completed':
            raise ValueError('Amendment requires completed review.')
        return self._event(cid, 'amend')
