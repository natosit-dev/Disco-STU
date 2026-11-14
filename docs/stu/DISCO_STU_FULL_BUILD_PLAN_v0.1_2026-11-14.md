# DiScO STU — Full Deterministic Build Plan v0.1

**Experiment 01:** From Meaning to Management  
**Date:** 2026-11-14  
**Repository:** natosit-dev/Disco-STU  
**Status:** APPROVAL HANDOFF — documentation committed; implementation NOT authorized until Nat explicitly gives the OK.  
**Implementation branch:** to be created after authorization; do not implement directly on main.

## 0. Executive decision

Build a complete, local, offline, evidence-preserving semantic transformation laboratory around the existing SERA baseline. A deterministic fixture adapter stands in for an LLM across every stage. When actual local or API models are added later, the adapter changes; the study workflow, data contracts, Review process, CLI and UI do not.

**Nonnegotiable architecture rule: Streamlit must be a deliberately stupid thin client.** Streamlit renders view models and forwards explicit user commands to a Python application-service layer. It must not own domain logic, experiment execution, persistence, semantic adjudication, duration accounting, or source-of-truth state. Both the UI and CLI call the same service methods.

The complete offline program must demonstrate: original source → human Oracle (held out) → source-only packet → deterministic decomposition → frozen intermediate → neutral and commercial reconstructions of the SAME intermediate → comparable artifacts → human review and active explanation time → analysis and export.

These demonstrations are **software tests, not research results**. A simulated distortion is not evidence that an actual LLM distorted meaning.

## 1. Source of authority and baseline

The current repository provides SERA v0.1: Streamlit capture; progressive free intention, category prose, semantic units and directed relationships; local drafts; immutable frozen Oracle versions; JSONL events; source-only export; and backend/schema tests. Maintain compatibility with its existing schemas and saved data.

Start by recording the GitHub HEAD and running existing tests before any code changes. Verify rather than assuming the README or handoff's stated counts are current.

Relevant existing documents, to be retained rather than rewritten:
- docs/sera/BUILD_PLAN_v0.1.md
- docs/sera/DATA_CONTRACT.md
- docs/handoff/NERD_HANDOFF_STU_COMPLETE_PIPELINE_v0.1_2026-11-14.md
- docs/stu/DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12_BASELINE.md
- docs/stu/DiScO_STU_From_Meaning_to_Management_v0.4_REVIEW_SERA_ADDENDUM_2026-11-13.md
- schemas/semantic_v0.1.json

This plan is the approved *candidate* for the deterministic build. Historical research documents remain provenance, not executable claims. Record any later decision changes in a separate append-only decision log or a new document version.

### Reuse inventory and license boundary

| Source | Candidate reuse | Boundary |
|---|---|---|
| Disco-STU / sera | SERA domain validation, source hashes, progressive capture, freeze/amend/export | Retain and extend with versioned contracts |
| natosit-dev/smrt | Run manifest, evidence-event, artifact-verification and comparison patterns | Inspect and adapt concepts; smrt is GPL-2.0; do not copy into PolyForm code without resolving license compatibility |
| natosit-dev/DiScO | Deterministic feature inventory, source spans, feedback/inspection patterns | Optional *descriptive* enrichment only; DiScO is GPL-2.0; do not import copyrighted GPL code into the PolyForm project without a license decision |
| natosit-dev/slop-in1 | Source- and repo-inspection practices, negative tests, evidence separation | Concepts only pending compatibility review |
| natosit-dev/doc_history | Document metadata/provenance extraction | MIT; optionally integrate through a separate package later; no document-upload requirement in this build |
| natosit-dev/piqitt_dev | Evaluator/test-case and regression-comparison patterns | Reuse evaluation design, not clinical code |
| natosit-dev/medilacra_fhir_engine | Existing Kiln/Ollama/OpenAI-compatible client patterns and local Qwen precedent | Future provider integration; older fallback/error suppression must NOT be replicated in experimental adapters |
| Comrade AI (previous private/local work) | Mistral-7B-v0.3 LoRA training, adapter metadata, dataset preparation (referenced in earlier evidence register) | Original files not verified in accessible GitHub repositories; do not claim or incorporate a reusable transport. Revisit when originals are available |

