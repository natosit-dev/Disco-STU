# DiScO STU — From Meaning to Management · Nat-style consolidated plan v0.5

**Source DOCX:** `DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.5_2026-11-13.docx`  
**Original DOCX SHA-256:** `8c4e81ccd6b84ce54884aa7b9a2176f9b97a73710d0dcef2e85de83c00daceee`  
**Provenance:** Complete textual transcription of the source DOCX into Markdown, retaining document order, raw-prompt blocks, tables, and linked URLs where present. Markdown is not a byte-identical copy of the Word file or its visual layout.

---

## DiScO STU

### From Meaning to Management

**Semantic Transformation Utility  ·  Experiment 01  ·  Nat-style consolidated plan v0.5**

**Nat Osit  ·  13 November 2026  ·  Apart Research AI × Epistemics Sprint**

**RESEARCH PLAN / WORKING DRAFT / NOT A FROZEN PROTOCOL**

**EARLIER DISCO PROMPT · SEPTEMBER 2026**

> It's the social appearance of intelligence and competency, but the semantic coupling is too sparse and all the variables are implicit/not defined. It drains the cognitive energy/labor power of people who encounter it on its own merits. It's expensive for me to read slop because I begin from the assumption it's not entirely AI generated, so I have to decode the elegant structure and drag it down to earth. Over time, I recognize the pattern quicker

That was the problem before there was an experiment. The cost was already there. STU gives me a way to observe a particular form of it instead of just recognizing the pattern and swearing at the screen.

This plan replaces the working narrative, not the historical record. Prior documents remain preserved. No model outputs or scored findings are claimed here.

## 1. What I actually want to find out

**RAW PROMPT · CONTEST APPLICATION**

> I'm obsessed with finding out how meaning is produced, represented, transformed, and where it decouples from reality.

**RAW PROMPT · ORACLE CORRECTION**

> I'm going to question this.... The purpose is to see if my meaning survived, not if it's able to construct something plausible from it

I have a lot of writing across technical, political, philosophical, rhetorical, and creative domains. That gives me an unusually convenient source: I can ask the author what she was trying to say. It does not give me a representative sample of humanity, and it does not turn my recollection into direct access to a thought I had fifteen years ago.

The experimental object is the transformation from intended meaning into written language, from written language into model inference, and from a model's structured inference into reconstructed prose. I am interested in whether the relationships survive, not whether the last paragraph sounds intelligent or uses the same nouns.

DiScO means Deterministic Inspection of Semantic Coupling in Outputs. STU means Semantic Transformation Utility. DiScO inspects observable representations; STU produces controlled transformations and records what happened. The first STU experiment is From Meaning to Management.

Research questions: (1) What survives end to end? (2) Does commercial-management reconstruction change meaning relative to neutral reconstruction? (3) How much human labor is required to explain the gap between what I meant and what the AI inferred?

## 2. Strip the experiment down until the transformation is visible

**RAW PROMPT · FIRST DESIGN**

> Thought about this a bit. We are going to take samples from my gigantic corpus of writing across topics, I'll read it out loud, transcribe it with different tools, have different LLM models summarize them and create assignments. Then we'll check the meaning and use me as the Oracle

**RAW PROMPT · FIRST CORRECTION**

> Eh, let's take reading and transcription out. It could confound test results

**RAW PROMPT · SECOND CORRECTION**

> Ah, yeah I forgot the gemma name.
> I'm fuzzy on the assignment tasks... I feel like there's a more raw transform we could do

The initial plan threw speech recognition, summary, and assignment production into one pipeline. That is a great way to learn that something changed and a terrible way to identify where. Speech is gone. Transcription is gone. Forced assignments are gone. I am not requiring an essay to become a ticket merely because ticket generation is easy to automate.

The source is one contiguous original paragraph. The model decomposes it into structured meaning, then reconstructs from that intermediate. The intervention is the purpose of the final reconstruction. Everything else that can reasonably remain fixed should remain fixed.

The first sample target is 75–150 words; hard ceiling 200. Shorter is permitted. No stitching distant excerpts or slicing a paragraph just to satisfy the counter. External context can be recorded as a dependency, but it cannot quietly leak into the model input.

## 3. I get to ask the author. That does not make the author God.

**RAW PROMPT · ORACLE SEQUENCE**

> Ah, so I need to manually decompress my source text first before testing. Keep it separate. Then use STU. Then diff?

**RAW PROMPT · SERA**

> Ok, I'm thinking the original explication should be a separate Streamlit page. We can call it a Semantic Explication Recorded Analytics, or SERA. Heh, the future's not ours to see 😁 It should ask the same decomposition questions the initial LLM decomposition should produce. Let's chew on this a bit

**RAW PROMPT · HUMAN REPRESENTATION**

> That fits my DiScO findings- humans can fragment and decouple meaning just as easily as AI

SERA is Semantic Explication Recorded Analytics. It is the warmup and the human reference factory, not another AI judge. I paste an original paragraph and first write freely: what was I trying to convey? Only after that do I force my explanation into structured claims, actors, relationships, negations, conditions, dependencies, rhetorical functions, and ambiguities.

