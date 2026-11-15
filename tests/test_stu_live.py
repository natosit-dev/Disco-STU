"""Mocked live Adaption execution: no network, no credentials, no semantic scoring."""
from __future__ import annotations

import json
from types import SimpleNamespace
from zipfile import ZipFile

import pytest

from sera.schema import CATEGORIES
from stu.application import StuApplication
from stu.contracts import digest
from stu.projection import projection_bytes
from stu.adaption_api import AdaptionApiError

SOURCE = ("Velocity is not productivity.\n"
          "Coherence is not accuracy.\n"
          "Complexity is not sophistication.")
PRIVATE_INTENT = "PRIVATE_ORACLE_NOT_A_MODEL_INPUT"


def decomposition():
    return {
        'category_prose': {key: ("Three denied equivalences" if key == 'claims' else '')
                           for key in CATEGORIES},
        'units': [{
            'unit_id': 'M-U1', 'kind': 'claim',
            'text': 'Velocity does not equal productivity',
            'importance': 'essential', 'polarity': 'negated',
            'source_support': 'Velocity is not productivity.',
            'notes': 'Distinct concepts need not be mutually exclusive.',
        }],
        'relations': [],
    }


class MockResponse:
    def __init__(self, output, status='completed', response_id='resp_mock_1',
                 model='gemma-4-31b-it'):
        self.output_text = output
        self.status = status
        self.id = response_id
        self.model = model
        self.usage = {'input_tokens': 21, 'output_tokens': 30, 'total_tokens': 51}
        self.error = {'code': 'provider_failed'} if status == 'failed' else None
        self.incomplete_details = ({'reason': 'max_output_tokens'}
                                   if status == 'incomplete' else None)

    def model_dump(self, **kwargs):
        return {
            'id': self.id, 'status': self.status, 'model': self.model,
            'output_text': self.output_text,
            'output': [{'type': 'message', 'role': 'assistant',
                        'content': [{'type': 'output_text', 'text': self.output_text}]}],
            'usage': self.usage, 'error': self.error,
            'incomplete_details': self.incomplete_details,
            'created_at': 1794700800, 'provider_extension': {'cost': 0.00004},
        }


class MockProvider:
    def __init__(self, replies):
        self.replies = replies
        self.calls = []
        self.clients = []
        self.keys = []

    def __call__(self, key):
        self.keys.append(key)
        provider = self

        class Client:
            def __init__(self):
                self.responses = self
                self.closed = False

            def create(self, **kwargs):
                provider.calls.append(kwargs)
                reply = provider.replies[len(provider.calls) - 1]
                if isinstance(reply, Exception):
                    raise reply
                return reply

            def close(self):
                self.closed = True

        client = Client()
        self.clients.append(client)
        return client


def capture_and_study(tmp_path, monkeypatch):
    app = StuApplication(tmp_path / 'data')
    sample = app.capture.create_sample(SOURCE, title='Three False Equivalences',
                                       domain='philosophical')
    sid = sample['sample_id']
    app.capture.save_intention(sid, PRIVATE_INTENT)
    app.capture.save_categories(sid, {key: '' for key in CATEGORIES})
    app.capture.save_units(sid, [{
        'unit_id': 'H-U1', 'kind': 'negation',
        'text': 'Velocity does not entail productivity',
        'importance': 'essential', 'polarity': 'negated',
        'source_support': 'Velocity is not productivity.', 'notes': '',
    }])
    app.capture.freeze(sid)
    study = app.create_study(sid, mode='live', model_id='gemma-4-31b-it')
    assert study['mode'] == 'live' and not study['synthetic']
    assert study['adapter'] == 'adaption'
    return app, study, sid


def use_mock(monkeypatch, provider):
    from stu.live import AdaptionModelAdapter
    import stu.application as application
    monkeypatch.setattr(application, 'AdaptionModelAdapter',
                        lambda api_key=None: AdaptionModelAdapter(
                            api_key=api_key, client_factory=provider))


