# WAIT, WHAT??!

**A human intervention in the DiScO STU experiment—and an accidental demonstration of its premise**

**Source DOCX:** `Wait_What_Intervention_DiScO_STU_2026-11-14.docx`  
**Source SHA-256:** `71152e1760ea05fcad9526c236ce0e103ca3fcddf999481cb82bf37a4b01ad9a`  
**Date:** 14 November 2026  
**Status:** Standalone design intervention and incident reconstruction, not scored research or a change to the experiment code.  
**Transcription note:** Converted from the complete Word document; retains document content, tables, chronological sequence, decisions WWH-01–WWH-09, 21 raw prompts, and provenance. Markdown is not a reproduction of the Word layout. The closing source statement that this intervention was not yet committed records its status *when authored*.

---

Experiment 01: From Meaning to Management \| 14 November 2026 \| Nat-style working intervention record

STATUS · Design intervention and source-backed incident reconstruction. Not a scored experiment, not a finding about LLM semantic performance, and not an instruction to discard the deterministic test rig.

**NAT · 14 NOV 2026**

The value of this is going to be the test rig. My explication is going to produce some baseline data. If others think it makes sense, additional testing can be done in Studio or fellowship phase.

## The intervention, in one page

I set out to build a test rig for a fairly simple research act. I explain what I meant by a paragraph. Models infer a structured representation from the original writing and reconstruct it twice: neutral prose and commercial advice. I explain what is missing or changed at the end. We record the explanation and the time it took. That gives us an initial, author-specific baseline. It does not establish a universal theory of semantic labor.

Then I gave the AI implementers room to build. They produced a more elaborate, coherent system: multiple comparison types, persistent records, hashes, structured judgments, a review workflow, and a 15-minute timer guard. The system was not simply wrong; much of that is useful test infrastructure. But a possible transformation happened in the design conversation itself: available diagnostic comparisons became assumed human tasks, and a 15-minute cutoff became an estimate of how long I would spend on each task.

**NAT · CORRECTIVE PROMPT**

Yeah, I think that's what the original idea was- I manually explicate once, then describe what's missing from the end of the pipeline- neutral and advice. 3 for each sample. Though now I'm not sure.... Your 15 minute estimation is fucking with me. I don't see myself spending more than a minute, 5 max.

That is what stopped the drift. I had not authorized an eight-comparison review obligation. I had not predicted a quarter-hour of labor per output. The AI generated a defensible instrument and then interpreted its capabilities as human workflow requirements. The human corrected the interpretation.

The repair is not to flatten the test rig. It is to separate what the rig CAN inspect from what the researcher MUST do, and to treat operator labor as a design constraint with the same seriousness as code correctness.

## 1. What I was trying to build

The original experimental sequence is visible in the November 13 Nat-style v0.5 plan. I had already removed speech recognition, transcription, and forced assignment generation because they introduced extra transformation boundaries. I had already separated the human Oracle from model input and identified the last two outputs as a controlled contrast.

| **Stage**                 | **Who acts**                       | **What gets recorded**                                                                                                      |
|---------------------------|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Source and SERA           | Human, once per source paragraph   | Exact source text; unrestricted intended meaning; category prose; structured semantic units and relations; frozen reference |
| Decompose                 | Model, once per source/model pair  | Structured inference from the original text alone, source linked and hashed                                                 |
| Neutral reconstruction    | Same model, fresh context          | Prose rebuilt from frozen decomposition only                                                                                |
| Commercial reconstruction | Same model, another fresh context  | Advice for a competitive, product-selling business from the identical frozen decomposition                                  |
| Final review              | Human, twice per source/model pair | What survived, disappeared, reversed or was added in the neutral and commercial final outputs; explanation labor time       |

The meaningful human pattern is “one initial explication + two end-output reviews” for a SINGLE model/source pairing. With three models, the SERA reference is still created only once; there are six final reviews, not three SERA sessions and not twenty-four diagnostic reviews. This is a correction to loose language in the conversation, not a change to the research goal.

