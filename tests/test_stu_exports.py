"""Private full export is a verifiable research record, not a redacted summary."""
from __future__ import annotations

import json
from zipfile import ZipFile

import pytest

from stu.application import StuApplication
from stu.cli import smoke
from stu.contracts import digest
from stu.fixtures import FIXTURES


def bundle(app, study_id):
    info = app.export_study(study_id)
    assert info['privacy_level'] == 'full'
    with ZipFile(info['path']) as archive:
        material = {name: archive.read(name) for name in archive.namelist()}
    manifest = json.loads(material['BUNDLE_MANIFEST.json'])
    assert manifest['file_count'] == len(material) - 1
    assert set(manifest['files']) == set(material) - {'BUNDLE_MANIFEST.json'}
    for name, item in manifest['files'].items():
        assert item['sha256'] == digest(material[name])
        assert item['bytes'] == len(material[name])
    return info, manifest, material


def test_full_bundle_contains_pinned_sera_stu_reviews_and_provenance(tmp_path):
    app = StuApplication(tmp_path / 'data')
    smoke_result = smoke(app, fixture_id='F01')
    study_id = smoke_result['study_id']
    run_id = smoke_result['run_id']
    cid = next(c['comparison_id'] for c in app.list_comparisons(study_id)
               if c['kind'] == 'oracle_vs_neutral')
    app.begin_gap_explanation(cid)
    app.save_gap_explanation(cid, 'The condition was omitted.',
                             gaps=[{'label': 'omitted', 'rationale': 'Missing the condition.'}])
    app.complete_gap_explanation(cid)

    info, manifest, files = bundle(app, study_id)
    sample_id = manifest['sample_id']
    assert manifest['privacy_class'] == 'private_unredacted'
    oracle = json.loads(files[f'private/sera/{sample_id}/oracle-v1.json'])
    assert oracle['intention_free_text'].startswith('SYNTHETIC ORACLE')
    assert oracle['source']['original_text'] == FIXTURES['F01']['source']
    assert f'private/sera/{sample_id}/events.through_pinned_freeze.jsonl' in files
    assert f'private/studies/{study_id}.json' in files
    assert f'studies/{study_id}/manifest.json' in files
    assert f'studies/{study_id}/events.jsonl' in files
    assert files[f'runs/{run_id}/artifacts/neutral.response.txt'].decode() == FIXTURES['F01']['neutral']
    assert f'runs/{run_id}/artifacts/decompose.request.json' in files
    assert f'runs/{run_id}/artifacts/decompose.parsed.json' in files
    assert f'runs/{run_id}/artifacts/commercial.response.txt' in files
    assert f'comparisons/{cid}.json' in files
    review = files[f'reviews/{cid}/events.jsonl'].decode()
    assert 'The condition was omitted.' in review
    assert 'Missing the condition.' in review
    assert 'analysis/results.json' in files
    result = json.loads(files['analysis/results.json'])
    assert result['recorded_run_count'] == 1
    assert 'planned_run_count' not in result
    assert 'schemas/semantic_v0.1.json' in files
    for kind in ('decompose', 'neutral', 'commercial'):
        assert f'prompts/{kind}_v0.1.txt' in files

    decomposition_request = json.loads(files[f'runs/{run_id}/artifacts/decompose.request.json'])
    assert 'intention_free_text' not in json.dumps(decomposition_request)
    for kind in ('neutral', 'commercial'):
        request = json.loads(files[f'runs/{run_id}/artifacts/{kind}.request.json'])
        assert 'source_packet' not in request['messages'][1]['content']
        assert 'intention_free_text' not in json.dumps(request)
    assert info['sha256'] == digest(open(info['path'], 'rb').read())


def test_full_bundle_uses_historical_oracle_not_later_amendment(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app)
    sid = result['sample_id']
    app.capture.begin_amendment(sid)
    app.capture.save_intention(sid, 'LATER VERSION MUST NOT REPLACE PINNED ORACLE')
    app.capture.freeze(sid)
    _, manifest, files = bundle(app, result['study_id'])
    assert manifest['pinned_oracle']['version'] == 1
    assert f'private/sera/{sid}/oracle-v1.json' in files
    assert f'private/sera/{sid}/oracle-v2.json' not in files
    assert 'LATER VERSION MUST NOT REPLACE PINNED ORACLE' not in b'\n'.join(files.values()).decode('utf-8', errors='ignore')


def test_optional_redacted_export_remains_safe_and_renamed(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app)
    safe = app.export_study(result['study_id'], privacy_level='safe')
    contents = app.get_export_bytes(result['study_id'], privacy_level='safe').decode()
    assert safe['path'].endswith('-safe.json')
    assert 'SYNTHETIC ORACLE TEST REFERENCE' not in contents
    assert FIXTURES['F01']['source'] not in contents
    assert json.loads(contents)['report']['recorded_run_count'] == 1
    assert 'planned_run_count' not in contents
    assert app.get_export_bytes(result['study_id'])[:2] == b'PK'


def test_incomplete_run_still_exports_as_incomplete_evidence(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app, fixture_id='F08')
    _, _, files = bundle(app, result['study_id'])
    report = json.loads(files['analysis/results.json'])
    assert report['run_status_counts']['incomplete'] == 1
    assert not report['paired_reconstructions']
    assert f'runs/{result["run_id"]}/run.json' in files


def test_export_refuses_corrupted_run_artifact(tmp_path):
    app = StuApplication(tmp_path / 'data')
    result = smoke(app)
    run_id = result['run_id']
    artifact = app.store.run_path(run_id) / 'artifacts' / 'decompose.request.json'
    artifact.write_text('tampered', encoding='utf-8')
    with pytest.raises(RuntimeError, match='Corrupted artifact'):
        app.export_study(result['study_id'])
