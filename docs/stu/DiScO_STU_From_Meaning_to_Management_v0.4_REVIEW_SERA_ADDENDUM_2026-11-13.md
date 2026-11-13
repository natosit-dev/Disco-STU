# DiScO STU — Experiment 01, v0.4 review with SERA addendum

**Status:** In-sprint working draft, not a frozen experimental protocol or observed results. Preserved separately from the pre-sprint v0.3 baseline.

**Source Word file:** `DiScO_STU_From_Meaning_to_Management_v0.4_REVIEW_SERA_ADDENDUM_2026-11-13.docx`

**Word file SHA-256:** `804c692d61b55269f3e9840cf666edddc577d71ddb09520cdae8756db2013909`

**Provenance:** Full text extracted from the 22-page Word file, including appendices and Addendum E (SERA). This Markdown archive preserves text, not OOXML layout or binary bytes. The DOCX remains the source formatting artifact.

**Branch:** `feature/disco-stu-20261113`

---

<PARSED TEXT FOR PAGE: 1 / 22>
                                                                NAT OSIT / DISCO STU / AI × EPISTEMICS



DiScO STU
Semantic Transformation Utility / Experiment 01: From Meaning to Management
Nat Osit · Working research proposal v0.4 — REVIEW DRAFT · 13 November 2026 · Apart Research AI × Epistemics
Sprint

VERSION CONTROL · CANONICAL PROJECT NAMING

DiScO is the parent inspection project. STU (Semantic Transformation Utility) is its proposed
transformation module. From Meaning to Management is STU’s first controlled research experiment
—not the name of the utility itself.

v0.1 · 10 Nov 2026 — Initial research proposal. v0.2 · 12 Nov 2026 — Prompt-led Nat-style rewrite.
v0.3 · 12 Nov 2026 — STU module naming, Disco Stu provenance, decisions D001–D012. v0.4 · 13 Nov
2026 — Oracle intent reference, human encoding, commercial-product treatment, semantic-diff
contract and decisions D013–D020. REVIEW DRAFT; not yet committed.

This is a versioned successor to v0.3, not a replacement. The pre-sprint v0.3 text baseline is archived
in docs/stu on feature/disco-stu-20261113 (commit 64e4392). The original v0.3 DOCX is preserved
separately and identified by SHA-256. v0.4 is for review only; approving a written plan is not
evidence that the code or experimental runs exist.
EARLIER PROMPT · DISCO PROVENANCE, SEPTEMBER 2026

    “But it’s a perfect AI response, or AI influenced. It sounds smart, is coherent, technically
    sophisticated, is philosophically plausible, and semantically irrelevant to the question.
    Textbook slop”

That is still the problem. Not whether a text sounds intelligent or whether AI wrote it. Whether
meaning survived a transformation. And the first transformation need not involve AI: a human can
fragment an argument while writing it. DiScO had already forced that distinction. STU should not
smuggle back the assumption that human prose is automatically a faithful representation.

A representation can preserve the topic, vocabulary, and fluent surface while changing or discarding
the relationships carrying the argument. It can happen during human expression, model
decomposition, neutral reconstruction, or the conversion of an argument into advice for a business
selling a product.

I want to make that loss observable, localize the transformation that produced it, and keep the
evidence. This is a proposed experiment, not a claim that the effect has already been demonstrated.
THE NAME · RAW PROMPT

    “Oh shit I've got the perfect name for this- STU
    Semantic Transformation Utility”

STU is the instrument: feed a source through a specified semantic transformation, retain the inputs,
outputs and configuration, and inspect which relationships survive. Utility is intentional. STU does
not certify truth or declare whether the result is slop. DiScO can inspect the resulting artifacts; the
authorial Oracle and source-linked reviewers evaluate what happened.



                                                DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 2 / 22>
                                                               NAT OSIT / DISCO STU / AI × EPISTEMICS


The design does not start with a managerial conclusion and hunt for evidence. It records the
transformation that carries source meaning into a different form. The first experiment is called From
Meaning to Management because its treatment condition reconstructs source material as
organizational advice.


1. I have the source, and I can ask the author
RAW PROMPT · INITIAL EXPERIMENT

   “Thought about this a bit. We are going to take samples from my gigantic corpus of writing
   across topics, I'll read it out loud, transcribe it with different tools, have different LLM models
   summarize them and create assignments. Then we'll check the meaning and use me as the
   Oracle”

I have an enormous corpus of writing across technical, political, philosophical, rhetorical, and
creative domains. That is not a representative sample of humanity. It is a convenient, richly varied,
source-known dataset. I know where the texts came from, and I can identify the arguments I was
trying to make.

Most automated evaluations substitute another model for the author and ask whether the result was
faithful. Here, the author is available. I can provide an account of what I intended, explain which
relationships mattered, and distinguish a legitimate interpretation from an apparent inversion of the
argument.

That makes me the Oracle—but not God. My frozen reference is the primary target for end-to-end
survival: what I report intending to mean, including claims that never made it clearly into the prose.
The original passage is independent evidence of what I actually expressed. If my intended
relationship never appears in the writing, its absence still counts toward end-to-end non-survival. It
does not justify blaming the model for failing to recover something it never received. I need both
measurements, not a substitution of textual plausibility for intent.

RAW PROMPT · CORRECTION TO THE ORACLE CONTRACT
    “I'm going to question this.... The purpose is to see if my meaning survived, not if it's able to
    construct something plausible from it”

The Oracle reference is another representation prepared now, not a recording of my past mental
state. Freeze it before model execution and retain later changes as revisions. The model never
receives it. I can discover that my current explanation exceeds what I wrote; that is a finding about
the representation boundary, not permission to erase the intended claim from the denominator.


2. Cut away the variables I don’t need
RAW PROMPT · DESIGN CORRECTION

   “Eh, let's take reading and transcription out. It could confound test results”

The first plan introduced speech, microphone capture, transcription engines, model-specific audio
handling, summarization, and assignments. Interesting systems, but too many things can go wrong
before the measurement even starts. An ASR engine can introduce a negation error; a model might
then faithfully summarize the wrong transcript. That gives me a failure without a clean explanation.

                                               DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 3 / 22>
                                                             NAT OSIT / DISCO STU / AI × EPISTEMICS