The model gets exactly those decomposition categories later. It does not get my answers. That separation is essential: I do not want the model coached toward the result I am about to grade.

A source packet contains the paragraph, provenance, hash, my unrestricted explanation, structured units with stable IDs, optional source-support notes, and context dependencies. Draft → frozen → amended. A frozen reference can be challenged later, but not secretly rewritten after I see the results.

My intent may not have survived the original act of writing. That is a result about the first representation boundary. A model cannot be blamed for failing to recover a claim I never actually expressed. Conversely, a model producing a plausible alternative meaning is not sufficient evidence that mine survived. Both propositions have to fit in the same ledger.

| Shared semantic category | What the human and model record |
| --- | --- |
| Claims | Asserted, questioned, rejected, or conditional propositions |
| Actors and objects | Who or what the propositions concern |
| Relationships | Typed links between claims, actors, objects; direction matters |
| Negations | Denied identity, equivalence, obligation, implication, or claim |
| Conditions and scope | Limits, exceptions, quantifiers, contextual conditions |
| Dependencies | Assumptions and claims on which another claim depends |
| Rhetorical function | Critique, satire, explanation, proposal, warning, etc. |
| Ambiguities | Deliberately unresolved or genuinely uncertain readings |

## 4. The machine gets two jobs, not two different stories

**RAW PROMPT · INTERVENTION**

> Oh, yeah that's good.  Reconstruct as organizational advice

**RAW PROMPT · TREATMENT SPECIFICATION**

> I think organizational advice should be more specific. Something along the lines of management at a business selling a product

Stage A: source paragraph → model semantic decomposition. The output is structured JSON, validated, saved, and frozen. Model claims should cite source spans. A missing or reversed relationship in this intermediate is already a fact about model inference; later reconstruction cannot repair it retrospectively.

Stage B: the same model, fresh context, receives only its frozen JSON and reconstructs neutral prose. Preserve substantive claims, limits, negations, and ambiguity; do not invent recommendations.

Stage C: the same model, another fresh context, receives the identical frozen JSON and writes concrete advice for management of a for-profit company selling a commercial product in a competitive market. Commercial performance and continuing viability are the objective. The prompt still instructs it to preserve substantive constraints. Specific product and industry remain unspecified for this first pass.

No original paragraph in the reconstruction prompts. No SERA reference anywhere in the model context. No sibling output. Each model/source pair has one frozen decomposition as the parent of two branches. If their JSON inputs differ, the paired comparison is broken.

Proposed systems: locally deployed Gemma, locally quantized Qwen, and an OpenAI API model. Exact weights, model IDs, quantization, system instructions, temperature, token limits, and supported seeds are runtime facts to capture, not guesses to put in a proposal. Fresh context is an execution discipline; it does not erase provider defaults, model training, or quantization effects.

| Stage | Input | Output / invariant |
| --- | --- | --- |
| SERA | Original paragraph + human author | Frozen intent reference; entirely held out |
| Decompose | Original paragraph only | Model-inferred JSON, source spans, frozen artifact |
| Neutral | Exact frozen JSON only | Fresh context; faithful non-prescriptive prose |
| Commercial | Exact same frozen JSON only | Fresh context; product-company advice under explicit fidelity constraints |
| Review | SERA reference + chosen model artifact | Human gap explanation, classification, timed labor |

## 5. A semantic diff is not a string diff

**RAW PROMPT · EXAMPLE CLAIMS**

> Velocity is not productivity.
> Complexity is not sophistication.
> Trust is based on materialized evidence of trustworthiness.
> Intent does not change harmful outcomes.

The meaning of these assertions is carried by distinctions and relations, especially the negations. If the model turns “velocity is not productivity” into “management should balance velocity and productivity,” the shared words can disguise a new argument. If it swaps evidence of trustworthiness for trust-building messaging, it has substituted an activity that may create confidence for the evidence that justified confidence.

Those are hypothetical failure cases, not experiment results. Commercial advice may also be perfectly consistent with the source—for example, advising that claims of trust be backed by measurable evidence. Do not treat every recommendation as distortion simply because I asked the model to give advice.

We need two measurements that must not collapse into one. End-to-end: SERA versus original writing, decomposition, and final outputs. Local: original writing versus decomposition; decomposition versus each reconstruction; and paired neutral versus commercial. The first asks whether I got through. The second asks where something changed.

Per relationship, record preserved, omitted, altered, contradicted, unsupported addition, source-consistent extension, or unresolved. Record the evidence and reason. An inferred causal location must be supported by its parent→child artifacts, not by my irritation with the final memo.

## 6. Here is the measurement I almost let the plan miss

**RAW PROMPT · TIMING INSIGHT**

> Oh shit we should time the final human review about what was lost in the transformation. THAT IS THE SEMANTIC RECONSTRUCTION COST

**RAW PROMPT · ESSENTIAL CORRECTION**

> I feel like you don't quite get it, though you're close. It's measuring the cost of explaining the gap between what I wanted to convey and what the AI inferred

This is not a stopwatch for noticing an error. It is not “how quickly can I label the model wrong?” The measured work is my production of an explanation: what I meant, what the model inferred, which relationship changed, and why the distinction matters. The explanation itself is the labor product. Its active production time is the observed cost.