Intermediate comparisons remain scientifically useful. They help locate where a discrepancy first entered the chain. They are diagnostic tools, not automatic assignments to the person operating the instrument.

## 2. What happened, chronologically

| **When / stage**              | **Observable action**                                                                                                                                                       | **What changed**                                                                      |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| 13 Nov · research v0.5        | The project defined SERA, held-out intent, shared frozen intermediate, two reconstruction conditions, and human gap-explication cost.                                       | A bounded research purpose and explicit provenance.                                   |
| 14 Nov · SERA                 | Nat chose progressive explication; an independent SERA capture/freeze/export application and backend tests were committed.                                                  | The human reference became a durable artifact.                                        |
| 14 Nov · Nerd handoff         | Nat instructed the AI implementer to build the entire rig first so she could test piece by piece later.                                                                     | Execution autonomy widened; research approval was not delegated.                      |
| 14 Nov · deterministic build  | The Nerd built an offline harness with eight typed comparison records, Review event journal, fixed synthetic fixtures, and reported 25 passing tests.                       | Diagnostic capacity grew. Real LLM adapters and empirical trials remained unbuilt.    |
| 14 Nov · review of handoff    | The assistant treated all eight possible comparisons as if each needed 15 minutes of human adjudication.                                                                    | A technical affordance was promoted into an imagined labor obligation.                |
| 14 Nov · human correction     | Nat stated the original three-action pattern, expected roughly a minute per final explanation, five maximum, and retained the 15-minute threshold as a Boolean observation. | The authorized review grain and interpretation of time were restored.                 |
| 14 Nov · present intervention | Nat named the drift: AI-assisted architecture hid a cathedral of human labor inside a semantic-labor experiment.                                                            | The incident itself became a separate development case study—not a scored STU result. |

## 3. What actually went wrong—and what did not

### 3.1 The core drift was semantic, not necessarily a code requirement

The Nerd created eight comparison TYPES: Oracle/original, original/decomposition, Oracle/decomposition, decomposition/neutral, decomposition/commercial, neutral/commercial, Oracle/neutral, and Oracle/commercial. The build report does not say the UI requires the author to complete all eight reviews. The assistant later inferred that workload anyway. Responsibility for the 36–48-hour estimate therefore belongs to that analytic leap, not automatically to the implementation.

**ASSISTANT · THE INFLATED ESTIMATE**

If each comparison receives a full 15-minute explanation allocation, that's 36–48 hours of possible human review.

The arithmetic was technically conditional and dramatically misleading as a description of likely work. It multiplied eight diagnostic comparisons by every source/model pair and then used a 15-minute ceiling as if it were a meaningful anticipated duration. The error was in the assumptions, not multiplication.

### 3.2 Two meanings of fifteen minutes became entangled

The implemented Review code defines MAX_UNCONFIRMED_SECONDS = 15 \* 60. If a single closed interval exceeds that value, it flags timing_uncertain and excludes that interval from counted active seconds. That is a guard against accidental unattended time, not the normalized labor-budget Boolean Nat described.

It also behaves differently for one 16-minute continuous interval versus two 12-minute intervals, even though the second has more cumulative active time. That is acceptable only if the intended measurement is unconfirmed idle sessions. It does not faithfully implement “Did this explanation reach a fixed labor budget?” These two measures should be stored separately.

### 3.3 The infrastructure still has value

Record types, parent hashes, source/Oracle separation, a frozen shared intermediate, synthetic failure cases, and a CLI/domain layer separate from Streamlit are not wasted work. They make the test rig reproducible, inspectable and transferable. The cathedral appears when speculative analytical breadth becomes an obligation on a scarce human reviewer without asking that reviewer.

### 3.4 This is not an observed LLM-semantic-loss result