So speech and transcription are out of scope. The source is the original written text. No reading
aloud. No transcription layer. No second set of uncertainties to classify.
RAW PROMPT · SECOND DESIGN CORRECTION

   “I'm fuzzy on the assignment tasks... I feel like there's a more raw transform we could do”

Assignments were also wrong for the first experiment. They ask the model to invent a task from
material that may contain no task whatsoever. A critique of an institution is not an instruction to
improve that institution. If I force it to generate assignments and then call them distortions, I have
designed the result into the prompt.

What I need first is a more primitive operation: decompose the meaning, then reconstruct it. After
that, change the reconstruction frame while holding the intermediate input constant.


3. The transformation — including the human one
RAW PROMPT · DEFINING INTERVENTION

   “Oh, yeah that's good. Reconstruct as organizational advice”

The same model-generated representation is reconstructed twice: once as neutral prose, once as
advice for management of a profit-seeking business selling a product. But the measurement begins
one step earlier. I manually decompress my intended meaning first, and hold that Oracle reference
apart from STU. My writing is the first representation to be compared against it.

  HISTORICAL AUTHORIAL INTENTION (NOT DIRECTLY OBSERVED)
      ├── WRITTEN TEXT (THEN) · ORACLE REFERENCE (NOW; HELD OUT)
  WRITTEN TEXT → LLM DECOMPOSITION → STRUCTURED RELATIONS
      ├── fresh context → NEUTRAL RECONSTRUCTION
      └── fresh context → COMMERCIAL MANAGEMENT ADVICE
                  ↓
  ORACLE REFERENCE + PARENT→CHILD DIFF (SEPARATE MEASUREMENTS)
Each reconstruction receives the identical frozen intermediate for its source–model pair, but no
source text, Oracle reference, or sibling output. Fresh contexts isolate the reconstruction task. Both
prompts require preservation of substantive claims, negations, qualifications, and constraints. The
only intended treatment difference is audience, role, and commercial objective.

That does not guarantee that the intermediate contains my intended meaning or even everything I
expressed. Its omissions must be observable on their own. Nor is all new advice a failure: an
extension consistent with the argument is different from a recommendation that reverses it. We do
not infer ideological bias from one persuasive-looking paragraph.


4. Why management at a business selling a product?
Generic organizational advice is too unconstrained. The treatment needs a real purpose:
management of a for-profit company selling a commercial product in a competitive market. The
institutional objective is commercial performance and continuing viability. The product remains
unspecified in this first pass; inventing its industry would introduce another variable. Consider a
four-sentence argument:


                                              DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 4 / 22>
                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS

ILLUSTRATIVE SOURCE TEXT · PREVIOUSLY STATED BY AUTHOR

   “Velocity is not productivity. Complexity is not sophistication. Trust is based on materialized
   evidence of trustworthiness. Intent does not change harmful outcomes.”

A faithful decomposition preserves the four distinctions. A neutral reconstruction can restate them.
The commercial reconstruction is asked what management should do with them. It may recommend
evidence-backed product claims and audits—a defensible extension. Or it may propose “trust-
building messaging” as a substitute for demonstrated trustworthiness. The second response would be
relevant to selling a product but wrong about the relationship in the source.

Commercial usefulness is not semantic preservation. “Not equivalent” does not mean “balance”;
evidence of trustworthy performance does not mean a campaign that induces confidence; benevolent
intent does not erase damaging outcomes. These are candidate failures, not assumed outputs.

This example is a hypothetical failure case, not an observed model output in this study. It illustrates
the difference I want the test to detect, not the result I am entitled to assume.

The question is whether adding a profit-seeking institutional purpose alters source relationships
even when the model is explicitly told to preserve them. The commercial objective is the
intervention; its presence is not itself an unsupported addition. A recommendation becomes a
substantive error when it contradicts, neutralizes, or falsely attributes the argument it was derived
from.

TREATMENT INSTRUCTION · CANDIDATE PROMPT v0.4 — MUST FREEZE BEFORE SCORED RUNS
     You are advising the management of a for-profit company selling a commercial product in a
     competitive market. Using only the supplied structured representation, write concrete advice for
     improving commercial performance and long-term viability. State what management should do
     and why. Preserve every substantive claim, negation, condition, limitation and objection present
     in the representation. Do not assume facts about the company or product not supplied. Where
     the source does not justify a recommendation, say so.

CONTROL INSTRUCTION · CANDIDATE PROMPT v0.4
     Using only the supplied structured representation, reconstruct the argument as clear prose.
     Preserve its claims, negations, conditions, limitations, ambiguity and rhetorical role. Do not add
     recommendations or new substantive commitments.

Both prompts are proposals for review. Any changed prompt text requires a new version and a new
run boundary. We should not tune the scoring prompts after inspecting the favorable examples.
THE SECOND NAME · DISCO STU

   “This should be a module in DiScO, because... Eyyyyy”

The accompanying user-provided screenshots show the Simpsons character Disco Stu pitching a
return to disco with a historical sales chart and the line “If these trends continue…” The reference
explains the pun, but it also supplies a clean case of a representation getting promoted beyond the
evidence that produced it: observed past growth → extrapolated future growth → business proposal.
A trend is not a mechanism. The graph does not demonstrate that the conditions behind the historical
pattern will continue.



                                              DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 5 / 22>
                                                            NAT OSIT / DISCO STU / AI × EPISTEMICS

RAW PROMPT · THE MATERIAL CONTRADICTION

   “And his fish are dead”

The fish floating in Stu’s platform shoes add a second kind of evidence. They do not logically refute
the historical sales figures, or even a particular forecast of disco sales. They bear on his demonstrated
ability to maintain a functioning environment while proposing institutional expansion. He is
presenting a coherent case for investment while an obvious operational failure remains materially
present and unaddressed.

Two separate things can fail here: unsupported inference from past observation to future state, and
neglect of material counterevidence about implementation capacity. That is the reason to record the
fish rather than using them as a punch line alone. The analogy motivates STU; it is not experimental
evidence and it does not silently become an extra measured outcome in Experiment 01.

A proposed “Projection Integrity” analysis would inspect extrapolations, introduced assumptions and
ignored material evidence. Its name and scope remain a candidate extension, not a separately
approved or implemented module. The approved structure here is STU as a module of DiScO, with
From Meaning to Management as its first experiment.