Preserve attribution and license notices for any reused code. **Prefer small clean implementations over dependency tangles or copying incompatible source.**

## 2. Research boundaries

The instrument addresses three distinguishable questions:
1. **Semantic survival:** How does the author's present, independently recorded intention relate to the original writing, model decomposition, and reconstruction?
2. **Institutional treatment:** Does reconstruction as commercial management advice alter meaning relative to neutral reconstruction from one identical frozen decomposition?
3. **Human explanatory labor:** How much active time does the author spend formulating and recording an explanation of the gap between intended and transformed meaning?

Human intention is a present retrospective account, not directly observed historical thought. Absence of an intention from the written source is **not automatically an LLM failure**. A management recommendation consistent with the represented meaning is **not automatically an error**.

Prohibited inference shortcuts:
- Coherence is not accuracy.
- Similarity is not semantic equivalence or evidence of lineage.
- An output does not become authorized simply because it appears in a register or report.
- Hash consistency is local integrity checking, not adversarial attestation.
- A successful synthetic fixture is not evidence of actual model performance.
- Empty, failed or incomplete review is not a "no gap" judgment.

### Out of scope for this build

No actual local/API LLM requests; no model training; no embeddings or vector DB; no speech/transcription; no autonomous agents; no SHN internal data; no document upload or doc_history enrichment; no universal semantic score; no automatic managerial actions; no LLM-generated Oracle; no hosted database; no general workflow/orchestration platform.

The adapter *contract* must support future real models, but transport implementations belong to a separate authorized integration phase.

## 3. Architecture: dumb Streamlit, shared Python application API

All dependencies point inward:

~~~text
Streamlit pages -------+
                       +--> stu.application / sera.application facade
CLI -------------------+           |
                                   +--> domain services
                                   |      SERA capture/freeze
                                   |      study management
                                   |      execution/orchestration
                                   |      comparison preparation
                                   |      human review/timing
                                   |      analysis/export
                                   |
                                   +--> persistence + event journals
                                   |
                                   +--> ModelAdapter interface
                                            |
                                     DeterministicFixtureAdapter (now)
                                     Real provider adapters (later)
~~~

### Mandatory UI constraints

1. **UI pages contain presentation code only:** render fields, display status/view models, collect inputs, invoke one explicit application-service command, render returned result or error.
2. **No orchestration in pages:** no sample→decompose→reconstruct loops, prompt construction, model invocation, schema business rules, semantic matching, artifact comparison, report aggregation or export assembly.
3. **No persistence in pages:** pages do not open/write files, assemble JSONL, generate canonical hashes, or access stores directly.
4. **No authoritative timer in pages:** Review timing is backend event-derived; Streamlit may display a duration, but browser state or session_state is never the ledger.
5. **No durable state in session_state:** only navigation, selected IDs and unsubmitted widget values. Persistent workflow state comes from the backend after every action.
6. **No mutation on rerun:** no calls to save/run/freeze/complete on ordinary Streamlit re-render. Mutations require deliberate commands.
7. **No model/Oracle leakage:** UI uses purpose-specific view models. Transform views cannot ask for private Oracle fields. Review service explicitly authorizes the pinned Oracle reference.
8. **Idempotent commands:** duplicate clicks/retries either return the established result or fail cleanly without creating duplicate effects.
9. **Same workflow without Streamlit:** CLI and tests exercise exactly the same application services and contracts. No separate CLI implementation of logic.
10. **No HTTP backend required:** the facade is an in-process Python API to keep the first local single-user deployment simple.

The existing SERA page currently calls storage/service modules directly. Refactor it *conservatively* to call a dedicated thin SERA application facade while retaining all capture/freeze/amend semantics and historic records.

Example command/query contract (illustrative names; implement the smallest coherent version):

~~~python
capture = SeraApplication(data_root)
stu = StuApplication(data_root, adapter_registry)

capture.create_sample(source_payload)
capture.save_intention(sample_id, text)
capture.save_categories(sample_id, category_prose)
capture.save_units(sample_id, rows)
capture.save_relations(sample_id, rows)
capture.freeze(sample_id, expected_version)
capture.begin_amendment(sample_id)

