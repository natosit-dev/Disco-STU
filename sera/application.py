"""The sole application-facing facade for existing SERA domain and storage code.

Streamlit and the STU application call commands here instead of SeraStore directly.
"""
from __future__ import annotations

import json
from pathlib import Path

from .schema import new_record, artifact_fingerprint
from .service import update_source, save_intention, save_category_prose, save_units, save_relations
from .storage import SeraStore


class SeraApplication:
    def __init__(self, data_root: str | Path = 'data'):
        self.store = SeraStore(data_root)

    def list_samples(self) -> list[dict]:
        return [self.get_sample(sid) for sid in self.store.sample_ids()]

    def get_sample(self, sample_id: str) -> dict:
        return self.store.load(sample_id)

    def create_sample(self, text: str, *, title: str = '', origin: str = '',
                      original_date: str = '', domain: str = 'other',
                      context_dependencies: str = '') -> dict:
        rec = new_record(text, title=title, origin=origin, original_date=original_date,
                         domain=domain, context_dependencies=context_dependencies)
        return self.store.save_draft(rec, event='source_created')

    def save_source(self, sample_id: str, **fields: str) -> dict:
        rec = self.get_sample(sample_id)
        update_source(rec, **fields)
        return self.store.save_draft(rec, event='source_saved')

    def save_intention(self, sample_id: str, text: str) -> dict:
        rec = self.get_sample(sample_id)
        save_intention(rec, text)
        return self.store.save_draft(rec, event='intention_saved')

    def save_categories(self, sample_id: str, prose: dict[str, str]) -> dict:
        rec = self.get_sample(sample_id)
        save_category_prose(rec, prose)
        return self.store.save_draft(rec, event='categories_saved')

    def save_units(self, sample_id: str, units: list[dict]) -> dict:
        rec = self.get_sample(sample_id)
        save_units(rec, units)
        return self.store.save_draft(rec, event='units_saved')

    def save_relations(self, sample_id: str, relations: list[dict]) -> dict:
        rec = self.get_sample(sample_id)
        save_relations(rec, relations)
        return self.store.save_draft(rec, event='relations_saved')

    def freeze(self, sample_id: str, *, expected_version: int | None = None) -> dict:
        rec = self.get_sample(sample_id)
        if expected_version is not None and rec['version'] != expected_version:
            raise ValueError('SERA version changed; reload before freeze.')
        return self.store.freeze(rec)

    def begin_amendment(self, sample_id: str) -> dict:
        return self.store.begin_amendment(sample_id)

    def get_frozen_version(self, sample_id: str, version: int, *,
                           explication_id: str | None = None,
                           sha256: str | None = None) -> dict:
        """Read and verify one *historical* frozen Oracle, never 'latest'."""
        if not isinstance(version, int) or version < 1:
            raise ValueError('Invalid Oracle version.')
        path = self.store.sample_dir(sample_id) / f'oracle-v{version}.json'
        if not path.is_file():
            raise FileNotFoundError(f'Oracles version {version} not found.')
        rec = json.loads(path.read_text(encoding='utf-8'))
        if rec.get('sample_id') != sample_id or rec.get('version') != version or rec.get('status') != 'frozen':
            raise RuntimeError('Oracle identity/version mismatch.')
        actual = artifact_fingerprint(rec)
        if rec.get('artifact_sha256') != actual:
            raise RuntimeError('Oracle artifact integrity mismatch.')
        if sha256 is not None and sha256 != actual:
            raise RuntimeError('Pinned Oracle hash mismatch.')
        if explication_id is not None and explication_id != rec.get('explication_id'):
            raise RuntimeError('Pinned Oracle explication ID mismatch.')
        if not any(e.get('event') == 'frozen' and e.get('explication_id') == rec['explication_id']
                   and e.get('artifact_sha256') == actual for e in self.store.events(sample_id)):
            raise RuntimeError('Frozen Oracle has no matching freeze event.')
        return rec

    def private_oracle(self, sample_id: str) -> dict:
        rec = self.store.latest_frozen(sample_id)
        if rec is None:
            raise ValueError('Must freeze SERA before creating a study.')
        return rec

    def model_packet(self, sample_id: str) -> dict:
        return self.store.model_packet(sample_id)

    def editor_spec(self) -> dict:
        from .schema import CATEGORIES, DOMAINS, UNIT_KINDS, IMPORTANCE, POLARITY, RELATION_TYPES
        return {'categories': CATEGORIES, 'domains': list(DOMAINS),
                'unit_kinds': list(UNIT_KINDS), 'importance': list(IMPORTANCE),
                'polarity': list(POLARITY), 'relation_types': list(RELATION_TYPES)}

    def validation_errors(self, sample_id: str) -> list[str]:
        from .schema import validate_freeze
        return validate_freeze(self.get_sample(sample_id))