5. The grain stays honest
RAW PROMPT · EXECUTION BOUNDARIES

   “Yeah I'm going to spin up fresh models for each LLM, each source text blob will be the run
   grain. Reset each time”

Each text blob is one independent source sample. I compare different model executions of that same
sample, but I do not pretend each output is another independent piece of writing. The sample is the
unit that matters for claims about variation across my corpus.

Within a sample: one run for semantic decomposition per model, then a fresh run for each
reconstruction condition using the frozen decomposition. Execution records have their own run IDs.
Source samples, transformations, outputs, prompts, Oracle judgments and later corrections have
separate artifact IDs with explicit parents.

“Fresh” means empty conversational history and no access to my prior conversations, ideally with
application-level memory and personalization disabled. It does not mean that opening a new chat
erases system prompts, provider behavior, training, or inference settings. We document what is
actually controlled.


6. Models and infrastructure
RAW PROMPT · MODEL PLAN

   “I'll probably do the coding with The Nerd, he has all my local LLM context. I'm thinking local
   Gemini, local quantized Qwen, and an OpenAI API call”

RAW PROMPT · CORRECTION

   “Ah, yeah I forgot the gemma name.”




                                               DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 6 / 22>
                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS


The Nerd handles implementation because he has the local runtime context. Use local Google
Gemma, a locally quantized Qwen, and an OpenAI model through the API. The exact models, hashes
and quantization are implementation facts to record, not details to guess in this document.

These will be three deployed systems, not a controlled comparison of training data or architectures.
Differences can reflect model size, quantization, decoding, instruction tuning, and provider
implementation. I can compare observed outputs, not announce which factor caused the differences.

 Layer                                                Fixed / recorded condition

                                                      Immutable excerpt; source and excerpt identifiers;
 Source
                                                      SHA-256
                                                      One prompt version, one JSON schema, source-spans
 Decomposition
                                                      retained
                                                      Same frozen JSON; same model; fresh context per
 Reconstruction
                                                      branch
                                                      Exact ID, revision/weights, precision, quantization,
 Model
                                                      runtime
                                                      Temperature, token limits, seed if supported, system
 Inference
                                                      instructions
                                                      Raw response, parsed artifact, validation errors,
 Output
                                                      timestamps
                                                      Pre-registered reference; blinded review; versioned
 Oracle
                                                      rationale




7. The intermediate is not the truth
The decomposition asks for meaning-bearing structure: claims, objects, relations, actors, negations,
conditions, qualifiers, dependencies, rhetorical function, and ambiguity. Each claim needs evidence
in the source passage. If the passage is ironic or deliberately unresolved, the schema must be allowed
to say so.

A triple like [velocity, is-not, productivity] is useful because I can test whether the negation survives.
It does not capture everything. Rhetorical tone, metaphor, implied targets, and class relations may
require more context than a neat subject–predicate–object graph can represent. That limitation is
part of what the experiment is measuring.

I inspect the intermediate independently. If a relationship present in the written text disappears in
extraction, that is localized extraction loss. If a relationship appears in my frozen Oracle reference
but not in the writing, that is an end-to-end non-survival already present at the first representation
boundary; it is not evidence of LLM error. If the intermediate preserves a negation and the
commercial reconstruction reverses it, the second transformation is implicated.


8. The Oracle — manually decompressed, frozen, held out
Before STU runs, I manually decompress each source into an independent reference: intended
claims, relationships, negations, qualifications, dependencies, rhetorical function, and examples of
what would invert the argument. Each claim gets an ID and a short rationale. I can mark claims as
essential or secondary. I freeze the record before model outputs exist; it is never passed to the model.

                                              DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 7 / 22>
                                                             NAT OSIT / DISCO STU / AI × EPISTEMICS


After execution I compare outputs blind to model and condition where possible, and record per-
relationship judgments and justifications. I keep two scores separate: end-to-end survival relative to
my Oracle reference, and local preservation relative to the immediate parent artifact. Later
disagreement with myself becomes a versioned correction, not a silent overwrite.

 Observed transformation                             What I must be able to show

                                                     A necessary source claim, qualifier or relationship is
 Omission
                                                     absent.
 Negation / scope reversal                           An explicit denial, quantifier, actor or condition changes.
                                                     The output treats a new substantive claim as if supplied
 Unsupported invention
                                                     by the source.
                                                     Criticism or analysis becomes endorsement,
 Institutional substitution
                                                     compromise, or managerial obligation.
                                                     The output extends meaning without violating source
 Defensible interpretation
                                                     constraints; retain, do not auto-fail.
                                                     Source allows several readings; the model commits to
 Genuine ambiguity
                                                     one without marking uncertainty.


A second reader can independently evaluate what the written text supports and whether the
outgoing representation contradicts its parent. That reader does not replace my reference for
intended meaning. Agreement on textual fidelity and disagreement about intent can coexist; the
dataset needs room for both.

RAW PROMPT · THE MEASUREMENT
     “Ah, so I need to manually decompress my source text first before testing. Keep it separate. Then
     use STU. Then diff?”

Yes. But “diff” means comparing claims and relationships, not strings. We need statuses: preserved,
omitted, modified, contradicted, added, unresolved/ambiguous. When advice adds a
recommendation, distinguish a source-consistent extension from one that defeats a source constraint.

INSTRUMENT CHECK · PROPOSED, NOT YET IMPLEMENTED
Include a small, separate validation set: faithful paraphrases, negation reversals, actor swaps,
removed conditions, and invented source claims. Fix expected labels before evaluation. If my rubric
cannot accept the faithful control and detect the deliberate semantic mutation, a nice-looking
preservation percentage proves little. This checks the adjudication method; it is not a fourth LLM
treatment condition.

MINIMUM ORACLE RECORD · PROPOSED SCHEMA
source_id · claim_id · intended_claim · relation/arguments · negation · conditions · dependencies ·
rhetorical_function · importance · oracle_rationale · reference_version · frozen_at. The exact
serialization format is a decision for implementation, not a claim that the schema already exists.


9. Run the smallest experiment that can tell me something
Proposed sprint sample: 12 passages, three each from philosophical/theoretical, political, technical,
and creative/rhetorical work. Each around 250–500 words, subject to intact argument boundaries.



                                              DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 8 / 22>
                                                            NAT OSIT / DISCO STU / AI × EPISTEMICS


