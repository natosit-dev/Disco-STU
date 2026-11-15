"""Freeze complete prompt/schema/projection bytes in each new study."""
from __future__ import annotations

from pathlib import Path
from .contracts import digest

ROOT = Path(__file__).resolve().parents[1]
PROJECTION_PATH = 'schemas/reconstruction_projection_v0.1.json'
SCHEMA_PATH = 'schemas/semantic_v0.1.json'


def prompt_paths(mode: str) -> dict[str, str]:
    if mode == 'live':
        return {'decompose': 'prompts/decompose_live_v0.1.txt',
                'neutral': 'prompts/neutral_v0.1.txt',
                'commercial': 'prompts/commercial_v0.1.txt'}
    if mode == 'synthetic_test':
        return {'decompose': 'prompts/decompose_v0.1.txt',
                'neutral': 'prompts/neutral_v0.1.txt',
                'commercial': 'prompts/commercial_v0.1.txt'}
    raise ValueError('Unsupported study protocol mode.')


def frozen_protocol(mode: str) -> tuple[dict[str, bytes], dict[str, str], dict[str, str]]:
    paths = prompt_paths(mode)
    names = {SCHEMA_PATH, *paths.values()}
    if mode == 'live':
        names.add(PROJECTION_PATH)
    artifacts = {rel: (ROOT / rel).read_bytes() for rel in sorted(names)}
    hashes = {stage: digest(artifacts[path]) for stage, path in paths.items()}
    return artifacts, paths, hashes


def read_frozen_prompt(store, study: dict, stage: str) -> str:
    name = study.get('prompt_paths', {}).get(stage)
    if name and study.get('protocol_files'):
        return store.load_protocol_file(study['study_id'], name).decode('utf-8')
    # Preserve old direct-storage fixture experiments without a protocol snapshot.
    path = prompt_paths('synthetic_test')[stage]
    payload = (ROOT / path).read_bytes()
    if digest(payload) != study['prompt_sha256'][stage]:
        raise ValueError('Legacy study prompt changed since creation.')
    return payload.decode('utf-8')
