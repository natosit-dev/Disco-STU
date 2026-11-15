# DiScO STU — Deterministic Build · Complete handoff for Radiant Control

**Source DOCX:** `Disco_STU_Deterministic_Build_Full_Handoff_Radiant_Control_2026-11-14.docx`  
**Original DOCX SHA-256:** `5c23436d195566906250b4e32fd13645755f659780efd9c1f40d58ee903fd9ae`  
**Provenance:** Complete textual transcription of the source DOCX into Markdown, retaining document order, raw-prompt blocks, tables, and linked URLs where present. Markdown is not a byte-identical copy of the Word file or its visual layout.

---

TECHNICAL IMPLEMENTATION RECORD

DiScO STU
Deterministic Build

Complete handoff for Radiant Control

Experiment 01  |  From Meaning to Management

| BUILD RECORD | CURRENT STATE |
| --- | --- |
| Date | 14 November 2026 |
| Implementation | deterministic-fixture-v0.1; offline synthetic laboratory |
| Feature branch | feature/stu-deterministic-pipeline-20261114 |
| Implementation commit | 98f50367c6458f840c5fd1cf0b1ba3b22ed6c7d6 |
| Pull request | Draft PR #1; open, not merged |
| Automated verification | 25 tests passed; CLI smoke and negative scenarios passed |
| Open gate | Full interactive browser acceptance; real model integration |

Prepared as a factual account of the code, artifacts, verification evidence, decisions and remaining engineering risks. It distinguishes implemented behavior from specifications and synthetic observations from empirical model results.

