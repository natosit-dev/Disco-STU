"""Plain Python contracts shared by the runner, CLI and thin UI."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Protocol


SCHEMA_VERSION = 'stu.v0.1'
CATEGORIES = ('claims', 'actors_objects', 'relationships', 'negations',
              'conditions_scope', 'dependencies', 'rhetorical_function', 'ambiguities')
UNIT_KINDS = {'claim', 'actor', 'object', 'negation', 'condition', 'qualification', 'dependency', 'other'}
RELATIONS = {'supports', 'depends_on', 'contradicts', 'qualifies', 'causes', 'denies_equivalence', 'relates_to', 'other'}
STATUSES = {'prepared', 'running', 'completed', 'failed', 'cancelled', 'incomplete'}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(',', ':')).encode('utf-8')


def digest(data: bytes | str | object) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = canonical(data)
    return hashlib.sha256(data).hexdigest()


def clean_semantics(value: object) -> dict:
    """Validate model JSON without silently normalizing invalid claims."""
    if not isinstance(value, dict) or set(value) != {'category_prose', 'units', 'relations'}:
        raise ValueError('Decomposition must have category_prose, units and relations only.')
    prose = value['category_prose']
    if not isinstance(prose, dict) or set(prose) != set(CATEGORIES) or not all(isinstance(v, str) for v in prose.values()):
        raise ValueError('Decomposition has invalid categories.')
    if not isinstance(value['units'], list) or not isinstance(value['relations'], list):
        raise ValueError('Decomposition units and relations must be lists.')
    ids = set()
    for unit in value['units']:
        if not isinstance(unit, dict) or set(unit) != {'unit_id', 'kind', 'text', 'importance', 'polarity', 'source_support', 'notes'}:
            raise ValueError('Invalid unit fields.')
        uid = unit['unit_id']
        if not isinstance(uid, str) or not uid or uid in ids:
            raise ValueError('Duplicate or missing unit ID.')
        ids.add(uid)
        if unit['kind'] not in UNIT_KINDS or unit['importance'] not in ('unspecified', 'essential', 'secondary') or unit['polarity'] not in ('unspecified', 'affirmed', 'negated', 'uncertain'):
            raise ValueError('Invalid unit classification.')
        if not isinstance(unit['text'], str) or not unit['text'].strip() or not isinstance(unit['source_support'], str) or not isinstance(unit['notes'], str):
            raise ValueError('Invalid unit text.')
    relation_ids = set()
    for edge in value['relations']:
        if not isinstance(edge, dict) or set(edge) != {'relation_id', 'from_unit_id', 'relation_type', 'to_unit_id', 'explanation'}:
            raise ValueError('Invalid relation fields.')
        rid = edge['relation_id']
        if not isinstance(rid, str) or not rid or rid in relation_ids:
            raise ValueError('Duplicate or missing relation ID.')
        relation_ids.add(rid)
        if edge['from_unit_id'] not in ids or edge['to_unit_id'] not in ids or edge['relation_type'] not in RELATIONS:
            raise ValueError('Broken semantic relationship.')
        if not isinstance(edge['explanation'], str) or (edge['relation_type'] == 'other' and not edge['explanation'].strip()):
            raise ValueError('Relation explanation missing/invalid.')
    return value


@dataclass(frozen=True)
class GenerationRequest:
    stage: str
    condition: str
    fixture_id: str
    model_profile: str
    system: str
    user: str
    input_sha256: str
    settings: dict = field(default_factory=dict)

    def wire(self) -> dict:
        """This is the *actual* serialized adapter request, stored and tested."""
        return {'stage': self.stage, 'condition': self.condition,
                'fixture_id': self.fixture_id, 'model_profile': self.model_profile,
                'messages': [{'role': 'system', 'content': self.system},
                             {'role': 'user', 'content': self.user}],
                'input_sha256': self.input_sha256, 'settings': self.settings}


@dataclass(frozen=True)
class GenerationResult:
    content: str
    adapter: str
    actual_model_id: str
    provider_response_id: str | None = None
    usage: dict = field(default_factory=dict)
    finish_reason: str | None = 'stop'
    metadata: dict = field(default_factory=dict)
    # Optional live provider state. Older deterministic fixtures omit these.
    provider_status: str | None = None
    raw_response: dict | None = None

    def as_dict(self) -> dict:
        return asdict(self)


class ModelAdapter(Protocol):
    name: str
    def generate(self, request: GenerationRequest) -> GenerationResult: ...
