"""SDK-mocked connectivity checks. No live network or real API keys required."""
from __future__ import annotations

from types import SimpleNamespace
import sys
import types

import pytest

from stu.adaption_api import (AdaptionDiagnosticService, AdaptionApiError,
                              DIAGNOSTIC_PROMPT, SUPPORTED_MODELS)


class FakeResponses:
    def __init__(self, response=None, exc=None):
        self.response = response
        self.exc = exc
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.exc:
            raise self.exc
        return self.response


class FakeClient:
    def __init__(self, api_key, response=None, exc=None):
        self.api_key = api_key
        self.responses = FakeResponses(response, exc)
        self.closed = False

    def close(self):
        self.closed = True


def response(status='completed', text='OK'):
    return SimpleNamespace(status=status, output_text=text, model='gemma-4-31b-it',
                           id='resp_abc', usage={'input_tokens': 9, 'output_tokens': 2},
                           error=None, incomplete_details=None)


def test_requires_key_without_network(monkeypatch):
    monkeypatch.delenv('ADAPTION_API_KEY', raising=False)
    service = AdaptionDiagnosticService(client_factory=lambda key: pytest.fail('SDK called without key'))
    with pytest.raises(AdaptionApiError, match='No Adaption API key'):
        service.test('gemma-4-31b-it')


def test_model_allowlist_no_network(monkeypatch):
    monkeypatch.setenv('ADAPTION_API_KEY', 'example-env-key')
    service = AdaptionDiagnosticService(client_factory=lambda key: pytest.fail('SDK called for unknown model'))
    with pytest.raises(AdaptionApiError, match='Unsupported diagnostic model'):
        service.test('unknown-model')


def test_one_stateless_request_and_response_fields(monkeypatch):
    monkeypatch.setenv('ADAPTION_API_KEY', 'example-env-key')
    client = FakeClient('example-session-key', response())
    result = AdaptionDiagnosticService(client_factory=lambda key: client).test(
        'gemma-4-31b-it', api_key='example-session-key'
    )
    assert result['ok'] and result['provider_response_id'] == 'resp_abc'
    assert result['output_text'] == 'OK'
    assert result['usage']['input_tokens'] == 9
    assert result['persisted'] is False
    assert client.closed
    assert len(client.responses.calls) == 1
    assert client.responses.calls[0] == {
        'model': 'gemma-4-31b-it', 'input': DIAGNOSTIC_PROMPT,
        'store': False, 'agentic_memory': False, 'tools': []
    }
    assert 'example-session-key' not in repr(result)
    assert 'example-env-key' not in repr(result)


def test_environment_fallback(monkeypatch):
    monkeypatch.setenv('ADAPTION_API_KEY', 'example-env-key')
    captured = []
    service = AdaptionDiagnosticService(client_factory=lambda key: (captured.append(key) or FakeClient(key, response())))
    service.test('qwen3.5-397b')
    assert captured == ['example-env-key']


@pytest.mark.parametrize('status,text', [
    ('incomplete', 'OK'), ('failed', ''), ('completed', ''), (None, 'OK')
])
def test_incomplete_failed_or_empty_do_not_pass(status, text):
    client = FakeClient('secret', response(status, text))
    result = AdaptionDiagnosticService(client_factory=lambda key: client).test('gemma-4-31b-it', api_key='secret')
    assert result['ok'] is False
    assert result['provider_status'] == status


def test_sdk_exception_cannot_echo_key():
    token = 'pt_live_privatekey_should_not_echo'
    client = FakeClient(token, exc=RuntimeError('Request secret was ' + token))
    with pytest.raises(AdaptionApiError) as caught:
        AdaptionDiagnosticService(client_factory=lambda key: client).test('glm-5.2', api_key=token)
    assert token not in str(caught.value)
    assert 'RuntimeError' in str(caught.value)
    assert client.closed


def test_http_status_is_safe_and_visible():
    class Unauthorized(Exception):
        status_code = 401
    client = FakeClient('secret', exc=Unauthorized('authorization header secret'))
    with pytest.raises(AdaptionApiError, match=r'HTTP 401'):
        AdaptionDiagnosticService(client_factory=lambda key: client).test('gemma-4-31b-it', api_key='secret')


def test_real_sdk_constructor_contract_with_monkeypatched_module(monkeypatch):
    constructed = []
    client = FakeClient('injected', response())
    def factory(**kwargs):
        constructed.append(kwargs)
        return client
    monkeypatch.setitem(sys.modules, 'adaption', types.SimpleNamespace(Adaption=factory))
    result = AdaptionDiagnosticService().test('gemma-4-31b-it', api_key='injected')
    assert result['ok']
    assert constructed == [{'api_key': 'injected', 'max_retries': 0, 'timeout': 45.0}]
    assert client.closed


def test_sdk_does_not_import_if_creds_missing(monkeypatch):
    monkeypatch.delenv('ADAPTION_API_KEY', raising=False)
    with pytest.raises(AdaptionApiError):
        AdaptionDiagnosticService().test('gemma-4-31b-it')
