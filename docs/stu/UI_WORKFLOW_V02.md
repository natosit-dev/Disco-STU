# DiScO STU UI v0.2 — Write → Explain → Run → Review

**Checkpoint:** [Before UI v0.2](../checkpoints/DISCO_STU_HUMAN_WORKFLOW_BEFORE_V02_2026-11-15.md) at `96e3d1af102b88a0541cfbf3e286e765026bcfd6`. The evidence model, historical Oracle bytes and record identifiers were not migrated.

## 1. SERA — Write / Explain

Create a **new source** with a short title and up to 200 words of original writing. Advanced provenance is optional and collapsed by default.

For a new **SERA v0.2** draft:
- Write an unrestricted explanation of what you meant. This is the authoritative human meaning record.
- Optional checkboxes record characteristics of that explanation; they are **not equivalent** to a semantic graph.
- Optional eight guided questions and optional structured semantic units/relationships remain in Advanced.
- Click **Save draft** (one deliberate authoring write). Then separately **Freeze this version** when satisfied.

The source locks after the first saved intention. The frozen Oracle is immutable, versioned, independently hash-verifiable and kept out of model requests. Its initial version retains the source writing date separately from the capture timestamp.

Old **SERA v0.1** frozen records are read-only and still available. Existing v0.1 drafts and amendments retain their original mandatory category and semantic-unit gates in the legacy editor. No auto-upgrade or rewrite is permitted.

New v0.2 studies snapshot the corresponding capture schema in their private evidence protocol alongside the transformation prompts.

## 2. Transform — Run

- Choose a frozen source and hosted model. Enter the Adaption key in the masked local session field.
- Create a study, then explicitly initiate the three-stage, potentially billable run.
- Studies are labeled **source title → actual study creation time → short UID**; run history displays real model name, actual execution time and short run UID.
- Technical study IDs, hashes, requests, response metadata and stage outcomes remain behind an expander.
- Fixture diagnostics remain available, clearly marked as synthetic.

The app formats timestamps using `STU_UI_TIMEZONE` (default `America/New_York` on this WSL-based workflow). It never changes stored UTC timestamps or invents the original writing date.

## 3. Review — two primary judgments

- Select a titled source/study, then a **specific model run**, then Neutral or Commercial.
- The primary views are **original authored text** versus **final model output**, shown as readable prose.
- The historically pinned SERA intention is accessible in an expander, not forced onto the screen before judgment.
- Begin explanation only when ready; save free-text judgment and optional discrepancy classifications.
- Contextual buttons simplify the event-preserving Begin/Pause/Resume/Complete lifecycle.
- Enable **Show optional diagnostic comparisons** to expose the remaining types. They are instrumentation, not required work.

Original UUIDs, run IDs, comparison IDs and immutable review events remain unchanged. The human review domain service (`stu/review.py`) has not been modified by this UI release.

**Known unresolved timing question:** The Review service currently treats >15-minute single intervals as uncertain; that is distinct from a cumulative 15-minute labor-budget Boolean. Radiant Control owns this domain follow-up. The UI does **not** claim to have fixed the semantics.

## 4. Results — see completion, then dig deeper

- See run count, completed neutral/commercial pairs, and **primary reviews completed**.
- See human-readable run history instead of a wall of run-stage JSON.
- Technical coverage, full decomposition vs exact model-visible projection and reconciliation of older eight-comparison studies are separate expanders.
- A full private ZIP and a redacted JSON summary are available through explicit prepare/download controls. **The two-click export remains deliberate** to avoid silently materializing private evidence while merely viewing the page.

## Preservation and compatibility checks

- No new database, model calls, automatic semantic judge or UI storage model.
- Same `StuApplication` / `SeraApplication` service boundary for Streamlit and CLI.
- Legacy v0.1 validation remains strict; v0.2 optional annotations are validated if entered.
- New v0.2 source-only model packets still contain only the four-field allowlist.
- Historical private study ZIPs are not modified; fresh exports include the correct pinned SERA contract artifact and Oracle version.
- All raw model evidence, hashes, timestamps, frozen projections, comparisons and review event journals remain available for forensic examination.

## Local workflow

```bash
conda activate disco
cd ~/code/Disco-STU
git status
git branch --show-current
git fetch origin
git pull --ff-only   # only if clean / correct feature branch
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m streamlit run app.py --server.port 8511
```

If Radiant Control is editing the Review page concurrently, coordinate through Git before pulling or overwriting local edits. This redesign intentionally touched `pages/3_STU_Review.py` but **not** the review timing/domain state machine.