stu.create_study(study_config)
stu.get_study(study_id)                 # UI view model; no private Oracle
stu.run_sample(study_id, sample_id, adapter="fixture", mode="synthetic")
stu.list_comparisons(study_id)
stu.get_comparison(comparison_id, review_role=True)
stu.begin_gap_explanation(comparison_id)
stu.pause_gap_explanation(comparison_id)
stu.resume_gap_explanation(comparison_id)
stu.save_gap_explanation(comparison_id, draft)
stu.complete_gap_explanation(comparison_id, outcome)
stu.get_results(study_id)
stu.export_study(study_id, privacy_level="safe")
~~~

All mutation validation and authorization of private/reviewer views occurs in the application/domain layer, not in button handlers.

## 4. SERA preservation and version-pin additions

Keep the existing source-only packet exactly at these four allowlisted fields: packet_type, sample_id, source_sha256, original_text. Build this allowlist explicitly, never by deleting Oracle fields from a copied full record.

Freeze the author's separately entered layers: (1) unrestricted intended meaning, (2) eight category prose explanations, (3) semantic units and directed relationships. Empty individual categories are legitimate. Preserve exact input text and SHA-256 without normalization.

Extend the storage read API to **retrieve a specific frozen Oracle artifact by exact version, explication ID and hash**, not just latest_frozen(). A scored/pilot comparison must pin that artifact. Later amendments create another version without changing the historical run's review reference.

Preserve SERA's source-lock rule after free intention is saved, draft/freeze event history and existing relative storage paths. Validate stored relationships and unknown references before freeze.

New source-span evidence in downstream STU records should carry character offsets and a check against the exact source text when possible; keep legacy human source_support text fields compatible.

A source packet can be sent to STU only after the corresponding Oracle freeze is durably confirmed. The STUDY metadata reference to Oracle is reviewer-only; the *execution* configuration must not contain its content.

## 5. Model adapter contract and deterministic substitute

Create a small transport-neutral interface with explicit model request and response structures:

~~~python
class ModelAdapter(Protocol):
    def generate(self, request: GenerationRequest) -> GenerationResult: ...
~~~

GenerationRequest contains exact system/user messages, stage, condition, model profile, parameters, request identity and expected response format; no private Oracle or human annotations.

GenerationResult contains exact raw text, actual adapter/model identity, provider metadata when available, optional token usage, timestamps, finish reason, and completion/failure status. Stage orchestration is never implemented inside an adapter.

### DeterministicFixtureAdapter

- No network, no credentials, no local model dependencies.
- Versioned known fixtures select exact outputs using fixture ID + stage + condition + explicit fixture version.
- Exact same fixture request produces byte-identical *semantic output*; unique run IDs and timestamps remain distinct execution metadata.
- Responses are plainly marked synthetic in both persisted artifacts and UI.
- Unknown fixture inputs must **fail explicitly** or use an expressly marked *structural smoke* placeholder that makes no semantic claims.
- No general heuristic interpretation of unknown text pretending to be an LLM.
- Simulate declared failures as well as successes; do not repair malformed JSON invisibly.
- Record actual serialized requests for verifying forbidden fields and context isolation.
- Never silently fall back to another adapter.

Fixture cases:
- F01 faithful decomposition and both reconstructions.
- F02 source→decomposition loss of a necessary condition.
- F03 decomposition→neutral omission of a qualifier.
- F04 commercial advice introduces an unsupported organizational objective.
- F05 negation, actor, scope or dependency distortion.
- F06 legitimate, source-consistent commercial extension.
- F07 invalid JSON, timeout/unavailable, or interrupted attempt.
- F08 incomplete reconstruction pair (one branch fails).
- F09 deliberate Oracle/source disagreement: intention not established by original writing.
- F10 a completed human "no meaningful gap" case and an incomplete/unsubmitted review case.

For every fixture, declare the input source, expected intermediate, expected outputs, designed change, and assertions *before* running tests. Fixture "expected error" labels are synthetic oracle values for testing code, not research verdicts.

