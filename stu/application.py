"""Single in-process Python API for CLI and deliberately thin Streamlit pages."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from sera.application import SeraApplication
from .contracts import canonical, digest, now
from .fixtures import FIXTURES, get_fixture
from .review import HumanReview
from .runner import ExperimentRunner, prompt_hashes
from .storage import StuStore, atomic_json


class StuApplication:
    def __init__(self, data_root: str | Path = 'data', *, clock=now):
        self.store = StuStore(data_root)
        self.capture = SeraApplication(data_root)
        self.review = HumanReview(self.store, clock=clock)

    def list_studies(self) -> list[dict]:
        return self.store.list_studies()

    def create_study(self, sample_id: str, *, fixture_id: str = 'STRUCTURAL') -> dict:
        get_fixture(fixture_id)
        oracle = self.capture.private_oracle(sample_id)
        packet = self.capture.model_packet(sample_id)
        if fixture_id != 'STRUCTURAL' and packet['original_text'] != FIXTURES[fixture_id]['source']:
            raise ValueError('Synthetic fixture selected for an unrelated source. Use STRUCTURAL instead.')
        semantic_schema = (Path(__file__).resolve().parents[1] / 'schemas' / 'semantic_v0.1.json')
        return self.store.create_study(sample_id=sample_id,
            source_sha256=packet['source_sha256'], fixture_id=fixture_id,
            oracle_ref={'sample_id': sample_id, 'version': oracle['version'],
                        'explication_id': oracle['explication_id'],
                        'artifact_sha256': oracle['artifact_sha256']},
            prompts=prompt_hashes(), schema_sha256=digest(semantic_schema.read_bytes()),
            implementation='disco-stu-deterministic-v0.1')

    def run_sample(self, study_id: str, *, adapter: str = 'fixture',
                   mode: str = 'synthetic_test') -> dict:
        if adapter != 'fixture' or mode != 'synthetic_test':
            raise ValueError('Only deterministic synthetic execution is implemented.')
        return ExperimentRunner(self.store).run(study_id)

    def get_study(self, study_id: str) -> dict:
        return self.store.get_study(study_id)

    def list_comparisons(self, study_id: str) -> list[dict]:
        return [dict(comp, review=self.review.state(comp['comparison_id']))
                for comp in self.store.list_comparisons(study_id)]

    def get_comparison(self, comparison_id: str) -> dict:
        """Explicit reviewer-only API. Never invoke this from ModelAdapter/runner."""
        comp = self.store.get_comparison(comparison_id)
        private_ref = self.store.private_oracle_reference(comp['study_id'])
        oracle = self.capture.get_frozen_version(private_ref['sample_id'],
            private_ref['version'], explication_id=private_ref['explication_id'],
            sha256=private_ref['artifact_sha256'])

        def read_side(name: str) -> dict:
            if name == 'oracle':
                return {'kind': 'human_oracle', 'payload': oracle,
                        'sha256': private_ref['artifact_sha256'], 'private': True}
            raw = self.store.load_artifact(comp['run_id'], name)
            if name.endswith('.json'):
                payload = json.loads(raw)
            else:
                payload = raw.decode('utf-8')
            return {'kind': name, 'payload': payload, 'sha256': digest(raw), 'private': False}

        # Freshly resolve the pinned reference. Never silently use amended latest Oracle.
        ref = read_side(comp['reference'])
        target = read_side(comp['target'])
        if comp['reference'] != 'oracle' and ref['sha256'] != comp['reference_sha256']:
            raise RuntimeError('Comparison reference hash mismatch.')
        if target['sha256'] != comp['target_sha256']:
            raise RuntimeError('Comparison target hash mismatch.')
        return {**comp, 'reference_view': ref, 'target_view': target,
                'review': self.review.state(comparison_id)}

    def begin_gap_explanation(self, cid: str) -> dict:
        return self.review.begin(cid)

    def pause_gap_explanation(self, cid: str) -> dict:
        return self.review.pause(cid)

    def resume_gap_explanation(self, cid: str) -> dict:
        return self.review.resume(cid)

    def interrupt_gap_explanation(self, cid: str) -> dict:
        return self.review.interrupt(cid)

    def save_gap_explanation(self, cid: str, explanation: str, *,
                             gaps: list[dict] | None = None,
                             no_gap: bool = False) -> dict:
        return self.review.save(cid, explanation, gaps=gaps, no_gap=no_gap)

    def complete_gap_explanation(self, cid: str) -> dict:
        return self.review.complete(cid)

    def amend_gap_explanation(self, cid: str) -> dict:
        return self.review.amend(cid)

    def validate(self, study_id: str) -> dict:
        study = self.store.get_study(study_id)
        packet = self.store.source_packet(study['sample_id'])
        errors = []
        reports = []
        for run_id in study['runs']:
            try:
                reports.append(self.store.verify_run(run_id))
                run = self.store.get_run(run_id)
                decompose = next((s for s in run['steps'] if s['step'] == 'decompose' and s['status'] == 'completed'), None)
                branches = [s for s in run['steps'] if s['step'] in ('neutral', 'commercial')]
                if branches:
                    parsed = self.store.load_artifact(run_id, 'decompose.parsed.json')
                    for branch in branches:
                        if branch['input_sha256'] != digest(parsed):
                            raise RuntimeError('Reconstruction branches do not share exact intermediate hash.')
                        request = json.loads(self.store.load_artifact(run_id, branch['step'] + '.request.json'))
                        body = json.loads(request['messages'][1]['content'])
                        if set(body) != {'decomposition'}:
                            raise RuntimeError('Reconstruction contains other inputs, possible Oracle/source leak.')
                        if digest(canonical(body['decomposition'])) != digest(parsed):
                            raise RuntimeError('Reconstruction request contents differ from the frozen intermediate.')
                if decompose:
                    inp = json.loads(self.store.load_artifact(run_id, 'decompose.request.json'))
                    source_body = json.loads(inp['messages'][1]['content'])
                    if set(source_body) != {'source_packet'} or source_body['source_packet'] != packet:
                        raise RuntimeError('Decomposition source-only boundary failed.')
            except (ValueError, KeyError, RuntimeError, OSError) as exc:
                errors.append({'run_id': run_id, 'error': str(exc)})
        return {'study_id': study_id, 'valid': not errors,
                'synthetic': True, 'runs': reports, 'errors': errors}

    def get_results(self, study_id: str) -> dict:
        study = self.store.get_study(study_id)
        runs = [self.store.get_run(rid) for rid in study['runs']]
        comparisons = self.store.list_comparisons(study_id)
        reviews = [self.review.state(c['comparison_id']) for c in comparisons]
        counts = dict(Counter(r['status'] for r in runs))
        kinds = dict(Counter(g.get('label') for rev in reviews if rev['status'] == 'completed'
                             for g in rev['gaps']))
        pairs = []
        for run in runs:
            steps = {s['step']: s for s in run['steps']}
            n, c = steps.get('neutral'), steps.get('commercial')
            if n and c and n['status'] == c['status'] == 'completed' and n['input_sha256'] == c['input_sha256']:
                pairs.append({'run_id': run['run_id'], 'intermediate_sha256': n['input_sha256'],
                              'neutral_output_sha256': n['output_sha256'],
                              'commercial_output_sha256': c['output_sha256'],
                              'human_semantic_verdict': 'not_automatically_assessed'})
        return {'study_id': study_id, 'mode': study['mode'], 'synthetic': True,
                'planned_run_count': len(runs), 'run_status_counts': counts,
                'runs': [{'run_id': r['run_id'], 'status': r['status'], 'steps': r['steps']} for r in runs],
                'comparison_count': len(comparisons),
                'completed_reviews': sum(rev['status'] == 'completed' for rev in reviews),
                'review_gap_labels': kinds, 'completed_explanation_active_seconds':
                [rev['active_seconds'] for rev in reviews if rev['status'] == 'completed'],
                'paired_reconstructions': pairs, 'research_verdict': 'NO EMPIRICAL MODEL RESULTS',
                'validation': self.validate(study_id)}

    def export_study(self, study_id: str, *, privacy_level: str = 'safe') -> dict:
        if privacy_level != 'safe':
            raise ValueError('Only private-safe export implemented; explicit publication is out of scope.')
        report = self.get_results(study_id)
        summary = {'export_schema': 'stu.safe.v0.1', 'created_at': now(),
                   'privacy_level': 'safe', 'study_id': study_id,
                   'report': report,
                   'excluded': ['source_text', 'human_oracle', 'private_provenance',
                                'raw_model_requests', 'raw_model_responses', 'human_explanations']}
        destination = self.store.root / 'exports' / f'{study_id}-safe.json'
        atomic_json(destination, summary)
        return {'path': str(destination), 'sha256': digest(canonical(summary)),
                'privacy_level': 'safe', 'report': report}