Source of record: [GitHub draft pull request #1](https://github.com/natosit-dev/Disco-STU/pull/1)

Scope note: The full source code is in the linked commit and PR; this document records the implementation and a file-by-file inventory rather than reproducing thousands of lines of source.

## At a glance

The initial SERA capture/freeze prototype has been extended into an offline experiment harness that can run a synthetic decomposition, retain the resulting structured artifact, generate two controlled reconstructions, prepare human comparisons, measure explicitly recorded explanation time, and export a privacy-safe study summary. The implementation is designed for later adapter substitution; it does not run an LLM today.

| STATUS | OBSERVED EVIDENCE / LIMIT |
| --- | --- |
| Committed | 22 changed files in implementation commit 98f5036; new feature branch only. |
| CI | GitHub Actions: Python 3.11 compilation successful; 25 pytest cases passed in 1.37 s. |
| CLI | F01 completed with one valid paired reconstruction; F07 and F08 retained incomplete results. |
| UI | Streamlit pages pass AppTest startup without exceptions; full user interaction not yet exercised. |
| Isolation | Tests check serialized source-only and frozen-decomposition requests for forbidden data. |
| Research | No real Gemma, Qwen, OpenAI, or Comrade AI inference. No scored empirical study. |
| Repository | Draft PR #1 open; main remains at plan commit f0c9ea0. |

### Why this exists

The research asks whether human intended meaning survives writing, structured decomposition, and subsequent reconstruction, and whether the commercial-management treatment alters the output relative to neutral prose. It also aims to measure the labor a human spends explaining differences. The first build validates the experiment machinery with fixed known outcomes, not the hypothesis itself.

### Non-negotiable boundary

Streamlit is a deliberately stupid thin client. Pages render data, accept deliberate commands and display returned results. The CLI uses the same application-service layer. The domain logic, artifact store, run coordinator, historical Oracle resolution, comparison registration, timing calculations and exports all live in ordinary Python modules.

## 1. Work performed: chronological record

| STEP | ACTION / EVIDENCE |
| --- | --- |
| 1 — Inspect | Reviewed existing Disco-STU SERA implementation, its schema, storage, Streamlit capture page, backend tests and November 14 handoff. Identified incomplete STU/Review components. |
| 2 — Reuse survey | Inspected DiScO, smrt, doc_history, PIQITT, slop-in1 and MediLacra code patterns. Comrade AI artifacts could not be independently recovered. Chose conceptual reuse; avoided copying GPL-licensed code into PolyForm-licensed project. |
| 3 — Plan | Committed detailed build plan to docs/stu/DISCO_STU_FULL_BUILD_PLAN_v0.1_2026-11-14.md in main (f0c9ea0), with Streamlit thin-client requirement. |
| 4 — Branch | Created feature/stu-deterministic-pipeline-20261114 from f0c9ea028ea71ffc0692dbfadea20bb61ac07061. |
| 5 — Implement | Added SERA application facade; deterministic STU contracts, fixture adapter, runner, study/artifact store, human review/timer, shared application API, CLI, three Streamlit pages and refactored SERA UI. |
| 6 — Verify | Added backend, application integration, static UI-boundary and Streamlit startup tests, plus a GitHub Actions workflow. Inspected actual CI logs. |
| 7 — Publish | Committed 22 changed files in 98f5036; opened draft pull request #1 to main. No merge performed. |

## 2. As-built system architecture

| SERA / Capture (human-only)<br>   \|-- private frozen Oracle vN (never model input)<br>   +-- four-field source-only packet<br>             \|<br>             v<br>STU application service -> ExperimentRunner -> FixtureAdapter<br>             \|                       \|<br>             \|               deterministic decomposition<br>             \|                       \|<br>             \|                frozen structured JSON<br>             \|                   /           \<br>             \|         neutral request    commercial request<br>             \|           (fresh)             (fresh)<br>             \|                   \         /<br>             \|                   recorded outputs<br>             v<br>Comparison records -> HumanReview (pinned Oracle available HERE)<br>             \|<br>        timed explanation + labels + event journal<br>             \|<br>        Results / verification / safe export<br>Streamlit pages & CLI: both call SeraApplication / StuApplication |
| --- |

### 2.1 Application service boundaries

SeraApplication (sera/application.py) wraps existing SERA storage and domain functions. It exposes create/save/freeze/amend, source-only packet access, editor options, and exact historical Oracle retrieval. StuApplication (stu/application.py) is the shared entry point for studies, execution, typed comparisons, review commands, validation, results, and exports.

The runner imports StuStore and the deterministic adapter but does not import SeraStore or load the private Oracle. Each study stores an Oracle reference in a separate private path, resolved only when StuApplication.get_comparison() prepares a reviewer view. This is an application-level separation, not strong process isolation or an enterprise authorization system.

### 2.2 Thin Streamlit implementation

All four pages instantiate application facades and call their explicit methods. The SERA page converts editor tables to row dictionaries for presentation; validation and writes occur in SERA services. Transform creates a synthetic study and runs it. Review displays two artifacts and forwards start/pause/resume/interrupt/save/complete/amend commands. Results displays the backend report and invokes the safe-export method.

A static test rejects direct imports of storage, runner, SERA service or requests from pages and rejects direct file open() calls. The test supports the architecture claim but does not prove every UI interaction is correct. All durable state lives on disk; session_state is used only for selection/navigation.

### 2.3 Replaceable model interface

stu/contracts.py defines immutable GenerationRequest and GenerationResult dataclasses plus a ModelAdapter Protocol with generate(request) -> result. The GenerationRequest serializes explicit system/user messages, stage, condition, fixture ID, model profile, input SHA-256 and settings. The generated wire request is stored and tested.

The only implemented adapter, DeterministicFixtureAdapter, returns fixed fixture responses with synthetic metadata. Unknown fixture IDs fail; selecting a named fixture for unrelated source text is rejected; STRUCTURAL mode emits a prominent non-semantic placeholder. No endpoint probing, credentials, fallback, or model inference occurs.

## 3. End-to-end execution details

### 3.1 Human reference, frozen before execution

1.  The author creates a paragraph (SERA hard limit: 200 words), then independently writes unrestricted intention.

2.  The author enters eight category-level explanations, followed by units and directed relationships. Empty individual categories are valid.

3.  The reference is explicitly frozen with version ID, content hash and an event. Amendments produce a new version instead of modifying the old one.

4.  STU receives an allowlisted packet containing exactly packet_type, sample_id, source_sha256 and original_text.

### 3.2 Deterministic decomposition and reconstruction

1.  ExperimentRunner checks the synthetic_test mode, adapter identity, prompt hashes, source packet fields and source digest before starting.

2.  It persists the exact decompose request, raw response, response metadata, parsed semantic JSON (if valid), input/output hashes and step status.

3.  If decomposition is invalid, it preserves the raw failed response and finishes the run incomplete; it does not fabricate reconstructions.

4.  On valid decomposition, the frozen parsed JSON is loaded once. Neutral and commercial reconstruction requests each contain only a decomposition property and its shared intermediate hash.

5.  The two outputs, errors, metadata and timestamps are recorded independently. One failed branch leaves an incomplete pair. No silent re-decomposition repairs a pair.

6.  The runner creates available typed comparisons from artifacts actually present. Validation re-reads persisted request bodies and verifies source-only and same-intermediate invariants.

### 3.3 Fixed prompt files

| PROMPT | EXPERIMENTAL INSTRUCTION |
| --- | --- |
| decompose_v0.1.txt | Convert source-only paragraph into category_prose, units and directed relations. Preserve negation, scope, uncertainty, dependencies and rhetorical purpose; JSON only. |
| neutral_v0.1.txt | Reconstruct neutral prose from the frozen representation; preserve claims/qualifiers/ambiguity; do not add recommendations or facts. |
| commercial_v0.1.txt | Advise management of a for-profit business selling a commercial product in a competitive market; preserve objections/limits, and do not invent company/product facts. |

All three prompt files are hashed and pinned in each study. The fixture adapter does not interpret their natural-language instructions; it returns predetermined outputs, allowing request construction and artifact lineage to be tested separately from model behavior.

## 4. Data model and evidence persistence

### 4.1 Logical record grains

| RECORD | GRAIN / CONTENT |
| --- | --- |
| Source sample | One author-entered paragraph, identity/hash and provenance; existing SERA store. |
| Human Oracle | One frozen retrospective explication version; private and reviewer-accessed. |
| Study | One SERA sample and selected fixture, prompt hashes, schema hash, synthetic mode, list of run IDs. |
| Run | One attempt containing adapter, source reference, stage results, statuses, artifact inventory and timestamps. |
| Artifact | Write-once raw source packet, request, response, parsed decomposition, metadata or error object. |
| Comparison | One typed reference/target pair with exact artifact names and hashes. |
| Review journal | One persisted sequence of human review/timing events per comparison. |
| Safe export | One derived analysis report excluding private text, Oracle, requests/responses and explanation content. |

### 4.2 Important path layout

| data/<br>  private/sera/<sample-id>/{draft.json,oracle-vN.json,events.jsonl}<br>  private/studies/<study-id>.json       # pinned Oracle ref<br>  stu_inputs/<sample-id>.json           # source-only packet<br>  studies/<study-id>/{manifest.json,events.jsonl}<br>  runs/<run-id>/{run.json,events.jsonl,artifacts/*}<br>  comparisons/<comparison-id>.json<br>  reviews/<comparison-id>/events.jsonl<br>  exports/<study-id>-safe.json |
| --- |

### 4.3 Integrity method and limits

stu/storage.py uses canonical JSON, SHA-256 digests, write-once stage artifact files and per-run event chains recording sequence and previous-record hash. It checks artifact byte length/hash and run/event consistency. JSON metadata updates use atomic file replacement where possible. A run may explicitly remain incomplete after a crash or partial stage failure.

These controls detect many accidental modifications and inconsistencies, but do not provide adversarial signing, multi-file transactions, cross-process locks or independent attestation. Someone with unrestricted write access to all local files can rewrite self-consistent records. The system is single-user and not PHI-ready.

### 4.4 Comparison types

The design defines seven logical comparison categories; the Oracle-versus-final-output category yields two concrete tasks, so a full synthetic run creates eight comparison records: Oracle/original, original/decomposition, Oracle/decomposition, decomposition/neutral, decomposition/commercial, neutral/commercial, Oracle/neutral and Oracle/commercial.

Comparison creation is not an AI accuracy verdict. The database records semantic_verdict = not_evaluated. The human review layer provides free-text explanations and optional typed gap labels.

## 5. Human Review and explanatory labor

HumanReview stores each action as a durable event: begin, pause, resume, interrupt, save, complete and amend. A separate event-derived state machine rebuilds the current review state after restart; the UI does not own or infer the authoritative time. The unrestricted explanation text is primary, with optional per-gap labels and rationales.

| BEHAVIOR | IMPLEMENTED RULE |
| --- | --- |
| Start / stop | Time starts only after explicit Begin; ordinary comparison inspection is untimed. |
| Counted active time | Only fully closed begin/resume-to-pause/complete/interrupt intervals contribute. |
| Unclosed intervals | Open intervals do not silently grow across reloads. They are shown as open. |
| Long interval | A closed interval over 15 minutes is flagged timing_uncertain and excluded until manually resolved. |
| No gap | A completed no-meaningful-gap response is explicit; a blank unfinished review is not equivalent. |
| Explanations | Meaningful-gap completion requires nonempty written explanation; optional typed gaps require rationales. |
| Amendment | A completed explanation can be amended; the earlier event history remains readable. |

This estimates declared active explanatory work; it does not measure unconscious cognition, reading time, time before pressing Begin, or semantic correctness. Longer review, fatigue, sample exposure and typing speed remain research confounds.

## 6. Deterministic synthetic fixture catalog

The fixed examples are deliberately fictional and are labeled synthetic. Their expected outcomes are test cases defined in advance, not the results of any LLM run.

| ID | CONDITION UNDER TEST | EXPECTED SYSTEM OBSERVATION |
| --- | --- | --- |
| F01 | Faithful reconstruction | Valid decomposition and both branches; complete paired execution. |
| F02 | Decomposition loss | Condition omitted from the canned semantic representation. |
| F03 | Neutral reconstruction loss | Daylight qualification disappears only from neutral prose. |
| F04 | Commercial managerial reframing | Commercial branch adds an unsupported market-share objective. |
| F05 | Relational distortion | Alarm / switch / conveyor causality or direction changes. |
| F06 | Legitimate extension | Commercial output adds a recommendation consistent with source. |
| F07 | Malformed decomposition | Invalid JSON preserved; incomplete run; no invented downstream pair. |
| F08 | Commercial branch failure | Neutral output retained; failed commercial branch; incomplete pair. |
| F09 | Oracle-versus-source gap | Fixture illustrates a human intention that need not have been conveyed. |
| F10 | Explicit no-meaningful-gap path | Fixture supports no-gap review lifecycle testing. |

STRUCTURAL is an additional smoke mode for any eligible authored paragraph. Its outputs explicitly state that no semantic interpretation was performed. This enables a structural walkthrough with real writing but cannot validate meaning preservation.

## 7. Verification evidence

### 7.1 GitHub Actions results

The GitHub Actions workflow .github/workflows/deterministic-tests.yml runs on Python 3.11. The observed successful job log contains the following executed checkpoints:

| CHECK | OBSERVED RESULT |
| --- | --- |
| Dependency install | Completed successfully. |
| Compile | python -m compileall -q sera stu pages tests — success. |
| pytest | 25 passed in 1.37 s; includes 11 original SERA/schema cases and 14 added cases. |
| CLI doctor | Reports deterministic_fixture available; real model adapters not implemented; synthetic_test only. |
| F01 smoke | Completed run, validated evidence and exactly one valid paired reconstruction. |
| F07/F08 smoke | Both returned incomplete run status without treating them as successful pairs. |
| Page startup | Streamlit AppTest loaded four pages with no startup exception (pytest). |

The two GitHub check runs attached to implementation commit 98f5036 both report success. The original completed job 132597431170 is linked in the sources section. No complete human-driven browser walkthrough has been recorded.

### 7.2 Test coverage by kind

| AREA | EXPLICITLY EXERCISED BEHAVIOR |
| --- | --- |
| SERA integration | Source capture, original freeze and private export, source lock, amendments, historical Oracle pin after a newer freeze. |
| Adapter | Repeatable fixture response, unknown fixture rejection, mismatched source rejection. |
| Runner | Decomposition then two reconstruction stages, shared intermediate hash, serialized request body isolation. |
| Failure | Invalid JSON, unavailable branch, incomplete run retention, excluded incomplete pairs. |
| Storage | SHA-256 artifact corruption detection, journal chain corruption rejection. |
| Review | Pause/resume, duplicate commands, explicit no-gap, event-derived duration after reload, long uncertain interval. |
| Privacy/mode | Injected Oracle-like field rejected from model packet; real adapter/scored mode fail closed; safe export omits source and Oracle. |
| UI separation | Static forbidden-import/file-open checks and Streamlit AppTest initial page load. |

### 7.3 Evidence semantics

The validation report’s valid=true means stored evidence and implemented invariants passed verification, not that the semantic output is correct. An intentionally incomplete F08 run can be a validly preserved piece of evidence. The reporting API separately enumerates completed paired outputs and declines to invent a semantic verdict.

## 8. Source-file inventory — exact implementation commit

Implementation commit 98f5036 changed these 22 files. The original SERA domain modules and schema were retained; the existing SERA Streamlit page was rewritten to call the application facade.

| FILE | RESPONSIBILITY |
| --- | --- |
| .github/workflows/deterministic-tests.yml | CI job for compile, pytest and synthetic CLI verification. |
| docs/WORK_LOG.md | Chronological build notes, reuse boundaries, simplifications and limitations. |
| docs/stu/IMPLEMENTATION.md | Runtime instructions and implementation claims/limitations. |
| pages/1_SERA.py | Refactored SERA capture interface using SeraApplication commands. |
| pages/2_STU_Transform.py | Thin sample/study selection, synthetic run and stage display. |
| pages/3_STU_Review.py | Thin paired artifact viewer and human review/timer controls. |
| pages/4_STU_Results.py | Thin coverage, verification and safe-export view. |
| prompts/commercial_v0.1.txt | Treatment prompt: for-profit competitive business advice. |
| prompts/decompose_v0.1.txt | Structured semantic decomposition instruction. |
| prompts/neutral_v0.1.txt | Neutral reconstruction control instruction. |
| sera/application.py | Application facade and exact-version Oracle lookup. |
| stu/__init__.py | STU package identity/init. |
| stu/application.py | Shared backend for studies, run/review/analysis/export. |
| stu/cli.py | CLI commands using StuApplication, including smoke. |
| stu/contracts.py | Canonical hashing, structured validator, adapter protocol and data contracts. |
| stu/fixtures.py | F01–F10 predetermined outputs and deterministic adapter. |
| stu/review.py | Event-derived human review state and timing policy. |
| stu/runner.py | Stage orchestration, serialized requests, paired reconstruction and comparisons. |
| stu/storage.py | Local JSON/JSONL store, write-once artifacts and hash-linked events. |
| tests/test_stu_application.py | Full SERA/STU integration, historical pins, isolation and mode gates. |
| tests/test_stu_backend.py | Adapter, stage invariants, failure, storage, timing and static UI tests. |
| tests/test_stu_ui_smoke.py | Streamlit AppTest startup of all four pages. |

## 9. Limitations and questions for independent review

These are not hidden defects presented as completed work. They are explicit implementation boundaries and potential review targets. The source files and passing tests are available in the draft pull request.

| PRIORITY | REVIEW ITEM |
| --- | --- |
| HIGH | Scientific validity: fixture text and outcomes are canned; no real model behavior has been evaluated. Prompt wording is versioned but untested against actual LLMs. |
| HIGH | User acceptance: four pages start in AppTest, but the full interactive create/freeze/transform/review/export journey has not been browser-tested. |
| HIGH | Oracle/privacy boundary: code separates private Oracle references from runner requests, but process/filesystem access is single-user and not a security sandbox. |
| HIGH | Scored-study protocol: scored mode is explicitly rejected; no frozen multi-sample manifest, order randomization or blinded human adjudication is implemented. |
| MEDIUM | Timer policy: only closed active intervals count; >15-minute spans are excluded/uncertain, and intervention to resolve those cases is not yet a scored protocol. |
| MEDIUM | Fixture complexity: most canned decompositions use one unit and no relationships. Expand multi-node/edge fixture coverage before claiming realistic semantic graph testing. |
| MEDIUM | Persistence: manifest/artifact/event writes are not one transaction and no cross-process locking exists; verify crash recovery semantics before parallel runs. |
| MEDIUM | UI and reporting: the results field planned_run_count currently counts recorded runs; consider clearer naming. Review interface only allows one typed gap per save, although backend accepts a list. |
| MEDIUM | Research comparisons: all eight typed tasks are generated, but there is no automatic semantic truth score. Human labels remain required; condition masking/order protocols remain future work. |
| LOW | Documentation hygiene: the existing root README may still foreground SERA-only baseline; reconcile it with docs/stu/IMPLEMENTATION.md after review. |

### 9.1 Suggested independent challenge tests

Try a source-only packet with unexpected private fields and inspect the serialized adapter request; confirm execution refuses before any output.

Create an F01 study, amend its author Oracle to v2, then reopen the old comparison and verify it still reads the pinned v1 artifact and hash.

Modify one byte of an artifact and one event sequence/hash in separate test copies; observe integrity errors, not silent acceptance.

Run F07 and F08 and verify that an incomplete attempt remains reviewable as evidence but is excluded from paired treatment observations.

Interrupt an explanation, restart Streamlit, resume, and compare event-derived time to wall-clock logs; test the 15-minute uncertainty policy.

Walk through SERA → Transform → Review → Results using F01 and separately a personal paragraph with STRUCTURAL; check every warning communicates the distinction.

Confirm every Streamlit page invokes domain methods instead of implementing its own storage, scientific comparison, timer or request assembly logic.

## 10. How Radiant Control can reproduce the build

Commands below apply to a local checkout of the repository, including Windows PowerShell. They do not trigger any real model, external API request, or scored experiment.

| git fetch origin<br>git switch feature/stu-deterministic-pipeline-20261114<br>python -m pip install -r requirements-dev.txt<br>python -m compileall -q sera stu pages tests<br>pytest -q<br>python -m stu.cli doctor<br>python -m stu.cli smoke --fixture F01<br>python -m stu.cli smoke --fixture F07<br>python -m stu.cli smoke --fixture F08<br>streamlit run app.py |
| --- |

For isolated output files, set SERA_DATA_DIR to a local folder or supply --data-root before the CLI subcommand. Runtime records live under data/ by default and are gitignored. Use the F01 exact source paragraph below if selecting fixture F01 in the UI:

| The harbor gate remains closed until the safety inspection is complete. |
| --- |

### 10.1 Suggested five-step acceptance walkthrough

1.  SERA: create the F01 sample, save unrestricted intention, category prose and semantic units; inspect/freeze, reload, and optionally amend.

2.  Transform: choose the frozen sample, select F01 only if the source exactly matches the fixture; create the study and run it.

3.  Controlled branches: inspect the recorded decomposition and the neutral/commercial outputs; confirm both reference one intermediate hash.

4.  Review: select a comparison, Begin, save a free-text gap explanation and optional classification; Pause/Resume/Complete and inspect saved duration; also test explicit no-gap on another comparison.

5.  Results: examine run coverage, the paired result, validation and safe export. Review stored artifact identities; restart the app and confirm persistent state.

For actual authored writing, choose STRUCTURAL instead of a named fixture. The placeholder will not and cannot interpret the paragraph; it only proves workflow plumbing.

## 11. Next phase after acceptance

No further implementation has been authorized in this handoff. After UI acceptance, the natural next change is to implement real local/API adapters behind ModelAdapter, with exact actual model and transport identity, settings, raw responses, timeout/failure history and no silent fallback. Only after real adapter smoke tests and corpus/protocol freeze should scored runs be enabled.

An independent scientific review should decide whether the next fixture set needs multi-unit graphs, evidence spans, reviewer masking/order, stronger transaction recovery, or stricter private-role boundaries before any comparative model study.

## Appendix A. Canonical GitHub evidence

Repository: [Open in GitHub](https://github.com/natosit-dev/Disco-STU)

Approved build plan: [Open in GitHub](https://github.com/natosit-dev/Disco-STU/blob/main/docs/stu/DISCO_STU_FULL_BUILD_PLAN_v0.1_2026-11-14.md)

Implementation commit: [Open in GitHub](https://github.com/natosit-dev/Disco-STU/commit/98f50367c6458f840c5fd1cf0b1ba3b22ed6c7d6)

Draft pull request #1: [Open in GitHub](https://github.com/natosit-dev/Disco-STU/pull/1)

Passing GitHub Actions job: [Open in GitHub](https://github.com/natosit-dev/Disco-STU/actions/runs/43643946245/job/132597431170)

Implementation notes: [Open in GitHub](https://github.com/natosit-dev/Disco-STU/blob/feature/stu-deterministic-pipeline-20261114/docs/stu/IMPLEMENTATION.md)

Work log: [Open in GitHub](https://github.com/natosit-dev/Disco-STU/blob/feature/stu-deterministic-pipeline-20261114/docs/WORK_LOG.md)

SERA source-only export: [Open in GitHub](https://github.com/natosit-dev/Disco-STU/blob/main/sera/exports.py)