This incident involved AI-assisted requirements interpretation, research planning, code generation, and human correction. It is not an STU observation of Gemma, Qwen or OpenAI losing the semantic content of a source paragraph. Nor does one design episode establish a general population claim about AI productivity. The evidence supports a specific mechanism: low-cost expansion of technical affordances can increase the apparent amount of downstream human work if the operator’s objective and constraints are not checked.

## 4. The human observation

**NAT · DIAGNOSIS**

It's funny that when I let you and Nerd have more slack you started building a cathedral hidden inside, not taking into account human semantic labor costs. Why it's important to have one in the loop!

I am not objecting to a machine writing more code. I am noticing that more code can imply more obligations: more concepts to learn, more UI states to navigate, more decisions to adjudicate, more records to interpret, more meanings to reconstruct. Those costs need an owner. They do not vanish because the software was cheap to generate.

The useful intervention was neither “have a human approve everything” nor “stop automating.” I supplied an authoritative constraint that the AI had failed to preserve: the expected human action is a short explanation of what is missing from the final output, not a forensic pass through every available transformation boundary. That instruction changes how the instrument should be presented and measured.

The design failure is particularly apt because the experiment is about how coherent representations can displace the labor required to recover meaning. Here the research-planning system generated a coherent but expensive-sounding representation of its own workflow. I recognized the mismatch because I was the person expected to do the work.

## 5. The revised experimental operating contract

### 5.1 One SERA reference; two primary reviews per model

For each source paragraph, create and freeze the human explication exactly once, before model exposure. For each model execution, decompose the source, freeze its structured intermediate, and produce one neutral and one commercial reconstruction from identical intermediate data. The ordinary human review is limited to the two final outputs. Anything else is elective diagnosis of a surprising transformation or an instrument-validation exercise.

A reviewer may state “no meaningful gap.” A short natural-language explanation may be sufficient; the interface must not demand a dozen structured labels as a condition of completion. Optional labels, semantic-unit links, and comparison-local drilldowns can still be captured when useful. Preserve the full explanation; avoid forced overclassification.

### 5.2 Lab instrumentation versus review obligations

| **Retain in the test rig**                                                                | **Make primary human work**                                         | **Make optional / research expansion**                                                       |
|-------------------------------------------------------------------------------------------|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| All eight traceable comparison categories and artifact lineage                            | SERA once per source; neutral and commercial final review per model | Detailed intermediate-stage adjudication when the author wants to locate the origin of a gap |
| Schema validation; source hashes; pinned Oracle version; frozen intermediate; safe export | One short unrestricted gap explanation (or explicit no-gap result)  | Extensive per-unit labels, completeness audits, third-party reviewers                        |
| Review timestamps and event journal                                                       | Deliberate start, finish, pause/interruption                        | Studio/fellowship-scale multi-reviewer reliability protocol                                  |

### 5.3 Expected workload: do not confuse bound and forecast

| **Assumption**                                            | **Six source paragraphs**  | **Eight source paragraphs** |
|-----------------------------------------------------------|----------------------------|-----------------------------|
| 3 models / source                                         | 18 paired output sets      | 24 paired output sets       |
| 2 primary reviews / pair                                  | 36 final-output reviews    | 48 final-output reviews     |
| 1 minute / review (illustration)                          | 36 minutes final review    | 48 minutes final review     |
| 5 minutes / review (illustration)                         | 3 hours final review       | 4 hours final review        |
| 15 minutes / review (budget only)                         | 9 hours maximum allocation | 12 hours maximum allocation |
| All 8 comparisons × 15 min (REJECT as operating estimate) | 36 hours                   | 48 hours                    |

These figures EXCLUDE SERA capture and explication, navigation, pauses, and analysis. Nat expects many reviews to take around one minute and rarely more than five; that is a stated expectation, not an observed distribution. The earlier 36–48-hour figure is retained here as the incident, not the intended plan.

