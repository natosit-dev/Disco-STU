# DiScO STU Work Log

## 2026-11-14 — Deterministic pipeline build

- **Baseline:** GitHub `main` at `f0c9ea028ea71ffc0692dbfadea20bb61ac07061` when branch was created. Existing SERA source remains part of the target repository; no external runtime or actual model was inspected or executed.
- **Purpose:** Assemble the complete offline capture → source-only decomposition → frozen intermediate → paired reconstruction → human gap review/timing → analysis/export pipeline.
- **Design boundaries:** Streamlit and CLI call one Python application API. Neither owns research business logic. Model adapter is an explicitly synthetic, deterministic fixture. No model ever sees human Oracle data in adapter requests. Human reviewer loads pinned historical Oracle artifact on demand.
- **Reuse:** Reuse existing SERA source; adapt conceptual evidence patterns from `smrt` and deterministic inspection from `DiScO` without copying GPL source. Do not import old model clients with silent endpoint fallback. Comrade AI sources were not available to verify for this build.
- **Runtime limitations:** Only `synthetic_test` is executable. This program does not perform Gemma/Qwen/OpenAI inference, autonomous semantic judgments, or scored research. Streamlit's visual workflow must be smoke-tested in the target environment.
- **Tests:** Offline unit/integration/negative test suite; canonical bytes, artifact integrity, broken journal, branch failures, source/Oracle isolation, historic pins, restart-derived timer, and safe export. Record final CI and smoke-test outcomes in PR body; do not claim tests passed until observed.

### Deliberate simplifications

- Local JSON/JSONL instead of a database server; no DuckDB in first version.
- Mutable run manifests expose current state while produced artifacts remain write-once. Multi-file writes aren't transactional; incomplete/crash states are explicit.
- Hash chains detect local alterations relative to stored journals, not adversarial tampering.
- Timer counts explicit closed intervals; a >15-minute interval is conservatively marked uncertain and excluded from active-duration totals pending human resolution.
- No generic semantic scoring is computed. Fixture expectations are only assertions for testing the instrument.

## 2026-11-15 — Live Adaption inference work authorized (pre-implementation checkpoint)

- **Branch at authorization:** `feature/stu-deterministic-pipeline-20261114`, HEAD `980b90f78f2e2c04ccb3085826c183354393eea4`; `main` remains separate. Work-log entry committed before code changes per Nat's request.
- **Observed prerequisite:** Nat reported a genuine Adaption SDK diagnostic using `gemma-4-31b-it` returned `OK`, status `completed`, with a provider response ID and token usage (18 input / 2 output). This is user-supplied API evidence, not an STU pipeline result or a locally reproduced call.
- **Authorized objective:** Wire three fresh, stateless model calls per live study: source-only semantic decomposition, then neutral/commercial reconstruction from one exact frozen reconstruction projection. Keep full decomposition as evidence; exclude `source_support` from reconstruction inputs. Pin actual prompts, schema and projection in study artifacts for durable export.
- **Security and scope:** API key from existing masked Streamlit session or `ADAPTION_API_KEY` environment only; never persist or export it. Keep `stu/review.py` and `pages/3_STU_Review.py` unchanged for Radiant Control. Preserve comparison IDs and deterministic behavior/tests. No new database, agents, or semantic auto-scoring.
- **Simplification decision:** Live studies become the default visible Transform workflow. Retain synthetic fixtures as clearly labeled regression/diagnostic infrastructure (do not delete legacy studies or their evidence). Keep the one-prompt API diagnostic page.
- **Tests before merge:** Existing deterministic tests plus mocked API failures/credentials/projection fidelity, persisted evidence and full ZIP, streamlit startup and CLI synthetic replay. Mark CI and live outcomes separately. A genuine three-stage live run still requires Nat's key and frozen local SERA source.
- **Environment:** WSL Ubuntu + Conda `disco`, branch shown above, `python -m pytest -q`, Streamlit on port 8511. The GitHub executor is a separate isolated environment; no assumption of access to private WSL runtime artifacts.