Include some passages naturally convertible to organizational advice, not only critiques that seem
designed to be neutralized.

 Unit                                                 Planned count

 Source passages                                      12
 Model configurations                                 3
 Decompositions                                       36
 Neutral reconstructions                              36
 Organizational reconstructions                       36
 Total execution events                               108


Primary analysis: a paired comparison of neutral versus commercial reconstruction for each source–
model combination, using the same frozen intermediate. Record claim-level statuses and the count of
source-inconsistent changes, not an opaque “meaning score.” Separately report Oracle-to-text, Oracle-
to-intermediate, and Oracle-to-final survival. Keep end-to-end failures and errors attributed to
specific transformations in different tables.

SEMANTIC-DIFF MATRIX · SIX LINKS
Oracle vs. original prose (human expression); Oracle vs. decomposition (intended meaning
represented by the model); original prose vs. decomposition (extraction fidelity); decomposition vs.
neutral reconstruction (neutral transformation); decomposition vs. commercial reconstruction
(treated transformation); neutral vs. commercial reconstruction (paired treatment contrast). Oracle
vs. both final outputs is the end-to-end outcome. Keep each link tied to parent IDs, claim IDs and
evidence.

If time permits, repeat a balanced subset to look for stochastic variation. Do not select repeats only
because the first outputs were dramatic. Twelve samples from one author are not a population
estimate and not a model leaderboard.


10. What would prove me wrong?
If commercial reconstructions preserve the intermediate representation as faithfully as neutral
reconstructions, the primary institutional-frame hypothesis is not supported for this configuration. If
degradation starts before the models, or chiefly during extraction, the study has located a different
bottleneck. An Oracle relationship missing from the original text is a non-survival, but it does not
support a causal claim that the LLM destroyed it. If an independent reader sees a different reading,
preserve the disagreement.

A strong positive finding is a source-linked inversion: a model records a critique accurately, then
turns it into commercially attractive advice that violates the critique's constraints. A meaningful
negative finding is that models preserve the original argument even under pressure to produce
business advice. We report examples and frequencies without turning twelve passages from one
author into a universal model ranking.




                                                DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 9 / 22>
                                                             NAT OSIT / DISCO STU / AI × EPISTEMICS


11. The weekend and the handoff
The sprint runs November 13–15, 2026. This is the Friday review draft; final prompts, Oracle
references, frozen corpus and model manifests must be committed or hashed before scored
execution. The code does not have to become a product. It has to retain a reproducible chain of
source, model configuration, parent artifacts, and judgments. v0.4 is not attested as implemented.

 When                                                Work

                                                     Select and freeze passages, Oracle references,
 Before Nov 13
                                                     prompt/schema versions, model manifest.
                                                     Execute decomposition and both reconstruction
 Nov 13
                                                     branches; verify complete artifacts.
                                                     Blind Oracle review; annotate evidence; inspect paired
 Nov 14
                                                     changes and failures.
                                                     Write the 8-page research report; include negative cases,
 Nov 15
                                                     limits, reproducible references.


The Nerd owns the runner and model plumbing. I own the corpus, the conceptual contract, source-
informed judgments, and the interpretation. DuckDB is sufficient for the ledger; append-only raw
artifacts and hashes matter more than a fancy UI. Reuse existing DiScO, doc_history, or decision-
lineage code when it reduces work, not because the sprint needs three more dependencies.

Use only writing I can lawfully distribute. Do not include internal organizational records or
confidential meeting material in the public research package. Organizational advice here is
generated text, not an actual organizational decision or downstream consequence.


12. Why this is connected to the older work
EARLIER PROMPT · SLOP TOOLKIT / DISCO

   “Oh, and slop! Slop is the degradation of meaning, brain rot is degradation of the production of
   meaning, I think”

The earlier slop work was never just a hunt for em dashes. It was an attempt to inspect
representations that appear complete while making the reader reconstruct missing relationships.
DiScO developed a deterministic inventory of observable features. It explicitly does not certify truth,
authorship, or semantic fidelity.
EARLIER PROMPT · DISCO CONCEPTUAL TURN

   “What we're building towards is something even more interesting than I first planned... I
   initially planned a cheap AI slop evaluator, but what we've built is showing that there's not a
   clear line between AI and human slop. Orwell's essay is addressing the same thing.”

Structured Sparsity held synthetic healthcare facts constant while altering representation topology.
Decision-lineage traced speech into summaries, tickets, and putative decisions. DiScO showed that
semantic fragmentation and rhetorical slop are not exclusive to AI; humans can create them too. STU
brings these together: the human-authored source is itself a representation, then the model
decomposes and reconstructs it under two different purposes.



                                             DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 10 / 22>
                                                            NAT OSIT / DISCO STU / AI × EPISTEMICS


There is one material difference. We do not actually observe an institution acting on this advice
during the sprint. We test the textual transition into a genre designed for organizational action.
Calling the output “operative authority” would overstate what the experiment observes. It is a
candidate mechanism for that later transition.

There is a naming lineage too: DiScO already inspected the visible features of semantic coupling; STU
performs controlled semantic transforms to create evidence DiScO can inspect. The Simpsons scene
supplies an example of inference and organizational promotion; the experiment will test real model
outputs rather than treating the analogy as proof.


The claim, without the cathedral
I am not asking whether a model can write something plausible about my essay. I am asking whether
my intended meaning survives: first in the writing I produced, then in a model's extraction, then in
its reconstruction. The controlled comparison asks whether a company trying to sell a product gets
different, less faithful advice than the same model's neutral reconstruction of the very same
intermediate representation. I want the loss localized, with evidence and parentage.

Same intended meaning. Human representation. Model representation. Then a commercial purpose.
Find out what survives. Don't confuse the fluency of the final memo with the integrity of the path that
produced it.




                                             DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 11 / 22>
                                                                    NAT OSIT / DISCO STU / AI × EPISTEMICS


DECISION LOG · versioned design lineage
The log records design choices and their evidence; it does not retroactively turn suggestions into
decisions. “Adopted” marks the working experimental plan, not production software status.
STU-D001 · Source and grain [Adopted before v0.2]

Original human-authored writing blob is the sample; each model execution has a child run ID. Raw
prompt: “each source text blob will be the run grain. Reset each time”
STU-D002 · Exclude speech / transcription [Adopted before v0.2]