def test_live_pipeline_preserves_evidence_projection_metadata_and_zip(tmp_path, monkeypatch):
    app, study, sid = capture_and_study(tmp_path, monkeypatch)
    replies = [
        MockResponse(json.dumps(decomposition()), response_id='resp_decompose'),
        MockResponse('Three comparisons are not equivalences.', response_id='resp_neutral'),
        MockResponse('Management should not confuse speed with useful output.',
                     response_id='resp_commercial'),
    ]
    provider = MockProvider(replies)
    use_mock(monkeypatch, provider)
    run = app.run_sample(study['study_id'], api_key='SENSITIVE_KEY_FOR_TEST_ONLY')
    assert run['status'] == 'completed'
    assert len(provider.calls) == 3
    assert len(provider.clients) == 3
    assert all(client.closed for client in provider.clients)
    assert all(key == 'SENSITIVE_KEY_FOR_TEST_ONLY' for key in provider.keys)
    for call in provider.calls:
        assert call['model'] == 'gemma-4-31b-it'
        assert call['store'] is False and call['agentic_memory'] is False
        assert call['tools'] == [] and call['tool_choice'] == 'none'
        assert 'previous_response_id' not in call
        assert PRIVATE_INTENT not in json.dumps(call)
        assert 'SENSITIVE_KEY_FOR_TEST_ONLY' not in json.dumps(call)

    # The exact byte sequence is sent to BOTH independent reconstruction calls.
    projected = app.store.load_artifact(run['run_id'],
        'decompose.reconstruction_projection.json')
    assert projected == projection_bytes(decomposition())
    assert provider.calls[1]['input'].encode('utf-8') == projected
    assert provider.calls[2]['input'].encode('utf-8') == projected
    assert 'source_support' not in projected.decode('utf-8')
    assert 'source_packet' not in provider.calls[1]['input']
    assert SOURCE not in provider.calls[1]['input']
    assert 'source_support' in app.store.load_artifact(
        run['run_id'], 'decompose.parsed.json').decode('utf-8')
    assert json.loads(provider.calls[0]['input'])['source_packet']['original_text'] == SOURCE

    for stage in ('decompose', 'neutral', 'commercial'):
        raw = json.loads(app.store.load_artifact(
            run['run_id'], stage + '.provider_response.json'))
        assert raw['created_at'] == 1794700800
        assert raw['provider_extension']['cost'] == 0.00004
        assert raw['usage']['total_tokens'] == 51
        assert app.store.load_artifact(run['run_id'],
               stage + '.provider_request.json')
    assert app.validate(study['study_id'])['valid']
    results = app.get_results(study['study_id'])
    assert results['synthetic'] is False and results['mode'] == 'live'
    assert len(results['paired_reconstructions']) == 1
    assert results['paired_reconstructions'][0]['intermediate_sha256'] == digest(projected)
    comps = app.list_comparisons(study['study_id'])
    assert len(comps) == 8
    assert all(not c['synthetic'] and c['mode'] == 'live' for c in comps)

    # Complete private bundle must include exact pinned Oracle AND frozen protocol.
    info = app.export_study(study['study_id'])
    with ZipFile(info['path']) as z:
        names = set(z.namelist())
        bundle_manifest = json.loads(z.read('BUNDLE_MANIFEST.json'))
        assert bundle_manifest['mode'] == 'live'
        assert bundle_manifest['synthetic'] is False
        assert f'private/sera/{sid}/oracle-v1.json' in names
        assert PRIVATE_INTENT in z.read(f'private/sera/{sid}/oracle-v1.json').decode()
        assert 'prompts/decompose_live_v0.1.txt' in names
        assert 'schemas/reconstruction_projection_v0.1.json' in names
        assert f'runs/{run["run_id"]}/artifacts/neutral.provider_response.json' in names
        assert z.read(f'runs/{run["run_id"]}/artifacts/decompose.reconstruction_projection.json') == projected
        assert 'SENSITIVE_KEY_FOR_TEST_ONLY' not in b''.join(z.read(p) for p in names).decode(errors='replace')


def test_live_export_survives_prompt_file_changes(tmp_path, monkeypatch):
    app, study, _ = capture_and_study(tmp_path, monkeypatch)
    provider = MockProvider([MockResponse(json.dumps(decomposition())),
                             MockResponse('neutral'), MockResponse('commercial')])
    use_mock(monkeypatch, provider)
    import stu.protocol as protocol
    monkeypatch.setattr(protocol, 'ROOT', tmp_path / 'missing-repository-root')
    assert app.run_sample(study['study_id'], api_key='notpersisted')['status'] == 'completed'
    info = app.export_study(study['study_id'])
    with ZipFile(info['path']) as z:
        assert 'prompts/decompose_live_v0.1.txt' in z.namelist()