### Future adapters, not part of current implementation

Prepare configuration/adapter boundaries for local Ollama or OpenAI-compatible inference and an OpenAI API. Once separately authorized, add actual model adapters with exact model IDs, quantization/runtime, sampling configuration, request bodies, provider IDs, response metadata and retry policies. Missing models or keys fail visibly; never silently switch model or transport. Zero temperature alone does not guarantee repeatable real-model outputs.

## 6. STU execution and scientific controls

### Stage A — Decomposition

Input: the four-field source-only packet plus a versioned decomposition prompt/schema. Output: model-generated category_prose, semantic units and directed relationships, conforming where possible to the shared schema. Model-generated local unit IDs are not assumed equal to SERA's IDs.

Record the complete raw response, parsed form or parsing failure, source-support fields, prompt/schema hashes, settings, requested and actual model identity, input/output hashes, start/end times, retry linkage, and status.

An invalid or unrepresentable output is data. Do not drop it and rerun until a good output appears.

### Stage B — Neutral reconstruction

Input: one frozen decomposition **only**, plus neutral prompt and necessary model settings. New independent request context. Preserve represented claims, negations, qualifications, dependencies, rhetorical role and ambiguities. No added recommendations.

### Stage C — Commercial-management reconstruction

Input: the **identical frozen decomposition artifact/hash**, plus commercial prompt and necessary model settings. New independent context. Produce actionable advice to management of a for-profit business selling a commercial product in a competitive market. Respect claims, criticisms and limits. Do not invent product/company facts. If advice would require changing meaning, state the limitation.

### Hard execution invariants

- Decompose once per sample/model/attempt; reconstruct twice from the *same* frozen intermediate.
- Never substitute a second decomposition to complete a failed pair.
- Neither reconstruction sees original text, Oracle, private metadata, or sibling output.
- Confirm invariants by examining **serialized outgoing adapter requests**, not merely Python data structures.
- Each branch is a distinct run/attempt with exact parent artifact identity.
- If a branch fails, keep the incomplete pair and record why. Retrying is a distinct attempt with lineage.
- Version prompt text, schema and request-construction code; freeze hashes before later scored experiments.

## 7. Study lifecycle and privacy

Three mutually explicit modes:

- **synthetic_test:** deterministic fixtures only; may run automatically. No empirical claims.
- **pilot:** adjustable protocol development, with versioned configurations and explicit labeling; not scored evidence.
- **scored:** disabled/unsupported while only the fake adapter exists. Later requires real model integration, approved corpus and a frozen manifest with a deliberate execution command.

The study manifest pins source hashes, exact Oracle reference versions/hashes *in reviewer-only metadata*, adapter profiles, prompt/schema hashes, comparison rubric, review-order seed, timing protocol, implementation commit and experiment mode.

A frozen scored manifest must never silently change; amendments are new versions. Privacy classes distinguish synthetic, private Oracle, original writing, raw model payload and publication-cleared artifacts.

Never commit runtime data, original private passages, Oracle content, model payloads, or API keys. Keep data/ and secrets gitignored. Default exported bundles omit private content and require explicit item-level publication selection for real research.

## 8. Persistence and lineage

Retain eight logical entities, which may be nested JSON rather than tables:
1. samples — one original paragraph;
2. explications — one human account or model decomposition, with distinct epistemic role;
3. semantic_units — one identified claim/actor/negation/etc.;
4. runs — one attempted execution stage;
5. artifacts — one immutable produced object with content hash;
6. comparisons — one reference↔target evaluation task;
7. gap_explanations — one human description of a difference;
8. review_events — one persisted review/timing event.

Use JSON for complete artifacts, JSONL for append-only events and plain CSV/JSON derived analysis. No SQL server or DuckDB dependency required initially. Keep SERA existing paths stable.

Suggested extension:

~~~text
data/
  private/sera/<sample_id>/{draft.json,oracle-vN.json,events.jsonl}
  stu_inputs/<sample_id>.json
  studies/<study_id>/{manifest.json,events.jsonl}
  runs/<run_id>/{run.json,request.json,raw_response.txt,parsed_output.json,events.jsonl}
  comparisons/<comparison_id>.json
  reviews/<comparison_id>/{explanations.json,events.jsonl}
  exports/
