# Adaption API key input and single-prompt smoke test

## Purpose

This change is an **API connectivity diagnostic**, not the three-stage DiScO-STU live experiment. Fixture study execution remains unchanged. The new page sends **one** simple, potentially billable hosted-model request:

`Reply with exactly: OK`

The provider may respond differently; this is not a semantic correctness test. Nothing from SERA, including the private Oracle, enters the diagnostic input.

## Local Ubuntu WSL + Conda workflow

```bash
wsl -d Ubuntu                  # From Windows Terminal, not from inside WSL
conda activate disco
cd ~/code/Disco-STU
git status
git branch --show-current
git fetch origin
git pull --ff-only                # Only if clean and correct branch
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m streamlit run app.py --server.port 8511
```

Open **Transform** or **Adaption API Test** in the Streamlit sidebar. Paste the key into the masked field on either page; it is copied into a non-widget Streamlit session key to survive page navigation. Select `gemma-4-31b-it` and click **Send one API test request**. The page shows provider text, model, response ID, status and token usage (if any). The SDK uses `max_retries=0` and `timeout=45` to avoid hidden retries. The request is stateless (`store=False`, `agentic_memory=False`, `tools=[]`). `ADAPTION_API_KEY` in WSL is still an optional fallback.

**Do not enter the key into the ChatGPT chat, a GitHub issue or a code file.** Use Streamlit locally on a trusted machine; this application has no multi-user authentication or secure credential vault. Never expose the Streamlit port publicly.

## Explicit boundaries

- The API key stays in memory in the currently running Streamlit session, except for an optional separately managed environment variable. It is not stored in a study, log, ZIP, source file or committed to Git.
- SDK response metadata is displayed in the page but not persisted. This is a diagnostic; it must not be mistaken for a complete experimental run.
- Missing credentials, unsupported model choices, SDK errors and non-completed responses are shown explicitly. SDK exception messages are not echoed, because they may contain request data.
- No changes to `stu/review.py` or `pages/3_STU_Review.py`; no modifications to existing comparison identifiers.
- Tests use injected fake SDK clients, not real API keys or paid inference. A genuine request requires clicking the button from the local UI.

## Connected live experiment

The full live Experiment 01 runner is now implemented on the feature branch; the API Test page remains a separate, non-persistent connectivity check. For the live three-stage workflow, see [Live inference v0.1](stu/LIVE_INFERENCE_v0.1.md).