def test_live_missing_credential_does_not_create_run(tmp_path, monkeypatch):
    app, study, _ = capture_and_study(tmp_path, monkeypatch)
    monkeypatch.delenv('ADAPTION_API_KEY', raising=False)
    with pytest.raises(AdaptionApiError, match='No Adaption API key'):
        app.run_sample(study['study_id'])
    assert app.get_study(study['study_id'])['runs'] == []


@pytest.mark.parametrize('response', [
    MockResponse('not json'),
    MockResponse('{"units": [INVALID'),
])
def test_live_invalid_json_is_retained_without_repair(tmp_path, monkeypatch, response):
    app, study, _ = capture_and_study(tmp_path, monkeypatch)
    provider = MockProvider([response])
    use_mock(monkeypatch, provider)
    run = app.run_sample(study['study_id'], api_key='test-key')
    assert run['status'] == 'incomplete'
    assert run['steps'][0]['status'] == 'invalid_output'
    assert len(provider.calls) == 1
    assert app.store.load_artifact(run['run_id'], 'decompose.response.txt') == response.output_text.encode()
    assert app.validate(study['study_id'])['valid']


def test_live_timeout_persists_failure_without_credential_leak(tmp_path, monkeypatch):
    app, study, _ = capture_and_study(tmp_path, monkeypatch)
    provider = MockProvider([TimeoutError('secret: hidden-test-key')])
    use_mock(monkeypatch, provider)
    run = app.run_sample(study['study_id'], api_key='hidden-test-key')
    assert run['status'] == 'incomplete'
    assert run['steps'][0]['status'] == 'failed'
    assert 'hidden-test-key' not in json.dumps(run)
    assert app.validate(study['study_id'])['valid']
    assert len(provider.calls) == 1
    with ZipFile(app.export_study(study['study_id'])['path']) as z:
        assert 'hidden-test-key' not in b''.join(z.read(p) for p in z.namelist()).decode(errors='replace')


@pytest.mark.parametrize('status', ['failed', 'incomplete'])
def test_failed_or_incomplete_provider_response_is_preserved(tmp_path, monkeypatch, status):
    app, study, _ = capture_and_study(tmp_path, monkeypatch)
    provider = MockProvider([MockResponse('not valid json', status=status)])
    use_mock(monkeypatch, provider)
    run = app.run_sample(study['study_id'], api_key='test-key')
    assert run['status'] == 'incomplete'
    assert run['steps'][0]['status'] == status
    raw = json.loads(app.store.load_artifact(run['run_id'], 'decompose.provider_response.json'))
    assert raw['status'] == status
    assert not app.get_results(study['study_id'])['paired_reconstructions']


def test_live_partial_branch_never_counts_as_comparable_pair(tmp_path, monkeypatch):
    app, study, _ = capture_and_study(tmp_path, monkeypatch)
    provider = MockProvider([
        MockResponse(json.dumps(decomposition())),
        MockResponse('neutral done'),
        MockResponse('partial commercial', status='incomplete'),
    ])
    use_mock(monkeypatch, provider)
    run = app.run_sample(study['study_id'], api_key='test-key')
    assert run['status'] == 'incomplete'
    assert len(provider.calls) == 3
    assert app.validate(study['study_id'])['valid']
    assert not app.get_results(study['study_id'])['paired_reconstructions']
    comps = app.list_comparisons(study['study_id'])
    assert not any(c['kind'] == 'neutral_vs_commercial' for c in comps)


def test_live_model_allowlist_and_adapter_mismatch(tmp_path, monkeypatch):
    app, _, sid = capture_and_study(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match='Unsupported Adaption'):
        app.create_study(sid, mode='live', model_id='not-model')
    live = app.create_study(sid, mode='live', model_id='glm-5.2')
    with pytest.raises(ValueError, match='Live study requires'):
        app.run_sample(live['study_id'], adapter='fixture', api_key='test')
