"""STU decomposition and paired reconstruction; absolutely no Oracle access."""
from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from .contracts import GenerationRequest, clean_semantics, canonical, digest, now
from .fixtures import DeterministicFixtureAdapter
from .storage import StuStore

PROMPTS = Path(__file__).resolve().parents[1] / 'prompts'


def prompt(name: str) -> str:
    return (PROMPTS / f'{name}_v0.1.txt').read_text(encoding='utf-8')


def prompt_hashes() -> dict:
    return {kind: digest(prompt(kind)) for kind in ('decompose', 'neutral', 'commercial')}


class ExperimentRunner:
    """Executes an offline test; has no SeraStore reference, Oracle path or manifest secret."""
    def __init__(self, store: StuStore, adapter=None):
        self.store = store
        self.adapter = adapter or DeterministicFixtureAdapter()

    def _call(self, run_id: str, *, stage: str, condition: str,
              fixture_id: str, model_profile: str, body: dict,
              input_sha256: str) -> dict:
        step_name = stage if stage == 'decompose' else condition
        request = GenerationRequest(
            stage=stage, condition=condition, fixture_id=fixture_id,
            model_profile=model_profile,
            system=prompt('decompose' if stage == 'decompose' else condition),
            user=json.dumps(body, ensure_ascii=False, sort_keys=True),
            input_sha256=input_sha256, settings={'temperature': 0,
                                                   'synthetic_only': True})
        wire = request.wire()
        self.store.artifact(run_id, step_name + '.request.json', canonical(wire))
        info = {'step': step_name, 'stage': stage, 'condition': condition,
                'started_at': now(), 'input_sha256': input_sha256,
                'request_sha256': digest(wire), 'prompt_sha256': digest(request.system),
                'adapter': self.adapter.name, 'synthetic': True}
        try:
            response = self.adapter.generate(request)
            self.store.artifact(run_id, step_name + '.response.txt', response.content.encode('utf-8'))
            response_metadata = response.as_dict()
            response_metadata.pop('content', None)
            self.store.artifact(run_id, step_name + '.response_metadata.json', canonical(response_metadata))
            info['output_sha256'] = digest(response.content)
            if stage == 'decompose':
                try:
                    parsed = clean_semantics(json.loads(response.content))
                except (ValueError, TypeError) as exc:
                    info['status'] = 'invalid_output'
                    info['error'] = f'{type(exc).__name__}: {exc}'
                else:
                    self.store.artifact(run_id, 'decompose.parsed.json', canonical(parsed))
                    info['status'] = 'completed'
            else:
                info['status'] = 'completed' if response.content.strip() else 'invalid_output'
                if info['status'] != 'completed':
                    info['error'] = 'Empty reconstruction is not a valid result.'
        except Exception as exc:
            info['status'] = 'failed'
            info['error'] = f'{type(exc).__name__}: {exc}'
            self.store.artifact(run_id, step_name + '.error.json', canonical({'error': info['error']}))
        info['finished_at'] = now()
        self.store.step(run_id, info)
        return info

    def run(self, study_id: str, model_profile: str = 'fixture') -> dict:
        study = self.store.get_study(study_id)
        if study['mode'] != 'synthetic_test' or study.get('scored'):
            raise ValueError('Only synthetic_test studies are executable by this runner.')
        if study['adapter'] != self.adapter.name:
            raise ValueError('Study configured with a different adapter.')
        if study['prompt_sha256'] != prompt_hashes():
            raise ValueError('Prompt text has changed since the study was created.')
        source = self.store.source_packet(study['sample_id'])
        if set(source) != {'packet_type', 'sample_id', 'source_sha256', 'original_text'}:
            raise ValueError('Model packet contains unexpected fields.')
        if (source['sample_id'] != study['sample_id'] or
                digest(source['original_text']) != source['source_sha256'] or
                source['source_sha256'] != study['source_sha256']):
            raise ValueError('Source packet identity/integrity mismatch.')
        run = self.store.create_run(study_id, model_profile=model_profile)
        rid = run['run_id']
        self.store.artifact(rid, 'source_packet.json', canonical(source))
        fixture_id = study['fixture_id']
        a = self._call(rid, stage='decompose', condition='none',
                       fixture_id=fixture_id, model_profile=model_profile,
                       body={'source_packet': source}, input_sha256=source['source_sha256'])
        if a['status'] != 'completed':
            record = self.store.finish_run(rid, 'incomplete')
            self._comparisons(rid)
            return record
        frozen = self.store.load_artifact(rid, 'decompose.parsed.json')
        intermediate_hash = digest(frozen)
        # Both branches get the SAME bytes as their only substantive input.
        for condition in ('neutral', 'commercial'):
            self._call(rid, stage='reconstruct', condition=condition,
                       fixture_id=fixture_id, model_profile=model_profile,
                       body={'decomposition': json.loads(frozen)},
                       input_sha256=intermediate_hash)
        stages = self.store.get_run(rid)['steps']
        done = all(stage['status'] == 'completed' for stage in stages)
        record = self.store.finish_run(rid, 'completed' if done else 'incomplete')
        self._comparisons(rid)
        return record

    def _comparisons(self, run_id: str) -> None:
        run = self.store.get_run(run_id)
        existing = run['artifacts']
        candidates = [
            ('oracle_vs_original', 'oracle', 'source_packet.json'),
            ('original_vs_decomposition', 'source_packet.json', 'decompose.parsed.json'),
            ('oracle_vs_decomposition', 'oracle', 'decompose.parsed.json'),
            ('decomposition_vs_neutral', 'decompose.parsed.json', 'neutral.response.txt'),
            ('decomposition_vs_commercial', 'decompose.parsed.json', 'commercial.response.txt'),
            ('neutral_vs_commercial', 'neutral.response.txt', 'commercial.response.txt'),
            ('oracle_vs_neutral', 'oracle', 'neutral.response.txt'),
            ('oracle_vs_commercial', 'oracle', 'commercial.response.txt'),
        ]
        for kind, reference, target in candidates:
            if any(x not in existing for x in (reference, target) if x != 'oracle'):
                continue
            cid = f'{run_id}-{kind}'
            self.store.save_comparison({
                'comparison_id': cid, 'study_id': run['study_id'], 'run_id': run_id,
                'kind': kind, 'reference': reference, 'target': target,
                'reference_sha256': existing[reference]['sha256'] if reference != 'oracle' else 'private_ref',
                'target_sha256': existing[target]['sha256'],
                'status': 'available', 'created_at': now(),
                'synthetic': True, 'semantic_verdict': 'not_evaluated',
            })
