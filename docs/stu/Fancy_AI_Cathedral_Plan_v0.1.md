# Fancy AI Cathedral Plan v0.1

## DiScO STU
### Semantic Transformation Utility
#### Project Overview — Experiment 01: From Meaning to Management

**Nat Osit | November 13, 2026**  
**Status:** Consolidated planning draft · Not yet a frozen experimental protocol  
**Research context:** Apart Research AI × Epistemics Research Sprint, November 13–15, 2026

---

## 1. Purpose

**DiScO** stands for *Deterministic Inspection of Semantic Coupling in Outputs*.

**STU** stands for *Semantic Transformation Utility*.

STU extends the existing DiScO research by examining what happens to intended meaning when it is represented, decomposed, transformed, and reconstructed.

The central concern is not whether AI generates plausible prose. It is whether a representation preserves the relationships that made the original argument meaningful.

A transformation can preserve vocabulary, subject matter, rhetorical fluency, and apparent sophistication while omitting, reversing, or changing the relationships between claims.

This problem is not exclusive to AI. Human writing is itself a transformation of intended meaning into a communicable representation. A human author may fail to express an important relationship before any AI system encounters the text.

STU therefore examines the entire representational sequence, beginning with the human author's independently recorded account of what they intended.

**Experiment 01, *From Meaning to Management*, tests what happens when a model reconstructs the same semantic representation as either neutral prose or advice for a commercial business.**

The experiment also measures the human labor required to explain discrepancies between intended meaning and model-produced meaning.

Its guiding question:

**What survives the transformation, what changes, and how much human work is required to explain the difference?**

## 2. Conceptual foundation

The experiment builds on several existing projects and research directions.

**Structured Sparsity** explored how changing the representation of a system can affect what remains accessible, reconstructable, or intelligible without necessarily changing the underlying facts.

**DiScO** developed deterministic methods for inspecting observable features of text, including features associated with semantic fragmentation and reconstruction burden. Its findings motivated a broader distinction between apparent coherence and actual semantic integrity.

**PIQITT** established reusable approaches to structured transformations, evaluation profiles, and portable evidence artifacts.

**MediLacra** demonstrated reproducible testing with synthetic inputs, durable records, and inspectable data transformations.

STU applies these concerns to a new experimental object: **the relationship between authorial intention, written expression, model inference, and subsequent reconstruction**.

The experiment does not assume any representation is inherently faithful.

It also does not assume that every difference is a failure. A model may legitimately resolve ambiguity, summarize, reorganize, or derive recommendations consistent with its input.

The problem is determining which changes preserve the relevant relationships and which introduce a different meaning.

## 3. Research questions

The experiment has three connected questions.

### RQ1 — Semantic survival

To what extent does the author's independently recorded intended meaning survive successive transformations?

This includes the human-authored text itself, the model's semantic decomposition, and the final reconstructions.

### RQ2 — Institutional transformation

Does reconstructing a semantic representation as advice for management of a for-profit company produce different semantic outcomes from reconstructing that same representation as neutral prose?

The comparison holds the model-generated intermediate representation constant and changes the reconstruction purpose.

### RQ3 — Semantic reconstruction cost

How much human labor is required to **explain the gap between what the author intended to communicate and what the AI inferred or reconstructed**?

The human produces an actual explanation of the discrepancy. The experiment records that explanation and measures the time required to produce it.

This is not merely the time required to identify an error or assign a score.

It is the labor of articulating what was misunderstood, omitted, added, or transformed, including the relationships necessary to make the difference intelligible.

A further exploratory question follows: does commercial reconstruction change the amount of explanatory labor required?

## 4. Experimental material and the human reference

The initial corpus comes from the author's existing writing across philosophical, political, technical, and creative or rhetorical domains.

The author is available to explicate their own intended meaning.

This creates a reference unavailable in many conventional evaluations, where another model or an outside reader must infer what the author meant.

The author serves as the **Oracle**, with an important qualification: the Oracle is a frozen, contemporary account of historical intention, not direct access to the author's past mental state.

The original writing remains separate evidence of what was actually communicated.

If the author intended something that was absent from the source text, that constitutes an end-to-end failure of transmission relative to the author's reference. It does not establish that a model failed to infer something the text never expressed.

Both distinctions must remain visible.

### Source selection

Each experimental sample is:

