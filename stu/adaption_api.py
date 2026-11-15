"""One-request Adaption connectivity diagnostic.

No file writes, experiment creation, model scoring, or persistent credential storage.
The diagnostic is intentionally isolated from the STU experiment runner.
"""
from __future__ import annotations

import os
from typing import Any, Callable

# New study / connectivity selectors show Adaption's text-only hosted deployments.
# These exact IDs come from https://docs.adaptionlabs.ai/inference-stacks/models
TEXT_ONLY_MODELS = ("deepseek-v4-flash", "glm-53-flash", "glm-5.2")
# Do not remove historical model IDs: stored Gemma and Qwen experiments need
# to remain runnable/inspectable without mutating their pinned study contracts.
LEGACY_MODELS = ("gemma-4-31b-it", "qwen3.5-397b")
SUPPORTED_MODELS = TEXT_ONLY_MODELS + LEGACY_MODELS
DIAGNOSTIC_PROMPT = "Reply with exactly: OK"
SDK_TIMEOUT_SECONDS = 45.0


class AdaptionApiError(RuntimeError):
    """Safe diagnostic failure suitable for user-visible UI."""


def _field(obj: object, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _as_basic(value: object) -> object:
    """Read limited, non-secret response metadata; never serialize client objects."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _as_basic(v) for k, v in value.items()}
    if hasattr(value, "model_dump"):
        return _as_basic(value.model_dump(exclude_none=True))
    if hasattr(value, "to_dict"):
        return _as_basic(value.to_dict())
    return None


def _safe_failure(exc: Exception) -> AdaptionApiError:
    # Never expose SDK exception messages or headers: these can include request details.
    code = getattr(exc, "status_code", None)
    label = type(exc).__name__
    if isinstance(code, int):
        return AdaptionApiError(f"Adaption request failed: {label} (HTTP {code}).")
    return AdaptionApiError(f"Adaption request failed: {label}.")


class AdaptionDiagnosticService:
    """A small backend facade that makes exactly one stateless SDK call when asked."""

    def __init__(self, *, client_factory: Callable[[str], object] | None = None):
        self._client_factory = client_factory

    def _client(self, key: str) -> object:
        if self._client_factory is not None:
            return self._client_factory(key)
        try:
            from adaption import Adaption
        except ImportError as exc:
            raise AdaptionApiError(
                'Adaption SDK is not installed. Run: python -m pip install -r requirements-dev.txt'
            ) from None
        return Adaption(api_key=key, max_retries=0, timeout=SDK_TIMEOUT_SECONDS)

    def test(self, model: str, *, api_key: str | None = None) -> dict:
        if model not in SUPPORTED_MODELS:
            raise AdaptionApiError('Unsupported diagnostic model selection.')
        # UI-provided session credential takes precedence; env fallback is optional.
        key = (api_key or os.environ.get("ADAPTION_API_KEY") or "").strip()
        if not key:
            raise AdaptionApiError('No Adaption API key configured in this session or environment.')

        client = None
        try:
            client = self._client(key)
            # Fixed prompt; no model input from SERA or private Oracle.
            response = client.responses.create(
                model=model,
                input=DIAGNOSTIC_PROMPT,
                store=False,
                agentic_memory=False,
                tools=[],
            )
            status = _field(response, 'status', None)
            text = _field(response, 'output_text', '') or ''
            if not isinstance(text, str):
                text = str(text)
            return {
                'ok': status == 'completed' and bool(text.strip()),
                'requested_model': model,
                'actual_model': _field(response, 'model', None),
                'provider_response_id': _field(response, 'id', None),
                'provider_status': status,
                'output_text': text,
                'usage': _as_basic(_field(response, 'usage', None)),
                'error': _as_basic(_field(response, 'error', None)),
                'incomplete_details': _as_basic(_field(response, 'incomplete_details', None)),
                'store': False,
                'agentic_memory': False,
                'tools_enabled': False,
                'prompt': DIAGNOSTIC_PROMPT,
                'purpose': 'adaption_connectivity_only',
                'persisted': False,
            }
        except AdaptionApiError:
            raise
        except Exception as exc:
            raise _safe_failure(exc) from None
        finally:
            if client is not None:
                close = getattr(client, 'close', None)
                if callable(close):
                    try:
                        close()
                    except Exception:
                        pass  # No credential-bearing cleanup exceptions in UI.
