"""Known synthetic experiments. These are NOT observations of model behavior."""
from __future__ import annotations

import json
from .contracts import (CATEGORIES, GenerationRequest, GenerationResult,
                        clean_semantics, digest)

# All source sentences are fictional test data, not copied from a research corpus.
FIXTURES = {
    'F01': {'source': 'The harbor gate remains closed until the safety inspection is complete.',
            'meaning': 'The harbor gate stays closed until inspection is complete.',
            'neutral': 'The harbor gate remains closed until its safety inspection is complete.',
            'commercial': 'Management should keep the gate closed until the safety inspection is complete.',
            'expected': 'faithful'},
    'F02': {'source': 'The launch may proceed only after both the sensor and operator checks pass.',
            'meaning': 'The launch requires both checks to pass.',
            'neutral': 'The launch is ready to proceed.',
            'commercial': 'Management should schedule the launch.',
            'expected': 'decomposition_omission', 'drop_condition': True},
    'F03': {'source': 'The bridge can reopen during daylight, provided the inspection is complete.',
            'meaning': 'Reopening is allowed only in daylight after inspection.',
            'neutral': 'The bridge can reopen after inspection.',
            'commercial': 'Management should reopen the bridge during daylight after inspection.',
            'expected': 'neutral_qualification_loss'},
    'F04': {'source': 'The cooperative has not decided whether to replace its aging ferry.',
            'meaning': 'No decision about ferry replacement has been made.',
            'neutral': 'The cooperative has not decided whether to replace the ferry.',
            'commercial': 'Management should accelerate the ferry replacement to gain market share.',
            'expected': 'unsupported_management_objective'},
    'F05': {'source': 'The alarm disables the conveyor if the emergency switch is activated.',
            'meaning': 'The emergency switch activates the conveyor shutdown.',
            'neutral': 'The emergency switch disables the conveyor if the alarm is activated.',
            'commercial': 'Management should configure the alarm to turn on the conveyor.',
            'expected': 'relation_distortion'},
    'F06': {'source': 'The garden closes whenever the water quality test fails.',
            'meaning': 'Closure depends on failed water tests.',
            'neutral': 'The garden closes when the water quality test fails.',
            'commercial': 'Management should post the water test results and close the garden when a test fails.',
            'expected': 'source_consistent_extension'},
    'F07': {'source': 'The observatory needs a working telescope for night observations.',
            'meaning': 'Night observations depend on a working telescope.',
            'neutral': '', 'commercial': '',
            'expected': 'invalid_json', 'malformed_decomposition': True},
    'F08': {'source': 'The lighthouse is staffed while the radio system is offline.',
            'meaning': 'Staff remain at the lighthouse during a radio outage.',
            'neutral': 'The lighthouse remains staffed during radio outages.',
            'commercial': '', 'expected': 'incomplete_pair', 'fail_commercial': True},
    'F09': {'source': 'The ferry has a new schedule on Fridays.',
            'meaning': 'A different Friday timetable is in effect.',
            'neutral': 'The ferry has a new Friday schedule.',
            'commercial': 'Management should publish the revised Friday schedule.',
            'expected': 'oracle_source_gap'},
    'F10': {'source': 'The library closes at six on Thursdays.',
            'meaning': 'Thursday closing time is 6 p.m.',
            'neutral': 'The library closes at six on Thursdays.',
            'commercial': 'Management should honor the six o’clock Thursday closing time.',
            'expected': 'no_meaningful_gap'},
}


def get_fixture(fixture_id: str) -> dict:
    if fixture_id not in FIXTURES and fixture_id != 'STRUCTURAL':
        raise ValueError(f'Unknown deterministic fixture: {fixture_id}')
    return FIXTURES.get(fixture_id, {'source': '', 'meaning': '', 'neutral': '', 'commercial': '', 'expected': 'structural_smoke'})


def semantic_fixture(fixture_id: str) -> dict:
    f = get_fixture(fixture_id)
    meaning = ('SYNTHETIC STRUCTURAL PLACEHOLDER: no semantic interpretation performed.'
               if fixture_id == 'STRUCTURAL' else f['meaning'])
    if f.get('drop_condition'):
        meaning = 'The launch may proceed.'
    return clean_semantics({
        'category_prose': {k: (meaning if k == 'claims' else '') for k in CATEGORIES},
        'units': [{'unit_id': 'F-U1', 'kind': 'claim' if fixture_id != 'STRUCTURAL' else 'other',
                   'text': meaning, 'importance': 'essential' if fixture_id != 'STRUCTURAL' else 'unspecified',
                   'polarity': 'affirmed' if fixture_id != 'STRUCTURAL' else 'uncertain',
                   'source_support': '' if fixture_id == 'STRUCTURAL' or f.get('drop_condition') else f['source'],
                   'notes': 'SYNTHETIC_TEST; NOT A MODEL INFERENCE'}],
        'relations': [],
    })


class DeterministicFixtureAdapter:
    name = 'deterministic_fixture'

    def generate(self, request: GenerationRequest) -> GenerationResult:
        fixture = get_fixture(request.fixture_id)
        if request.stage not in ('decompose', 'reconstruct'):
            raise ValueError('Unrecognized stage.')
        if request.stage == 'decompose':
            payload = json.loads(request.user)
            packet = payload['source_packet']
            if packet['source_sha256'] != request.input_sha256:
                raise ValueError('Source identity mismatch.')
            if request.fixture_id != 'STRUCTURAL' and packet['original_text'] != fixture['source']:
                raise ValueError('Fixture must match exact known synthetic source text.')
            if fixture.get('malformed_decomposition'):
                content = '{"units": [NOT_VALID_JSON]'
            else:
                content = json.dumps(semantic_fixture(request.fixture_id), ensure_ascii=False, sort_keys=True)
        elif request.condition in ('neutral', 'commercial'):
            if fixture.get('fail_commercial') and request.condition == 'commercial':
                raise RuntimeError('Synthetic fixture: commercial branch unavailable.')
            if request.fixture_id == 'STRUCTURAL':
                content = ('SYNTHETIC STRUCTURAL PLACEHOLDER: no interpretation of source meaning performed. '
                           'This output is for workflow verification only.')
            else:
                content = fixture[request.condition]
        else:
            raise ValueError('Unknown reconstruction condition.')
        return GenerationResult(content=content, adapter=self.name,
                                actual_model_id='deterministic-fixture-v0.1',
                                provider_response_id='synthetic-' + digest(request.wire())[:16],
                                metadata={'synthetic': True, 'fixture': request.fixture_id,
                                          'expected_synthetic_case': fixture['expected']})