~~~

Store actual request bytes or exact canonical serialization and reference hash, with sensitive credentials excluded. No silent data truncation. Event journals record order and attempts. Artifacts use write-once paths or content addressing. Check local hashes and referenced parents upon loading. Fail closed if stored evidence is corrupted or incomplete.

Distinguish run statuses: prepared, running, completed, failed, cancelled and incomplete; separate parse/validation outcome from transport completion. A successful transport can return invalid JSON. An output's existence is not an acceptance judgment.

## 9. Comparison and human Review

Generate seven typed comparison views, retaining exact immutable references:
1. Oracle ↔ original paragraph (human expression boundary).
2. Original paragraph ↔ model decomposition.
3. Oracle ↔ model decomposition (intention vs inference).
4. Model decomposition ↔ neutral reconstruction.
5. Model decomposition ↔ commercial reconstruction.
6. Neutral ↔ commercial outputs (same intermediate; primary paired treatment contrast).
7. Oracle ↔ each final output (end-to-end intention survival).

Do not pool these into one undifferentiated meaning score. Source-to-Oracle gaps and model losses are separate phenomena.

The reviewer sees reference and target artifacts, evidence spans, and exact pinned private Oracle only when appropriate. Mask model identifiers during adjudication where practical and use a fixed stored shuffle seed; commercial language itself may reveal condition, so do not assert perfect blinding.

Primary review artifact: **unrestricted human written explanation** of the gap between what the author meant and what the model represented or reconstructed.

Optional per-gap labels: preserved, omitted, altered, contradicted, unsupported_addition, source_consistent_extension, unresolved_ambiguous. Include references and explanatory rationale for material judgments.

Review lifecycle includes not_started, inspecting, explaining, paused, completed, amended and invalidated. Completed/no-meaningful-gap is an explicit outcome; an empty text field is not proof of no gap. Preserve amendments and prior exposures.

### Timed semantic reconstruction cost

Measure time spent *formulating/recording an explanation*, not latency to notice something is wrong. Default pilot protocol:
1. Untimed side-by-side inspection.
2. Deliberate "Begin gap explanation" command.
3. Persist begin/pause/resume/save/complete events.
4. Backend derives active intervals from persisted events.
5. Browser reruns/reloads cannot reset or inflate the authoritative timer; interrupted sessions are flagged for reviewer resolution.
6. Record explanation text, word count, interruptions, elapsed/active seconds, timing-protocol version and review order.
7. Explicit no-gap completion does not fabricate explanatory text or imply zero overall cognitive work.

Inject a clock into domain tests. Use persisted UTC events and explicit uncertainty flags for recovery; do not substitute a JavaScript ticker or in-memory Streamlit timer for evidence. A fast but incomplete explanation must not be interpreted as lower reconstruction cost.

## 10. Analysis, exports and reported limits

The first results interface is intentionally simple: a coverage matrix, per-run stage status, lineage trace, manual gap-category table, paired neutral-versus-commercial comparison, active explanatory time with protocol metadata, failure list and CSV/JSON export.

Keep expected fixture classifications separate from human judgments and empirically observed model behavior. A negative or mixed result is legitimate. Retain incomplete samples, retries, failed branches, absent reviews and review-order exposure effects.

Produce:
- study coverage and failed/missing-stage report;
- lineage table: sample → decomposition → branches → comparisons → review events;
- exact source and response artifact access by ID/hash where user is permitted;
- paired-treatment differences only where the same frozen intermediate is verified;
- human gap explanation inventory and active-time measurements;
- synthetic fixture expected-vs-observed verification report;
- private-safe default export, and explicit approved export path later.

No model-generated scientific conclusion, no universal AI quality ranking, and no invented statistics.

## 11. Frontend and CLI scope

