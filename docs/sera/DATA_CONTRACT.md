# SERA data contract v0.1

**Source is not intention.** The frozen Oracle is the author's current retrospective account of intended meaning; it may contain relationships absent from the original paragraph. Their absence in source cannot automatically be attributed to a model.

## Shared semantics

The categories, unit types, and directed relationship types are documented in [`../../schemas/semantic_v0.1.json`](../../schemas/semantic_v0.1.json). The source-of-truth Python validators live in [`../../sera/schema.py`](../../sera/schema.py). Each explication has stable local unit IDs; model-provided IDs need not match human IDs.

Three progressive stages are retained independently:

1. `intention_free_text`: unrestricted human meaning, before viewing categories.
2. `category_prose`: separate human prose for eight categories, including empty ones.
3. `units` + `relations`: explicit semantic structure, directed edges and optional source support.

Stages are unlocked only after explicitly saving the preceding stage. Later draft edits are allowed; the final frozen record retains all layers.

## Oracle and model input

Private Oracle artifact: `data/private/sera/<uuid>/oracle-vN.json`. This includes all three semantic layers, source provenance, context, creation/freeze times and a self-checking SHA-256 of the canonical JSON payload (excluding the checksum field).

Model-visible source packet: `data/stu_inputs/<uuid>.json`, constructed from exactly these fields:

- `packet_type`: `stu_source_v0.1`
- `sample_id`
- `source_sha256`
- `original_text`

No intended meaning, category prose, structured units, provenance title, context annotations, or amendment information is included. The runner must read only the source packet.

## Storage and privacy

- `draft.json` may be atomically rewritten until frozen.
- `events.jsonl` appends explicit saves, freezes and amendment starts.
- `oracle-vN.json` is never modified in place by SERA; amendments create a new version and parent reference.
- Disk files are **not encrypted** by SERA. Keep the application local and use operating-system disk encryption/access controls where appropriate.
- `data/` is `.gitignore`-excluded. Explicitly check the files selected for public release.

No transactional multi-file guarantee is claimed. Freeze writes its private Oracle and allowlisted source packet, then appends an event, and reports failure if a required write fails. Integrity is checked on later reads.

## Hash convention

`source_sha256 = SHA256(original_text.encode('utf-8'))` (no normalization).

`artifact_sha256 = SHA256(json.dumps(record_without_artifact_sha256, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8'))`.

This detects accidental modification; without signing or external anchoring it is **not** a tamper-evident security system against an adversary able to edit all local files.