- One contiguous paragraph from an attributable original work.
- Preferably 75–150 words.
- No more than 200 words.
- Preserved without stitching unrelated passages together or arbitrarily truncating them.

Relevant external context may be recorded as a dependency, but is not silently added to model inputs.

The working sprint target is **six to eight paragraphs**, chosen across domains. Twelve paragraphs remains a possible expansion, not a requirement for a minimally complete experiment.

The sample is the grain of corpus-level analysis. Multiple model outputs from one paragraph are related observations, not independent source documents.

## 5. SERA — Semantic Explication Recorded Analytics

**SERA is the preparation stage of the experiment.**

Its purpose is to establish an independent human reference *before* model execution.

SERA will initially be a minimal Streamlit interface.

For each selected paragraph, the author first answers an unrestricted question:

**What did I intend to communicate?**

This free-text explanation is preserved before imposing a structured representation.

The author then decomposes that meaning using the same conceptual categories the LLM will later use:

| Semantic category | What is recorded |
|---|---|
| Claims | Assertions, denials, questions, propositions |
| Actors and objects | Who or what participates |
| Relationships | Connections between actors, objects, and claims |
| Negations | What is explicitly rejected or denied |
| Conditions and scope | Exceptions, qualifications, limitations |
| Dependencies | Relationships requiring other claims or assumptions |
| Rhetorical function | Critique, argument, satire, warning, description, etc. |
| Ambiguities | Uncertainty or deliberate openness |

Claims receive stable identifiers. Relationships can link claims or entities using typed edges.

The schema must accommodate meaningful omissions, uncertainty, and categories that do not apply. It must not require the author to invent semantic structure merely to complete a form.

The author can also record where an intended relationship appears in the source text, or acknowledge that it may not be clearly expressed.

### Freezing the reference

Each SERA record progresses through:

**Draft → Frozen → Amended**

A frozen record is immutable for the scored experiment.

Later corrections become separately recorded amendments rather than replacements.

The entire SERA reference—both free-text and structured—is **withheld from the models**.

The model receives the original paragraph, never the author's independently recorded explication.

## 6. STU — Controlled semantic transformation

For each frozen source paragraph, STU executes the following sequence.

```text
HUMAN INTENDED MEANING
          |
          v
     SERA EXPLICATION
       [FROZEN]
          |
          | HELD OUT FROM MODELS
          |
ORIGINAL WRITTEN PARAGRAPH
          |
          v
    LLM DECOMPOSITION
          |
          v
  FROZEN STRUCTURED JSON
          |
          +------------------------+
          |                        |
          v                        v
NEUTRAL RECONSTRUCTION    COMMERCIAL RECONSTRUCTION
          |                        |
          +------------+-----------+
                       |
                       v
             SEMANTIC COMPARISON
                       |
                       v
             HUMAN GAP EXPLICATION
                       |
                       v
           EXPLANATION + TIME COST
```

### Stage A — Model decomposition

A model receives the original paragraph and produces a structured semantic representation.

It uses the same semantic categories as SERA.

The model should identify supporting spans in the text for its inferred claims and relationships.

The decomposition is validated and frozen.

The model receives neither the SERA reference nor any information about the author's preferred interpretation.

### Stage B — Neutral reconstruction

The same model receives its frozen structured decomposition in a fresh context.

It reconstructs the argument as clear prose while preserving the claims, relationships, negations, qualifications, ambiguity, and rhetorical purpose represented in the JSON.

It must not receive the original paragraph, SERA reference, or commercial output.

### Stage C — Commercial reconstruction

The same model receives the **identical frozen decomposition**, again in a fresh context.

This time it writes actionable advice for management of a for-profit company selling a commercial product in a competitive market.

The institutional objective is commercial performance and continuing viability.

The model is still instructed to preserve substantive claims, constraints, objections, and qualifications.

It may derive defensible recommendations but must not assume unsupported company or product facts.

The initial design leaves the product and industry unspecified to avoid adding unnecessary variables.

The comparison is therefore between two reconstructions from the same input, performed under different purposes.

**A recommendation that extends the original argument consistently is not automatically semantic loss. A recommendation that contradicts or neutralizes the argument's constraints may be.**

### Execution isolation

Each decomposition and reconstruction occurs with fresh conversational context.

The experiment records model identity, runtime, prompt version, parameters, input artifact, and complete output.

Fresh context does not eliminate differences in model training, system instructions, or provider infrastructure.

## 7. Models and experimental scale