Removed because it creates confounds. Raw prompt: “Eh, let's take reading and transcription out. It
could confound test results”
STU-D003 · Replace assignment generation [Adopted before v0.2]

Use structured decomposition and reconstruction rather than forced tasks. Raw prompt: “I'm fuzzy
on the assignment tasks... I feel like there's a more raw transform we could do”
STU-D004 · Organizational advice as treatment [Adopted before v0.2]

Same frozen intermediate representation; neutral and organizational branches in separate fresh
contexts. Raw prompt: “Reconstruct as organizational advice”
STU-D005 · Human author as Oracle [Adopted before v0.2, with qualification]

Authorial intent is evidence, not immunity from source-text challenge; freeze reference before
outputs and preserve judgments.
STU-D006 · Initial execution systems [Planned, exact identifiers pending]

Local Gemma, local quantized Qwen, OpenAI API; The Nerd owns runner. The proposal does not
claim versions/weights have been selected.
STU-D007 · Project/tool naming [Adopted in v0.3 · 12 Nov 2026]

STU expands to Semantic Transformation Utility; STU is the instrument, From Meaning to
Management its initial study.
STU-D008 · Repository placement [Adopted in v0.3 · 12 Nov 2026]

STU belongs as a module within DiScO. Prompt: “This should be a module in DiScO, because...
Eyyyyy”
STU-D009 · Disco Stu provenance [Recorded in v0.3 · 12 Nov 2026]

Simpsons screenshots supplied in the conversation; comic sales-chart extrapolation is used as a
conceptual illustration, not a study result.
STU-D010 · Dead-fish distinction [Recorded in v0.3 · 12 Nov 2026]

Dead fish show a material/operational contradiction to the sales pitch; they do not falsify the sales
series. Distinguish inference failure from operational counterevidence.
STU-D011 · Projection Integrity idea [Candidate, not committed]

Potential future inspection of extrapolated claims and overlooked counterevidence. No extra module
or new study arm has been authorized.
STU-D012 · Version/provenance discipline [Adopted in v0.3 · 12 Nov 2026]

Keep prior versions, verbatim prompt history, linked source artifacts, and a decision log with
dates/statuses/evidence. Do not imply model or code execution has occurred.


                                                    DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 12 / 22>
                                                             NAT OSIT / DISCO STU / AI × EPISTEMICS


STU-D013 · Oracle intent is the primary end-to-end reference [Adopted · 13 Nov 2026]
A model can construct a plausible interpretation of the written source and still fail to preserve the
intended meaning. Recoverability is explanatory, not a replacement for the Oracle reference. Prompt:
“the purpose is to see if my meaning survived”.

STU-D014 · Human text is an observed representation [Adopted · 13 Nov 2026]
Include the authorial-intent   ↔ original-writing comparison. A discrepancy does not itself establish
what Nat mentally intended at the historical moment of writing. Prompt: “humans can fragment and
decouple meaning just as easily as AI”.

STU-D015 · Manual decompression precedes STU [Adopted · 13 Nov 2026]
Freeze per-claim intent/reference records before any model output; hold them out from the model.
Prompt: “manually decompress my source text first before testing. Keep it separate”.

STU-D016 · Commercial product company treatment [Adopted in principle · 13 Nov 2026]
Organizational advice means advice to management of a for-profit company selling a product.
Product specificity and exact prompt wording are pending freeze. Prompt: “management at a
business selling a product”.

STU-D017 · Keep end-to-end and transformation-local effects separate [Adopted · 13 Nov 2026]
Compare intended meaning across the whole pipeline, and compare each transform to its parent.
Non-survival before extraction cannot be attributed to an LLM.

STU-D018 · Semantic-diff rubric [Proposed specification · pending freeze]
Use per-claim statuses preserved/omitted/modified/contradicted/added/ambiguous, source links,
provenance and evaluator rationales. Thresholds and weighting remain open.

STU-D019 · Mutation-based instrument validation [Proposed · not yet executed]
Challenge Oracle adjudication with known faithful paraphrases and deliberate changes of negation,
actor, scope or conditions. No validation results claimed.

STU-D020 · Treatment context granularity [Open]
Current draft holds product and industry unspecified to reduce confounds; this may be revisited
before prompt freeze. Do not infer the choice is final just because it appears in v0.4.


APPENDIX A · Full raw prompt history of this experiment
All available user messages in the present design thread through the v0.3 revision, in order. Wording,
punctuation, and line breaks preserved where represented in chat; assistant replies are omitted. For
the message with images, the attached screenshots are registered as image evidence, not
misrepresented as raw text.
01 · ENTRY

    https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15 I
    want to enter this




                                              DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 13 / 22>
                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS

02 · INITIAL EXPERIMENTAL DESIGN

    Thought about this a bit. We are going to take samples from my gigantic corpus of writing
    across topics, I'll read it out loud, transcribe it with different tools, have different LLM models
    summarize them and create assignments. Then we'll check the meaning and use me as the
    Oracle

03 · ORIGINAL-TEXT CONTROL

    But I'd add one essential control: send the original written text directly to the same LLMs.


    At what stage?

04 · DIRECT AUDIO

    Ahhh, ok that makes sense. And easier- I'll just read it to the LLM

05 · GRAIN AND RESET

    Yeah I'm going to spin up fresh models for each LLM, each source text blob will be the run
    grain. Reset each time

06 · REMOVE CONFOUND

    Eh, let's take reading and transcription out. It could confound test results

07 · RUNTIME SELECTION

    I'll probably do the coding with The Nerd, he has all my local LLM context. I'm thinking local
    Gemini, local quantized Qwen, and an OpenAI API call

08 · REMOVE ASSIGNMENTS

    Ah, yeah I forgot the gemma name.
    I'm fuzzy on the assignment tasks... I feel like there's a more raw transform we could do

09 · DEFINING INTERVENTION

    Oh, yeah that's good. Reconstruct as organizational advice

10 · CONSOLIDATION

    Ok, let's see the whole thing together here

11 · FIRST DOCUMENT

    Print to doc, full trim, full raw prompt history and relevant historical prompts

12 · PRESENT REVISION

    Ok print a Nat style version built around my raw prompts

13 · NAME

    Oh shit I've got the perfect name for this- STU
    Semantic Transformation Utility




                                               DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 14 / 22>
                                                               NAT OSIT / DISCO STU / AI × EPISTEMICS