## 2026-11-15 — Live integration implemented (verification checkpoint)

- **Live model path:** Official Adaption SDK adapter (gemma-4-31b-it / qwen3.5-397b / glm-5.2), fresh request per stage, no tools, memory, conversation continuation, automatic SDK retry, or fixture substitution.
- **Freeze:** New studies snapshot prompt, semantic schema, and reconstruction-projection specification bytes. Both reconstruction calls receive byte-identical projected JSON with source_support excluded. Full decomposition is separately archived.
- **Persistence:** Real live study/run/comparison/result/ZIP records carry `mode=live`, `synthetic=false`, actual requested/returned model metadata, full provider JSON, usage, error/incomplete state and exact SDK parameters excluding credentials.
- **Frontend:** Masked session key on Transform, live study/model selection and explicit chargeable run button. Existing synthetic fixtures remain behind collapsed regression diagnostics; original tests and records are retained. Adaption API Test stays available.
- **Coordination:** No changes to `stu/review.py` or `pages/3_STU_Review.py`; all other edits scoped to live execution, application APIs, exported evidence, docs, or tests.
- **Observed verification:** At commit `7829c61ab016c419d2594d52fd56799df873c5e2`, GitHub Actions reported **52 passed in 2.57 s** (all mocked/offline) after correcting a test's escaped-newline expectation. Subsequent docs/API-parameter changes require their own final CI result.
- **Unverified / next human acceptance:** A full genuine three-stage live experiment has not been performed here, because Nat's WSL-only credential and frozen local SERA records are unavailable to the GitHub build runner. Nat previously reported a successful single-call live Adaption diagnostic. The first full live response may still expose model-specific JSON/schema issues; preserve and report them without automatic repair.
- **Parameter policy:** Request only model, instructions, input, store=False, agentic_memory=False, tools=[]; leave temperature/seed/extra controls unset to match known successful diagnostic behavior where possible. SDK max_retries=0; timeout=120 s.

## 2026-11-15 — Source-to-final comparisons and review prioritization

- **Trigger:** The first user-supplied complete live experiment ZIP contained eight comparisons and a valid frozen reconstruction projection. The direct `original_vs_neutral` and `original_vs_commercial` comparisons were missing.
- **New coverage:** Each completed reconstruction now permits a source-only packet → final output comparison. A fully completed run records ten comparisons, all with unchanged `not_evaluated` semantic verdicts. Failed/incomplete branches remain excluded from accepted pairs.
- **Human workload:** `oracle_vs_neutral` and `oracle_vs_commercial` are listed first as the two primary review activities. The other eight are explicitly optional diagnostics, not mandated human labor.
- **Exact model-visible evidence:** In Results, optional reconstruction diagnostics display the full decomposition and, separately, the precise saved reconstruction projection plus SHA-256 after verifying the recorded SDK input bytes. Existing diagnostic comparison IDs and saved reference artifacts remain unchanged.
- **Historical compatibility:** Results provides a deliberate `reconcile_original_final_comparisons` action. It validates saved run artifacts, writes only missing new comparison records, never reruns inference or rewrites original comparison/review files, and does not mutate data on normal read. When new records are written, the application also **appends** a `comparisons_reconciled` event to the existing study journal; repeated invocation writes nothing. A later full ZIP includes the added records and appended event. Do not edit the original uploaded ZIP itself.
- **Ownership:** `stu/review.py` and `pages/3_STU_Review.py` are unchanged; priorities use `StuApplication.list_comparisons` and diagnostics use the separate Results view.
- **Verification:** GitHub Actions reported 58 passing tests on commit `1c8cefd4199bf88adbc9a61c1da67dc8a387223b` (mocked live backfill without provider calls, source-to-final references, historical review persistence, exact projection views). After populated-Results AppTest and documentation updates, commit `aff3ea2cb915673a0f98f4502c17702d36fecfb6` passed **59 tests** and the synthetic CLI smoke suite; both CI checks succeeded (GitHub Actions job `132920339611`).
- **No semantic correctness claim:** These are instrumentation and archive-completeness changes; human interpretation remains outside automated validation.

