# DiScO STU — The Nerd Handoff
## Finish the instrument before the author tests it

**Experiment 01:** *From Meaning to Management*  
**Handoff v0.1 · 14 November 2026**  
**Target repository:** `natosit-dev/Disco-STU` — https://github.com/natosit-dev/Disco-STU  
**Author/research owner:** Nat Osit  
**Implementer:** The Nerd  
**Status:** Build instructions. This is not evidence of completed downstream code or research results.

> **Nat, 14 Nov:** “Let's create a handoff doc for The Nerd for the rest. We'll build the whole thing, then I'll test it piece by piece (I'm busy today but want to make progress)”

**That is the operating instruction.** Build the complete instrument—STU model execution, paired reconstructions, comparisons, human gap explication/timing, reporting, persistence, configuration, tests and documentation. Do not interrupt Nat between phases for manual test clicks. Test the software with deterministic synthetic fixtures yourself, and deliver one coherent branch with a staged acceptance walkthrough for her later. Model credentials, human Oracle judgments and scored experimental runs are separate gates. Never say they happened just because a synthetic fixture passed.

---

## 0. Start with what already exists

Public repo `main` was at commit `a8bdd1bb0d9d1ff73ed5bfccfb50eb93f083dffa` when inspected for this handoff. Recheck the current head before making a branch. SERA v0.1 is already checked in; its main implementation commit was `bb4b9fed8a679ee0701feaf0cd7be89c05c27abc`.

- `app.py`, `pages/1_SERA.py`: Streamlit human capture.
- `sera/schema.py`, `schemas/semantic_v0.1.json`: shared structural vocabulary and validation.
- `sera/service.py`, `sera/storage.py`, `sera/exports.py`: progressive human explication, draft/freeze/amend, source-only export.
- `tests/test_sera.py`, `tests/test_schema_contract.py`: 11 existing backend/schema tests; rerun them and do not conflate them with UI/browser verification.
- `docs/sera/BUILD_PLAN_v0.1.md`, `docs/sera/DATA_CONTRACT.md`: the approved SERA contract.
- `docs/stu/DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12_BASELINE.md` and `docs/stu/DiScO_STU_From_Meaning_to_Management_v0.4_REVIEW_SERA_ADDENDUM_2026-11-13.md`: archived research evolution.
- `docs/stu/Fancy_AI_Cathedral_Plan_v0.1.md`: additional consolidated technical content; its title is historical, not the naming convention to continue.

A later **Nat-style v0.5 Word planning document** exists in the source conversation; it was **not verified in this repository** during this handoff. This handoff deliberately reproduces its operative requirements so The Nerd can proceed from the repo. Preserve older documents and decision history; do not append contradictory conceptual patches to them.

**Read and test the existing code before modifying it.** Preserve SERA's record formats unless a versioned migration is needed. Keep model-facing code entirely separate from private Oracle loading. Treat the current Streamlit pages as an interface, not as the repository's data model.

## 1. What the experiment actually asks

The research questions are distinct:

1. **Semantic survival:** Does Nat's independently explicated intended meaning survive the original act of writing, model decomposition and later reconstruction?
2. **Institutional frame:** Does reconstruction as advice for management of a for-profit business selling a commercial product alter meaning compared with a neutral reconstruction generated from **the same frozen model decomposition**?
3. **Explanatory labor:** How long does Nat spend **explaining the gap between what she wanted to convey and what the AI inferred/reconstructed**?

**Not** how quickly she notices an error. The human gap explanation is the work product. Its event-derived active production time is the operational cost measurement. Store both the work and the time.

An LLM can produce an entirely plausible reading and still miss authorial intention. Conversely, the original writing might never have expressed part of that intention. Preserve the distinction; don't blame the model for a gap already present at the human-writing boundary.

### Data flow

