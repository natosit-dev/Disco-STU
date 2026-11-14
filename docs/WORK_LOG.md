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
