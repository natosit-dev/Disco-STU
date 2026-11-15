"""SERA v0.2 human capture is distinct from immutable legacy v0.1."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from sera.application import SeraApplication
from sera.schema import (SCHEMA_VERSION, SCHEMA_V2, CHARACTERISTICS,
                         new_record, validate_freeze, artifact_fingerprint)
from sera.service import save_intention, save_category_prose, save_units, save_relations


def test_v2_freezes_unrestricted_meaning_without_structured_labor(tmp_path):
    app = SeraApplication(tmp_path / 'data')
    sample = app.create_sample('Velocity is not productivity.', title='AI Principles')
    assert sample['schema_version'] == SCHEMA_V2
    assert sample['characteristics'] == []
    assert app.validation_errors(sample['sample_id'])  # first save human meaning
    saved = app.save_authoring_draft(
        sample['sample_id'], original_text=sample['source']['original_text'],
        title='AI Principles', origin='', original_date='', domain='philosophical',
        context_dependencies='', intention='Velocity alone does not prove useful work.',
        characteristics=['denies_equivalence'])
    assert saved['intention_free_text'] == 'Velocity alone does not prove useful work.'
    assert saved['characteristics'] == ['denies_equivalence']
    assert saved['categories_saved_at'] is None
    assert saved['units'] == []
    assert saved['relations'] == []
    assert app.validation_errors(sample['sample_id']) == []
    frozen = app.freeze(sample['sample_id'])
    assert frozen['status'] == 'frozen'
    assert frozen['schema_version'] == SCHEMA_V2
    assert artifact_fingerprint(frozen) == frozen['artifact_sha256']
    assert frozen['intention_free_text'] == saved['intention_free_text']
    packet = app.model_packet(sample['sample_id'])
    assert set(packet) == {'packet_type', 'sample_id', 'source_sha256', 'original_text'}
    assert packet['original_text'] == 'Velocity is not productivity.'
    assert 'intention_free_text' not in json.dumps(packet)
    assert 'characteristics' not in json.dumps(packet)


def test_v2_one_save_draft_and_explicit_freeze_with_no_overwrites(tmp_path):
    app = SeraApplication(tmp_path / 'data')
    record = app.create_sample('Original expression', title='First')
    sid = record['sample_id']
    assert app.get_sample(sid)['intention_saved_at'] is None
    first = app.save_authoring_draft(sid, original_text='Corrected before explanation',
        title='New title', origin='', original_date='', domain='other',
        context_dependencies='', intention='', characteristics=[])
    assert first['intention_saved_at'] is None
    second = app.save_authoring_draft(sid, original_text='Corrected before explanation',
        title='New title', origin='Notebook', original_date='', domain='technical',
        context_dependencies='', intention='My original meaning.',
        characteristics=['rhetorical_form', 'intentional_ambiguity'])
    with pytest.raises(ValueError, match='locked'):
        app.save_authoring_draft(sid, original_text='Changing text afterward',
            title='New title', origin='', original_date='', domain='technical',
            context_dependencies='', intention='My meaning.',
            characteristics=[])
    with pytest.raises(ValueError, match='cannot be cleared'):
        app.save_authoring_draft(sid, original_text='Corrected before explanation',
            title='New title', origin='', original_date='', domain='technical',
            context_dependencies='', intention='', characteristics=[])
    assert app.get_sample(sid)['source']['original_text'] == 'Corrected before explanation'
    assert app.get_sample(sid)['intention_free_text'] == 'My original meaning.'
    events = app.store.events(sid)
    assert [entry['event'] for entry in events].count('authoring_draft_saved') == 2
    frozen = app.freeze(sid)
    assert frozen['version'] == 1
    assert app.list_frozen_sources()[0]['sample_id'] == sid
    with pytest.raises(ValueError, match='Frozen'):
        app.save_authoring_draft(sid, original_text=frozen['source']['original_text'],
            title='New title', origin='', original_date='', domain='other',
            context_dependencies='', intention='Later', characteristics=[])


def test_v2_optional_categories_and_relationships_are_not_required(tmp_path):
    app = SeraApplication(tmp_path / 'data')
    source = app.create_sample('The switch disables the conveyor.', title='Switch')
    sid = source['sample_id']
    app.save_authoring_draft(sid, original_text=source['source']['original_text'],
        title='Switch', origin='', original_date='', domain='technical',
        context_dependencies='', intention='The switch acts upon the conveyor.',
        characteristics=['conditions_or_dependencies'])
    annotated = app.save_optional_annotations(sid, units=[
        {'unit_id': 'U1', 'kind': 'claim', 'text': 'Switch is involved',
         'importance': 'essential', 'polarity': 'affirmed'},
        {'unit_id': 'U2', 'kind': 'object', 'text': 'Conveyor'}],
        relations=[{'relation_id': 'R1', 'from_unit_id': 'U1',
                    'to_unit_id': 'U2', 'relation_type': 'relates_to'}])
    assert annotated['units'] and annotated['relations']
    assert annotated['categories_saved_at'] is None
    assert app.validation_errors(sid) == []
    frozen = app.freeze(sid)
    assert len(frozen['units']) == 2
    assert len(frozen['relations']) == 1


def test_v2_invalid_characteristics_or_dangling_graph_fail_closed(tmp_path):
    app = SeraApplication(tmp_path / 'data')
    sample = app.create_sample('A source', title='A')
    sid = sample['sample_id']
    for flags in [['not_real'], ['denies_equivalence', 'denies_equivalence']]:
        with pytest.raises(ValueError, match='Invalid or duplicated'):
            app.save_authoring_draft(sid, original_text='A source', title='A',
                origin='', original_date='', domain='other',
                context_dependencies='', intention='I mean A.', characteristics=flags)
    app.save_authoring_draft(sid, original_text='A source', title='A',
        origin='', original_date='', domain='other',
        context_dependencies='', intention='I mean A.', characteristics=[])
    app.save_optional_annotations(sid, units=[
        {'unit_id': 'U1', 'kind': 'claim', 'text': 'A exists'}],
        relations=[{'relation_id': 'R1', 'from_unit_id': 'U1',
                    'to_unit_id': 'U2', 'relation_type': 'relates_to'}])
    assert 'nonexistent' in ' '.join(app.validation_errors(sid))
    with pytest.raises(ValueError, match='Cannot freeze'):
        app.freeze(sid)


def test_v1_rules_and_frozen_bytes_survive_v2_capture(tmp_path):
    from sera.schema import CATEGORIES
    app = SeraApplication(tmp_path / 'data')
    v1 = app.create_sample('Old authored source', schema_version=SCHEMA_VERSION)
    sid = v1['sample_id']
    app.save_intention(sid, 'My explanation')
    # v1 still insists on categories and a structured unit.
    assert 'category-level prose' in ' '.join(app.validation_errors(sid))
    app.save_categories(sid, {key: '' for key in CATEGORIES})
    assert 'At least one structured semantic unit' in ' '.join(app.validation_errors(sid))
    app.save_units(sid, [{'unit_id': 'U1', 'kind': 'claim', 'text': 'Old source'}])
    v1_frozen = app.freeze(sid)
    path = app.store.sample_dir(sid) / 'oracle-v1.json'
    before = path.read_bytes()
    v2 = app.create_sample('New user source')
    app.save_authoring_draft(v2['sample_id'], original_text='New user source',
        title='new', origin='', original_date='', domain='other',
        context_dependencies='', intention='I meant something new',
        characteristics=[])
    app.freeze(v2['sample_id'])
    assert path.read_bytes() == before
    amended = app.begin_amendment(sid)
    assert amended['schema_version'] == SCHEMA_VERSION
    assert amended['version'] == 2
    assert app.list_frozen_sources()[0]['schema_version'] == SCHEMA_VERSION


def test_v2_amendment_remains_v2_and_pinned_version_stays_historical(tmp_path):
    app = SeraApplication(tmp_path / 'data')
    v2 = app.create_sample('Original writing', title='Original name')
    sid = v2['sample_id']
    app.save_authoring_draft(sid, original_text='Original writing', title='Original name',
        origin='', original_date='', domain='other', context_dependencies='',
        intention='Meaning v1', characteristics=[])
    old = app.freeze(sid)
    amended = app.begin_amendment(sid)
    assert amended['schema_version'] == SCHEMA_V2
    assert amended['version'] == 2
    assert app.list_frozen_sources()[0]['version'] == 1
    app.save_authoring_draft(sid, original_text='Original writing', title='Revised name',
        origin='', original_date='', domain='other', context_dependencies='',
        intention='Meaning v2', characteristics=['rhetorical_form'])
    recent = app.freeze(sid)
    assert recent['version'] == 2
    pinned = app.get_frozen_version(sid, 1, explication_id=old['explication_id'],
                                    sha256=old['artifact_sha256'])
    assert pinned['intention_free_text'] == 'Meaning v1'
    assert pinned['source']['title'] == 'Original name'