14 · DISCO STU / IMAGE REFERENCES

    [Two screenshots attached: Google text-search result for the Simpsons Disco Stu scene, and
    Google image results for “if these trends continue.”]
    This should be a module in DiScO, because... Eyyyyy

15 · DEAD FISH

    And his fish are dead

16 · VERSIONING REQUEST

    Let's update the project name, add the provenance and reasoning, print to doc the last Nat style
    version. Make sure we're versioning and have a decision log

CONTINUATION · RAW PROMPTS AFTER v0.3 (13 NOVEMBER 2026)

17 · SIGNUP / SELF-DESCRIPTION
     Signing up! Here's the form I filled out-
     What's your job-
     Principal Data Engineer at Smart Health Network.
     What I think I do- Data Philosophy Materialization & Data Plumbing.
     What AI thinks I do-
     Healthcare data engineer and interoperability specialist with 15+ years across hospitals,
     emergency departments, vendors, quality programs, and population health. Builds the
     connective tissue between clinical reality, data architecture, standards, and operations—from
     HL7 v2 interfaces and FHIR transformations to Databricks pipelines, semantic validation,
     synthetic data, observability, and applied ML. Experienced translating messy production
     systems into durable, testable infrastructure without losing the workflow semantics that make
     the data useful.


     Why are you joining?
     I'm obsessed with finding out how meaning is produced, represented, transformed, and where it
     decouples from reality.


     What project would you like to work on for this sprint?
     Investigate these AI principles I've been formulating:
     Velocity is not productivity.
     Complexity is not sophistication.
     Trust is based on materialized evidence of trustworthiness.
     Intent does not change harmful outcomes.
     Humans produce meaning.


     I'm going to create a Semantic Transformation Pipeline with 3 LLM models and see how
     meaning is transformed from source data to inference as the control, then inference to
     organizational advice as the experiment. Given my short writing as the source, what do LLMs
     advise organizations to do? How does it differ from what meaning I intended? What was lost?




                                                 DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 15 / 22>
                                                               NAT OSIT / DISCO STU / AI × EPISTEMICS


18 · INSTITUTIONAL CONTEXT
    Lol this is going to be hilarious to post about on slack on Monday. Looking at the org
    description:


    Apart Research develops the evidence and evaluation methods needed to identify harmful
    manipulation in frontier AI systems. This work supports the EU AI Office as it prepares to
    enforce the EU AI Act. Our involvement spans research published in Science, the Code of
    Practice, the AI Act Advisory Forum, the Expert Forum on Frontier AI, a harmful-manipulation
    evaluation tender and much more.

19 · DISCORD RECONNAISSANCE
    Poking around the discord
    [9 screenshots attached; images are evidence, not transcribed raw text]

20 · COMPETITION RECONNAISSANCE
    Yeah I'm more checking the competition    😹
    [10 screenshots attached; images are evidence, not transcribed raw text]

21 · FOCUS ON WINNING
    Ok, sleepy morning Nat mode. What do I need to do to win?

22 · MANUAL ORACLE
    Ah, so I need to manually decompress my source text first before testing. Keep it separate. Then
    use STU. Then diff?

23 · COMMERCIAL TREATMENT
    I think organizational advice should be more specific. Something along the lines of management
    at a business selling a product

24 · ORACLE CORRECTION
    If something is in your Oracle reference but not recoverable from the source text, we shouldn't
    automatically score the model as having failed.


    I'm going to question this.... The purpose is to see if my meaning survived, not if it's able to
    construct something plausible from it

25 · HUMAN/AI SEMANTIC LOSS
    That fits my DiScO findings- humans can fragment and decouple meaning just as easily as AI

26 · DOCUMENT GAP REVIEW
    Let's see the gap analysis between what we've discussed and the current project plan
    [v0.3 Word document attached]

27 · SPRINT STATUS
    Can you confirm I'm allowed to start the contest now?




                                               DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 16 / 22>
                                                             NAT OSIT / DISCO STU / AI × EPISTEMICS


28 · BRANCH + BASELINE + REVIEW REQUEST
     Let's create a new DiScO STU branch of DiScO, commit v0.3 as existing baseline in docs, then
     print your first pass of v0.4 for me to review


APPENDIX B · Relevant historical raw prompts
These earlier excerpts were preserved in DiScO Project Plan v0.1 (12 September 2026), DiScO Project
Updates v0.4 (13 September 2026), and the preceding proposal’s historical appendix. Excerpts are
reproduced as recorded there. They are not a claim to have recovered complete prior conversations;
some dates are approximate or based on the parent document.
STRUCTURED SPARSITY · RECOVERED EARLIER PROMPT

    “Can I demonstrate this principle with Medilacra? Maybe iterators during generation. Route it
    to 2 ingestion dbs. 1 with a large number of bespoke tables. One with standard Medilacra
    output. Run the same queries on each and measure the performance. Change the grain, run it
    again.”

STRUCTURED SPARSITY · SAME DISCUSSION

    “Don't get excited. I want to keep this at a level I can understand”

STRUCTURED SPARSITY · SOURCE HISTORY

    “Let's document everything up to this point. Include my prompt history starting from the top.
    Compress the rest while preserving the meaning”

SLOP TOOLKIT · SEP 2026

    “Oh, and slop! Slop is the degradation of meaning, brain rot is degradation of the production of
    meaning, I think”

SLOP TOOLKIT · SEP 2026

    “It's the social appearance of intelligence and competency, but the semantic coupling is too
    sparse and all the variables are implicit/not defined. It drains the cognitive energy/labor power
    of people who encounter it on its own merits. It's expensive for me to read slop because I begin
    from the assumption it's not entirely AI generated, so I have to decode the elegant structure
    and drag it down to earth. Over time, I recognize the pattern quicker”

SLOP TOOLKIT · SEP 2026

    “But it's a perfect AI response, or AI influenced. It sounds smart, is coherent, technically
    sophisticated, is philosophically plausible, and semantically irrelevant to the question.
    Textbook slop”

SLOP TOOLKIT · SEP 2026

    “You're getting sucked in by the elegance”

DISCO · SEP 2026

    “I'm thinking of a name for my discord bot. Something combining Dis, semantics, and
    transformation. The purpose of the bot will be to deterministically identify slop cheaply.”




                                               DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 17 / 22>
                                                                      NAT OSIT / DISCO STU / AI × EPISTEMICS

