# SERA — Build Plan v0.1

**Semantic Explication Recorded Analytics** · DiScO STU, Experiment 01 (*From Meaning to Management*)  
**Status:** Implementation contract, adopted 2026-11-14. This plan is not evidence of an implementation.

## Purpose and boundary

SERA records a human author's **present, retrospective explication of intended meaning** *before* any model sees a source passage. It generates two separate outputs: a **private, frozen Oracle record** and a **minimal model-visible source packet**. The latter must not contain intended meaning, claims, relations, annotations, or private context.

SERA does not generate meaning, judge the author, conduct STU model experiments, or time the later task of explaining a human–model gap. The timed gap explication belongs to STU's separate Review stage.

## Workflow — progressive explication (approved)

1. **Capture source.** Paste exactly one contiguous paragraph (target 75–150 words, hard maximum 200), title/provenance, domain, and optional context dependencies. Preserve exact source bytes as UTF-8 text without rewriting whitespace or truncating. Validate before freeze.
2. **Free intention first.** Ask: **“What did you intend to communicate?”** Save this unrestricted account before opening the next stage. No AI suggestions.
3. **Category prose second.** Ask independent free-text questions for claims, actors/objects, relationships, negations, conditions/scope, dependencies, rhetorical function, and ambiguity. Empty categories are legitimate. Save explicitly.
4. **Structure third.** Create semantic units (stable local IDs, type, text, importance, polarity, optional notes/source support) and directed relations (stable IDs, source/target unit IDs, type, explanation). Do not require a unit in every category. Provide a custom relation type and explanation when the vocabulary fails.
5. **Review and freeze.** Show the original paragraph, unrestricted intention, category prose, semantic units/edges, and provenance. Validate IDs and references, then require a distinct explicit confirmation. Save an immutable version with checksums and append a freeze event.
6. **Export.** Export one complete private Oracle artifact for later blinded evaluation, and a separately constructed source-only packet for STU's model runner. A frozen packet can be amended only by creating another version, never rewriting its original.

The free intention → category prose → structured network steps are **three representational boundaries**. Preserve each one; do not silently synthesize the category or structured layers from the preceding text.

## Data contract

Common metadata: `schema_version`, `sample_id`, `explication_id`, `producer=human`, `epistemic_role=declared_authorial_intention`, `created_at`, `updated_at`, `frozen_at`, `parent_version_id`, and artifact fingerprint.

Original sample fields: `original_text`, `source_sha256`, `word_count`, `title`, `origin`, `date`, `domain`, `context_dependencies`.

Reference fields: `intention_free_text`, `category_prose` (eight optional keys), `units`, and `relations`. Unit IDs are local to an explication; model-generated IDs will **not** be assumed to correspond. Preserve optional source support even if an intended relationship is not expressed in the paragraph.

Keep free text, category prose, and structured units separately observable. All serialized artifacts use canonical JSON encoding and SHA-256 for identity/integrity; raw history uses JSONL.

## Local persistence

```text
data/                         # excluded from git
  private/sera/<sample-id>/
    draft.json                # replaces atomically, not canonical evidence
    events.jsonl              # append-only save / freeze / amend history
    oracle-v1.json            # immutable once frozen
    oracle-v2.json            # later amendment, if any
  stu_inputs/<sample-id>.json # allowlisted model-visible source packet only
```

SERA is a single-user local baseline. No hosted database, concurrency guarantees, or encryption at rest is implied. Document uploads, LLM integrations, DuckDB, graph visualization, and a separate timer are deferred.

## Implementation layout

```text
app.py
pages/1_SERA.py
sera/{__init__,schema,storage,service,exports}.py
schemas/semantic_v0.1.json
tests/
docs/sera/
requirements.txt
```

The Streamlit page is a thin interface to independently testable Python domain functions. It must never mutate persistent records just because Streamlit reruns.

## Implementation order and gates

- **A. Schema:** declare typed units, directed relations, category fields, source metadata, sample/explication IDs; validate missing references and duplicates.
- **B. Storage:** implement local event journal, atomic draft saving, frozen version files, SHA-256, robust reload/restart behavior.
- **C. UI capture:** source input and free intention, explicit save/open controls.
- **D. Progressive editor:** category-level prose before editable semantic units and relationships; stable IDs; optional categories.
- **E. Freeze/export:** inspect all layers; deliberate confirmation; private artifact and source-only packet.
- **F. Pilot:** one real, legally publishable paragraph end-to-end. No model work is required to certify SERA's completion.

## Required verification

- Round-trip source, free text, category prose, units, edges, and provenance with no silent edits.
- Preserve IDs and records across Streamlit reruns/restarts.
- Reject invalid references and duplicate IDs before freeze.
- Preserve original frozen versions after amendments.
- Never write Oracle fields to STU exports; construct the allowed packet from an allowlist (not `pop()` on a full Oracle object).
- Do not leak raw source/Oracle data through Git: ignore `data/`.
- Verify checksums and surface corrupted/incomplete records.
- Do not claim durable freeze if event recording or artifact writing failed.
- The page remains usable with only local Streamlit and Python dependencies.

## Definition of done

A user can paste a paragraph, explain intention freely, explain each applicable category in prose, enter explicit units and directed relationships, inspect the complete record, freeze it once, reopen it unchanged, and export separate private Oracle and model-visible source records. Automated tests cover integrity, basic failure modes, and field isolation.

**What SERA records:** the meaning I say I intended.  
**What STU records:** what the models inferred and reconstructed.  
**What Review measures:** the actual human labor of explaining the gap.

## Provenance

Derived from the DiScO STU v0.5 Nat-style project plan and the in-chat SERA implementation discussion. **Progressive explication** was explicitly selected by Nat on 2026-11-14: *“Use progressive explication for SERA: free intention, category-level prose, then structured semantic units and relationships.”* The earlier research planning versions remain archived; this implementation document does not rewrite their history.
