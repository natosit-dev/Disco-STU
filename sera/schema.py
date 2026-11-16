"""SERA v0.1 data contract. No Streamlit or model dependencies."""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

SCHEMA_VERSION = "0.1.0"  # Existing frozen v1; never redefine this contract.
SCHEMA_V2 = "0.2.0"
CHARACTERISTICS = {
    "context_not_explicit": "It relies on context not explicit in the source",
    "denies_equivalence": "It denies an equivalence or common assumption",
    "conditions_or_dependencies": "It includes conditions or dependencies",
    "intentional_ambiguity": "Some ambiguity is intentional",
    "rhetorical_form": "Rhetorical form or tone is important",
}
CATEGORIES = {
    "claims": "What propositions were you asserting, questioning, or rejecting?",
    "actors_objects": "Who or what participates in those propositions?",
    "relationships": "What connects the actors, objects, and claims?",
    "negations": "What equivalences or implications were you denying?",
    "conditions_scope": "What qualifications, limits, exceptions, or uncertainty matter?",
    "dependencies": "What needs to be true for other claims to hold?",
    "rhetorical_function": "What were you doing: arguing, criticizing, describing, warning, satirizing?",
    "ambiguities": "What did you intentionally leave unresolved or open?",
}
UNIT_KINDS = ("claim", "actor", "object", "negation", "condition", "qualification", "dependency", "other")
RELATION_TYPES = (
    "supports", "depends_on", "contradicts", "qualifies", "causes", "denies_equivalence", "relates_to", "other"
)
IMPORTANCE = ("unspecified", "essential", "secondary")
POLARITY = ("unspecified", "affirmed", "negated", "uncertain")
DOMAINS = ("philosophical", "political", "technical", "creative_rhetorical", "other")
MAX_WORDS = 200


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_fingerprint(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def artifact_fingerprint(record: dict) -> str:
    payload = {k: v for k, v in record.items() if k != "artifact_sha256"}
    return sha256_bytes(canonical_bytes(payload))


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text, flags=re.UNICODE))


def validate_source(text: str) -> list[str]:
    errors = []
    if not isinstance(text, str) or not text.strip():
        return ["Source paragraph is required."]
    if re.search(r"\r?\n[ \t]*\r?\n", text):
        errors.append("Source must be one contiguous paragraph; blank-line paragraph breaks are not allowed.")
    if word_count(text) > MAX_WORDS:
        errors.append(f"Source exceeds {MAX_WORDS} words ({word_count(text)}). Do not truncate automatically.")
    return errors


def new_record(text: str, title: str = "", origin: str = "", original_date: str = "",
               domain: str = "other", context_dependencies: str = "",
               schema_version: str = SCHEMA_VERSION) -> dict:
    errors = validate_source(text)
    if errors:
        raise ValueError(" ".join(errors))
    if domain not in DOMAINS:
        raise ValueError("Unknown source domain.")
    if schema_version not in (SCHEMA_VERSION, SCHEMA_V2):
        raise ValueError("Unknown SERA capture contract version.")
    now = utc_now()
    record = {
        "schema_version": schema_version,
        "sample_id": str(uuid4()),
        "explication_id": str(uuid4()),
        "producer": "human",
        "epistemic_role": "declared_authorial_intention",
        "version": 1,
        "parent_version_id": None,
        "status": "draft",
        "created_at": now,
        "updated_at": now,
        "frozen_at": None,
        "intention_saved_at": None,
        "categories_saved_at": None,
        "source": {
            "original_text": text,
            "source_sha256": source_fingerprint(text),
            "word_count": word_count(text),
            "title": title,
            "origin": origin,
            "original_date": original_date,
            "domain": domain,
            "context_dependencies": context_dependencies,
        },
        "intention_free_text": "",
        "category_prose": {key: "" for key in CATEGORIES},
        "units": [],
        "relations": [],
    }
    if schema_version == SCHEMA_V2:
        record["characteristics"] = []
    return record