```text
HUMAN INTENTION (historical mental state not directly observed)
    |
    +-- SERA: original text + free intention + category prose + units/edges
             |
             +-- PRIVATE, FROZEN ORACLE: exact version and hash
             |
             +-- MODEL-VISIBLE SOURCE-ONLY PACKET (four allowlisted fields)
                      |
                      v
              LLM SEMANTIC DECOMPOSITION
                      |
              FROZEN STRUCTURED JSON
                      |
                +-----+-----+
                |           |
           FRESH CONTEXT  FRESH CONTEXT
           NEUTRAL       COMMERCIAL MANAGEMENT
           RECONSTRUCTION RECONSTRUCTION
                |           |
                +-----+-----+
                      |
              SEMANTIC COMPARISONS
                      |
             HUMAN GAP EXPLICATION
                      |
              TEXT + ACTIVE DURATION
                      |
              ANALYSIS AND EXPORT
```

**Out of scope:** transcription, forced assignment generation, model-generated Oracle entries, automatic managerial action, unapproved extra treatments, ungrounded slop scoring, simulated human judgments, invented empirical findings.

## 2. Work autonomously, without modifying the research by accident

Create a feature branch, for example `feature/stu-complete-pipeline-20261114`. Keep coherent commits, automated tests and technical documentation. Complete the whole software system before asking Nat for acceptance clicks. Offer one PR/branch link and a short walkthrough after coding. Do not push blind overwrites to `main`.

Use a deterministic **fake model adapter** for the full development cycle. Wire real provider adapters and local runtime configuration, but if the local models or API credentials aren't available, mark them **unverified** with exact later smoke-test commands. An absent API key is not a reason to stop building the Review page. A passing fake-model test is not evidence that Gemma/Qwen/OpenAI behaved a certain way.

Use only fictional/synthetic samples in committed test fixtures. Do not use SHN confidential material, unapproved writing, source intentions or private model payloads as fixtures. Keep all runtime data under `data/`, which is gitignored.

Do not conduct scored model experiments or create human Oracle annotations on Nat's behalf. Provide a visibly separate `synthetic_test`, `pilot`, and `scored` mode. Require a frozen study manifest and deliberate scored-run action before execution; development defaults to synthetic or pilot.

**Version decisions rather than guessing.** Implement adjustable pilot defaults for model profiles and timer protocol and record exactly which were used. Nothing in this handoff authorizes quietly changing the experimental intervention after seeing favorable results.

## 3. SERA remains the held-out boundary

The SERA sequence Nat approved is **source paragraph → unrestricted intended meaning → category-level prose → structured units and relationships → freeze**. Preserve the three human representation layers separately. SERA does no model inference and no timer-based gap review.

The source-only packet in `sera/exports.py` has exactly:

```json
{
  "packet_type": "stu_source_v0.1",
  "sample_id": "<uuid>",
  "source_sha256": "<SHA-256>",
  "original_text": "<exact paragraph>"
}
```

The runner loads **only this packet**. It must not send SERA's free intention, human category prose, human semantic units, private context dependencies, provenance or amendments to an LLM. The model may later *produce its own* `category_prose`; that does not permit using the human's version.

**Important integration fix:** `SeraStore.latest_frozen(sample_id)` currently retrieves the latest amendment. Each scored study needs to **pin an exact Oracle artifact ID/version/hash** and Review must load that version, not whichever is latest months later. Implement read-by-version or read-by-content-address in SERA storage without breaking historical records. The source packet and its hash stay the same after amendments; amendments to intention do not rewrite the past experiment.

SERA's backend tests previously passed, but its browser interaction was not verified at handoff time. Smoke test source creation, stage gates, data editors, saves, reload, freeze, source-only download and amendment in a real Streamlit session when possible.

## 4. Build the full STU model runner

### 4A. Provider-neutral adapters

Implement model handling outside Streamlit, with a small adapter interface:

```python
@dataclass
class GenerationResult:
    content: str                # exact returned text
    provider_response_id: str | None
    model_reported_id: str | None
    usage: dict                 # may be unavailable
    finish_reason: str | None
    request_metadata: dict
    response_metadata: dict

class ModelAdapter(Protocol):
    def generate(self, *, system: str, user: str, settings: dict) -> GenerationResult: ...
```

Planned provider *classes*:

