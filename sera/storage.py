"""Single-user, local, revisioned SERA storage. No database server required."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from uuid import UUID, uuid4

from .exports import stu_source_packet
from .schema import (
    amended_copy, artifact_fingerprint, canonical_bytes, utc_now, validate_freeze,
)


def _sample_id(value: str) -> str:
    try:
        normalized = str(UUID(value))
    except (ValueError, AttributeError, TypeError) as exc:
        raise ValueError("Invalid sample UUID.") from exc
    if normalized != value:
        raise ValueError("Sample UUID must be canonical.")
    return value


def _write_json_atomic(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".sera-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(obj, handle, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _read_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            record = json.load(handle)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Cannot read SERA record {path}: {exc}") from exc
    if not isinstance(record, dict):
        raise RuntimeError(f"SERA record is not an object: {path}")
    return record


class SeraStore:
    def __init__(self, root: str | Path = "data") -> None:
        self.root = Path(root)

    def sample_dir(self, sample_id: str) -> Path:
        return self.root / "private" / "sera" / _sample_id(sample_id)

    def source_path(self, sample_id: str) -> Path:
        return self.root / "stu_inputs" / f"{_sample_id(sample_id)}.json"

    def sample_ids(self) -> list[str]:
        base = self.root / "private" / "sera"
        if not base.exists():
            return []
        result = []
        for d in base.iterdir():
            if d.is_dir():
                try:
                    result.append(_sample_id(d.name))
                except ValueError:
                    continue
        return sorted(result)

    def _append_event(self, sample_id: str, event: str, record: dict, **extra: object) -> None:
        path = self.sample_dir(sample_id) / "events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "event_id": str(uuid4()), "event": event, "at": utc_now(),
            "sample_id": sample_id, "explication_id": record["explication_id"],
            "version": record["version"], **extra,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_bytes(entry).decode("utf-8") + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def events(self, sample_id: str) -> list[dict]:
        path = self.sample_dir(sample_id) / "events.jsonl"
        if not path.exists():
            return []
        result = []
        with path.open("r", encoding="utf-8") as handle:
            for n, line in enumerate(handle, 1):
                if line.strip():
                    try:
                        result.append(json.loads(line))
                    except ValueError as exc:
                        raise RuntimeError(f"Corrupt event journal at line {n}: {path}") from exc
        return result

    def _frozen_versions(self, sample_id: str) -> list[int]:
        return sorted(int(f.stem.split("-v", 1)[1]) for f in self.sample_dir(sample_id).glob("oracle-v*.json")
                      if f.stem.split("-v", 1)[-1].isdigit())

    def latest_frozen(self, sample_id: str) -> dict | None:
        versions = self._frozen_versions(sample_id)
        if not versions:
            return None
        version = versions[-1]
        record = _read_json(self.sample_dir(sample_id) / f"oracle-v{version}.json")
        if record.get("status") != "frozen" or record.get("version") != version:
            raise RuntimeError("Invalid frozen SERA record status/version.")
        if artifact_fingerprint(record) != record.get("artifact_sha256"):
            raise RuntimeError("Frozen Oracle integrity check failed (SHA-256 mismatch).")
        if not any(event.get("event") == "frozen" and
                   event.get("explication_id") == record.get("explication_id") and
                   event.get("artifact_sha256") == record.get("artifact_sha256")
                   for event in self.events(sample_id)):
            raise RuntimeError("Frozen Oracle lacks a matching freeze event; incomplete write suspected.")
        return record

    def load(self, sample_id: str) -> dict:
        draft_path = self.sample_dir(sample_id) / "draft.json"
        frozen = self.latest_frozen(sample_id)
        if draft_path.exists():
            draft = _read_json(draft_path)
            if draft.get("sample_id") != sample_id or draft.get("status") != "draft":
                raise RuntimeError("Invalid saved draft identity/status.")
            if frozen is None or draft.get("version", 0) > frozen["version"]:
                return draft
        if frozen is not None:
            return frozen
        raise FileNotFoundError(f"No SERA record for sample {sample_id}")

    def save_draft(self, record: dict, event: str = "draft_saved") -> dict:
        if record.get("status") != "draft":
            raise ValueError("Cannot save a frozen record as a draft.")
        sample_id = _sample_id(record["sample_id"])
        frozen = self.latest_frozen(sample_id)
        if frozen and record["version"] <= frozen["version"]:
            raise ValueError("Cannot overwrite a frozen version. Begin an amendment.")
        path = self.sample_dir(sample_id) / "draft.json"
        if path.exists():
            prior = _read_json(path)
            if (prior.get("explication_id"), prior.get("version")) != (record.get("explication_id"), record.get("version")):
                raise ValueError("Draft version mismatch; reload before saving.")
            if prior.get("intention_saved_at") and record.get("source", {}).get("original_text") != prior.get("source", {}).get("original_text"):
                raise ValueError("Source paragraph cannot change after saving free intention.")
        record["updated_at"] = utc_now()
        _write_json_atomic(path, record)
        self._append_event(sample_id, event, record)
        return record

    def freeze(self, record: dict) -> dict:
        sample_id = _sample_id(record["sample_id"])
        saved = self.load(sample_id)
        if saved.get("status") != "draft" or saved.get("explication_id") != record.get("explication_id"):
            raise ValueError("Draft no longer current. Reload before freezing.")
        if canonical_bytes(saved) != canonical_bytes(record):
            raise ValueError("Unsaved changes detected. Save your edits before freezing.")
        errors = validate_freeze(record)
        if errors:
            raise ValueError("Cannot freeze: " + "; ".join(errors))
        version = record["version"]
        path = self.sample_dir(sample_id) / f"oracle-v{version}.json"
        if path.exists():
            raise FileExistsError(f"Frozen version {version} already exists.")
        frozen = json.loads(canonical_bytes(record))
        frozen["status"] = "frozen"
        frozen["frozen_at"] = utc_now()
        frozen["artifact_sha256"] = artifact_fingerprint(frozen)
        packet = stu_source_packet(frozen)
        out = self.source_path(sample_id)
        if out.exists() and _read_json(out) != packet:
            raise RuntimeError("Existing STU packet disagrees with frozen source; refusing overwrite.")
        wrote_packet = False
        try:
            _write_json_atomic(path, frozen)
            if not out.exists():
                _write_json_atomic(out, packet)
                wrote_packet = True
            self._append_event(sample_id, "frozen", frozen, artifact_sha256=frozen["artifact_sha256"])
        except Exception:
            # Best effort rollback of this multi-file local operation, never report a false freeze.
            if path.exists():
                path.unlink()
            if wrote_packet and out.exists():
                out.unlink()
            raise
        draft_path = self.sample_dir(sample_id) / "draft.json"
        if draft_path.exists():
            draft_path.unlink()
        return frozen

    def begin_amendment(self, sample_id: str) -> dict:
        frozen = self.latest_frozen(sample_id)
        if frozen is None:
            raise ValueError("No frozen record to amend.")
        path = self.sample_dir(sample_id) / "draft.json"
        if path.exists():
            existing = _read_json(path)
            if existing.get("version", 0) > frozen["version"]:
                return existing
        record = amended_copy(frozen)
        _write_json_atomic(path, record)
        self._append_event(sample_id, "amendment_started", record,
                           parent_version_id=frozen["explication_id"])
        return record

    def model_packet(self, sample_id: str) -> dict:
        frozen = self.latest_frozen(sample_id)
        if frozen is None:
            raise ValueError("Sample has no frozen Oracle.")
        packet = _read_json(self.source_path(sample_id))
        if packet != stu_source_packet(frozen):
            raise RuntimeError("STU source packet does not match the frozen source.")
        return packet