## 6. Measure semantic explanation labor without manufacturing it

The explanatory text is the primary observation. Time is an operational measure attached to that work. It does not prove the explanation is true, complete, socially necessary, or representative of another person. Recording more events is not the same as measuring more meaning.

| **Field / observable**          | **Interpretation**                                                                                  | **Status**                                     |
|---------------------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------|
| explanation_text                | Human explanation of the gap between frozen intention and a final reconstruction; may be very short | Keep as primary                                |
| no_meaningful_gap               | Explicit review outcome rather than an empty or abandoned record                                    | Keep                                           |
| active_explanation_seconds      | Sum of confirmed closed active intervals, not a running Streamlit clock                             | Keep, correct handling                         |
| reached_15min_budget            | Cumulative confirmed explanation time reached 900 seconds; normalized Boolean outcome               | Implement separately from uncertainty          |
| timing_uncertain                | Possible idle/unreliable interval, clock issue, or unresolved session                               | Keep as distinct quality flag                  |
| completed / partial / abandoned | Human disposition of explanation, not a machine-generated semantic score                            | Minimal completion state; definition to freeze |
| optional 1m / 5m flags          | Derived from the same timestamp data for descriptive pilot exploration                              | Candidate, not mandatory                       |

A single 16-minute interval and two 12-minute intervals should not be conflated with idle-time uncertainty. Raw event history must survive; a threshold crossing must not retroactively erase recorded work. A genuine cap or exceeded-budget event should be visible even if the author later continues for experimental reasons. Decide whether the timer begins after untimed inspection (current implementation) or on first exposure to the comparison, and state plainly what labor that choice includes or excludes.

“Socially necessary labor time” is the provocative political-economic connection, not a claim that one author’s stopwatch directly measures Marx’s category. A development/pilot baseline can ask whether AI produces representations cheaply while imposing explanatory work elsewhere. A fellowship-scale design would need more authors, reviewers, conditions, and a stronger account of typical labor under prevailing conditions.

## 7. Minimal changes to the rig

**Review default —** Open with the original frozen SERA intent and either the neutral OR commercial final artifact. Make the two final-review tasks the obvious default. Keep the other comparison types accessible under “Diagnostic comparisons,” not as a to-do queue.

**Task counts —** Display “2 primary reviews per model/source pair”; do not present eight detected comparison records as eight incomplete human jobs.

**Timer —** Count cumulative active closed intervals. Expose the 15-minute reached-budget flag separately from timing_uncertain. Preserve all event times and a transparent method for determining completion.

**Structured labels —** Make labels and per-unit mapping optional except where an explicit label is chosen; then require enough explanation to understand the choice. No compulsory exhaustive rubric at baseline.

**Study output —** Distinguish baseline descriptive observations from synthetic instrument tests and from scored empirical claims. Export the two final human reviews per model as the primary evidence set; retain intermediate comparisons for tracebacks.

**Protocol discipline —** Freeze study settings only after one human walkthrough and one real-model pilot. Version changes without altering earlier runs. Do not add features because they are easy to generate.

**Handoff —** Record this intervention in the change/decision lineage. Existing code and prior plans remain historical evidence; changes should be traceable, not presented as if the new intention had always been implemented.

## 8. What remains unchanged

- SERA is a human-created, frozen retrospective reference; it is not infallible and may describe meaning that the original writing never made recoverable.

- The model never receives the author’s Oracle; it sees only the allowlisted source paragraph during decomposition.

- Neutral and commercial outputs must share the same frozen intermediate; fresh contexts prevent previous outputs from contaminating sibling branches.

- Commercially useful advice is not automatically distortion; only unsupported semantic alteration is a candidate loss.

- A model result may be coherent, fluent or commercially actionable without preserving the original meaning-bearing relations.

- Synthetic fixtures test the machinery, not model cognition. The reported deterministic build is an engineering achievement, not an empirical research result.