- **Local Gemma**, using Nat's actual installed inference runtime. The model is Gemma, not Gemini. Inspect available runtimes rather than guessing a port or model identifier.
- **Local quantized Qwen**, recording model tag, quantization and runtime. May share transport with Gemma if the local API warrants it.
- **OpenAI API**, with a selected exact model ID, credentials from environment/secret store, and no secrets in artifacts or Git.
- **Deterministic fake adapter**, available offline to exercise every stage without a network or pretending to have experimental results.

Profiles should live in a nonsecret example config; real runtime settings in an ignored local file or environment. Record true model IDs, provider response IDs, model revision/weights where available, decoding settings, quantization, seed (if supported), token limit, timing and token usage where returned. An unavailable adapter fails visibly; **never silently substitute another provider**.

### 4B. Decompose once for each source/model pair

Input is **only** the model-visible source packet, prompt/schema instructions and necessary execution metadata. Output is a source-linked semantic decomposition conforming to `schemas/semantic_v0.1.json`: `category_prose`, `units`, `relations`. Use its eight categories, enums, stable *local* IDs and typed edges. Never assume model unit IDs match SERA IDs.

Ask models to identify evidence in the paragraph and preserve negations, scope, uncertainty, dependencies, rhetorical role and unresolved ambiguity. If source support is absent, represent uncertainty/unsupported inference explicitly; don't force fabricated quotes. The existing SERA **human freeze** rule requiring at least one unit need not automatically become a rule requiring a model to invent a proposition from an uninterpretable source. Document any validation-policy differences.

Save **raw response**, parsed output, schema errors, prompt/schema hashes, model settings, input hash, timestamps, usage, error/timeout/retry history. Invalid JSON is an observable result, not a file to throw away. A repair or retry is a distinct, logged attempt and cannot overwrite the first response.

### 4C. Reconstruct twice from identical frozen JSON

For each successful `(sample, model, decomposition)`:

**Neutral/control:** Use only the frozen decomposition in an empty conversational context. Reconstruct clear prose preserving substantive claims, negations, qualifiers, ambiguity, dependencies and rhetorical purpose. Do not add recommendations.

**Commercial/treatment:** Use the **exact same frozen decomposition**, in a separate empty context. Write concrete advice for management of a **for-profit business selling a commercial product in a competitive market**, aimed at commercial performance and continued viability. Still preserve substantive claims, objections, negations and constraints. Do not invent company or product facts; say when the material does not support a particular recommendation.

**Hard invariants:** neither reconstruction gets the original paragraph, SERA Oracle, SERA context notes, sibling output or previous chat history. Both point to the **same intermediate artifact hash**, not merely similar JSON content. If a branch fails, keep an incomplete pair; don't quietly re-decompose one branch and report it as controlled.

### 4D. Prompt versioning and clean boundaries

Keep versioned prompt files under `prompts/`: `decompose_v0.1.txt`, `neutral_v0.1.txt`, `commercial_v0.1.txt`. Store each exact SHA-256, the request construction code version and the schema hash. Development prompts may be tuned; **scored prompts must be frozen** in the study manifest before real evaluations. No editing prompts in the UI after a scored run starts.

Initial prompt wording is a **candidate implementation**, not a completed protocol. The underlying treatment (commercial product-selling business versus neutral prose) must remain unchanged unless Nat explicitly changes the experiment.

## 5. Capture artifact lineage, not just pretty outputs

Preserve the eight logical grains already proposed for STU, even if some are nested JSON rather than separate SQL tables:

| Logical entity | One record per | Links that matter |
|---|---|---|
| `samples` | Original paragraph | sample ID, exact text hash |
| `explications` | SERA intention or model decomposition | producer, epistemic role, parent/source |
| `semantic_units` | Claim, object, actor, qualifier etc. | explication ID, local unit ID |
| `runs` | Model execution attempt | input hash, provider, model config, prompt hash |
| `artifacts` | Immutable produced representation | run/parent IDs and content hash |
| `comparisons` | One reference ↔ target review task | exact reference and target artifacts |
| `gap_explanations` | One human description of a discrepancy | comparison ID and related units/evidence |
| `review_events` | One timing/interaction event | comparison ID, actor, sequence, UTC time |

