"""Single in-process Python API for CLI and deliberately thin Streamlit pages."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from sera.application import SeraApplication
from .bundle import build_full_bundle
from .adaption_api import SUPPORTED_MODELS
from .live import AdaptionModelAdapter
from .protocol import frozen_protocol, SCHEMA_PATH
from .contracts import canonical, digest, now
from .fixtures import FIXTURES, get_fixture
from .review import HumanReview
from .runner import ExperimentRunner, prompt_hashes
from .storage import StuStore, atomic_json


PRIMARY_REVIEW_KINDS = ('oracle_vs_neutral', 'oracle_vs_commercial')
ORIGINAL_FINAL_KINDS = frozenset(('original_vs_neutral', 'original_vs_commercial'))
RECONSTRUCTION_DIAGNOSTIC_KINDS = ('decomposition_vs_neutral', 'decomposition_vs_commercial')


class StuApplication:
    def __init__(self, data_root: str | Path = 'data', *, clock=now):
        self.store = StuStore(data_root)
        self.capture = SeraApplication(data_root)
        self.review = HumanReview(self.store, clock=clock)

    def list_studies(self) -> list[dict]:
        return self.store.list_studies()

    def create_study(self, sample_id: str, *, fixture_id: str = 'STRUCTURAL',
                     mode: str = 'synthetic_test',
                     model_id: str | None = None) -> dict:
        if mode not in ('synthetic_test', 'live'):
            raise ValueError('Study mode must be live or synthetic_test.')
        if mode == 'live':
            if model_id not in SUPPORTED_MODELS:
                raise ValueError('Unsupported Adaption model selection.')
        else:
            get_fixture(fixture_id)
        oracle = self.capture.private_oracle(sample_id)
        packet = self.capture.model_packet(sample_id)
        if (mode == 'synthetic_test' and fixture_id != 'STRUCTURAL'
                and packet['original_text'] != FIXTURES[fixture_id]['source']):
            raise ValueError('Synthetic fixture selected for an unrelated source. Use STRUCTURAL instead.')
        artifacts, paths, hashes = frozen_protocol(mode)
        return self.store.create_study(
            sample_id=sample_id, source_sha256=packet['source_sha256'],
            fixture_id=fixture_id,
            oracle_ref={'sample_id': sample_id, 'version': oracle['version'],
                        'explication_id': oracle['explication_id'],
                        'artifact_sha256': oracle['artifact_sha256']},
            prompts=hashes, schema_sha256=digest(artifacts[SCHEMA_PATH]),
            implementation='disco-stu-live-v0.1' if mode == 'live'
                           else 'disco-stu-deterministic-v0.1',
            mode=mode, model_id=model_id if mode == 'live' else None,
            protocol_artifacts=artifacts, prompt_paths=paths)

    def run_sample(self, study_id: str, *, adapter: str | None = None,
                   mode: str | None = None, api_key: str | None = None) -> dict:
        study = self.store.get_study(study_id)
        wanted_mode = mode or study['mode']
        wanted_adapter = adapter or ('adaption' if wanted_mode == 'live' else 'fixture')
        if wanted_mode != study['mode']:
            raise ValueError('Only deterministic synthetic or pinned live execution for this study.')
        if wanted_mode == 'live':
            if wanted_adapter != 'adaption':
                raise ValueError('Live study requires the Adaption adapter.')
            live_adapter = AdaptionModelAdapter(api_key=api_key)
            return ExperimentRunner(self.store, live_adapter).run(
                study_id, model_profile=study['model_id'])
        if wanted_adapter != 'fixture':
            raise ValueError('Only deterministic synthetic fixture execution for this study.')
        return ExperimentRunner(self.store).run(study_id)

    def get_study(self, study_id: str) -> dict:
        return self.store.get_study(study_id)

    def list_comparisons(self, study_id: str) -> list[dict]:
        """Put final-output human reviews first; keep diagnostics available, optional."""
        comparisons = self.store.list_comparisons(study_id)
        priority = {kind: i for i, kind in enumerate(PRIMARY_REVIEW_KINDS)}
        comparisons.sort(key=lambda comp: (0 if comp['kind'] in priority else 1,
                                            priority.get(comp['kind'], 99),
                                            comp['run_id'], comp['kind']))
        return [dict(comp,
                     review_role='primary' if comp['kind'] in priority else 'diagnostic',
                     review=self.review.state(comp['comparison_id']))
                for comp in comparisons]

    def reconcile_original_final_comparisons(self, study_id: str) -> dict:
        """Explicit, idempotent historical backfill. No model call or old-file rewrite."""
        study = self.store.get_study(study_id)
        created = []
        for run_id in study['runs']:
            run = self.store.get_run(run_id)
            if run['study_id'] != study_id:
                raise RuntimeError('Run belongs to a different study.')
            self.store.verify_run(run_id)
            created.extend(ExperimentRunner(self.store)._comparisons(
                run_id, only_kinds=ORIGINAL_FINAL_KINDS))
        return {'study_id': study_id, 'created_count': len(created),
                'comparison_ids': created,
                'note': 'Existing comparisons and human review events were not changed.'}

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
        result = {**comp, 'reference_view': ref, 'target_view': target,
                  'review': self.review.state(comparison_id)}
        if comp['kind'] in RECONSTRUCTION_DIAGNOSTIC_KINDS:
            run = self.store.get_run(comp['run_id'])
            if run['mode'] == 'live':
                # The persisted comparison still refers to the FULL decomposition.
                # This additive view shows the EXACT bytes the model actually saw.
                projection_name = 'decompose.reconstruction_projection.json'
                raw = self.store.load_artifact(comp['run_id'], projection_name)
                condition = comp['kind'].rsplit('_vs_', 1)[1]
                step = next((step for step in run['steps'] if step['step'] == condition), None)
                if step is None or step['status'] != 'completed':
                    raise RuntimeError('Diagnostic reconstruction has no successful stage.')
                if step['input_sha256'] != digest(raw):
                    raise RuntimeError('Reconstruction input hash does not match frozen projection.')
                provider = json.loads(self.store.load_artifact(
                    comp['run_id'], condition + '.provider_request.json'))
                if provider['input'].encode('utf-8') != raw:
                    raise RuntimeError('Provider received different projection bytes.')
                result['model_visible_projection_view'] = {
                    'kind': 'exact_model_visible_reconstruction_input',
                    'artifact_name': projection_name, 'payload': json.loads(raw),
                    'sha256': digest(raw), 'byte_count': len(raw), 'private': False,
                    'verified_against_stage': condition,
                }
        return result

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
                    live = study['mode'] == 'live'
                    projected = (self.store.load_artifact(run_id,
                        'decompose.reconstruction_projection.json') if live else parsed)
                    if live:
                        from .projection import projection_bytes
                        if projected != projection_bytes(json.loads(parsed)):
                            raise RuntimeError('Frozen reconstruction projection differs from full decomposition.')
                    for branch in branches:
                        if branch['input_sha256'] != digest(projected):
                            raise RuntimeError('Reconstruction branches do not share exact intermediate hash.')
                        request = json.loads(self.store.load_artifact(run_id, branch['step'] + '.request.json'))
                        user_text = request['messages'][1]['content']
                        if live:
                            if user_text.encode('utf-8') != projected or 'source_support' in user_text:
                                raise RuntimeError('Live reconstruction request differs from frozen projection.')
                            provider = json.loads(self.store.load_artifact(
                                run_id, branch['step'] + '.provider_request.json'))
                            if provider['input'] != user_text or provider['instructions'] != request['messages'][0]['content']:
                                raise RuntimeError('Recorded SDK reconstruction request mismatch.')
                            if provider.get('store') is not False or provider.get('agentic_memory') is not False or provider.get('tools') != []:
                                raise RuntimeError('Live provider request is not stateless/tool-free.')
                        else:
                            body = json.loads(user_text)
                            if set(body) != {'decomposition'}:
                                raise RuntimeError('Reconstruction contains other inputs, possible Oracle/source leak.')
                            if digest(canonical(body['decomposition'])) != digest(parsed):
                                raise RuntimeError('Reconstruction request contents differ from frozen intermediate.')
                if decompose:
                    inp = json.loads(self.store.load_artifact(run_id, 'decompose.request.json'))
                    source_body = json.loads(inp['messages'][1]['content'])
                    if set(source_body) != {'source_packet'} or source_body['source_packet'] != packet:
                        raise RuntimeError('Decomposition source-only boundary failed.')
                    if study['mode'] == 'live':
                        provider = json.loads(self.store.load_artifact(run_id,
                            'decompose.provider_request.json'))
                        if provider['input'] != inp['messages'][1]['content']:
                            raise RuntimeError('SDK decomposition input mismatch.')
                        if provider.get('store') is not False or provider.get('agentic_memory') is not False or provider.get('tools') != []:
                            raise RuntimeError('SDK decomposition request is not stateless/tool-free.')
            except (ValueError, KeyError, RuntimeError, OSError) as exc:
                errors.append({'run_id': run_id, 'error': str(exc)})
        return {'study_id': study_id, 'valid': not errors,
                'mode': study['mode'], 'synthetic': study['mode'] == 'synthetic_test',
                'runs': reports, 'errors': errors}

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
        primary = [c for c in comparisons if c['kind'] in PRIMARY_REVIEW_KINDS]
        completed_primary = sum(self.review.state(c['comparison_id'])['status'] == 'completed'
                                for c in primary)
        return {'study_id': study_id, 'mode': study['mode'],
                'synthetic': study['mode'] == 'synthetic_test',
                'model_id': study.get('model_id'),
                'recorded_run_count': len(runs), 'run_status_counts': counts,
                'runs': [{'run_id': r['run_id'], 'status': r['status'], 'steps': r['steps']} for r in runs],
                'comparison_count': len(comparisons),
                'primary_comparison_count': len(primary),
                'completed_primary_reviews': completed_primary,
                'diagnostic_comparison_count': len(comparisons) - len(primary),
                'completed_reviews': sum(rev['status'] == 'completed' for rev in reviews),
                'review_gap_labels': kinds, 'completed_explanation_active_seconds':
                [rev['active_seconds'] for rev in reviews if rev['status'] == 'completed'],
                'paired_reconstructions': pairs,
                'research_verdict': ('NO EMPIRICAL MODEL RESULTS' if study['mode'] == 'synthetic_test'
                                      else 'LIVE INFERENCE; SEMANTIC CORRECTNESS NOT ASSESSED'),
                'validation': self.validate(study_id)}

    def export_study(self, study_id: str, *, privacy_level: str = 'full') -> dict:
        """Default: complete private bundle. Explicit 'safe': redacted sharing summary."""
        if privacy_level not in ('full', 'safe'):
            raise ValueError('Export privacy_level must be full or safe.')
        report = self.get_results(study_id)
        if privacy_level == 'full':
            return build_full_bundle(self.store, self.capture, study_id, report)
        summary = {'export_schema': 'stu.safe.v0.1', 'created_at': now(),
                   'privacy_level': 'safe', 'study_id': study_id,
                   'report': report,
                   'excluded': ['source_text', 'human_oracle', 'private_provenance',
                                'raw_model_requests', 'raw_model_responses', 'human_explanations']}
        destination = self.store.root / 'exports' / f'{study_id}-safe.json'
        atomic_json(destination, summary)
        return {'path': str(destination), 'sha256': digest(canonical(summary)),
                'privacy_level': 'safe', 'report': report}

    def get_export_bytes(self, study_id: str, *, privacy_level: str = 'full') -> bytes:
        """Allow the thin UI to download an explicitly created local export."""
        from .storage import safe_id
        if privacy_level not in ('full', 'safe'):
            raise ValueError('Export privacy_level must be full or safe.')
        self.store.get_study(study_id)
        suffix = 'full.zip' if privacy_level == 'full' else 'safe.json'
        return (self.store.root / 'exports' / f'{safe_id(study_id)}-{suffix}').read_bytes()