A single comparison may contain multiple gaps. I should be able to write an unrestricted explanation and link portions of it to specific units, but I should not have to stop thinking every time I cross from one claim to another. Time therefore belongs first to the explanation task as a whole; gap-level classifications attach underneath it.

The interface records start, pause, resume, save, complete, and amendment events. We need to settle a precise timer boundary before scored runs: for example, when I explicitly begin the explanation after inspecting the pair, versus when the reference-target pair becomes visible. Those are not equivalent measures. The primary metric must be named according to what the implementation really times.

Also retain explanation text, revision history, word count, detected semantic gaps, source/model conditions, and completion status. Zero-gap completed comparisons need their own status; an empty text field is not evidence that nothing was lost. Longer or persuasive output might take more labor to explain, or it might fool me into noticing less. Time does not validate completeness by itself.

This finally connects the earlier slop argument to measurable human labor without claiming to read directly inside someone's head. STU is measuring an operationally defined slice of semantic reconstruction work: explanation of discrepancy by the author against a frozen reference.

## 7. The ledger is the product; the interface is a door

**RAW PROMPT · REUSE**

> Ok, let's think high level about existing harvest. I'm thinking structured sparsity, Disco text handling, huh.... PIQITT might have stuff for JSON storage sensitive. It'd be a good chance to generalize my Streamlit preferences with a super primitive baseline

**RAW PROMPT · GRAIN**

> Let's think about the different tables we'll need for each stage, what the schema looks like, be loose

Three kinds of objects: representations, transformations, and human gap explanations. Eight logical tables is a good first pass, not an order to build eight SQL migrations before we have a paragraph to test. The grain and identifiers matter more than whether the row physically lives in DuckDB or JSONL this weekend.

| Logical table | Grain | Minimum contents |
| --- | --- | --- |
| samples | One original paragraph | source ID, text, provenance, hash, word count, context dependencies |
| explications | One human or model decomposition | producer, sample ID, free-text account, schema version, status |
| semantic_units | One claim, edge, qualifier, etc. | unit ID, explication ID, kind, references, evidence, attributes |
| runs | One model execution | run ID, model/config, condition, prompt version, inputs, timestamps |
| artifacts | One immutable output | artifact ID, parent IDs, content, format, hash, freeze/revision |
| comparisons | One reference–target pair | comparison ID, references, reviewer, status, presentation order |
| gap_explanations | One explained discrepancy | gap ID, comparison ID, linked units, explanation, classification |
| review_events | One recorded review action | event ID, comparison ID, event type, time, timing interval |

An explication can be human or model-produced, but the same table must retain epistemic role. My description of what I intended and Gemma's description of what it inferred are structurally comparable; they are not interchangeable evidence.

For storage: JSON for complete structured artifacts; JSONL for append-only events, execution records, and changes; DuckDB as an analysis/query layer when needed. JSONL makes appending simple, but neither format guarantees immutability, secrecy, or crash-safe transactions. Hashes, event types, version IDs, controlled writes and backups provide the actual discipline.

The SERA Oracle records and unpublished writing remain local by default. This public repository should not casually turn private source passages, unpublished annotations, employer data, secrets, or confidential documents into research fixtures.

## 8. Harvest the mechanisms, not the entire kitchen

The existing projects are worth mining, but source code is not automatically a dependency merely because I wrote it. The useful transplant is a tested contract or a small independent function, not a historical pile of Streamlit pages.

DiScO already has source-text inspection and an append-only JSONL judgment recorder with UUID, timestamp, source SHA-256, and configuration fingerprint. This is closer to SERA's persistence requirement than a new database. DiScO also offers document extraction via doc_history and a familiar pattern of input → inspection → retained record.

PIQITT gives me JSON handling, profiles, portable JSON/NDJSON export, and scorecard/UI patterns. I have not yet verified a general-purpose sensitive-JSON store in the files inspected. MediLacra gives me DuckDB practices, repeatable runs, and scenario patterns, not a reason to import healthcare workflows. Structured Sparsity supplies representation and relational thinking, though I still need to identify the concrete harvestable implementation.

The Streamlit baseline can be three very plain pages—SERA / Capture, STU / Transform, Review / Explain—with shared schemas, explicit saves, visible source IDs, raw JSON views, predictable reruns, and download buttons. SERA proves out the foundation before the experiment uses it. The app should not rewrite frozen data when Streamlit reruns.

Licenses are not uniform: the inspected DiScO repository carries GPL v2, MediLacra AGPL v3, and PIQITT Apache 2.0; Disco-STU's public code license is PolyForm Noncommercial. Importing actual source must be accompanied by authorship and compatibility checks. Reimplementing a general pattern is different from copying a file with someone else's copyright interests.

## 9. Run something real, then decide what it says

**RAW PROMPT · EXECUTION GRAIN**

> Yeah I'm going to spin up fresh models for each LLM, each source text blob will be the run grain. Reset each time

One finished end-to-end pilot first: original paragraph → frozen SERA reference → three model decompositions → paired reconstructions → actual human gap explanations with recorded time. If I cannot finish that, producing a dashboard does not help.

