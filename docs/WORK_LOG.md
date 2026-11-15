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