- The core deliverable is the test rig plus a small, openly bounded personal baseline. Broader study belongs to a later Studio/fellowship phase if the method earns it.

## 9. What this intervention establishes, suggests and leaves open

| **Evidence establishes**                                                                                                                                            | **Reasonable inference**                                                                                                | **Not established / open**                                                                     |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| A documented expansion of available comparisons and test infrastructure; assistant assumed all eight needed timed manual review.                                    | Human labor constraints were insufficiently protected when interpreting implementation scope.                           | That the Nerd’s UI actually forces eight reviews; no browser walkthrough establishes this.     |
| The assistant calculated a 36–48-hour maximum by combining 8 comparisons with a 15-minute ceiling. Nat corrected expected review duration to ~1 minute, at most ~5. | More AI design autonomy can create self-consistent but labor-intensive workflows when requirements are underdetermined. | That this observed episode generalizes to all AI-generated systems.                            |
| Review code treats \>15-minute single intervals as uncertain, not as cumulative budget crossings.                                                                   | Timer semantics need a narrow correction before scored use.                                                             | Actual distribution of explanation lengths; number of genuine threshold crossings.             |
| Deterministic fixtures and 25 tests are reported in the build handoff; no real-model scored run is documented.                                                      | The rig is a viable basis for a small illustrative pilot if live UI and adapter checks succeed.                         | Any conclusion that commercial prompting causes semantic degradation or increased human labor. |

## 10. What happens next

I do not need another giant architecture document. The next action is a small intervention against unnecessary human obligations: adjust Review presentation, preserve the events and diagnostic graph, fix the 15-minute Boolean, and run one paragraph through the entire real workflow. After that, freeze the experiment around the actual work I am willing to perform rather than an invented fifteen-minute chore.

The near-term output is a functioning, documented test rig and a modest SERA/reference + final-output explanation baseline. If other people find the instrument and framing useful, a Studio or fellowship phase can expand the samples, independent reviewers, timing distribution, semantic adjudication and model comparisons. That larger study is conditional future work, not part of the present evidence.

**NAT NOTES · REPO README**

The trends look good, but the fish is dead.

This time the fish were not the AI models. They were the missing human in the labor estimate.

## Intervention decision record · 14 Nov 2026

These WWH entries are a SUPPLEMENT to the existing STU-D001–D038 design lineage and later Nerd handoff decisions. They do not renumber or retroactively rewrite those documents. “User-settled” means Nat stated the preference; it does not mean implementation was tested or scored protocol frozen.

| **ID / status**                    | **Decision or action**                                                                                                                                                               |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| WWH-01 · User-settled              | The practical human workflow is SERA once per source and end-output review for neutral and commercial reconstructions per model.                                                     |
| WWH-02 · User-settled              | The test rig is the primary near-term value; personal explications provide limited baseline data; wider claims/testing are deferred to Studio or fellowship conditional on interest. |
| WWH-03 · User-settled              | 15 minutes is a normalization threshold / Boolean data point, not an expected time per review. User anticipates approximately one minute and rarely more than five.                  |
| WWH-04 · Observed correction       | Eight technical comparison types must not be inferred to mean eight mandatory human reviews. Assistant’s 36–48-hour extrapolation was not an operating specification.                |
| WWH-05 · Proposed implementation   | Make only final neutral and commercial reviews primary; preserve other comparisons as opt-in diagnostics.                                                                            |
| WWH-06 · Proposed implementation   | Separate cumulative labor-budget crossing from session timing uncertainty; preserve raw timestamps.                                                                                  |
| WWH-07 · Open before scored trials | Define timer start, completion/partial/abandoned semantics and optional short-threshold indicators after pilot.                                                                      |
| WWH-08 · Evidence limitation       | Do not present infrastructure tests, the present intervention, or personal pilot data as model-performance findings or socially necessary labor-time measurements.                   |
| WWH-09 · Provenance                | Preserve this record alongside historical v0.5 and the factual deterministic-build handoff without rewriting earlier decisions.                                                      |