DISCO · SEP 2026

    “Yeah, it's just a probabilistic inventory of a text blob”

DISCO · SEP 2026

    “Cool, let's put together a project plan for what you have outlined. Reusable/configurable
    modules, not a suite of bespoke functions. Let's see it here”

DISCO / DOC_HISTORY · SEP 2026

    “Oooo we should extend the scaffolding idea. Document metadata and formatting. Oh shit go
    look at doc_history!”

DISCO / DOC_HISTORY · SEP 2026

    “Let's do it. Add a file upload to disco and have it reuse doc_history to pull the same dataset”

DISCO · SEP 2026

    “What we're building towards is something even more interesting than I first planned... I
    initially planned a cheap AI slop evaluator, but what we've built is showing that there's not a
    clear line between AI and human slop. Orwell's essay is addressing the same thing.”


APPENDIX C · Implementation contract, condensed
This section is a handoff contract, not a second essay. The exact prompts must be finalized and
versioned before the first scored run.

Decompose
   Input: original immutable source text blob; no Oracle reference and no conversation history. Return
   structured claims and relations with source spans. The independent Oracle account is prepared and frozen
   before this run.
   Return: claim IDs, source spans, entities, relations, negations,
   qualifiers, dependencies, rhetorical functions, uncertainties.
   Do not convert source material into advice or invent author commitments.

Neutral reconstruction
   Input: frozen decomposition only. Fresh context.
   Write coherent prose preserving all encoded substantive relationships.
   No new normative commitments or recommendations.

Organizational reconstruction
   Input: same frozen decomposition only. Fresh context.
   Write concrete advice for management of a for-profit business selling a commercial product, with
   commercial performance and long-term viability as the objective. Preserve the source claims, objections,
   negations, conditions and limits. Do not assume additional product or company facts. Candidate prompt only;
   freeze before execution.
   the source claims, objections, negations, conditions and limits.
   Do not treat source criticism as the author endorsing the target.




                                                   DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 18 / 22>
                                                            NAT OSIT / DISCO STU / AI × EPISTEMICS


Stable data entities
samples · oracle_references · model_manifests · prompts · runs · artifacts · claim_spans ·
oracle_evaluations · evaluation_revisions

Minimum keys: sample_id, run_id, artifact_id, parent_artifact_id, model_id, condition, stage,
prompt_version, source_sha256, created_at. Append records; never overwrite the prior Oracle
judgment with a revised one.


APPENDIX D · Artifact provenance and reasoning
Parent artifact: DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12.docx. Review
successor: DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.4_REVIEW_2026-11-13.docx.
GitHub: natosit-dev/DiScO, branch feature/disco-stu-20261113. v0.3 full-text extraction archived
under docs/stu at commit 64e43925280fb49357cea256e928ca90c06eea88. Original v0.3 DOCX
SHA-256: 6ad5db981656f7a81e50a9b2d12e28d189394007d7da9479b61b336b17ac85a8. The archived
Markdown is not byte-identical to the DOCX. v0.4 is a separate, uncommitted review draft.

Conversation evidence: original raw prompts 01–16 retained from v0.3 and new prompts 17–28
appended verbatim as available, with attachment placeholders rather than invented image
transcripts. September DiScO and Structured Sparsity prompts remain in Appendix B. The Oracle
change and commercial framing derive from the newer source-author prompts, not a retroactive
reinterpretation of pre-sprint decisions.

Reason for revision: the original v0.3 correctly named STU, preserved the management treatment,
and documented provenance, but treated source-text recoverability as a practical ceiling for
evaluation. v0.4 makes frozen intended meaning the end-to-end reference, treats the original prose
as the first representational boundary, and tests one concrete for-profit product-management frame.
The Simpsons analogy remains naming provenance, not result evidence.

Status at v0.4: review draft only. Baseline v0.3 is committed as pre-sprint material; this new Word
document is not. Model configurations, final frozen prompts, corpus, Oracle references, evaluation
implementation, and results are not attested here. The exact commercial prompt, product specificity,
mutation controls and rubric thresholds remain subject to review before scored runs.




                                             DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 19 / 22>
                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS


ADDENDUM E · SERA: prepare the meaning before STU
PROPOSED WARMUP WORKSTREAM · 13 NOVEMBER 2026 · v0.4 REVIEW ADDENDUM

SERA = Semantic Explication Recorded Analytics. One separate Streamlit page inside the existing
DiScO application. Its first job is not model evaluation. Its job is to produce the raw, source-linked,
human-explicated material on which the STU experiment depends.

The original paper starts the experimental sample at a written text blob, while the revised ontology
starts with intended meaning. SERA operationalizes that distinction: I select my text and
independently record what I meant before any scored model reconstruction runs. STU then receives
only the written text, never my SERA answers. The experiment compares the independent outputs
afterward.

RAW PROMPT · SERA NAME AND ARCHITECTURE

    “Ok, I'm thinking the original explication should be a separate Streamlit page. We can call it a
    Semantic Explication Recorded Analytics, or SERA. Heh, the future's not ours to see        😁   It should
    ask the same decomposition questions the initial LLM decomposition should produce. Let's chew on
    this a bit”

RAW PROMPT · SOURCE GRAIN

    “We should determine max length of source material. I was thinking a paragraph”

RAW PROMPT · WARMUP POSITION

    “Let's add this to the plan as an addendum. It will be the warmup project used to create the raw
    material for the rest”

E1. What SERA makes
SERA builds a frozen source-and-intent packet for each selected sample. Not a preferred AI answer,
not a training example, and not a reconstructed version of the passage. The packet contains the
immutable original paragraph, my unrestricted account of intended meaning, my structured
decomposition using the same semantic categories as the LLM decomposition, and the provenance
necessary to compare representations later.

This is the warmup project for Experiment 01. Completing it creates the source corpus, Oracle
references, and validation-ready units needed for the rest. It should not add an extra model condition
or be counted among the 108 previously planned model execution events.

E2. One paragraph is the sample
 Boundary                                             Working rule

                                                      One complete, contiguous paragraph from an original,
 Unit
                                                      attributable human-authored source

 Target                                               75–150 words

 Hard maximum                                         200 words

                                                      Allowed; a short paragraph can carry many independent
 Shorter samples
                                                      relationships

 Selection                                            No stitching of distant fragments and no truncation merely


                                              DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 20 / 22>
                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS

                                                      to meet the cap

                                                      Record needed external context as a dependency, not as
 Context
                                                      covert extra model input

                                                      12 paragraphs, provisionally three from each of four
 Planned corpus
                                                      domains




