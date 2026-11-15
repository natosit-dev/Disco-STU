# SERA human-first capture contract v0.2.0

This is an **additive** research contract. Do not rewrite, recalculate or relabel existing frozen v0.1.0 `oracle-vN.json` records or their source-only packets.

## Required for v0.2 freezing

- A valid source (200 words or less, one paragraph without blank-line breaks) and unchanged source SHA-256.
- An explicit, **saved**, unrestricted human `intention_free_text`. That text is the authoritative authorial reference.
- An explicit Freeze action; a plain Save draft does not freeze the record.

## Optional annotations

- `characteristics`: zero or more of the five named checkboxes. They classify the *presence* of a feature, never its proposition, causal relation or target.
- `category_prose`: same eight keys as legacy v0.1, but no mandatory category-save event.
- `units` and `relations`: still available under Advanced, never mandatory. If supplied, their IDs/fields/references are validated. They do **not** get generated automatically from checkboxes.
- Source provenance beyond the title is optional and collapsed in the UI.

## Capture workflow

1. New source → title, paragraph, optional provenance.
2. Draft → unrestricted intended meaning, optional characteristics, optional guided prose → **Save draft**.
3. Optionally add structured semantic units and relations in Advanced. These are separately saved by a deliberate command.
4. **Freeze** the explicitly saved authorial baseline.

Every write is an explicit backend service command and is recorded in SERA events. SERA v0.1 drafts continue to use their original progressive-save and mandatory-unit gates.

## Compatibility and privacy

- `schema_version=0.1.0` freeze logic is unchanged, including mandatory saved category prose and a nonempty semantic-unit list.
- `schema_version=0.2.0` freeze logic only requires source integrity and saved free-text explanation; optional annotations are still validated when present.
- Amendments preserve the original schema version. No silent migration from v0.1 to v0.2.
- Frozen versions retain their canonical hashes; study references are pinned to the exact historical version, independent of later amendments.
- Model-visible exports still consist of exactly `packet_type`, `sample_id`, `source_sha256` and `original_text`. **Intention, category prose, characteristics, private context, and graph annotations never enter model requests.**
- Checkboxes are a usability affordance, **not** a semantically equivalent replacement for explicit graph relationships.

## Known scope boundary

The 15-minute Review budget/uncertainty issue belongs to the separately maintained Review domain contract. This SERA schema change does not alter Review events or timing.
