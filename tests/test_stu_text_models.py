"""Model catalog and Streamlit selector regression tests; no live API use."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
from stu.adaption_api import (TEXT_ONLY_MODELS, LEGACY_MODELS, SUPPORTED_MODELS,
                              AdaptionDiagnosticService)
from stu.presentation import model_name
from stu.live import AdaptionModelAdapter
from stu.contracts import GenerationRequest
from stu.application import StuApplication
from stu.cli import smoke


def test_text_only_catalog_and_historical_compatibility():
    # https://docs.adaptionlabs.ai/inference-stacks/models
    assert TEXT_ONLY_MODELS == ('deepseek-v4-flash', 'glm-53-flash', 'glm-5.2')
    assert LEGACY_MODELS == ('gemma-4-31b-it', 'qwen3.5-397b')
    assert set(TEXT_ONLY_MODELS).isdisjoint(LEGACY_MODELS)
    assert set(SUPPORTED_MODELS) == set(TEXT_ONLY_MODELS + LEGACY_MODELS)
    assert model_name('deepseek-v4-flash') == 'DeepSeek V4 Flash'
    assert model_name('glm-53-flash') == 'GLM 5.3 Flash'


@pytest.mark.parametrize('model_id', TEXT_ONLY_MODELS)
def test_new_model_uses_stateless_direct_hosted_api(model_id):
    req = GenerationRequest(stage='decompose', condition='none', fixture_id='LIVE',
        model_profile=model_id, system='frozen system', user='source-only payload',
        input_sha256='test-hash', settings={'synthetic_only': False})
    params = AdaptionModelAdapter(api_key='fake').provider_request(req)
    assert params == {'model': model_id, 'instructions': req.system, 'input': req.user,
                      'store': False, 'agentic_memory': False, 'tools': []}
    assert not params['model'].startswith('stack:')


def test_historical_model_ids_still_usable_for_existing_studies(tmp_path):
    app = StuApplication(tmp_path / 'data')
    sid = smoke(app)['sample_id']
    for model in LEGACY_MODELS:
        study = app.create_study(sid, mode='live', model_id=model)
        assert app.get_study(study['study_id'])['model_id'] == model


def test_deepseek_one_call_diagnostic_uses_hosted_id():
    calls = []
    class Client:
        def __init__(self):
            self.responses = self
        def create(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(status='completed', output_text='OK',
                model='deepseek-v4-flash', id='resp_mock',
                usage={'input_tokens': 9, 'output_tokens': 2},
                error=None, incomplete_details=None)
        def close(self):
            pass
    result = AdaptionDiagnosticService(client_factory=lambda key: Client()).test(
        'deepseek-v4-flash', api_key='fake')
    assert result['ok'] is True
    assert result['requested_model'] == result['actual_model'] == 'deepseek-v4-flash'
    assert result['persisted'] is False
    assert calls == [{'model': 'deepseek-v4-flash', 'input': 'Reply with exactly: OK',
                      'store': False, 'agentic_memory': False, 'tools': []}]


def test_transform_and_api_test_show_text_only_dropdowns(tmp_path, monkeypatch):
    pytest.importorskip('streamlit')
    from streamlit.testing.v1 import AppTest
    data_root = tmp_path / 'data'
    smoke(StuApplication(data_root))
    monkeypatch.setenv('SERA_DATA_DIR', str(data_root))
    root = Path(__file__).resolve().parents[1]
    for page in ('2_STU_Transform.py', '5_Adaption_API_Test.py'):
        ui = AppTest.from_file(str(root / 'pages' / page),
                               default_timeout=15).run()
        assert not ui.exception, list(ui.exception)
        choices = [s for s in ui.selectbox if s.label == 'Hosted model']
        assert len(choices) == 1
        assert tuple(choices[0].options) == TEXT_ONLY_MODELS
        assert choices[0].value == 'deepseek-v4-flash'