The proposed execution environments are:

1. Locally deployed Google Gemma.
2. Locally deployed quantized Qwen.
3. An OpenAI model accessed through the API.

Exact model identifiers, weights, quantization, runtime settings, and API versions must be recorded once selected.

The three deployments are heterogeneous systems, not a controlled comparison of architecture or training data alone.

At six paragraphs, the design produces:

| Operation | Number |
|---|---:|
| Human SERA references | 6 |
| Model decompositions | 18 |
| Neutral reconstructions | 18 |
| Commercial reconstructions | 18 |
| **Model executions** | **54** |
| **Paired neutral/commercial observations** | **18** |

Eight paragraphs would produce 72 model executions and 24 paired observations.

Twelve paragraphs would produce 108 executions and 36 paired observations.

One complete end-to-end pilot should establish that the workflow and instrumentation work before scored execution begins.

The planned corpus supports exploratory, within-sample analysis. It does not support universal claims about model reliability or human semantic behavior.

## 8. Semantic comparison

STU must preserve two distinct ways of evaluating transformation.

### End-to-end survival

Compare each representation against the frozen SERA reference.

This answers whether the author's declared intended meaning survived the full sequence, including any failures already present in the original writing.

### Local transformation fidelity

Compare each output against its immediate parent.

This identifies where relationships were preserved or changed.

The major comparisons are:

| Reference | Target | What the comparison establishes |
|---|---|---|
| SERA | Original paragraph | What survived human expression |
| Original paragraph | Model decomposition | Fidelity of model extraction |
| SERA | Model decomposition | Intended meaning present in model inference |
| Decomposition | Neutral prose | Fidelity of neutral reconstruction |
| Decomposition | Commercial advice | Fidelity of commercial reconstruction |
| Neutral prose | Commercial advice | Paired treatment difference |
| SERA | Either final output | End-to-end semantic survival |

The initial semantic-difference vocabulary includes:

**Preserved, omitted, altered, contradicted, unsupported addition, source-consistent extension, and unresolved or ambiguous.**

Comparisons operate primarily on claims and relationships, not string similarity.

Every substantive judgment should have a rationale and a link to the relevant semantic unit or evidence.

A difference does not automatically establish which transformation caused it. For example, an intended relationship missing from the original writing cannot be classified as an LLM omission merely because it is also absent from the final result.

## 9. Human gap explication and reconstruction cost

This is a central part of the experiment, not an informal commentary added after scoring.

The author compares the frozen SERA meaning with a model-produced representation and explains the differences.

The explanation may identify:

- A relationship the model misunderstood.
- A qualification or negation it omitted.
- A new claim or assumption it introduced.
- A shift in agency, causation, or obligation.
- A reinterpretation of criticism as managerial advice.
- An ambiguity the model resolved without sufficient support.
- A failure in the author's original writing to express an intended relationship.

The resulting explanation is itself an experimental artifact.

### What is timed

**The primary timing measure is the active time required for the human to produce an explanation of the semantic gap.**

It is not defined as the time to click through a checklist or merely notice that two representations differ.

The interface should begin the timed task when the reviewer is presented with the material necessary to perform gap explication, and finish when the explanation is submitted.

Pauses and resumptions are recorded. Idle time is excluded where possible.

The workflow should preserve both the final explanation and the underlying event history.

### Unit of measurement

One review task is associated with one comparison.

A comparison may contain several individual semantic gaps. The time spent explaining them together is recorded at the comparison level, since thinking about multiple related gaps cannot always be separated into independent intervals.

Individual gap explanations can have their own identifiers and classifications.

### Interpretive limits

Elapsed time is an operational measure of explanatory labor, not a direct reading of cognitive effort.

Time may be influenced by output length, fatigue, familiarity, typing speed, and the complexity of the source.

A brief explanation may also be incomplete or mistaken. Lower time is not automatically evidence of better semantic preservation.

For that reason, STU preserves the actual explanatory text alongside duration.

When practical, reviews should conceal model and condition labels, vary presentation order, and retain output lengths.

A completed judgment of **no meaningful gap** must be distinguishable from a missing explanation.

The central empirical object is the relationship between **the semantic discrepancy, the explanation produced to account for it, and the labor spent producing that explanation**.

## 10. Data model

The initial design uses three logical layers.

**Representations:** What each human or model produced.

**Transformations:** How one representation was generated from another.

**Gap explications:** How a human accounted for differences between representations.

