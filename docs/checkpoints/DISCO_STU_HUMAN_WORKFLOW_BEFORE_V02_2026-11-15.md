# DiScO STU — Human Workflow UI Checkpoint
**Recorded:** 2026-11-15  
**Branch:** `feature/stu-deterministic-pipeline-20261114`  
**Baseline commit:** `09eeb47920c285a57bb38168c424c2c0ca7996bf`  
**Status:** implementation checkpoint **before** UI redesign; main untouched; draft PR #1 open.

## Baseline that must survive

- 59 tests passed on previous engineering head; full mock live inference and deterministic smoke covered.
- Existing SERA v0.1: original/source, free intended meaning, eight category fields, mandatory structured units, optional relationships; frozen `oracle-vN.json` artifacts and source-only packets are private/versioned/hash-checked.
- Existing STU: three fresh Adaption model calls with full decomposition and projection bytes, immutable run artifacts/metadata, 10 comparison types, and explicit original-to-final archival reconciliation.
- Existing human-review events, elapsed time, comparisons, UUIDs, timestamps, ZIP exports, experiment prompts and model-visible projections are evidence. **Do not rewrite, silently migrate or delete**.
- Repo remains Ubuntu WSL + Conda `disco`, `~/code/Disco-STU`, `python -m pytest -q`, Streamlit port 8511. Runtime `data/` stays local and uncommitted.
- Prior coordination: Radiant Control owns the human-review timer/domain state machine. Avoid changing `stu/review.py` and existing event semantics; review presentation can be replaced with care, checking the branch HEAD first.

## Human-centered design request

The author's essential workflow is **Write → Explain → Run → Review**.
The original human-meaning explanation is the authoritative reference. Eight categories and units/relations must not remain mandatory clerical tasks for all new records.

### Release A — UI v0.2

- Human-readable source/study/run labels using real timestamps in a configured local timezone; internal IDs remain available for provenance.
- Default Review to **original → neutral** and **original → commercial** for each model run; the historical frozen Oracle becomes a disclosed reference. Other comparison types are optional diagnostics, not expected labor.
- Format source and model output as readable prose, not raw JSON; model/run grouping and clear review statuses.
- Simpler visible review actions and free-text-first judgment, while preserving the review event service.
- Plain-language Results summary and clear export/download; hide reconciliation and raw diagnostic structures under maintenance.
- Slim Transform details; preserve shared Python service boundary. No new database.

### Release B — SERA capture v0.2

- A **new explicit schema version** for new records, with required unrestricted authorial explanation and optional characteristics; category prose, semantic units and relationships become optional annotations.
- One deliberate Save draft + separate explicit Freeze; title and text first, provenance collapsed.
- Legacy v0.1 drafts/freezes and historical private ZIPs retain exact prior semantics and hash IDs. Do not retroactively relabel v1 records as v2.
- Characteristics are helpful flags only, **not** equivalent to full graphs and not model inputs.
- Versioned schema/validation rules + tests; freeze not silently forced through v1 gates.

## Scientific/engineering constraints

- UI labels are presentation-only, derived from existing source/study/run records; no ID replacements.
- No automatically inferred semantic correctness. Human review primary task selection is a *UI workflow choice*, not a rewrite of evidence contracts.
- No automatic review-time budget distortion: the 15-minute uncertainty/threshold issue is tracked separately for Radiant Control. Do not pretend a nicer interface repairs it.
- Every release requires passing existing tests, new UI/schema tests, evidence-preservation checks and CI before acceptance.