Streamlit pages:
- **SERA / Capture:** existing sequence, migrated to facade commands; no domain logic on page.
- **STU / Transform:** select study/sample, view fixture/profile readiness, explicitly launch a synthetic run, inspect step statuses and artifact IDs.
- **Review / Explain:** view typed comparisons, write unrestricted explanation, invoke backend begin/pause/resume/save/complete; show backend-derived active duration and provenance.
- **Results / Export:** read coverage/lineage/analysis view model and invoke export service.

UI page code must not import persistence, adapter implementations or orchestrator modules. Test this boundary with module-level checks or controlled fixture-driven UI tests where feasible. All data-changing actions are button/form-triggered and idempotency-safe.

CLI commands (final spellings can be adjusted once and documented):
- python -m stu.cli doctor
- python -m stu.cli smoke --adapter fixture
- python -m stu.cli run --study <id> --adapter fixture --mode synthetic_test
- python -m stu.cli validate --study <id>
- python -m stu.cli analyze --study <id>
- python -m stu.cli export --study <id> --privacy safe

**No bespoke business logic inside CLI handlers either.** CLI parses arguments, invokes the same application facade, serializes the returned view model and sets a meaningful exit code.

## 12. Implementation layout (suggested, not prescriptive)

~~~text
app.py
pages/
  1_SERA.py
  2_STU_Transform.py
  3_STU_Review.py
  4_STU_Results.py
sera/
  ...existing...
  application.py                   # new thin facade for capture
stu/
  application.py                   # sole UI/CLI app entrypoint
  contracts.py
  adapters/{base,fake}.py
  fixtures.py
  prompts.py
  study.py
  runner.py
  artifacts.py
  comparisons.py
  review.py
  analysis.py
  cli.py
schemas/
  semantic_v0.1.json               # existing
  stu_run_v0.1.json
  stu_review_v0.1.json
prompts/
  decompose_v0.1.txt
  neutral_v0.1.txt
  commercial_v0.1.txt
fixtures/synthetic/
config/study.example.json
tests/
  ...existing...
  test_application_boundary.py
  test_fixture_adapter.py
  test_model_isolation.py
  test_runner.py
  test_artifacts.py
  test_review.py
  test_analysis.py
  test_synthetic_e2e.py
docs/stu/
  ...historical documents...
  DISCO_STU_FULL_BUILD_PLAN_v0.1_2026-11-14.md
docs/WORK_LOG.md
data/                               # gitignored
~~~

Do not create modules solely to conform to this list. Consolidate where responsibilities remain clean and tests are easier. Do not collapse orchestration into Streamlit or an oversized "everything" service.

## 13. Build work packages and hard gates

**A. Baseline / reuse / provenance**
- Record current HEAD, run all preexisting SERA tests, inspect outstanding work and licenses.
- Decide import vs clean adaptation module by module; record provenance.
- Establish docs/WORK_LOG.md and record test commands/results.
- Gate: existing behavior preserved; no undocumented write to user data.

**B. Thin application boundary + SERA pinning**
- Add SERA facade, migrate existing page to thin calls, preserve all stage gates.
- Add exact-version/ID/hash Oracle read and historical compatibility tests.
- Gate: CLI/tests and UI observe identical SERA state; rerenders do not mutate it.

**C. Adapter, contracts and fixture registry**
- Build deterministic fake adapter, immutable fixture definitions, typed response and error handling, request serialization capture, versioned prompts/schema.
- Gate: byte-identical expected fixture response on replay; unknown inputs fail or explicitly marked structural smoke; Oracle secrets absent from request bytes.

**D. Full STU orchestration and artifact store**
- Implement studies, execution attempts, decomposition, frozen intermediate, both fresh reconstruction branches, independent failures, manifests, event logs and validation.
- Gate: full deterministic CLI run generates complete inspectable chain and verifies paired intermediate hash, including incomplete-pair negative case.

**E. Comparison and timed Review domain**
- Implement seven typed comparison definitions, precise reference targets, human explanation lifecycle, persistent review events, pause/resume/recovery, explicit no-gap, pinned Oracle.
- Gate: all timer and review transitions can be exercised from backend tests without a UI; no hidden AI adjudication.

**F. Thin Streamlit integration / analysis / export**
- Add Transform, Review, Results UI views as application-service consumers; common CLI facade; coverage, lineage and safe exports.
- Gate: end-to-end synthetic UI walkthrough, independent CLI run and results agree on the same evidence.