A preliminary schema requires approximately eight logical tables.

| Table | Grain | Principal fields |
|---|---|---|
| `samples` | One source paragraph | `sample_id`, source, text, provenance, word count, SHA-256 |
| `explications` | One human or model semantic decomposition | `explication_id`, `sample_id`, producer, free-text meaning, schema version, status |
| `semantic_units` | One semantic element | `unit_id`, `explication_id`, type, content, links, qualifiers, evidence |
| `runs` | One model execution | `run_id`, model, stage, condition, prompt version, configuration, timestamps |
| `artifacts` | One produced representation | `artifact_id`, `run_id`, parent ID, type, content, hash, version |
| `comparisons` | One reference-target evaluation | `comparison_id`, reference ID, target ID, reviewer, status |
| `gap_explanations` | One explicated discrepancy | `gap_id`, `comparison_id`, classification, related units, explanation |
| `review_events` | One human review action | `event_id`, `comparison_id`, action, timestamp |

These are logical tables, not a requirement to implement eight normalized SQL tables immediately.

### Shared semantic schema

Human and model decompositions use the same conceptual structure, but retain distinct producers and epistemic roles.

SERA describes intended meaning.

The model describes meaning inferred from the text.

The shared schema makes comparison possible without pretending the two records have equal authority or access to the same information.

### Artifact lineage

Every generated artifact should identify its input.

In particular, both reconstructions from a given source-model pair must reference the exact same frozen decomposition.

Raw inputs, prompts, outputs, validation errors, and relevant configuration must be retained.

Artifacts and reviews receive separate identifiers. Human amendments and reruns never silently overwrite earlier observations.

## 11. Persistence: JSON, JSONL, and DuckDB

The initial persistence strategy should be deliberately primitive.

**JSON** stores complete structured artifacts: SERA packets, model decompositions, reconstruction outputs, and finalized explanations.

**JSONL** stores append-only sequences of events or records: executions, freezes, amendments, review starts, pauses, resumptions, and completions.

**DuckDB** can query these records and support analysis without becoming the authoritative source of raw experimental history.

The distinction is practical:

**JSON preserves a representation. JSONL preserves the record of what happened.**

Neither format guarantees immutability, confidentiality, or transaction safety by itself.

Stable IDs, source hashes, controlled writes, and explicit revision policies provide the necessary additional discipline.

Local persistence is sufficient for the initial experiment. A hosted database is unnecessary.

Private Oracle references and unpublished writing should remain local unless explicitly selected for publication.

## 12. Existing code harvest

The project should reuse existing capabilities rather than recreate them unnecessarily.

| Existing project | Candidate harvest |
|---|---|
| Structured Sparsity | Representation and relationship-modeling methods |
| DiScO | Text input, extraction, hashes, JSONL persistence, evidence inspection |
| PIQITT | JSON transformation, validation, scorecard, and export patterns |
| MediLacra | DuckDB integration, repeatable execution, test-fixture patterns |
| Existing Streamlit applications | Forms, configuration, tables, raw artifact inspection, downloads |

**DiScO's existing judgment storage is a particularly useful starting point.** It already records identifiers, timestamps, source hashes, configuration fingerprints, and structured evidence in append-only JSONL.

It should be generalized for STU without carrying over assumptions that textual style scores determine semantic meaning.

Existing components should be assessed for actual suitability rather than copied wholesale.

The original repositories use different software licenses. Direct code imports require explicit provenance and license review before inclusion under Disco-STU's public noncommercial licensing arrangement.

## 13. Minimal application architecture

SERA is the first working interface and should establish reusable conventions for STU.

A minimal Streamlit application needs three pages.

### SERA — Capture

Select a paragraph, record free-text intention, enter structured semantic units, and freeze the source-and-intent packet.

### STU — Transform

Select eligible frozen samples, execute model decomposition, reconstruct under the two conditions, validate outputs, and retain all artifacts.

### Review — Explain

Display reference-target pairs, record semantic differences, time human gap explication, preserve review events, and export evidence.

All pages should share:

- Common schemas and identifiers.
- The same persistence interface.
- Explicit save, freeze, and amend operations.
- Consistent validation and error reporting.
- Downloadable raw artifacts and evidence.
- A basic, reusable Streamlit layout.

An interface rerun must not silently mutate frozen data or reset an active review measurement.

