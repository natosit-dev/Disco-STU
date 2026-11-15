"""Official one-shot Adaption SDK adapter for live STU experiments.

No storage, Oracle access, tool invocation, automatic retries or synthetic fallback.
A fresh SDK client is used for every independent experiment stage.
"""
from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version
from typing import Callable

from .adaption_api import AdaptionApiError, SUPPORTED_MODELS, _field, _safe_failure
from .contracts import GenerationRequest, GenerationResult

LIVE_TIMEOUT_SECONDS = 120.0


def _full_response(response: object) -> dict:
    """Capture complete JSON-compatible SDK response, including null fields."""
    if isinstance(response, dict):
        return response
    if hasattr(response, 'model_dump'):
        try:
            result = response.model_dump(mode='json', exclude_none=False)
        except TypeError:
            result = response.model_dump(exclude_none=False)
        if isinstance(result, dict):
            return result
    if hasattr(response, 'to_dict'):
        result = response.to_dict()
        if isinstance(result, dict):
            return result
    # Fallback for mocked or unusual response objects; no SDK repr or secrets.
    return {name: _field(response, name) for name in (
        'id', 'object', 'created_at', 'status', 'model', 'output', 'output_text',
        'usage', 'error', 'incomplete_details', 'metadata', 'store', 'previous_response_id')}


class AdaptionModelAdapter:
    name = 'adaption'

    def __init__(self, *, api_key: str | None = None,
                 client_factory: Callable[[str], object] | None = None):
        self._key = (api_key or os.getenv('ADAPTION_API_KEY') or '').strip()
        if not self._key:
            raise AdaptionApiError('No Adaption API key configured in this session or environment.')
        self._client_factory = client_factory

    def provider_request(self, request: GenerationRequest) -> dict:
        if request.model_profile not in SUPPORTED_MODELS:
            raise AdaptionApiError('Unsupported Adaption model selection.')
        # Every field here is an actual Responses API argument (no key/headers).
        # No seed: undocumented. Temperature omitted to use provider defaults.
        return {
            'model': request.model_profile,
            'instructions': request.system,
            'input': request.user,
            'store': False,
            'agentic_memory': False,
            'tools': [],
        }

    def generate(self, request: GenerationRequest) -> GenerationResult:
        params = self.provider_request(request)
        client = None
        try:
            if self._client_factory is not None:
                client = self._client_factory(self._key)
            else:
                from adaption import Adaption
                client = Adaption(api_key=self._key, max_retries=0,
                                  timeout=LIVE_TIMEOUT_SECONDS)
            response = client.responses.create(**params)
            full = _full_response(response)
            content = _field(response, 'output_text', '') or ''
            if not isinstance(content, str):
                content = str(content)
            try:
                sdk_version = version('adaption')
            except PackageNotFoundError:
                sdk_version = 'mocked_or_unavailable'
            return GenerationResult(
                content=content, adapter=self.name,
                actual_model_id=str(_field(response, 'model', '') or ''),
                provider_response_id=_field(response, 'id'),
                usage=full.get('usage') or {},
                finish_reason=_field(response, 'status'),
                metadata={'sdk': 'adaption', 'sdk_version': sdk_version,
                          'timeout_seconds': LIVE_TIMEOUT_SECONDS, 'max_retries': 0,
                          'sampling_parameters': 'not_set_provider_defaults'},
                provider_status=_field(response, 'status'),
                raw_response=full,
            )
        except AdaptionApiError:
            raise
        except Exception as exc:
            # No SDK message/headers: they can contain credentials or private inputs.
            raise _safe_failure(exc) from None
        finally:
            if client is not None:
                close = getattr(client, 'close', None)
                if callable(close):
                    try:
                        close()
                    except Exception:
                        pass