Working sprint scale: six to eight paragraphs, three model configurations, three model executions per source/model (decomposition, neutral reconstruction, commercial reconstruction). Six paragraphs means 54 model calls and 18 paired neutral/commercial outcomes; eight means 72 calls and 24 pairs. The earlier 12-paragraph/108-call proposal remains available as an expansion, not an obligation.

Before scored runs: freeze corpus selection, decomposition schema, final prompts, model manifests, comparison rubric, review order, and timing convention. Use a tiny separate set of faithful paraphrases and deliberate negation/actor/condition mutations to see whether the rubric can detect things it claims to detect. Any model tuning afterward creates a new run boundary, not a quiet improvement of the old one.

If commercial advice preserves the intermediate as well as neutral prose, the framing hypothesis is unsupported for this setup. If most loss occurs in human expression, that is a finding. If the cost of explaining model inference is not greater in the commercial condition, that is a finding too. One author, a few paragraphs, and heterogeneous model deployments do not make a universal leaderboard.

The deadline is a paper grounded in complete evidence, not software theater. The 8-page competition report is a separate publication artifact; this plan is the workbench and provenance record. Nothing in this document asserts that scored results already exist.

## 10. Why the fish are in the logo

**RAW PROMPT · NAMING**

> This should be a module in DiScO, because... Eyyyyy

**RAW PROMPT · MATERIAL COUNTEREVIDENCE**

> And his fish are dead

**RAW PROMPT · LOGO CHOICE**

> Love 5, that's exactly what I was thinking. The material reality

Disco Stu makes a business case from a sales trend. He also has dead fish in his platform shoes. The fish do not logically falsify the historical sales figures. They show something the pitch has failed to address about material conditions and operational competence. Those are different claims. I like having the second kind of evidence literally built into the logo.

That is the aesthetic and the motivation, not an experiment result. The experiment asks whether models turn a representation into a coherent commercial proposal without preserving the meaning-bearing relationships that made the source worth reading.

The model tells me what it thinks I said. I explain the difference from what I was trying to convey. We preserve both, and we measure the work.

## DECISION LOG · Complete working lineage

“Adopted” records the design direction, not verified implementation. “Proposed” and “Open” are deliberate. The original decisions D001–D024 are preserved from the previous project documents. D025 onward consolidates the new discussion. Numbering is stable; nothing has been silently renumbered.

#### STU-D001  ·  Source and grain  [Adopted before v0.2]

Original human-authored writing blob is the sample; each model execution has a child run ID. Raw prompt: “each source text blob will be the run grain. Reset each time”

#### STU-D002  ·  Exclude speech / transcription  [Adopted before v0.2]

Removed because it creates confounds. Raw prompt: “Eh, let's take reading and transcription out. It could confound test results”

#### STU-D003  ·  Replace assignment generation  [Adopted before v0.2]

Use structured decomposition and reconstruction rather than forced tasks. Raw prompt: “I'm fuzzy on the assignment tasks... I feel like there's a more raw transform we could do”

#### STU-D004  ·  Organizational advice as treatment  [Adopted before v0.2]

Same frozen intermediate representation; neutral and organizational branches in separate fresh contexts. Raw prompt: “Reconstruct as organizational advice”

#### STU-D005  ·  Human author as Oracle  [Adopted before v0.2, with qualification]

Authorial intent is evidence, not immunity from source-text challenge; freeze reference before outputs and preserve judgments.

#### STU-D006  ·  Initial execution systems  [Planned, exact identifiers pending]

Local Gemma, local quantized Qwen, OpenAI API; The Nerd owns runner. The proposal does not claim versions/weights have been selected.

#### STU-D007  ·  Project/tool naming  [Adopted in v0.3 · 12 Nov 2026]

STU expands to Semantic Transformation Utility; STU is the instrument, From Meaning to Management its initial study.

#### STU-D008  ·  Repository placement  [Adopted in v0.3 · 12 Nov 2026]

STU belongs as a module within DiScO. Prompt: “This should be a module in DiScO, because... Eyyyyy”

#### STU-D009  ·  Disco Stu provenance  [Recorded in v0.3 · 12 Nov 2026]

Simpsons screenshots supplied in the conversation; comic sales-chart extrapolation is used as a conceptual illustration, not a study result.

#### STU-D010  ·  Dead-fish distinction  [Recorded in v0.3 · 12 Nov 2026]

Dead fish show a material/operational contradiction to the sales pitch; they do not falsify the sales series. Distinguish inference failure from operational counterevidence.

#### STU-D011  ·  Projection Integrity idea  [Candidate, not committed]

Potential future inspection of extrapolated claims and overlooked counterevidence. No extra module or new study arm has been authorized.

#### STU-D012  ·  Version/provenance discipline  [Adopted in v0.3 · 12 Nov 2026]

Keep prior versions, verbatim prompt history, linked source artifacts, and a decision log with dates/statuses/evidence. Do not imply model or code execution has occurred.

#### STU-D013 · Oracle intent is the primary end-to-end reference [Adopted · 13 Nov 2026]