The initial design should favor plain Streamlit components over elaborate styling, autonomous agents, dashboards, or custom frontend infrastructure.

**SERA is the first consumer of the reusable application conventions, not a separate application that later requires another migration.**

## 14. Experimental validity

The experiment needs a small amount of instrument validation before interpreting its measurements.

A separate set of deliberate semantic mutations can test whether the comparison method detects:

- Faithful paraphrases.
- Negation reversals.
- Changed actors.
- Removed conditions.
- Invented source claims.

Expected judgments should be recorded before applying the rubric to scored outputs.

These checks evaluate the comparison method. They do not constitute a new model treatment.

Where practical, a second reviewer can evaluate textual fidelity independently. That reviewer can challenge whether a reading is supported by the written passage without replacing the author's frozen reference for intended meaning.

### What would challenge the hypotheses?

The commercial framing hypothesis receives no support if commercial reconstructions are no less faithful than their paired neutral reconstructions under the tested conditions.

If most losses arise during human expression or initial model decomposition, the experiment may identify those stages as more consequential than reconstruction framing.

The explanatory-labor hypothesis may also yield a negative or mixed result. Commercial outputs could be easier to explain, or explanation duration might have little relationship to recorded semantic divergence.

These are legitimate findings.

No result should be presumed merely because the prompt makes a particular distortion imaginable.

## 15. Scope and deliverables

The initial sprint is not intended to deliver a production software platform.

Its minimum completed experiment consists of:

1. A frozen set of source-and-intent packets produced by SERA.
2. A reproducible model runner with independent reconstruction branches.
3. Complete source-to-output lineage.
4. A semantic comparison rubric with human judgments.
5. Timed, preserved human explanations of identified gaps.
6. An analysis of paired outcomes and explanatory labor.
7. A research report grounded in actual recorded results.

A complete one-paragraph pilot should precede the larger sample.

The initial target is six to eight paragraphs and three model deployments, adjusted only according to what can be executed and reviewed reliably.

The research report should distinguish inherited infrastructure and pre-sprint work from work actually conducted during the sprint.

No scores, findings, or validation outcomes are claimed until the corresponding experimental artifacts exist.

## 16. Boundaries and outstanding decisions

### Established design direction

- Human-authored text, not speech transcription, is the experimental input.
- One paragraph constitutes one source sample.
- SERA produces a frozen, held-out reference before scored model execution.
- Human and model semantic decompositions share a schema.
- Models reconstruct their own frozen decompositions in fresh contexts.
- Neutral prose is the control; commercial-management advice is the treatment.
- End-to-end semantic survival and local transformation fidelity are distinct.
- Human gap explanations are retained as evidence.
- Time spent producing those explanations is a measured outcome.
- The application begins as a minimal local Streamlit system using durable artifacts.

### Still to specify before scored runs

- Exact shared semantic schema and relationship types.
- Model identifiers and inference settings.
- Final decomposition, neutral, and commercial prompts.
- Corpus composition and selection procedure.
- Detailed semantic-difference adjudication rules.
- Timing event definitions, interruption handling, and review ordering.
- Definition of a completed explanation.
- Whether and how explanation completeness receives independent review.
- Final storage serialization and validation contracts.

These decisions should be resolved and versioned before interpreting scored data, not repeatedly adjusted in response to whether the findings look interesting.

## 17. Interpretation

The original DiScO project asked whether sophisticated-looking text could nevertheless impose substantial semantic reconstruction work on its reader.

STU gives that concern an experimental structure.

It begins with an author who can state what she intended. It preserves the writing through which she attempted to communicate that meaning. It observes what models infer and what they subsequently reconstruct under different institutional purposes.

It then asks the author to explain the difference.

The resulting record contains not merely a statement that meaning was lost, but **what was lost, where the discrepancy appeared, how the author explained it, and how much time producing that explanation required**.

That provides a way to investigate whether apparently fluent transformations relocate the labor of maintaining semantic integrity onto a human downstream.

The hypothesis may or may not be supported.

The infrastructure should make either result equally observable.

**Hold the source constant. Change the representation. Change the purpose. Record what survives—and the human work required to explain what doesn't.**

---

**Project repository:** [natosit-dev/Disco-STU](https://github.com/natosit-dev/Disco-STU)

**Status of this document:** Fresh consolidated overview for review. Earlier versions remain archived for provenance. This document contains no invented experimental findings and does not assert that the proposed software has been implemented.