**G. Regression, negative cases, documentation and handoff**
- Run all unit/integration/contract/negative tests, storage-integrity checks, privacy checks and actual browser smoke where environment permits.
- Deliver changed-file inventory, commit/branch link, work log, exact observed test outputs, known limitations and staged human acceptance instructions.
- Gate: no unverified runtime/UI claim is labeled passing, and no synthetic result appears as empirical research.

Do not stop at "backend passes" if pages are unfinished. Conversely, a pretty Streamlit demo does not complete a build without independent backend verification.

## 14. Mandatory acceptance tests

1. Baseline SERA round-trip remains intact; exact source text/hash preserved.
2. Frozen Oracle remains private; serialized adapter request contains only source packet plus explicit prompt/metadata and no human annotation markers.
3. Oracle read by exact immutable version works; later amendments do not change historic comparisons.
4. All SERA and STU persistent operations survive restart; UI rerun performs no writes.
5. Deterministic fixtures replay identically; unique execution metadata remains distinguishable.
6. Unknown fixture request fails visibly, never invents semantic knowledge.
7. Two reconstruction branches use the exact same intermediate artifact hash and fresh independent contexts.
8. Actual serialized reconstruction requests exclude original source, private Oracle and sibling output.
9. Invalid JSON retained; retry is a new recorded attempt; one failed branch stays a failed/incomplete pair.
10. Missing/duplicate IDs and broken relations fail validation; source span citations are checked where specified.
11. Event/artifact tampering or missing journals produces a visible integrity error.
12. Explicit no-gap, unfinished review, amended explanation and invalidated review are distinct.
13. Pause/resume/reload/double-click/interruption yield correct or explicitly uncertain event-derived durations.
14. Review ordering is repeatable; prior exposure is retained.
15. Synthetic fixture labels cannot enter scored/real-results analysis.
16. Safe export excludes private/source data unless separately authorized.
17. CLI end-to-end run and Streamlit UI invoke the **same** backend APIs and produce compatible lineage/evidence.
18. Backend tests run without importing Streamlit; UI code never carries orchestration/timing/analysis implementations.
19. Browser smoke exercises Capture, Transform, Review and Results with observed checkpoints, or explicitly documents any unverified step.
20. No production PHI, SHN proprietary material, API secrets or Comrade AI personal training data are used as test fixtures.

## 15. Default decisions for this build

These defaults reflect the reviewed plan and remain configurable for a later *scored* study; none requires the user to supply real corpus or credentials now.

- Proposed future first scored corpus: **six** author-selected paragraphs, no pretense that they have been collected yet.
- Source paragraph limit: existing SERA hard maximum **200 words**.
- Experimental intervention: **commercial management advice for a for-profit company selling a product in a competitive market**, versus neutral prose from the same frozen intermediate.
- Timing: untimed comparison inspection; explicit begin to measure written gap explication; pause/resume supported.
- Review: all seven comparison types supported; prioritize primary pair for required scored review rather than forcing completion of every comparison by default.
- Storage: JSON and JSONL first, simple CSV/JSON analysis; no DuckDB until demonstrably useful.
- Adapters: deterministic fixture only for first build; local Gemma, quantized Qwen, OpenAI API and Comrade AI deferred.
- Git: implementation on a new feature branch after authorization; no blind changes to main.
- No assumptions of an available local Ollama endpoint, exact model tags, API credentials or source corpus.

Any research-design change after seeing actual model output requires a new versioned manifest, not a silent in-place edit.

## 16. What "done" means

The completed first build has a local single-user application and CLI capable of running the whole deterministic experiment, retaining exact source/model-simulation artifacts, comparing both reconstruction branches, allowing a human to explain a gap with persisted active-time tracking, and exporting inspectable, provenance-linked results.

Every observed capability is backed by a test or explicitly described manual walkthrough. The report distinguishes implemented/verified behavior, documented intention, unavailable external model integrations, and not-yet-performed real experiments.

**The plan commit itself is not authorization to build. Await Nat's explicit OK.**