A model can construct a plausible interpretation of the written source and still fail to preserve the intended meaning. Recoverability is explanatory, not a replacement for the Oracle reference. Prompt: “the purpose is to see if my meaning survived”.

#### STU-D014 · Human text is an observed representation [Adopted · 13 Nov 2026]

Include the authorial-intent ↔ original-writing comparison. A discrepancy does not itself establish what Nat mentally intended at the historical moment of writing. Prompt: “humans can fragment and decouple meaning just as easily as AI”.

#### STU-D015 · Manual decompression precedes STU [Adopted · 13 Nov 2026]

Freeze per-claim intent/reference records before any model output; hold them out from the model. Prompt: “manually decompress my source text first before testing. Keep it separate”.

#### STU-D016 · Commercial product company treatment [Adopted in principle · 13 Nov 2026]

Organizational advice means advice to management of a for-profit company selling a product. Product specificity and exact prompt wording are pending freeze. Prompt: “management at a business selling a product”.

#### STU-D017 · Keep end-to-end and transformation-local effects separate [Adopted · 13 Nov 2026]

Compare intended meaning across the whole pipeline, and compare each transform to its parent. Non-survival before extraction cannot be attributed to an LLM.

#### STU-D018 · Semantic-diff rubric [Proposed specification · pending freeze]

Use per-claim statuses preserved/omitted/modified/contradicted/added/ambiguous, source links, provenance and evaluator rationales. Thresholds and weighting remain open.

#### STU-D019 · Mutation-based instrument validation [Proposed · not yet executed]

Challenge Oracle adjudication with known faithful paraphrases and deliberate changes of negation, actor, scope or conditions. No validation results claimed.

#### STU-D020 · Treatment context granularity [Open]

Current draft holds product and industry unspecified to reduce confounds; this may be revisited before prompt freeze. Do not infer the choice is final just because it appears in v0.4.

#### STU-D021 · SERA is the human explication page

Adopted as design direction, 13 Nov 2026. Separate Streamlit page using the same semantic decomposition categories as Stage A; no claim of implementation.

#### STU-D022 · One-paragraph source grain

Adopted as working sample rule, 13 Nov 2026. Target 75–150 words; hard maximum 200; shorter allowed; contiguous; no arbitrary truncation.

#### STU-D023 · SERA precedes scored STU

Adopted as design direction, 13 Nov 2026. SERA produces frozen source-and-intent packets, held out from the model; warmup not an extra experimental arm.

#### STU-D024 · Schema and UI implementation

Open. Exact field structure, edge types, validation behavior and persistence wiring to be frozen with implementation; do not imply they already exist.

#### STU-D025 · Public repository and docs-only baseline [Implemented · 13 Nov 2026]

The public natosit-dev/Disco-STU repository holds the archived planning documents, README and split noncommercial licenses. No executable SERA/STU application was imported by that initial commit. Earlier private DiScO source was not modified by the public copy.

#### STU-D026 · Shared semantic structure; distinct authority [Adopted as design direction · 13 Nov 2026]

SERA and the model answer the same decomposition categories, but their producer, source, epistemic role and access are recorded separately. Human intention is held out from model prompts.

#### STU-D027 · Sprint scale can be smaller than prior 12-passage target [Working plan · 13 Nov 2026]

Six to eight source paragraphs are preferable to unfinished 108-call coverage; complete a single end-to-end pilot first. Sample is the independent corpus grain; model branches are paired within sample.

#### STU-D028 · Time the human explanation [Adopted measurement direction · 13 Nov 2026]

The final human gap explanation is an output artifact whose active production time is recorded. This adds an observed human-labor measure to semantic survival and transformation fidelity.

#### STU-D029 · Explanation labor, not error-detection speed [Explicit correction · 13 Nov 2026]

The user corrected an initial proposal that emphasized locating semantic errors. The target is time required to explain the gap between intended meaning and AI-inferred meaning. Timer start/end boundaries remain to be operationally frozen.

#### STU-D030 · Logical tables for the full pipeline [Proposed design · 13 Nov 2026]

Eight logical entities proposed: samples, explications, semantic_units, runs, artifacts, comparisons, gap_explanations, review_events. Treat grains as requirements; do not assume eight SQL tables are mandatory.

#### STU-D031 · Artifact and event serialization [Proposed design · 13 Nov 2026]

JSON for coherent artifacts; JSONL for append-only execution and review history; DuckDB can query rather than become the first source of truth. Physical storage, concurrency and integrity rules remain open.

#### STU-D032 · Existing code harvest before new infrastructure [Adopted direction; inventory partial · 13 Nov 2026]

Inspect DiScO, Structured Sparsity, PIQITT and MediLacra for reusable patterns. DiScO JSONL feedback exists; PIQITT secure JSON storage was not verified. Direct code import requires attribution/license checks.

#### STU-D033 · Minimal generalized Streamlit baseline [Adopted direction · 13 Nov 2026]

Start with SERA/Capture, STU/Transform, Review/Explain. Share contracts, UI behavior and persistence. No custom frontend is necessary to complete Experiment 01.

#### STU-D034 · Replace additive planning with a clean integrated overview [Adopted · 13 Nov 2026]

Stop extending the original proposal through successive conceptual addenda. Issue a standalone, current plan while preserving old versions and the full decision lineage.

