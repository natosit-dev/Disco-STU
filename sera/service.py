"""Explicit transitions between SERA's three progressive human-explication stages."""
from __future__ import annotations

from uuid import uuid4

from .schema import (CATEGORIES, IMPORTANCE, POLARITY, RELATION_TYPES, UNIT_KINDS,
                     SCHEMA_V2, CHARACTERISTICS, utc_now)


def _draft(record: dict) -> None:
    if record.get("status") != "draft":
        raise ValueError("Frozen records cannot be edited. Begin an amendment.")


def update_source(record: dict, **fields: str) -> dict:
    _draft(record)
    if "original_text" in fields and fields["original_text"] != record["source"]["original_text"]:
        if record.get("intention_saved_at"):
            raise ValueError("The source is locked after intention is saved. Create a new sample.")
        from .schema import validate_source, source_fingerprint, word_count
        text = fields["original_text"]
        errors = validate_source(text)
        if errors:
            raise ValueError(" ".join(errors))
        record["source"]["source_sha256"] = source_fingerprint(text)
        record["source"]["word_count"] = word_count(text)
    for key, value in fields.items():
        if key not in ("original_text", "title", "origin", "original_date", "domain", "context_dependencies"):
            raise ValueError(f"Unexpected source field {key!r}")
        record["source"][key] = value
    record["updated_at"] = utc_now()
    return record


def save_intention(record: dict, text: str) -> dict:
    _draft(record)
    if not text.strip():
        raise ValueError("Free intended meaning is required.")
    record["intention_free_text"] = text
    record["intention_saved_at"] = utc_now()
    record["updated_at"] = record["intention_saved_at"]
    return record


def save_category_prose(record: dict, prose: dict[str, str]) -> dict:
    _draft(record)
    if not record.get("intention_saved_at"):
        raise ValueError("Save the unrestricted intention first.")
    if set(prose) != set(CATEGORIES) or any(not isinstance(v, str) for v in prose.values()):
        raise ValueError("The eight category prose fields must all be provided as strings.")
    record["category_prose"] = prose.copy()
    record["categories_saved_at"] = utc_now()
    record["updated_at"] = record["categories_saved_at"]
    return record


def _rows(rows: list[dict], kind: str) -> list[dict]:
    result = []
    for row in rows:
        row = {k: "" if v is None else str(v).strip() for k, v in row.items()}
        if not any(row.values()):
            continue
        if kind == "unit":
            item = {
                "unit_id": row.get("unit_id") or f"U-{uuid4().hex[:12]}",
                "kind": row.get("kind") or "claim",
                "text": row.get("text", ""),
                "importance": row.get("importance") or "unspecified",
                "polarity": row.get("polarity") or "unspecified",
                "source_support": row.get("source_support", ""),
                "notes": row.get("notes", ""),
            }
            if item["kind"] not in UNIT_KINDS or item["importance"] not in IMPORTANCE or item["polarity"] not in POLARITY:
                raise ValueError("Invalid semantic unit category, importance, or polarity.")
        else:
            item = {
                "relation_id": row.get("relation_id") or f"R-{uuid4().hex[:12]}",
                "from_unit_id": row.get("from_unit_id", ""),
                "relation_type": row.get("relation_type") or "relates_to",
                "to_unit_id": row.get("to_unit_id", ""),
                "explanation": row.get("explanation", ""),
            }
            if item["relation_type"] not in RELATION_TYPES:
                raise ValueError("Unknown relationship type.")
        result.append(item)
    id_field = "unit_id" if kind == "unit" else "relation_id"
    ids = [x[id_field] for x in result]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate {id_field} values.")
    return result


def save_units(record: dict, rows: list[dict]) -> dict:
    _draft(record)
    if record.get("schema_version") == SCHEMA_V2:
        if not record.get("intention_saved_at"):
            raise ValueError("Save your unrestricted explanation before optional annotations.")
    elif not record.get("categories_saved_at"):
        raise ValueError("Save category-level prose before creating units.")
    record["units"] = _rows(rows, "unit")
    record["updated_at"] = utc_now()
    return record


def save_relations(record: dict, rows: list[dict]) -> dict:
    _draft(record)
    if record.get("schema_version") == SCHEMA_V2:
        if not record.get("intention_saved_at"):
            raise ValueError("Save your unrestricted explanation before optional annotations.")
    elif not record.get("categories_saved_at"):
        raise ValueError("Save category-level prose before creating relationships.")
    record["relations"] = _rows(rows, "relation")
    record["updated_at"] = utc_now()
    return record
