# STU deterministic implementation notes

The first build is an **offline research instrument skeleton with real event and artifact persistence**. Synthetic cases exercise the complete flow but do not support empirical claims about any LLM.

### Quick start

Use the dependencies already declared in the root project (`requirements.txt` and `requirements-dev.txt`). From the repository root:

```bash
python -m pip install -r requirements-dev.txt
pytest -q
python -m stu.cli doctor
python -m stu.cli smoke --adapter fixture --fixture F01
python -m stu.cli smoke --adapter fixture --fixture F08
streamlit run app.py
```

The Streamlit sidebar provides **SERA**, **STU Transform**, **STU Review**, and **STU Results**. Synthetic F01–F10 fixtures require exact known source text; choose **STRUCTURAL** when using a real paragraph you authored. Structural smoke output explicitly refuses to pretend to infer meaning.

The CLI and Streamlit call `stu.application.StuApplication` and `sera.application.SeraApplication`; page scripts must not directly import storage, runner, semantic validator, or timer internals.

### Additional CLI commands

```bash
python -m stu.cli validate --study <uuid>
python -m stu.cli analyze --study <uuid>
python -m stu.cli export --study <uuid>                      # complete private ZIP (default)
python -m stu.cli export --study <uuid> --privacy-level safe # redacted JSON
python -m stu.cli run --study <uuid> --adapter fixture --mode synthetic_test
```

Persistent data are under `data/`, or another directory via the `SERA_DATA_DIR` environment variable (CLI also accepts `--data-root`). Private Oracle records are separated from the four-field source-only packets. The runner references the latter only. Review resolves a specific pinned Oracle version; never automatically the latest amendment.

### Integrity and limitations

- `stu/storage.py` stores immutable stage artifacts, hashes, and ordered hash-linked journal events. Hashes detect local changes, not attackers who can edit all files.
- No remote LLMs, training, real semantic evaluation, model output quality scores or external services are included.
- The fixture adapter has deterministic canned outputs; an unknown fixture fails. `STRUCTURAL` is an explicitly meaningless placeholder, not a cheap NLP model.
- Distinct review tasks represent human-writing, model-decomposition, local reconstruction and condition-contrast boundaries. Do not collapse them into one automatic accuracy score.
- Timed review counts human explanation intervals explicitly closed by review actions; interrupted/long gaps are flagged instead of silently inflating counted active time.
- **Default full export** writes a private ZIP to `data/exports/<study-id>-full.zip`: pinned SERA Oracle, source, SERA freeze history, study/run manifests and journals, every run artifact, comparison and review event, versioned prompts/schema and results, plus a SHA-256 file inventory. Never publish it unreviewed. The runner still only sees the four-field source packet.
- The optional **redacted summary** (`--privacy-level safe`) omits source text, Oracle, raw model requests/responses and human explanation content. Both exports remain under gitignored `data/`.
- `recorded_run_count` counts actual stored runs, not planned study allocations. Older saved safe JSON exports may still have the old `planned_run_count` name.
- This is a single-user prototype. It does not provide cross-process locking, transactional multi-file writes, cryptographic attestation, or PHI safeguards. Do not use for restricted clinical data.