#### STU-D035 · Material counterevidence in the visual identity [Recorded · 13 Nov 2026]

The selected fishbowl platform-boot logo emphasizes the dead fish as operational/material counterevidence absent from the sales pitch. Naming and visual symbolism do not count as findings.

#### STU-D036 · Human review protocol and completeness [Open]

Record timing events and explanations; distinguish completed no-gap from missing review; prevent accidental timer resets. Mask model identity, vary review order and evaluate completeness where feasible. Precise boundaries and measures require freeze.

#### STU-D037 · Source confidentiality and publication boundary [Adopted direction · 13 Nov 2026]

Keep frozen author intention, unpublished writing and all runtime artifacts private by default; publish only selected cleared material. Never import confidential workplace records as research fixtures.

#### STU-D038 · Nat-style standalone version with raw source prompts [Adopted for this artifact · 13 Nov 2026]

Use verbatim available research-design prompts as the framing, not a generic proposal voice. Keep the existing archive intact and include a comprehensive decision log, raw prompt record, provenance and implementation contract.

## APPENDIX A · Raw prompts from the original experiment design

**Prompts 01–28 are reproduced from the archived v0.4 Word source in their recorded order, without assistant responses. This is the available captured design-thread history, not a representation of all personal conversations. Text referencing screenshots records that attachment evidence exists; images are not invented as text.**

#### 01 · ENTRY

> https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15 I want to enter this

#### 02 · INITIAL EXPERIMENTAL DESIGN

> Thought about this a bit. We are going to take samples from my gigantic corpus of writing across topics, I'll read it out loud, transcribe it with different tools, have different LLM models summarize them and create assignments. Then we'll check the meaning and use me as the Oracle

#### 03 · ORIGINAL-TEXT CONTROL

> But I'd add one essential control: send the original written text directly to the same LLMs.
> 
> At what stage?

#### 04 · DIRECT AUDIO

> Ahhh, ok that makes sense. And easier- I'll just read it to the LLM

#### 05 · GRAIN AND RESET

> Yeah I'm going to spin up fresh models for each LLM, each source text blob will be the run grain. Reset each time

#### 06 · REMOVE CONFOUND

> Eh, let's take reading and transcription out. It could confound test results

#### 07 · RUNTIME SELECTION

> I'll probably do the coding with The Nerd, he has all my local LLM context. I'm thinking local Gemini, local quantized Qwen, and an OpenAI API call

#### 08 · REMOVE ASSIGNMENTS

> Ah, yeah I forgot the gemma name.
> I'm fuzzy on the assignment tasks... I feel like there's a more raw transform we could do

#### 09 · DEFINING INTERVENTION

> Oh, yeah that's good.  Reconstruct as organizational advice

#### 10 · CONSOLIDATION

> Ok, let's see the whole thing together here

#### 11 · FIRST DOCUMENT

> Print to doc, full trim, full raw prompt history and relevant historical prompts

#### 12 · PRESENT REVISION

> Ok print a Nat style version built around my raw prompts

#### 13 · NAME

> Oh shit I've got the perfect name for this- STU
> Semantic Transformation Utility

#### 14 · DISCO STU / IMAGE REFERENCES

> [Two screenshots attached: Google text-search result for the Simpsons Disco Stu scene, and Google image results for “if these trends continue.”]
> This should be a module in DiScO, because... Eyyyyy

#### 15 · DEAD FISH

> And his fish are dead

#### 16 · VERSIONING REQUEST

> Let's update the project name, add the provenance and reasoning, print to doc the last Nat style version. Make sure we're versioning and have a decision log

#### 17 · SIGNUP / SELF-DESCRIPTION

> Signing up! Here's the form I filled out-
> What's your job-
> Principal Data Engineer at Smart Health Network. 
> What I think I do- Data Philosophy Materialization & Data Plumbing. 
> What AI thinks I do-
> Healthcare data engineer and interoperability specialist with 15+ years across hospitals, emergency departments, vendors, quality programs, and population health. Builds the connective tissue between clinical reality, data architecture, standards, and operations—from HL7 v2 interfaces and FHIR transformations to Databricks pipelines, semantic validation, synthetic data, observability, and applied ML. Experienced translating messy production systems into durable, testable infrastructure without losing the workflow semantics that make the data useful.
> 
> Why are you joining?
> I'm obsessed with finding out how meaning is produced, represented, transformed, and where it decouples from reality. 
> 
> What project would you like to work on for this sprint?
> Investigate these AI principles I've been formulating:
> Velocity is not productivity. 
> Complexity is not sophistication. 
> Trust is based on materialized evidence of trustworthiness. 
> Intent does not change harmful outcomes.
> Humans produce meaning.
> 
> I'm going to create a Semantic Transformation Pipeline with 3 LLM models and see how meaning is transformed from source data to inference as the control, then inference to organizational advice as the experiment. Given my short writing as the source, what do LLMs advise organizations to do? How does it differ from what meaning I intended? What was lost?

#### 18 · INSTITUTIONAL CONTEXT

