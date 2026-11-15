# DiScO STU — Live Adaption execution v0.1

Status: **implemented; automated verification only until a human initiates a genuine hosted experiment**.

## Standard local workflow

Ubuntu WSL, Conda `disco`, `~/code/Disco-STU`; no virtualenv needed.

```bash
conda activate disco
cd ~/code/Disco-STU
git status
git branch --show-current
git fetch origin
git pull --ff-only               # only on clean correct branch
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m stu.cli doctor
python -m streamlit run app.py --server.port 8511
```

In SERA, finish and **freeze** one private author explication. On Transform, paste the Adaption key in the masked session field (or set `ADAPTION_API_KEY` locally), choose the frozen SERA source and available model, create a **live** study and click **Run live model experiment**. A complete experiment attempts three independently billed calls. The key is passed to the backend as a transient value; it is not stored in manifests, requests, exports or events.

Adaption model selection initially allows `gemma-4-31b-it`, `qwen3.5-397b` and `glm-5.2`. Actual authorization and model availability depend on the account. Do not expose the locally hosted Streamlit port publicly.

## What the runner sends

1. **Decomposition:** only the four-field SERA source-only packet, with the frozen `decompose_live_v0.1` system prompt. Human Oracle contents never enter an SDK request.
2. **Projection:** retain the *complete* validated `decompose.parsed.json`. Derive `decompose.reconstruction_projection.json` by removing all unit `source_support` fields; it includes the other structured semantic content and the projection version. Store its canonical bytes and SHA-256.
3. **Paired reconstructions:** two fresh, stateless requests: neutral and commercial. Each sends **exactly the same** saved projection byte sequence as the user input. The neutral response is not available to the commercial request, and the original source packet is unavailable to either reconstruction.

The actual Adaption request parameters are `model`, `instructions`, `input`, `store=False`, `agentic_memory=False`, `tools=[]`. SDK constructor uses `max_retries=0` and a 120-second timeout. **Temperature and seed are not set**; provider defaults apply, and seed is not documented. Unsupported parameters are not silently retried or removed.

Each live stage preserves its original SDK request parameters (excluding authorization), full JSON model response, concatenated output_text, response metadata, output SHA, actual model ID, provider response ID, usage and timestamps. Failed, incomplete, empty and invalid-JSON outputs are preserved, not repaired; subsequent reconstruction stages do not run if decomposition is invalid.

## Comparison policy: two primary human reviews, eight optional diagnostics

A completed run now records **ten** possible comparison types. Two are the
primary human review activities: `oracle_vs_neutral` and
`oracle_vs_commercial`. They appear first in Review. The other eight
comparisons remain available for optional diagnosis; their existence does
**not** require the human author to explain every one.

Two direct source-to-final comparisons were added:
`original_vs_neutral` and `original_vs_commercial`. Their reference is the
immutable source-only packet; their targets are the corresponding completed
final outputs. Incomplete/failed outputs do not create misleading pairs.

Existing studies recorded before this enhancement retain their original
eight comparisons and review events. To add the two new records **without
calling the model again**, open **Results → Archived runs: add missing
original-to-final comparisons → Add missing comparisons for this study**.
This is an explicit, idempotent action; merely opening Results does not
alter archived evidence. A newly generated complete private ZIP will
include the added comparison records.

For live `decomposition_vs_neutral` and `decomposition_vs_commercial`
diagnostics, **Results → Optional reconstruction diagnostics** displays
the full recorded decomposition side by side with the **exact frozen
model-visible reconstruction projection**, with its SHA-256. These are
different artifacts: only the projection was supplied to the model. The
comparison's original full-decomposition reference and identifier remain
unchanged to preserve provenance.

## Full private export and historical reproducibility

Results → **Create complete private ZIP bundle**. It contains the exact pinned Oracle (not the latest amended version), source-only packet, versioned study protocol artifacts (prompts/schema/projection definition), all run metadata and responses, comparisons, review journal and analysis. Full ZIPs are unredacted and **not safe to publish or commit**. The safe JSON summary remains an explicit optional export.

The study stores immutable copies of prompt/schema/projection **bytes**, so a future repository edit does not change a historical experiment or invalidate its ZIP. Legacy fixture studies without snapshots retain the original compatibility export path.

## Kept deliberately separate

- `stu/review.py` and `pages/3_STU_Review.py` remain untouched (Radiant Control's domain).
- Legacy deterministic fixtures remain available through the collapsed **Legacy regression fixtures** section on Transform and through `stu.cli smoke`. They are clearly synthetic, not model results.
- The one-call **Adaption API Test** page remains available for low-cost connectivity checks without creating research artifacts.
- No local inference, agents, tools, memory, automated semantic judges, extra databases, or separate UI execution engine.

## Evidence and limitations

The SDK connectivity check previously reported by Nat for `gemma-4-31b-it` returned `OK` with status `completed`, 18 input tokens and 2 output tokens; that was **not** a three-stage experiment. Mocked live-run tests and existing fixture tests run in CI without a key.

The first user-supplied full private ZIP has now been inspected with three completed live stages and eight original comparisons. Historical records stay unchanged until explicit reconciliation. A valid decomposition and two successful reconstructions establish execution, **not semantic preservation**. Live run state remains `live`, `synthetic=False`, with no semantic correctness verdict.