## APPENDIX A · Relevant raw prompt history

The quotations below are preserved verbatim from the v0.5 source Word plan or this November 14 conversation, except that surrounding platform/file markup is omitted. They are a selected trace of the design and intervention—not an attempt to reproduce every historical chat. Each entry is labeled by its available source.

**A01 · EARLIER / SEPTEMBER 2026 · ORIGINAL DISCO LABOR OBSERVATION**

It's the social appearance of intelligence and competency, but the semantic coupling is too sparse and all the variables are implicit/not defined. It drains the cognitive energy/labor power of people who encounter it on its own merits. It's expensive for me to read slop because I begin from the assumption it's not entirely AI generated, so I have to decode the elegant structure and drag it down to earth. Over time, I recognize the pattern quicker

**A02 · 10–13 NOV · ORIGINAL THOUGHT ABOUT THE EXPERIMENT**

Thought about this a bit. We are going to take samples from my gigantic corpus of writing across topics, I'll read it out loud, transcribe it with different tools, have different LLM models summarize them and create assignments. Then we'll check the meaning and use me as the Oracle

**A03 · 10–13 NOV · CONFOUND REMOVED**

Eh, let's take reading and transcription out. It could confound test results

**A04 · 10–13 NOV · TREATMENT**

Oh, yeah that's good. Reconstruct as organizational advice

**A05 · 10–13 NOV · TREATMENT SPECIFICITY**

I think organizational advice should be more specific. Something along the lines of management at a business selling a product

**A06 · 13 NOV · AUTHOR AS PRIOR INDEPENDENT REFERENCE**

Ah, so I need to manually decompress my source text first before testing. Keep it separate. Then use STU. Then diff?

**A07 · 13 NOV · HUMAN MEANING NOT PLAUSIBILITY**

I'm going to question this.... The purpose is to see if my meaning survived, not if it's able to construct something plausible from it

**A08 · 13 NOV · SERA**

Ok, I'm thinking the original explication should be a separate Streamlit page. We can call it a Semantic Explication Recorded Analytics, or SERA. Heh, the future's not ours to see 😁 It should ask the same decomposition questions the initial LLM decomposition should produce. Let's chew on this a bit

**A09 · 13 NOV · TIMING IDENTIFIED**

Oh shit we should time the final human review about what was lost in the transformation. THAT IS THE SEMANTIC RECONSTRUCTION COST

**A10 · 13 NOV · TIMING CLARIFIED**

I feel like you don't quite get it, though you're close. It's measuring the cost of explaining the gap between what I wanted to convey and what the AI inferred

**A11 · 13 NOV · STOP PROLIFERATING ADDENDA**

Ok, I feel like this should all be a new planning doc... but I'm not sure. I don't want endless addenda that change the foundations of the experiment. Better to start fresh. Let's see a fresh project overview with all updates incorporated here in chat

**A12 · 14 NOV · DELEGATE SERA BUILD**

Let's see a build plan for SERA, I feel like you can put that part together. If you need my feedback on any specifics, ask

**A13 · 14 NOV · CHOOSE PROGRESSIVE HUMAN EXPLICATION**

Use progressive explication for SERA: free intention, category-level prose, then structured semantic units and relationships.

**A14 · 14 NOV · AUTHORIZE SERA IMPLEMENTATION**

Commit the build plan to the repo and go build it

**A15 · 14 NOV · AUTHORIZE DELEGATED FULL RIG**

Let's create a handoff doc for The Nerd for the rest. We'll build the whole thing, then I'll test it piece by piece (I'm busy today but want to make progress)

**A16 · 14 NOV · KEEP THRESHOLD AS DATA**

I actually like the 15 minute timer. I'd actually considered a shorter one. Hitting it is a normalized Boolean data point