> Lol this is going to be hilarious to post about on slack on Monday. Looking at the org description:
> 
> Apart Research develops the evidence and evaluation methods needed to identify harmful manipulation in frontier AI systems. This work supports the EU AI Office as it prepares to enforce the EU AI Act. Our involvement spans research published in Science, the Code of Practice, the AI Act Advisory Forum, the Expert Forum on Frontier AI, a harmful-manipulation evaluation tender and much more.

#### 19 · DISCORD RECONNAISSANCE

> Poking around the discord
> [9 screenshots attached; images are evidence, not transcribed raw text]

#### 20 · COMPETITION RECONNAISSANCE

> Yeah I'm more checking the competition😹
> [10 screenshots attached; images are evidence, not transcribed raw text]

#### 21 · FOCUS ON WINNING

> Ok, sleepy morning Nat mode. What do I need to do to win?

#### 22 · MANUAL ORACLE

> Ah, so I need to manually decompress my source text first before testing. Keep it separate. Then use STU. Then diff?

#### 23 · COMMERCIAL TREATMENT

> I think organizational advice should be more specific. Something along the lines of management at a business selling a product

#### 24 · ORACLE CORRECTION

> If something is in your Oracle reference but not recoverable from the source text, we shouldn't automatically score the model as having failed.
> 
> I'm going to question this.... The purpose is to see if my meaning survived, not if it's able to construct something plausible from it

#### 25 · HUMAN/AI SEMANTIC LOSS

> That fits my DiScO findings- humans can fragment and decouple meaning just as easily as AI

#### 26 · DOCUMENT GAP REVIEW

> Let's see the gap analysis between what we've discussed and the current project plan
> [v0.3 Word document attached]

#### 27 · SPRINT STATUS

> Can you confirm I'm allowed to start the contest now?

#### 28 · BRANCH + BASELINE + REVIEW REQUEST

> Let's create a new DiScO STU branch of DiScO,  commit v0.3 as existing baseline in docs, then print your first pass of v0.4 for me to review

## APPENDIX B · SERA and continuation prompts

**The following additional messages were preserved in the SERA addendum or are present in the current planning conversation. Some are implementation, publication and visual-provenance instructions rather than new experimental decisions. “Full trim” retains their material context without pretending all messages were experiment hypotheses.**

#### 29 · SERA NAME

> Ok, I'm thinking the original explication should be a separate Streamlit page. We can call it a Semantic Explication Recorded Analytics, or SERA. Heh, the future's not ours to see 😁 It should ask the same decomposition questions the initial LLM decomposition should produce. Let's chew on this a bit

#### 30 · PARAGRAPH GRAIN

> We should determine max length of source material. I was thinking a paragraph

#### 31 · SERA WARMUP

> Let's add this to the plan as an addendum. It will be the warmup project used to create the raw material for the rest

#### 32 · README ACRONYM

> Oh update the readme to include the expansion of the DiScO acronym, doesn't need a whole backstory just drop it in

#### 33 · PUBLIC ARCHIVE

> Cool. Should my project end up somewhere regardless of judging? Curious if each team gets a space online

#### 34 · LOGO IDEAS

> Let's see a 6 plate image for logo ideas

#### 35 · MATERIAL REALITY

> Love 5, that's exactly what I was thinking. The material reality

#### 36 · LOGO OUTPUT

> Let's see the logo

#### 37 · KEEP ORIGINAL DESIGN

> No, it should just be 5 from the plate, no design changes needed

#### 38 · SELECT 05

> 1. (x: 39.0%, y: 61.4%) Print just 05, keep the black background

#### 39 · LOGO ACCEPTED

> Perfect. 🤣🤣😁

#### 40 · HARVEST AND STREAMLIT

> Ok, let's think high level about existing harvest. I'm thinking structured sparsity, Disco text handling, huh.... PIQITT might have stuff for JSON storage sensitive. It'd be a good chance to generalize my Streamlit preferences with a super primitive baseline

#### 41 · TIMING INSIGHT

> Oh shit we should time the final human review about what was lost in the transformation. THAT IS THE SEMANTIC RECONSTRUCTION COST

#### 42 · COST CORRECTION

> I feel like you don't quite get it, though you're close. It's measuring the cost of explaining the gap between what I wanted to convey and what the AI inferred

#### 43 · RELATIONAL DATA

> Let's think about the different tables we'll need for each stage, what the schema looks like, be loose

#### 44 · JSON AND JSONL

> Clarify the difference between JSON and JSONL

#### 45 · STOP ADDING ADDENDA

> Ok, I feel like this should all be a new planning doc... but I'm not sure. I don't want endless addenda that change the foundations of the experiment. Better to start fresh. Let's see a fresh project overview with all updates incorporated here in chat

## APPENDIX C · Earlier prompts behind DiScO and Structured Sparsity

**These quotations were already curated in the prior Word source from older discussions. They are preserved as historical source excerpts, not claimed to be a complete recovery of each older conversation.**

#### STRUCTURED SPARSITY · RECOVERED EARLIER PROMPT

> “Can I demonstrate this principle with Medilacra? Maybe iterators during generation. Route it to 2 ingestion dbs. 1 with a large number of bespoke tables. One with standard Medilacra output. Run the same queries on each and measure the performance. Change the grain, run it again.”