## 2026-11-15 — Pre-UI-cleanup checkpoint (no code changed)

- Recorded baseline `09eeb47920c285a57bb38168c424c2c0ca7996bf` after the ten-comparison/live-inference milestone; **59 tests** previously passed.
- New request grounded in human workflow: **Write → Explain → Run → Review**. Approved a two-stage effort: (A) human-readable UI/Review/Results, then (B) SERA v0.2 capture contract with optional structured annotations and strict v1 preservation.
- Full scope and compatibility/ownership constraints are frozen in `docs/checkpoints/DISCO_STU_HUMAN_WORKFLOW_BEFORE_V02_2026-11-15.md`.
- Radiant Review timer/domain code should not be changed by UI cleanup; carry 15-minute budget-vs-uncertainty issue as explicit follow-up, not as an unverified fix.

## 2026-11-15 — UI v0.2 / SERA capture v0.2 implementation

- **Pre-change checkpoint:** `96e3d1af102b88a0541cfbf3e286e765026bcfd6`, [checkpoint document](checkpoints/DISCO_STU_HUMAN_WORKFLOW_BEFORE_V02_2026-11-15.md). Baseline was 59 passing tests.
- **UI release:** Added pure display helpers deriving source/study/run/comparison labels from pinned provenance and actual local-time conversion. Transform and Results now prioritize readable human workflows; raw metadata and archived-run reconciliation remain available under expanders.
- **Human Review:** Changed the two primary visible choices to **original_vs_neutral** and **original_vs_commercial**, grouped by model run. The original and output are shown as prose, with frozen authorial intention available but not forced into the reader's initial view. Diagnostic comparisons and typed labels remain optional; the old comparison IDs and stored review history are preserved.
- **SERA v0.2:** Added explicit `schema_version=0.2.0` records requiring only a saved unrestricted authorial explanation plus valid source and explicit Freeze. Five characteristics, eight category questions, units and relations are optional annotations, not semantic equivalents; existing v0.1 validation and draft editor remain strict, historical frozen files remain unchanged, and amendments preserve their version. New studies pin v0.2 schema bytes in full private ZIPs.
- **Thin-client boundary:** Domain writes still flow through `SeraApplication`/`StuApplication`, with no new database, agent, model behavior or semantic judge.
- **Ownership:** `stu/review.py` was not edited. The Review **page** was redesigned to satisfy the current user request; Radiant Control should review UI differences before merging to avoid parallel page edits.
- **Observed verification:** GitHub Actions at commit `c017f8f9815edc3f6804db8f7f9d0478318918a6`: **71 pytest tests passed**, and synthetic CLI smoke/negative scenarios passed; both CI checks succeeded. Includes optional v0.2 freeze, unchanged v0.1 behavior, Oracle hashes, model-packet isolation, v0.2 schema ZIP capture, real-record UI smoke, historical labels and run-level comparison selection. Subsequent documentation commits require their own final CI result.
- **Open usability items:** Review's cumulative 15-minute labor-budget Boolean vs >15-minute interval uncertainty is unresolved in the separately owned timing service; exports retain explicit prepare-then-download (two-step) to avoid generating sensitive ZIPs on ordinary page render. Full manual WSL browser acceptance remains outstanding.

## 2026-11-15 — First live reviewed run recorded; UI repair authorized