**A17 · 14 NOV · POLITICAL-ECONOMIC CONNECTION**

Socially necessary labor time 😹

**A18 · 14 NOV · CONSTRAIN OVERSTATEMENT**

How are we doing so far? Anything I'm not thinking of? Note I am trying not to overdo it overstate anything

**A19 · 14 NOV · CORRECT REVIEW GRAIN AND ESTIMATE**

Yeah, I think that's what the original idea was- I manually explicate once, then describe what's missing from the end of the pipeline- neutral and advice. 3 for each sample. Though now I'm not sure.... Your 15 minute estimation is fucking with me. I don't see myself spending more than a minute, 5 max.

**A20 · 14 NOV · DIAGNOSE CATHEDRAL**

It's funny that when I let you and Nerd have more slack you started building a cathedral hidden inside, not taking into account human semantic labor costs. Why it's important to have one in the loop!

**A21 · 14 NOV · SET THE INTERVENTION OUTPUT**

Yeah, the value of this is going to be the test rig. My explication is going to produce some baseline data. If others think it makes sense, additional testing can be done in Studio or fellowship phase. Let's see a full intervention doc called "Wait, What??!" with what happened, what I noticed, and what needs to change about the experiment. Full trim, relevant prompt history. Print

## APPENDIX B · Assistant-generated language that triggered the correction

**ASSISTANT · REVIEW-SCOPE ANALYSIS**

If each comparison receives a full 15-minute explanation allocation, that's 36–48 hours of possible human review.

**ASSISTANT · LATER CORRECTION**

The Nerd built eight comparison records, which can be perfectly reasonable infrastructure. I converted that technical affordance into an assumed human workflow.

These are excerpts from the present conversation. The first statement was conditional mathematics, but it was presented in a way that gave the conditional burden more weight than the authorized three-action workflow. The second identifies the inferential error. Neither is a quote from the Nerd’s build report.

## APPENDIX C · Documentary and code provenance

Primary references used to prepare this intervention:

- Nat-style working research plan v0.5, 13 Nov 2026, original 20-page Word document; section 1–10 and appendices A–E; included raw historical prompts and STU-D001–D038.

- The Nerd deterministic build factual handoff, 14 Nov 2026, original 12-page Word document; reports 25 tests, CLI smoke/negative scenarios, draft PR \#1 and the limits of synthetic evidence.

- GitHub natosit-dev/Disco-STU: docs/INDEX.md, docs/stu/..., docs/handoff/...; deterministic implementation commit 98f50367c6458f840c5fd1cf0b1ba3b22ed6c7d6; the code inspection of stu/review.py establishes the 15-minute interval handling.

- Conversation: user-selected SERA workflow; full-rig delegation; timer/Boolean clarification; review-workload correction; intervention request, all on 14 Nov 2026.

Original DOCX SHA-256 DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.5_2026-11-13.docx 8c4e81ccd6b84ce54884aa7b9a2176f9b97a73710d0dcef2e85de83c00daceee

Original DOCX SHA-256 Disco_STU_Deterministic_Build_Full_Handoff_Radiant_Control_2026-11-14.docx 5c23436d195566906250b4e32fd13645755f659780efd9c1f40d58ee903fd9ae

Repo documentation index: https://github.com/natosit-dev/Disco-STU/blob/main/docs/INDEX.md

Implementation: https://github.com/natosit-dev/Disco-STU/blob/feature/stu-deterministic-pipeline-20261114/stu/review.py

Draft PR: https://github.com/natosit-dev/Disco-STU/pull/1

Source limitations: The build report is an implementer’s factual account and the repo code is a prototype snapshot. The reported CI findings were not re-run in producing this document. User quotes from older conversations are quoted only where preserved in v0.5; present-turn prompts are quoted from the conversation. This intervention has not been committed to the public repository and does not change software or the frozen experiment protocol.