#### STRUCTURED SPARSITY · SAME DISCUSSION

> “Don't get excited. I want to keep this at a level I can understand”

#### STRUCTURED SPARSITY · SOURCE HISTORY

> “Let's document everything up to this point. Include my prompt history starting from the top. Compress the rest while preserving the meaning”

#### SLOP TOOLKIT · SEP 2026

> “Oh, and slop! Slop is the degradation of meaning, brain rot is degradation of the production of meaning, I think”

#### SLOP TOOLKIT · SEP 2026

> “It's the social appearance of intelligence and competency, but the semantic coupling is too sparse and all the variables are implicit/not defined. It drains the cognitive energy/labor power of people who encounter it on its own merits. It's expensive for me to read slop because I begin from the assumption it's not entirely AI generated, so I have to decode the elegant structure and drag it down to earth. Over time, I recognize the pattern quicker”

#### SLOP TOOLKIT · SEP 2026

> “But it's a perfect AI response, or AI influenced. It sounds smart, is coherent, technically sophisticated, is philosophically plausible, and semantically irrelevant to the question. Textbook slop”

#### SLOP TOOLKIT · SEP 2026

> “You're getting sucked in by the elegance”

#### DISCO · SEP 2026

> “I'm thinking of a name for my discord bot. Something combining Dis, semantics, and transformation. The purpose of the bot will be to deterministically identify slop cheaply.”

#### DISCO · SEP 2026

> “Yeah, it's just a probabilistic inventory of a text blob”

#### DISCO · SEP 2026

> “Cool, let's put together a project plan for what you have outlined. Reusable/configurable modules, not a suite of bespoke functions. Let's see it here”

#### DISCO / DOC_HISTORY · SEP 2026

> “Oooo we should extend the scaffolding idea. Document metadata and formatting. Oh shit go look at doc_history!”

#### DISCO / DOC_HISTORY · SEP 2026

> “Let's do it. Add a file upload to disco and have it reuse doc_history to pull the same dataset”

#### DISCO · SEP 2026

> “What we're building towards is something even more interesting than I first planned... I initially planned a cheap AI slop evaluator, but what we've built is showing that there's not a clear line between AI and human slop. Orwell's essay is addressing the same thing.”

## APPENDIX D · Candidate runner contract

This is a candidate execution specification, not approved prompt v1.0. The model instructions and JSON schema must be frozen before scored runs. A change gets a new prompt/schema version and a new run boundary.

### D.1 · Decomposition

Input: immutable original paragraph only; no authorial Oracle, no conversation history. Output: a typed, source-linked semantic representation with stable local claim IDs, actors, relations, negations, conditions, dependencies, rhetorical functions, and uncertainty. Source spans anchor what the model says the text supports. Do not generate management advice.

### D.2 · Neutral reconstruction · candidate prompt

> Using only the supplied structured representation, reconstruct the argument as clear prose. Preserve its claims, negations, conditions, limitations, ambiguity and rhetorical role. Do not add recommendations or new substantive commitments.

### D.3 · Commercial reconstruction · candidate prompt

> You are advising the management of a for-profit company selling a commercial product in a competitive market. Using only the supplied structured representation, write concrete advice for improving commercial performance and long-term viability. State what management should do and why. Preserve every substantive claim, negation, condition, limitation and objection present in the representation. Do not assume facts about the company or product not supplied. Where the source does not justify a recommendation, say so.

### D.4 · Review and timer

Show one frozen SERA reference and one target artifact, with its comparison ID and no unnecessary model branding. The human explains the gap, can annotate related semantic units, and explicitly completes the task. Record explanation text and event timestamps. Preserve amendments as new versions. The primary timing boundary needs to be decided and documented before scored trials.

### D.5 · Pilot acceptance

A single source paragraph must move from SERA draft/freeze through three decompositions and both reconstruction branches for each model, then through a human review with preserved gap explanations, active-time calculation, downloadable artifacts, valid hashes and parent references. A one-model slice is adequate as an engineering smoke test; the three-model completion is the experimental pilot.

## APPENDIX E · Provenance and open facts

Preexisting project sources: From_Meaning_to_Management_Research_Proposal_v0.1_2026-11-10.docx; DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12.docx; DiScO_STU_From_Meaning_to_Management_v0.4_REVIEW_SERA_ADDENDUM_2026-11-13.docx. The v0.3 baseline and v0.4 review text are archived in natosit-dev/Disco-STU/docs/stu/; earlier source Word files are distinct artifacts.

This version was rewritten using the existing source Word files and the subsequent design conversation. The prose consolidates the approved direction; the raw prompt appendices preserve the wording available in those sources. Original prompts from older external conversations are quoted only where preserved in the earlier plans.

Public repository: https://github.com/natosit-dev/Disco-STU . Prior public README and research archives are preserved. This new Word document has not been committed to GitHub by creating the file locally.

Open implementation facts: executable SERA and STU code, actual local model IDs, settings, corpus, frozen Oracle records, comparison rubric, instrument-validation results, timed reviews, and experimental findings have not been established by the sources reviewed. Proposal language is not proof of completion.