Prefer **JSON for complete frozen artifacts**, **JSONL for append-only event records**, and DuckDB (optional) for derived analytical views, consistent with DiScO's existing patterns. No database server is needed for a single-user instrument. Keep SERA's established paths stable.

Suggested additional structure; change it if a smaller, testable design is cleaner:

```text
stu/
  models/{base,local,openai_api,fake}.py
  prompts.py
  runner.py
  study.py
  artifacts.py
  comparisons.py
  review.py
  analysis.py
  cli.py
pages/
  1_SERA.py                   # existing; preserve
  2_STU_Transform.py
  3_STU_Review.py
  4_STU_Results.py            # optional
prompts/{decompose,neutral,commercial}_v0.1.txt
config/model_profiles.example.yaml
schemas/stu_run_v0.1.json
schemas/stu_review_v0.1.json
tests/test_model_isolation.py
tests/test_runner.py
tests/test_review_timer.py
tests/test_analysis.py
tests/test_synthetic_e2e.py
data/                         # already ignored
  private/sera/<sample_id>/
  stu_inputs/<sample_id>.json
  runs/<run_id>/
  reviews/<comparison_id>/
  studies/<study_id>/
  exports/
```

Common fields: `study_id`, `sample_id`, `run_id`, `attempt_id`, `stage`, `condition`, `input_artifact_id`, `input_sha256`, `output_artifact_id`, `output_sha256`, `parent_artifact_id`, `schema_version`, `schema_sha256`, `prompt_version`, `prompt_sha256`, `model_profile`, `actual_model_id`, `decoding_settings`, `usage`, `started_at`, `completed_at`, `status`, `error`, `retry_of`, and `privacy_class`.

**Frozen means frozen** for study and run artifacts. Record amendments as new artifacts or events. A file hash detects unexpected local changes but does not magically provide adversarial tamper evidence, and JSONL does not create multi-file transactions. Document the guarantees actually implemented. Never commit user source texts, private Oracle content or API request/response bodies.

## 6. Build the comparisons and human Review page

### 6A. Distinct comparisons, distinct inference boundaries

Generate review tasks with explicit kind and immutable artifact references:

1. **SERA Oracle vs original paragraph** — human expression / encoding.
2. **Original paragraph vs model decomposition** — what the model inferred from the available text.
3. **SERA Oracle vs model decomposition** — end-to-end intention versus AI inference.
4. **Model decomposition vs neutral prose** — local neutral reconstruction fidelity.
5. **Model decomposition vs commercial advice** — local commercial reconstruction fidelity.
6. **Neutral vs commercial outputs** — paired condition contrast (same frozen intermediate).
7. **SERA Oracle vs each final output** — end-to-end result in both conditions.

These comparisons cannot be pooled into one undifferentiated “meaning score.” Some targets are free prose rather than structured units. Allow human evidence spans and unrestricted explanation without secretly running an extra LLM to structure the outputs. Automatic text diff is ancillary, not a semantic verdict.

### 6B. What the reviewer actually does

The Review interface should show the relevant pair, the exact pinned Oracle **only when the comparison's reference requires it**, the immediate parent/source chain, raw artifacts and immutable hashes. Mask model/condition labels where reasonably possible; commercial prose may reveal its own genre, so don't claim perfect blinding. Shuffle order deterministically using a saved seed, so Streamlit reruns cannot reshuffle it.

For every comparison, preserve:

- `not_started`, `inspecting`, `explaining`, `paused`, `completed`, `amended`, `invalidated` statuses;
- the author's **unrestricted written gap explanation** as the primary human artifact;
- optional individual gaps linked to units/evidence with categories `preserved`, `omitted`, `altered`, `contradicted`, `unsupported_addition`, `source_consistent_extension`, `unresolved_ambiguous`;
- a separate **completed / no meaningful gap** outcome, never inferred from empty text;
- independent rationale for each meaningful relationship judgment;
- complete record of review ordering, earlier exposure, reviewer actions and amendments;
- exact Oracle version/hash used, including when a new amendment exists later.