- Verified the original user-supplied full ZIP SHA-256 `9e6316f7378c97bd00953790a7db09f4743e19dbd16f8b6c4df7eca9c7e8ccff`, 45/45 manifest file hashes, 3 hosted Gemma stages, 10 comparisons and both 7-event review journals. See [public research summary](results/EXPERIMENT_01_GEMMA_FIRST_HUMAN_REVIEW_2026-11-15.md).
- Neutral: author observed preservation of the three explicit negations but loss of rhetorical line separation. Commercial: author observed a jarring critical intervention becoming routine management advice, partly as designed by the commercial treatment prompt.
- Confirmed logged human active time: Neutral 171.808s, Commercial 51.713s (223.521s total); commercial last pause to next save was ~6m29s unmeasured. Mark labor-time measurement incomplete; preserve original journals unmodified.
- **Confidentiality:** Only an author-approved research summary and minimal non-private result manifest are committed. The original full private ZIP, Oracle, provider responses and raw human review journals are not committed.
- **Next engineering change:** stabilize Streamlit review selection/draft state; prevent overlapping active reviews and paused editing; make Save & Complete idempotent; report free-text independently of optional labels; separate cumulative 15-minute threshold from uncertain long intervals; exercise complete UI state transitions. No new model runs needed for regression.

## 2026-11-15 — Review state-machine and Streamlit repairs after first Gemma assessment

- **Research checkpoint committed first:** [First Gemma authorial review](results/EXPERIMENT_01_GEMMA_FIRST_HUMAN_REVIEW_2026-11-15.md) and [minimal public verification metadata](results/experiment_01_gemma_verified_summary_v0.1.json) at `27fd99305122be2dfb0b5a60ef5808b7c4539b2c`. Only derived non-private observations were committed; original 45-file private bundle and 7-event review journals remain untouched.
- **Reproducible failure:** Earlier UI permitted saving edited text while paused or amended, reopening Neutral while Commercial's timer ran, and appending duplicate identical saves. Existing commercial assessment has ~6m29s of wall time between last pause and next save, which cannot be equated to labor time.
- **Review state machine:** Added single-active-timer guard across local reviews; amendment/resume also respect the guard. Editing changed text requires active timing; paused/interrupted/amended saves are rejected unless identical no-op. Repeated identical Save is a no-op; amended review must explicitly resume timing before new writing. Event names and historical replay remain compatible.
- **Measurement policy:** Cumulative **confirmed active** time `>=900s` yields `reached_15min_budget`. This is independent of `timing_uncertain` for any single interval longer than 900s. Legacy paused/amended changed saves are interpreted as `unmeasured_edit_event` / `labor_measurement_incomplete` derived flags **without adding events or assigning labor to unmeasured wall-clock gaps**.
- **Streamlit Review:** Stable keyed source/run/comparison, automatic restoration of one active comparison, comparison-specific transient draft memory, untimed inspection before Begin, disabled navigation while timer active, no editable paused screen, explicit Resume to edit, one Save & Complete action plus optional Save Draft / Pause & Save Draft, optional labels. Review statuses include timing caveats.
- **Results:** Independently counts reviews with author-written meaningful differences, explicit no-gap outcomes, and incomplete labor timing. Optional classifications remain secondary; an empty `review_gap_labels` is not interpreted as zero findings.
- **Verification:** GitHub Actions on `36bf41ce28ea4458eac6b3acf4342220ba4eac0d` passed **78 pytest cases** including existing SERA/STU tests, six new Review-domain tests, and an interactive Streamlit Review lifecycle test. Compile and synthetic CLI smoke/negative stages also passed; both CI checks green. The local Ubuntu WSL human walkthrough remains necessary before the next hosted experiment.
- **No inference changed:** Adaption SDK calls, source-only/model-visible artifacts, SERA frozen Oracle, and deterministic fixture behavior were not modified. Single-user file-backed local system remains non-transactional and cannot prevent a user switching to another Streamlit page while an active timer is running; returning to Review restores the active comparison and permits explicit pause.
- **Coordination:** This repair intentionally touches `stu/review.py` (state rules) and `pages/3_STU_Review.py` (Streamlit interaction). Radiant Control should review the exact diff before independently editing these shared modules.

## 2026-11-15 — Text-only hosted model selector after two Qwen 504 failures

