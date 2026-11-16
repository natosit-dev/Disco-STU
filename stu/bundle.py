"""Private, complete STU evidence export. Never used by the model runner."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from .contracts import canonical, digest, now
from .storage import EventJournal, StuStore, safe_id


def build_full_bundle(store: StuStore, capture, study_id: str, report: dict) -> dict:
    """Export pinned SERA and all study artifacts as a single private ZIP."""
    study = store.get_study(study_id)
    sample_id = safe_id(study['sample_id'])
    pinned = store.private_oracle_reference(study_id)
    if pinned['sample_id'] != sample_id:
        raise RuntimeError('Pinned Oracle refers to another sample.')
    oracle = capture.get_frozen_version(
        sample_id, pinned['version'], explication_id=pinned['explication_id'],
        sha256=pinned['artifact_sha256'])
    packet = store.source_packet(sample_id)
    if (set(packet) != {'packet_type', 'sample_id', 'source_sha256', 'original_text'}
            or packet['sample_id'] != sample_id
            or packet['source_sha256'] != study['source_sha256']
            or digest(packet['original_text']) != packet['source_sha256']
            or packet['original_text'] != oracle['source']['original_text']):
        raise RuntimeError('STU source packet does not match pinned SERA source.')

    entries: dict[str, bytes] = {}

    def add(name: str, content: bytes) -> None:
        if name in entries or name.startswith('/') or '..' in Path(name).parts:
            raise ValueError(f'Duplicate or unsafe bundle entry: {name}')
        entries[name] = content

    def add_file(name: str, path: Path) -> None:
        add(name, path.read_bytes())

    # Include the historical Oracle selected when the study was created,
    # not whichever amended version is now latest.
    add_file(f'private/sera/{sample_id}/oracle-v{pinned["version"]}.json',
             capture.store.sample_dir(sample_id) / f'oracle-v{pinned["version"]}.json')
    sera_events = capture.store.sample_dir(sample_id) / 'events.jsonl'
    lines = sera_events.read_bytes().splitlines(keepends=True)
    freeze_index = None
    for i, line in enumerate(lines):
        event = json.loads(line)
        if (event.get('event') == 'frozen'
                and event.get('explication_id') == pinned['explication_id']
                and event.get('artifact_sha256') == pinned['artifact_sha256']):
            freeze_index = i
            break
    if freeze_index is None:
        raise RuntimeError('Pinned SERA freeze event missing.')
    add(f'private/sera/{sample_id}/events.through_pinned_freeze.jsonl',
        b''.join(lines[:freeze_index + 1]))
    add_file(f'private/studies/{safe_id(study_id)}.json',
             store.root / 'private' / 'studies' / f'{study_id}.json')
    add_file(f'stu_inputs/{sample_id}.json',
             store.root / 'stu_inputs' / f'{sample_id}.json')

    add_file(f'studies/{study_id}/manifest.json',
             store.study_path(study_id) / 'manifest.json')
    study_events = store.study_path(study_id) / 'events.jsonl'
    EventJournal(study_events).read()
    add_file(f'studies/{study_id}/events.jsonl', study_events)

    runs = {safe_id(run_id) for run_id in study['runs']}
    if len(runs) != len(study['runs']):
        raise RuntimeError('Duplicate run IDs in study.')
    for run_id in sorted(runs):
        run = store.get_run(run_id)
        if run['study_id'] != study_id or run['sample_id'] != sample_id:
            raise RuntimeError('Run does not belong to this study/source.')
        store.verify_run(run_id)
        add_file(f'runs/{run_id}/run.json', store.run_path(run_id) / 'run.json')
        add_file(f'runs/{run_id}/events.jsonl',
                 store.run_path(run_id) / 'events.jsonl')
        for artifact_name in sorted(run['artifacts']):
            add(f'runs/{run_id}/artifacts/{safe_id(artifact_name)}',
                store.load_artifact(run_id, artifact_name))

    for comp in store.list_comparisons(study_id):
        cid = safe_id(comp['comparison_id'])
        if comp['run_id'] not in runs:
            raise RuntimeError('Comparison does not belong to a study run.')
        add_file(f'comparisons/{cid}.json', store.comparison_path(cid))
        review_journal = store.review_path(cid) / 'events.jsonl'
        if review_journal.exists():
            EventJournal(review_journal).read()
            add_file(f'reviews/{cid}/events.jsonl', review_journal)

    if study.get('protocol_files'):
        # New studies pin exact bytes. Export needs NO mutable repository files.
        for rel in sorted(study['protocol_files']):
            add(rel, store.load_protocol_file(study_id, rel))
        schema_bytes = store.load_protocol_file(study_id, 'schemas/semantic_v0.1.json')
        if digest(schema_bytes) != study['semantic_schema_sha256']:
            raise RuntimeError('Pinned semantic schema digest mismatch.')
        for kind, rel in study['prompt_paths'].items():
            if digest(store.load_protocol_file(study_id, rel)) != study['prompt_sha256'][kind]:
                raise RuntimeError('Pinned prompt digest mismatch.')
    else:
        # Legacy studies predate protocol snapshots.
        root = Path(__file__).resolve().parents[1]
        schema_bytes = (root / 'schemas' / 'semantic_v0.1.json').read_bytes()
        if digest(schema_bytes) != study['semantic_schema_sha256']:
            raise RuntimeError('Semantic schema changed since study creation.')
        add('schemas/semantic_v0.1.json', schema_bytes)
        for kind in ('decompose', 'neutral', 'commercial'):
            prompt_path = root / 'prompts' / f'{kind}_v0.1.txt'
            prompt_bytes = prompt_path.read_bytes()
            if digest(prompt_bytes) != study['prompt_sha256'][kind]:
                raise RuntimeError(f'Prompt {kind} changed since study creation.')
            add(f'prompts/{kind}_v0.1.txt', prompt_bytes)

    add('analysis/results.json', canonical(report) + b'\n')
    add('README.txt', (
        'DiScO STU — COMPLETE PRIVATE STUDY BUNDLE\n'
        'This contains source text, the pinned human SERA explication, raw '
        'test/model requests and responses, human judgments and event histories.\n'
        'DO NOT publish or commit this ZIP without inspecting its contents.\n'
        'The model runner never received the Oracle. This export combines '
        'evidence AFTER execution for human examination.\n'
        'SHA-256 manifests detect changed bytes, not semantic accuracy or '
        'adversarial tampering. Synthetic fixtures are not model findings; live execution does not prove semantic correctness.\n'
    ).encode('utf-8'))

    manifest = {
        'bundle_schema': 'stu.full.bundle.v0.1',
        'created_at': now(),
        'study_id': study_id,
        'sample_id': sample_id,
        'privacy_class': 'private_unredacted',
        'contains_private_sera_and_human_explanations': True,
        'pinned_oracle': pinned,
        'mode': study['mode'],
        'synthetic': study['mode'] == 'synthetic_test',
        'file_count': len(entries),
        'files': {name: {'sha256': digest(data), 'bytes': len(data)}
                  for name, data in sorted(entries.items())},
    }
    manifest_bytes = canonical(manifest) + b'\n'
    destination = store.root / 'exports' / f'{safe_id(study_id)}-full.zip'
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.stu-bundle-', suffix='.zip',
                                dir=destination.parent)
    os.close(fd)
    try:
        with ZipFile(tmp, 'w', compression=ZIP_DEFLATED) as archive:
            for name, raw in sorted(entries.items()):
                archive.writestr(name, raw)
            archive.writestr('BUNDLE_MANIFEST.json', manifest_bytes)
        os.replace(tmp, destination)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

    return {
        'path': str(destination),
        'sha256': digest(destination.read_bytes()),
        'manifest_sha256': digest(manifest_bytes),
        'file_count': len(entries) + 1,
        'privacy_level': 'full',
        'contains_private_data': True,
        'study_id': study_id,
    }