Never convert an end-to-end SERA-to-output gap automatically into a claim of model failure. The missing relationship may already have been absent from the written source. A legitimate commercial recommendation may extend rather than contradict the representation.

### 6C. Timed *gap explanation*, not error spotting

> **Nat:** “Oh shit we should time the final human review about what was lost in the transformation. THAT IS THE SEMANTIC RECONSTRUCTION COST”
>
> **Nat's correction:** “I feel like you don't quite get it, though you're close. It's measuring the cost of explaining the gap between what I wanted to convey and what the AI inferred”

Time the human work of **formulating and recording that explanation**. The default *pilot* protocol can present the pair for untimed inspection, then expose a deliberate **Begin gap explication** button to start active-time measurement. Pause/resume and submission stop/interleave active intervals. This is a **candidate timing protocol**, not yet approved for scored research; store its version visibly and make it configurable before study freeze.

Persist events: `begin_explanation`, `pause`, `resume`, `save_draft`, `complete_explanation`, `amend`, and interrupted/recovered status when applicable. Calculate active duration from **persisted intervals**, not an in-memory counter reset by Streamlit reruns. Repeated clicks must be idempotent or rejected, and a browser reload must not silently inflate or erase time. If using monotonic in-session timing, preserve wall-clock event evidence too; document clocks, uncertainty and interruption behavior.

One comparison may contain several gaps. The primary duration belongs to the **whole explanatory task**, not forcibly apportioned across individual claims. Preserve explanation text, word count, revisions, number/type of gaps, timing protocol, interruptions and no-gap outcome. A quick but incomplete explanation is not evidence of small reconstruction cost.

The same source may be reviewed repeatedly under different models and conditions. Record review order and prior exposure; memory, fatigue, length, familiarity and typing speed are possible confounds. Do not fabricate causal precision.

## 7. Study manifests and analysis

Create a study manifest that can be drafted, piloted, and explicitly frozen for scored work. It pins:

- selected sample IDs, exact original source hashes and **exact frozen Oracle versions/hashes** (available to Review only);
- model profiles, actual runtime/model/weights/quantization and decoding settings;
- decomposition, neutral and commercial prompt file versions/hashes;
- shared semantic schema and validation policy;
- retries, sampling and failure policy;
- comparison rubric version, review-order seed and timing-protocol version;
- creation/freeze times, implementation commit and a manifest checksum.

A scored run refuses to start without an approved immutable manifest. A later fix creates a **new version**, not a silent rewrite of the old study. Never let the model runner read Oracle references just because they exist in a study manifest; split manifest views or fields by role.

The independent **source-sample** grain is a paragraph. Within each source/model pair, neutral and commercial outputs are paired. Six paragraphs × three models × (one decomposition + two reconstructions) would yield **54 calls / 18 paired observations** if no retries or failures; those are planned counts, not observed results. Eight paragraphs yields 72 calls / 24 pairs. Report exact completed calls, incomplete pairs, retries and missing reviews.

Implement a local analysis/export layer that can produce:

- **Coverage matrix:** sample/model/decomposition/neutral/commercial and human-review completion, with failed and unavailable states retained.
- **Lineage view:** source → decomposition → both branches → comparison → human explanation/event journal, with hashes and IDs.
- **Semantic comparison table:** counts and examples by relationship and human label; separate end-to-end survival from immediate-parent fidelity.
- **Paired treatment contrasts:** only pairs with the identical frozen intermediate; do not treat two branches as independent paragraphs.
- **Explanatory labor:** active seconds, protocol version, explanation length, completeness and gap classifications; compare conditions without equating quickness with accuracy.
- **Validation controls:** known faithful paraphrase versus deliberately modified negation, actor, scope or invented claim; expected labels frozen before adjudication.
- **Clear negative/ambiguous cases:** do not rank models universally from one author's exploratory corpus.

Use a modest CSV/JSON/JSONL export or DuckDB views if helpful. Don't build a dashboard before the data lineage works. Default publication exports must be **private-safe**; publishing real source writing, model responses or Oracle annotations requires explicit item-level selection by Nat. The code must not silently upload anything to a service beyond the chosen model API.