- Nat reported a second `qwen3.5-397b` decomposition attempt failed with the same approximately one-minute HTTP 504 as the first, despite a successful one-prompt Qwen API diagnostic. The second failure is **user-reported** here; this change did not fetch or modify that private run ZIP.
- Scoped decision: stop blind Qwen retries, **change only new-study/diagnostic model selection**, not the frozen experiment prompts, retries, live transport, schema, historic models or review protocol.
- Official Adaption model catalog (https://docs.adaptionlabs.ai/inference-stacks/models) identifies text-input-only deployments `deepseek-v4-flash`, `glm-53-flash`, and `glm-5.2`. Those appear in the new-study and API Test dropdowns; readable labels and CLI doctor metadata are updated.
- **Compatibility:** `gemma-4-31b-it` and `qwen3.5-397b` remain in backend supported IDs so previously pinned Gemma and failed Qwen studies and their evidence can be opened or rerun without migration. New UI creation no longer offers them.
- **Stack boundary:** Nat already configured a DeepSeek Flash inference stack, but STU uses the **direct hosted** `deepseek-v4-flash` model ID to avoid introducing stack-specific memory/tools/settings into the controlled study. The configured stack is not altered.
- **Verified:** Commit `8a3aa4cd10b2a304654373d00af2bba0088e51d5` passed **86 pytest cases** (including new text-only selector tests and a mocked DeepSeek three-stage study) plus the full synthetic CLI smoke/negative checks; both GitHub Actions jobs succeeded. No real provider request was made by CI.
- **Not yet verified by live request:** new DeepSeek choice needs an Adaption API Test from Nat's WSL-held credential, followed by a fresh DeepSeek study on the **same frozen SERA source and Oracle**. Mocked test and CI do not establish provider availability or semantic performance.

## 2026-11-15 — Second completed live study and rig acceptance

- **User acceptance:** “We're done enough—the rig works and produces usable data.” This closes the **exploratory STU rig** milestone; no new code changes, schema changes or additional model runs were requested.
- **DeepSeek evidence:** User-uploaded full private ZIP SHA-256 `fadc3b06d8965e32f03fe503d1a8ad3a3ff5e2294d12d7299449a7fd0570bd0a`, safe JSON SHA-256 `7f13d057a6c12635872b8b9f4c17ad1583148e5f690d771a1bcc18db511a3295`. Verified **45/45** manifest entry bytes/hashes and both Review event hash chains (7 Neutral, 3 Commercial).
- **Run:** Direct hosted `deepseek-v4-flash`, 3/3 completed, 10 comparisons, 2/2 completed primary authorial reviews; exact same saved projection bytes in both reconstruction provider requests; reported provider execution ~47.49 s, 5,986 tokens.
- **Human findings:** Explicit negations survived but intended rhetorical function did not fully transfer; Neutral described an intervention instead of reproducing it; Commercial treated negations as definitions, imposed business framing and qualifications, with some passages found useful. Free-text author judgments remain primary; not an automated correctness verdict.
- **Time quality:** DeepSeek Neutral 144.962 s, Commercial 866.748 s confirmed active (1,011.710 s combined), no recorded timing-quality flags. Do not equate this with complete evaluation/lookup labor; unlike Gemma's first run, no historically unmeasured paused-edit interval was detected.
- **Git privacy boundary:** Committed **derived** research memo `docs/results/EXPERIMENT_02_DEEPSEEK_FIRST_HUMAN_REVIEW_2026-11-15.md`, minimal structured verification summary `docs/results/experiment_02_deepseek_verified_summary_v0.1.json`, and acceptance checkpoint `docs/checkpoints/DISCO_STU_RIG_ACCEPTED_2026-11-15.md`. No original private ZIP, raw reviews/Oracle, or API payloads committed.
- **Disposition:** Baseline accepted as a local, repeatable experimental rig with usable evidence. This is an intentional stop point, not a claim of generalized model findings or production readiness. Earlier 86-test CI milestone is unchanged by documentation-only closure.