def validate_freeze(record: dict) -> list[str]:
    errors = []
    if record.get("status") != "draft":
        errors.append("Only a draft can be frozen.")
    version = record.get("schema_version")
    if version not in (SCHEMA_VERSION, SCHEMA_V2):
        errors.append("Unrecognized schema version.")
    source = record.get("source", {})
    original = source.get("original_text", "")
    errors.extend(validate_source(original))
    if source.get("source_sha256") != source_fingerprint(original):
        errors.append("Source SHA-256 does not match the text.")
    if source.get("word_count") != word_count(original):
        errors.append("Stored word count does not match the text.")
    if not record.get("intention_free_text", "").strip() or not record.get("intention_saved_at"):
        errors.append("Save a free-text intention before freezing.")
    if version == SCHEMA_VERSION and not record.get("categories_saved_at"):
        errors.append("Explicitly save category-level prose before freezing (empty categories are allowed).")
    if version == SCHEMA_V2:
        characteristics = record.get("characteristics")
        if (not isinstance(characteristics, list)
                or len(characteristics) != len(set(x for x in characteristics if isinstance(x, str)))
                or any(not isinstance(x, str) or x not in CHARACTERISTICS
                       for x in characteristics)):
            errors.append("Optional characteristics must be unique recognized strings.")
    prose = record.get("category_prose", {})
    if not isinstance(prose, dict) or set(prose) != set(CATEGORIES) or any(not isinstance(v, str) for v in prose.values()):
        errors.append("Category prose must contain all eight named string fields.")
    units = record.get("units", [])
    relations = record.get("relations", [])
    if not isinstance(units, list):
        errors.append("Semantic units must be a list.")
        units = []
    elif not units and version == SCHEMA_VERSION:
        errors.append("At least one structured semantic unit is required.")
    if not isinstance(relations, list):
        errors.append("Relations must be a list.")
        relations = []
    ids = set()
    for i, unit in enumerate(units, 1):
        if not isinstance(unit, dict):
            errors.append(f"Unit {i} is not an object.")
            continue
        uid = unit.get("unit_id", "")
        if not uid or uid in ids:
            errors.append(f"Unit {i} has a missing or duplicate ID.")
        ids.add(uid)
        if unit.get("kind") not in UNIT_KINDS:
            errors.append(f"Unit {uid} has an unknown type.")
        if not isinstance(unit.get("text"), str) or not unit["text"].strip():
            errors.append(f"Unit {uid} needs a description.")
        if unit.get("importance") not in IMPORTANCE or unit.get("polarity") not in POLARITY:
            errors.append(f"Unit {uid} has invalid importance or polarity.")
    seen_relations = set()
    for i, relation in enumerate(relations, 1):
        if not isinstance(relation, dict):
            errors.append(f"Relation {i} is not an object.")
            continue
        rid = relation.get("relation_id", "")
        if not rid or rid in seen_relations:
            errors.append(f"Relation {i} has a missing or duplicate ID.")
        seen_relations.add(rid)
        if relation.get("from_unit_id") not in ids or relation.get("to_unit_id") not in ids:
            errors.append(f"Relation {rid} references a nonexistent unit.")
        if relation.get("relation_type") not in RELATION_TYPES:
            errors.append(f"Relation {rid} has an unknown type.")
        if relation.get("relation_type") == "other" and not str(relation.get("explanation", "")).strip():
            errors.append(f"Relation {rid} needs an explanation when its type is 'other'.")
    return errors


def amended_copy(frozen: dict) -> dict:
    if frozen.get("status") != "frozen":
        raise ValueError("Only frozen records can be amended.")
    result = deepcopy(frozen)
    result.pop("artifact_sha256", None)
    result["version"] += 1
    result["parent_version_id"] = frozen["explication_id"]
    result["explication_id"] = str(uuid4())
    result["status"] = "draft"
    result["created_at"] = utc_now()
    result["updated_at"] = result["created_at"]
    result["frozen_at"] = None
    return result