## 8. Finish the user-facing app *and* CLI

Keep Streamlit primitive: **SERA / Capture**, **STU / Transform**, **Review / Explain**, optionally **Results / Export**. Reuse the existing application's explicit save/status, JSON download and error conventions. Do not replace it with React, a hosted platform or a generalized agent framework.

Make the backend runnable without the UI, using real commands documented in the README (these are proposed names, adapt and document):

```bash
python -m stu.cli doctor                         # dependencies and model profiles
python -m stu.cli smoke --adapter fake          # full synthetic path, no creds
python -m stu.cli run --study <draft> --model <profile> --mode pilot
python -m stu.cli validate --study <id>          # links, checksums, paired inputs
python -m stu.cli analyze --study <id>           # local reports/coverage
python -m pip install -r requirements-dev.txt
pytest -q
streamlit run app.py
```

The fake adapter should produce **obviously labeled synthetic** outputs for both a faithful and a deliberately distorted case. The synthetic Review record can exercise form and timer calculations, but it must never masquerade as Nat's human judgment. The model runner UI should display profile availability, source/branch states and precise artifact links; asynchronous/batch UI progress must not imply success before actual artifacts exist.

## 9. Tests and evidence of completion — The Nerd owns these

Maintain SERA's existing tests, then extend to cover:

1. **Boundary checks:** source-only packet is the sole model input source; secret marker in every SERA field is absent from serialized model requests; Oracle is accessible only in Review.
2. **Version pins:** later Oracle amendments never change a past scored comparison or run manifest. Test read-by-version and source hash stability.
3. **Schema:** valid/invalid JSON, missing/broken unit IDs, unsupported source evidence, empty categories, precise errors and raw response retention.
4. **Same intermediate:** neutral and commercial conditions reference **identical** frozen JSON hash; no extra decomposition call to fabricate a pair.
5. **Fresh contexts:** no previous messages, original paragraph, SERA, or sibling output inside either reconstruction request. Inspect the actual outgoing serialized request, not just internal Python arguments.
6. **Adapters:** offline fake; local runtime unavailable/timeout; OpenAI missing key; explicit failures; no fallback provider or leaked credential.
7. **Storage:** event-journal replay, corrupt checksum detection, atomic artifact writes, retry-as-new-attempt, immutable frozen records and visible partial failure recovery.
8. **Review timing:** start, pause, resume, complete, reload, double click, interruption, amendment; event-derived intervals remain consistent; blank incomplete review differs from completed no-gap.
9. **Review science:** exact comparison kind/reference/target, deterministic masked order, correct original-versus-intended boundary, unpaired data excluded from paired analysis.
10. **Analysis:** synthetic data labeled; planned counts not reported as actual results; missing branches/reviews retained; no false statistical independence.
11. **Privacy:** data directory ignored; default export doesn't contain Oracle or user source; no secrets in traces; approved publication is explicit.
12. **Browser smoke:** SERA capture/freeze/amend, STU mock execution, Review timer/no-gap, Analysis/export and restart. State precisely which screens were actually exercised.

Tests run offline by default. Make real-network integration tests opt-in. Do not claim Gemma/Qwen/OpenAI integration verified without a successful, logged smoke test against each actual runtime. If a local environment blocks browser testing, document the blocker and finish everything else.

## 10. Definition of done and Nat's *later* acceptance sequence

The Nerd is done when one coherent branch contains the SERA integration, all model interfaces, offline mock full-path execution, real-provider adapters/config templates, frozen intermediate and paired branches, version-pinned review, timed human gap explanations, artifact lineage, analysis/export, tests and instructions. Deliver a changed-file inventory, test outputs, any unverified model integration status, configuration requirements and PR/commit link.

Only **after the whole instrument is assembled**, Nat can test it step by step:

| Later walkthrough | What Nat does | Evidence she can inspect |
|---|---|---|
| **1. SERA** | Paste a real distributable paragraph; free intention → category prose → units/edges → freeze; restart and amend | Private Oracle version + separate four-field STU source packet; prior freeze remains unchanged |
| **2. Decomposition** | Execute one sample and one available real model | Exact input source packet, prompt/model settings, raw response, parsed semantic JSON; no Oracle leak |
| **3. Paired reconstructions** | Generate neutral and commercial outputs from that model's frozen decomposition | Two fresh request payloads, **same intermediate hash**, original/Oracle/sibling absent |
| **4. Review and timer** | Explain an actual discrepancy; pause/resume; save and complete; separately complete a no-gap case | Explanation text, gap links, timeline, active seconds; no-gap ≠ incomplete |
| **5. Whole study** | Select corpus and approve frozen protocol, execute available models, review, examine paired contrasts and labor results | Exact manifests, hashes, coverage, failures, negative cases, reproducible local exports |

No need to request these human tests during the build. Generate short scripts with observed-vs-expected checkpoints. Nat is busy today; her job later is **research judgment and acceptance**, not supervising every line of implementation.

## 11. Open decisions — implement reversibly, freeze before scored runs

| Decision | Default during development | Required scored-study freeze |
|---|---|---|
| Local Gemma/Qwen runtimes | Inspect actual existing installation and configure adapters; offline fake works regardless | Exact model weights/ID, quantization, runtime and inference settings |
| OpenAI endpoint | Adapter and ignored credential configuration | Exact model ID, sampling parameters, response mode and limits |
| Commercial treatment | General for-profit product-selling management | Final instruction text and whether product industry remains unspecified |
| Timing boundary | Untimed inspect, explicit **Begin gap explication**, pause/resume/complete | Timer protocol, interruption policy, explanation completeness criteria |
| Semantic-difference rubric | Typed manual annotations plus free explanation | Exact definitions, expected-control labels, adjudication thresholds |
| Corpus | Purely synthetic test fixtures | Nat's chosen paragraphs, source hashes and frozen Oracle versions |
| Experiment mode | Synthetic or pilot only | Explicit approved immutable study manifest |
| Publication | Private local outputs | Nat's per-artifact clearance and actual disclosure |

Only stop the build if there is a genuine technical incompatibility that cannot be isolated behind a configuration choice. Otherwise preserve the uncertainty explicitly and build the reversible default.

## 12. Intellectual and ethical boundary

The instrument can observe source writing, Nat's current retrospective account of her intention, model-inferred structured meaning, two model reconstructions, and the labor of authoring a gap explanation. It **cannot** directly observe historical mental states, real business decision-making, unrecorded cognition or model “understanding.” An attractive commercial memo is not proof of semantic preservation; a dead fish in a platform shoe is not proof that the historical sales numbers were false. Neither the software nor the report should infer more than the evidence supports.

**The Nerd builds evidentiary infrastructure. Nat owns intended meaning, substantive gap explanations and the ultimate research interpretation.**

---

### Implementation decision lineage (append; do not rewrite old decisions)

The Nat-style v0.5 planning file recorded **STU-D001 through STU-D038**; those prior decisions remain the source history. This handoff adds:

- **STU-D039 — Progressive SERA implementation (adopted, 14 Nov):** Nat selected unrestricted intention → category prose → structured units and relations; current code implements the initial version. Verify full UI behavior.
- **STU-D040 — Complete-build handoff (adopted, 14 Nov):** The Nerd builds the whole instrument and self-tests with synthetic data before Nat performs staged interactive acceptance.
- **STU-D041 — Exact Oracle version pin (implementation safeguard proposed, 14 Nov):** Never silently use the latest amended Oracle in an old study; freeze an exact reference ID/version/hash.
- **STU-D042 — Timer pilot convention (candidate, NOT scored-protocol approval):** Untimed inspection followed by explicit start of gap explanation, paused/resumed active time, explanation + event history.
- **STU-D043 — Offline fake-adapter proof (implementation safeguard proposed):** Full-path tests without claiming real model execution.
- **STU-D044 — Explicit study-freeze gate (implementation safeguard proposed):** Distinguish synthetic/pilot/scored and freeze all critical study inputs before scoring.

Any later decision change receives a new ID, date, evidence/source, status and rationale, not another silent rewrite of the foundation.
