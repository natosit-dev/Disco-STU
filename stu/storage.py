"""Small local artifact store: explicit runs, immutable artifacts, append-only events.

SHA-256 is a local integrity check, not an adversarial signature or attestation.
"""
from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path, PurePosixPath
from uuid import uuid4

from .contracts import canonical, digest, now

SAFE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,150}$')
ZERO_HASH = '0' * 64


def safe_id(value: str) -> str:
    if not isinstance(value, str) or not SAFE.fullmatch(value) or value in ('.', '..'):
        raise ValueError('Unsafe artifact identifier/path.')
    return value


def read_json(path: Path) -> dict:
    result = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(result, dict):
        raise ValueError(f'Expected an object: {path}')
    return result


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.stu-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(canonical(value) + b'\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_once(path: Path, content: bytes) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    return {'path': str(path.name), 'sha256': digest(content), 'bytes': len(content)}


class EventJournal:
    """Single-user write-serialized append-only hash chain with verifiable sequence."""
    def __init__(self, path: Path):
        self.path = path

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        results = []
        previous = ZERO_HASH
        for n, raw in enumerate(self.path.read_bytes().splitlines(), 1):
            record = json.loads(raw)
            if (not isinstance(record, dict) or record.get('sequence') != n
                    or record.get('previous_sha256') != previous):
                raise RuntimeError(f'Event chain broken at {self.path} line {n}')
            payload = {k: v for k, v in record.items() if k != 'sha256'}
            if record.get('sha256') != digest(payload):
                raise RuntimeError(f'Event hash invalid at {self.path} line {n}')
            previous = record['sha256']
            results.append(record)
        return results

    def append(self, kind: str, details: dict | None = None, *, at: str | None = None) -> dict:
        events = self.read()
        entry = {'sequence': len(events) + 1,
                 'previous_sha256': events[-1]['sha256'] if events else ZERO_HASH,
                 'at': at or now(), 'kind': kind, 'details': details or {}}
        entry['sha256'] = digest(entry)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('ab') as f:
            f.write(canonical(entry) + b'\n')
            f.flush()
            os.fsync(f.fileno())
        return entry


class StuStore:
    def __init__(self, root: str | Path = 'data'):
        self.root = Path(root)

    def study_path(self, study_id: str) -> Path:
        return self.root / 'studies' / safe_id(study_id)

    def run_path(self, run_id: str) -> Path:
        return self.root / 'runs' / safe_id(run_id)

    def comparison_path(self, comparison_id: str) -> Path:
        return self.root / 'comparisons' / (safe_id(comparison_id) + '.json')

    def review_path(self, comparison_id: str) -> Path:
        return self.root / 'reviews' / safe_id(comparison_id)

    def source_packet(self, sample_id: str) -> dict:
        return read_json(self.root / 'stu_inputs' / (safe_id(sample_id) + '.json'))

    def create_study(self, *, sample_id: str, source_sha256: str, fixture_id: str,
                     oracle_ref: dict, prompts: dict, schema_sha256: str,
                     implementation: str, mode: str = 'synthetic_test',
                     model_id: str | None = None,
                     protocol_artifacts: dict[str, bytes] | None = None,
                     prompt_paths: dict[str, str] | None = None) -> dict:
        if mode not in ('synthetic_test', 'live'):
            raise ValueError('Unsupported study mode.')
        if mode == 'live' and not model_id:
            raise ValueError('A pinned model ID is required for live studies.')
        study_id = str(uuid4())
        path = self.study_path(study_id)
        path.mkdir(parents=True, exist_ok=False)
        protocol_hashes = {}
        for rel, raw in (protocol_artifacts or {}).items():
            path_parts = PurePosixPath(rel).parts
            if not path_parts or any(part in ('', '.', '..') for part in path_parts) or rel.startswith('/'):
                raise ValueError('Unsafe protocol artifact path.')
            protocol_path = path / 'protocol' / rel
            write_once(protocol_path, raw)
            protocol_hashes[rel] = digest(raw)
        study = {'study_id': study_id, 'mode': mode, 'status': 'draft',
                 'schema_version': 'stu.v0.1', 'sample_id': sample_id,
                 'source_sha256': source_sha256,
                 'fixture_id': fixture_id if mode == 'synthetic_test' else None,
                 'model_id': model_id if mode == 'live' else None,
                 'adapter': 'adaption' if mode == 'live' else 'deterministic_fixture',
                 'created_at': now(), 'prompt_sha256': prompts,
                 'semantic_schema_sha256': schema_sha256,
                 'prompt_paths': prompt_paths or {},
                 'protocol_files': protocol_hashes,
                 'implementation': implementation, 'runs': [],
                 'privacy_class': 'private_live' if mode == 'live' else 'synthetic_test',
                 'synthetic': mode == 'synthetic_test', 'scored': False}
        atomic_json(path / 'manifest.json', study)
        # Private reviewer-only reference is never loaded by runner or serialized in a model request.
        secret_path = self.root / 'private' / 'studies' / (study_id + '.json')
        write_once(secret_path, canonical(oracle_ref))
        EventJournal(path / 'events.jsonl').append('study_created', {'mode': mode})
        return study

    def get_study(self, study_id: str) -> dict:
        return read_json(self.study_path(study_id) / 'manifest.json')

    def private_oracle_reference(self, study_id: str) -> dict:
        return read_json(self.root / 'private' / 'studies' / (safe_id(study_id) + '.json'))

    def load_protocol_file(self, study_id: str, name: str) -> bytes:
        study = self.get_study(study_id)
        if name not in study.get('protocol_files', {}):
            raise ValueError('Protocol artifact is not pinned to this study.')
        parts = PurePosixPath(name).parts
        if not parts or '..' in parts or name.startswith('/'):
            raise ValueError('Unsafe protocol artifact name.')
        raw = (self.study_path(study_id) / 'protocol' / name).read_bytes()
        if digest(raw) != study['protocol_files'][name]:
            raise RuntimeError('Frozen protocol artifact integrity mismatch: ' + name)
        return raw

    def list_studies(self) -> list[dict]:
        base = self.root / 'studies'
        if not base.exists():
            return []
        return [self.get_study(p.name) for p in sorted(base.iterdir())
                if p.is_dir() and (p / 'manifest.json').exists()]

    def create_run(self, study_id: str, model_profile: str = 'fixture') -> dict:
        study = self.get_study(study_id)
        if study.get('mode') not in ('synthetic_test', 'live') or study.get('scored'):
            raise ValueError('Study mode is not executable.')
        if study['mode'] == 'live' and model_profile != study['model_id']:
            raise ValueError('Live run model does not match pinned study model.')
        run_id = str(uuid4())
        path = self.run_path(run_id)
        path.mkdir(parents=True, exist_ok=False)
        record = {'run_id': run_id, 'study_id': study_id, 'mode': study['mode'],
                  'adapter': study['adapter'], 'model_profile': model_profile,
                  'fixture_id': study['fixture_id'], 'sample_id': study['sample_id'],
                  'started_at': now(), 'status': 'running', 'steps': [],
                  'artifacts': {}, 'synthetic': study['mode'] == 'synthetic_test'}
        atomic_json(path / 'run.json', record)
        EventJournal(path / 'events.jsonl').append('run_started', {'study_id': study_id})
        study['runs'].append(run_id)
        atomic_json(self.study_path(study_id) / 'manifest.json', study)
        return record

    def get_run(self, run_id: str) -> dict:
        return read_json(self.run_path(run_id) / 'run.json')

    def artifact(self, run_id: str, name: str, content: bytes) -> dict:
        path = self.run_path(run_id) / 'artifacts' / safe_id(name)
        info = write_once(path, content)
        record = self.get_run(run_id)
        record['artifacts'][name] = info
        atomic_json(self.run_path(run_id) / 'run.json', record)
        return info

    def load_artifact(self, run_id: str, name: str) -> bytes:
        record = self.get_run(run_id)
        info = record['artifacts'][name]
        raw = (self.run_path(run_id) / 'artifacts' / safe_id(name)).read_bytes()
        if digest(raw) != info['sha256'] or len(raw) != info['bytes']:
            raise RuntimeError(f'Corrupted artifact {run_id}/{name}')
        return raw

    def step(self, run_id: str, event: dict) -> None:
        record = self.get_run(run_id)
        record['steps'].append(event)
        atomic_json(self.run_path(run_id) / 'run.json', record)
        EventJournal(self.run_path(run_id) / 'events.jsonl').append('step_finished', event)

    def finish_run(self, run_id: str, status: str) -> dict:
        if status not in {'completed', 'incomplete', 'failed', 'cancelled'}:
            raise ValueError('Invalid terminal status.')
        path = self.run_path(run_id)
        record = self.get_run(run_id)
        if record['status'] != 'running':
            return record
        EventJournal(path / 'events.jsonl').append('run_finished', {'status': status})
        record['status'] = status
        record['finished_at'] = now()
        atomic_json(path / 'run.json', record)
        return record

    def verify_run(self, run_id: str) -> dict:
        record = self.get_run(run_id)
        events = EventJournal(self.run_path(run_id) / 'events.jsonl').read()
        for name, info in record['artifacts'].items():
            self.load_artifact(run_id, name)
        if not events or events[0]['kind'] != 'run_started':
            raise RuntimeError('Run journal missing start evidence.')
        if record['status'] != 'running' and events[-1]['kind'] != 'run_finished':
            raise RuntimeError('Final run missing completion event.')
        if len([e for e in events if e['kind'] == 'step_finished']) != len(record['steps']):
            raise RuntimeError('Run steps and journal disagree.')
        return {'run_id': run_id, 'valid': True, 'artifact_count': len(record['artifacts']),
                'event_count': len(events), 'status': record['status']}

    def save_comparison(self, comparison: dict) -> dict:
        path = self.comparison_path(comparison['comparison_id'])
        write_once(path, canonical(comparison))
        return comparison

    def get_comparison(self, comparison_id: str) -> dict:
        return read_json(self.comparison_path(comparison_id))

    def list_comparisons(self, study_id: str) -> list[dict]:
        folder = self.root / 'comparisons'
        if not folder.exists():
            return []
        return [value for path in sorted(folder.glob('*.json'))
                if (value := read_json(path)).get('study_id') == study_id]