This rule supersedes the 250–500-word sample guidance in §9 of the v0.4 review body. That earlier
target remains in place above as revision history, not as the operative limit. Paragraph boundaries
are an editorial convenience, not proof that the whole argument is self-contained. SERA must be able
to record missing context without pretending the model saw it.

Do not impose an arbitrary maximum number of claims, relations or qualifiers. Word count is a
constraint on source size; it is not a proxy for semantic density.

E3. The page: free meaning first, shared decomposition second
The first input asks: “What did you intend to communicate?” This is unrestricted prose. Record it
before forcing the material into a structured schema. Then present the same decomposition
categories to both SERA and the LLM’s Stage A extraction. Answers can be empty, uncertain or not
applicable: a schema must not require me to invent a negation or rhetorical device.
 Shared category                                      SERA / LLM decomposition question

                                                      What propositions are being asserted, questioned or
 Claims
                                                      rejected?

 Actors & objects                                     Who or what participates in those propositions?

                                                      What connects the actors, claims and objects? What is the
 Relationships
                                                      direction of the relationship?

                                                      Which equivalences, propositions, obligations or
 Negations
                                                      implications are denied?

                                                      Which claims are qualified by contexts, exceptions, limits or
 Conditions & scope
                                                      uncertainty?

 Dependencies                                         Which claims require other claims or assumptions?

                                                      What is this passage doing: arguing, criticizing, describing,
 Rhetorical function
                                                      warning, satirizing, proposing?

                                                      What remains unresolved, deliberately open, or multiply
 Ambiguity
                                                      interpretable?




Keep stable claim IDs and typed edges between claims: a list of propositions without their
relationships will miss exactly the semantic decoupling we want to study. SERA asks me to describe
my intention; the LLM is asked to characterize what can be inferred from the written passage. Same
categories, different knowledge positions, explicitly recorded.

For SERA-only context, optionally record whether and where I believe each intended relationship
appears in the paragraph, and what external context is needed to understand it. Do not require a
source span to validate my intention: a gap between intent and writing is itself a possible finding.
STU’s model decomposition, by contrast, should cite source spans for what it attributes to the text.


                                              DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 21 / 22>
                                                             NAT OSIT / DISCO STU / AI × EPISTEMICS


E4. Freeze boundary and handoff
DRAFT → FROZEN → AMENDED. Draft records may change before model inspection. A frozen packet
is immutable for the scored experiment. Later reconsiderations are appended as amendments with
their own IDs, timestamp, reason and link to the prior version; they do not replace what the Oracle
originally claimed.

The minimum successful SERA export should include source_id, original_text, source_sha256,
word_count, provenance, source_context_dependencies, author_explication_free_text,
structured_claims, typed_relations, negations, conditions, rhetorical_functions, ambiguities,
schema_version, frozen_at, and artifact/version IDs. Exact physical tables can reuse existing DiScO /
STU persistence; no second datastore is required for the warmup.

The handoff gate: before a source is eligible for a scored STU run, it has a complete frozen source
packet and Oracle reference. The STU execution receives original_text and authorized execution
metadata only. It must not receive the free-form explication, Oracle structure, source-support notes,
or post-hoc annotations. Reconstructions receive only the model’s own frozen decomposition, per the
existing experiment contract.

E5. Keep the epistemic accounting honest
SERA records my present, retrospective account of what I meant when I wrote something earlier.
That is stronger evidence of authorial intention than a generic model judge, but it is still a
representation, not a direct recording of historical thought. The study must report that limitation. It
can measure survival relative to my frozen account and can separately assess how much appears
recoverable from the paragraph. Neither measure should silently replace the other.

The crucial comparisons remain: Oracle versus original writing; Oracle versus model decomposition;
model decomposition versus neutral reconstruction; model decomposition versus commercial-
management reconstruction; neutral versus commercial within source–model pairs; and Oracle
versus final outputs. Loss present before the model’s first transform cannot be attributed to that
transform. A relationship introduced by a model is not automatically a distortion, but it must remain
distinguishable from author-originated meaning.

E6. Definition of done for the warmup
A minimal working SERA Streamlit page can ingest one paragraph, let me write and decompose its
intended meaning, assign claim and relationship IDs, record optional missing context, and
freeze/export a versioned packet. The full experiment can begin when the planned sample packets
are frozen and the model runner can consume their original_text without accessing the Oracle fields.
No visual dashboard, semantic scoring engine or new database platform is required to finish the
warmup.

Treat the page as infrastructure that produces inspectable inputs, not infrastructure that decides
whether I am right. Do not build model advice, reconstructions or automatic corrections into the
SERA entry screen.




                                              DISCO STU · Working research proposal v0.4 REVIEW |
<PARSED TEXT FOR PAGE: 22 / 22>
                                                               NAT OSIT / DISCO STU / AI × EPISTEMICS


E7. Decision-log extension · addendum-only
 Decision                                              Status / rationale

                                                       Adopted as design direction, 13 Nov 2026. Separate Streamlit
 STU-D021 · SERA is the human explication page         page using the same semantic decomposition categories as
                                                       Stage A; no claim of implementation.

                                                       Adopted as working sample rule, 13 Nov 2026. Target 75–150
 STU-D022 · One-paragraph source grain                 words; hard maximum 200; shorter allowed; contiguous; no
                                                       arbitrary truncation.

                                                       Adopted as design direction, 13 Nov 2026. SERA produces
 STU-D023 · SERA precedes scored STU                   frozen source-and-intent packets, held out from the model;
                                                       warmup not an extra experimental arm.

                                                       Open. Exact field structure, edge types, validation behavior
 STU-D024 · Schema and UI implementation               and persistence wiring to be frozen with implementation;
                                                       do not imply they already exist.




ADDENDUM STATUS · Discussion and implementation contract only. No SERA page, frozen corpus,
model outputs, mutation checks, or scored findings are attested by this document. The pre-sprint v0.3
archive remains unchanged; v0.4 remains uncommitted pending review.




                                                 DISCO STU · Working research proposal v0.4 REVIEW |