import json
from copy import deepcopy
from pathlib import Path

import pytest

from sera.exports import stu_source_packet
from sera.schema import (
    CATEGORIES, artifact_fingerprint, new_record, source_fingerprint,
    validate_freeze, validate_source, word_count,
)
from sera.service import (
    save_category_prose, save_intention, save_relations, save_units, update_source,
)
from sera.storage import SeraStore


def ready_record(text="Velocity is not productivity. Complexity is not sophistication."):
    rec = new_record(text, title="Example", domain="technical")
    save_intention(rec, "My intention is not the surface wording; ORIGINAL_ORACLE_SECRET.")
    save_category_prose(rec, {k: ("NEGATION_SECRET" if k == "negations" else "") for k in CATEGORIES})
    save_units(rec, [
        {"unit_id": "C001", "kind": "claim", "text": "Velocity is not productivity",
         "importance": "essential", "polarity": "negated", "source_support": "Velocity is not productivity"},
        {"unit_id": "C002", "kind": "claim", "text": "Complexity is not sophistication", "importance": "essential"},
    ])
    save_relations(rec, [{"relation_id": "R001", "from_unit_id": "C001", "relation_type": "relates_to",
                          "to_unit_id": "C002", "explanation": "Both reject equivalences."}])
    return rec


def test_source_validation_no_truncation():
    assert validate_source("hello\n\nworld")
    text = "word " * 201
    assert validate_source(text)
    with pytest.raises(ValueError):
        new_record(text)
    assert word_count("It's high-velocity work") == 3


def test_progressive_gates():
    rec = new_record("An original paragraph.")
    with pytest.raises(ValueError, match="unrestricted intention first"):
        save_category_prose(rec, {key: "" for key in CATEGORIES})
    with pytest.raises(ValueError, match="category-level prose"):
        save_units(rec, [{"text": "unlocked too early"}])
    assert validate_freeze(rec)
    save_intention(rec, "Present intention")
    save_category_prose(rec, {key: "" for key in CATEGORIES})
    assert "At least one structured semantic unit" in " ".join(validate_freeze(rec))


def test_freeze_and_private_export(tmp_path):
    store = SeraStore(tmp_path / "data")
    rec = ready_record()
    store.save_draft(rec)
    fresh = store.load(rec["sample_id"])
    assert fresh["category_prose"]["negations"] == "NEGATION_SECRET"
    frozen = store.freeze(fresh)
    assert frozen["status"] == "frozen"
    assert store.load(rec["sample_id"]) == frozen
    assert artifact_fingerprint(frozen) == frozen["artifact_sha256"]
    packet = store.model_packet(rec["sample_id"])
    assert packet == stu_source_packet(frozen)
    assert set(packet) == {"packet_type", "sample_id", "source_sha256", "original_text"}
    assert "ORACLE_SECRET" not in json.dumps(packet)
    assert "NEGATION_SECRET" not in json.dumps(packet)
    assert "context_dependencies" not in json.dumps(packet)
    events = store.events(rec["sample_id"])
    assert any(e["event"] == "frozen" for e in events)
    with pytest.raises(ValueError, match="Cannot save a frozen"):
        store.save_draft(frozen)
    assert not (store.sample_dir(rec["sample_id"]) / "draft.json").exists()


def test_structured_roundtrip_and_amendment(tmp_path):
    store = SeraStore(tmp_path)
    rec = ready_record()
    store.save_draft(rec)
    frozen = store.freeze(store.load(rec["sample_id"]))
    amended = store.begin_amendment(rec["sample_id"])
    assert amended["version"] == 2
    assert amended["parent_version_id"] == frozen["explication_id"]
    assert amended["explication_id"] != frozen["explication_id"]
    assert amended["relations"][0]["from_unit_id"] == "C001"
    save_intention(amended, "A later interpretation, retaining the historical reference.")
    store.save_draft(amended)
    newer = store.freeze(store.load(rec["sample_id"]))
    assert newer["version"] == 2
    assert store.model_packet(rec["sample_id"]) == stu_source_packet(newer)
    old = json.loads((store.sample_dir(rec["sample_id"]) / "oracle-v1.json").read_text())
    assert old == frozen
    assert old["intention_free_text"] != newer["intention_free_text"]


def test_missing_reference_and_custom_relation():
    rec = ready_record()
    rec["relations"][0]["to_unit_id"] = "DOES_NOT_EXIST"
    assert "nonexistent" in " ".join(validate_freeze(rec))
    rec["relations"][0]["to_unit_id"] = "C002"
    rec["relations"][0]["relation_type"] = "other"
    rec["relations"][0]["explanation"] = ""
    assert "needs an explanation" in " ".join(validate_freeze(rec))
    rec["relations"][0]["explanation"] = "custom association"
    assert validate_freeze(rec) == []
    rec["units"].append(deepcopy(rec["units"][0]))
    assert "duplicate" in " ".join(validate_freeze(rec))


def test_source_lock(tmp_path):
    store = SeraStore(tmp_path)
    rec = new_record("The first expression")
    store.save_draft(rec)
    update_source(rec, original_text="A revised expression")
    store.save_draft(rec)
    save_intention(rec, "Meaning follows this expression")
    store.save_draft(rec)
    with pytest.raises(ValueError, match="locked"):
        update_source(rec, original_text="A changed source")
    copied = store.load(rec["sample_id"])
    copied["source"]["original_text"] = "Something completely different"
    with pytest.raises(ValueError, match="cannot change"):
        store.save_draft(copied)


def test_corrupted_frozen_record_detected(tmp_path):
    store = SeraStore(tmp_path)
    rec = ready_record()
    store.save_draft(rec)
    store.freeze(store.load(rec["sample_id"]))
    path = store.sample_dir(rec["sample_id"]) / "oracle-v1.json"
    data = json.loads(path.read_text())
    data["intention_free_text"] = "tampered"
    path.write_text(json.dumps(data))
    with pytest.raises(RuntimeError, match="SHA-256"):
        store.latest_frozen(rec["sample_id"])


def test_model_packet_requires_frozen(tmp_path):
    rec = ready_record()
    with pytest.raises(ValueError):
        stu_source_packet(rec)
    with pytest.raises(ValueError, match="no frozen Oracle"):
        SeraStore(tmp_path).model_packet(rec["sample_id"])


def test_freeze_event_failure_is_not_reported_as_success(tmp_path, monkeypatch):
    store = SeraStore(tmp_path)
    rec = ready_record()
    store.save_draft(rec)
    original = store._append_event

    def fail_freeze(sample_id, event, record, **kwargs):
        if event == "frozen":
            raise OSError("disk journal unavailable")
        return original(sample_id, event, record, **kwargs)

    monkeypatch.setattr(store, "_append_event", fail_freeze)
    with pytest.raises(OSError, match="disk journal"):
        store.freeze(store.load(rec["sample_id"]))
    assert store.latest_frozen(rec["sample_id"]) is None
    assert store.load(rec["sample_id"])["status"] == "draft"
    assert not store.source_path(rec["sample_id"]).exists()


def test_sample_path_cannot_traverse(tmp_path):
    store = SeraStore(tmp_path)
    with pytest.raises(ValueError, match="UUID"):
        store.sample_dir("../../private")
