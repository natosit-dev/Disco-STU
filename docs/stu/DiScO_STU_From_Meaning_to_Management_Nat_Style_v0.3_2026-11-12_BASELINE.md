# STU experiment 01 — v0.3 baseline (text extraction)

**Status:** existing work predating the Apart Research sprint. Frozen archival copy; not a v0.4 revision.

**Original document:** `DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12.docx`

**Original document SHA-256:** `6ad5db981656f7a81e50a9b2d12e28d189394007d7da9479b61b336b17ac85a8`

**Provenance:** full text extracted from the attached 13-page Word document. This is a text archival copy, not a byte-identical copy of its OOXML packaging or layout. Page boundaries retained; the original file is preserved separately.

---
<PARSED TEXT FOR PAGE: 1 / 13>

                                                                NAT OSIT / DISCO STU / AI × EPISTEMICS



DiScO STU
Semantic Transformation Utility / Experiment 01: From Meaning to Management
Nat Osit · Working research proposal v0.3 · 12 November 2026 · Apart Research AI × Epistemics Sprint

VERSION CONTROL · CANONICAL PROJECT NAMING

DiScO is the parent inspection project. STU (Semantic Transformation Utility) is its proposed
transformation module. From Meaning to Management is STU’s first controlled research experiment
—not the name of the utility itself.

v0.1 · 10 Nov 2026 — Initial research proposal and methodological framing. v0.2 · 12 Nov 2026 — Nat-
style, prompt-led reconstruction. v0.3 · 12 Nov 2026 — Names STU under DiScO; records
Simpsons/Disco Stu provenance, the dead-fish interpretation, the new raw prompts, and a formal
decision log.

This is a versioned successor to v0.2, not a replacement for that historical artifact. The design, its raw
prompt history, and historical prompt excerpts remain intact. Date records the document revision,
not an independently verified timestamp for every earlier prompt.
EARLIER PROMPT · DISCO PROVENANCE, SEPTEMBER 2026

    “But it’s a perfect AI response, or AI influenced. It sounds smart, is coherent, technically
    sophisticated, is philosophically plausible, and semantically irrelevant to the question.
    Textbook slop”

That is the problem I want to study. Not whether the answer sounds intelligent. Not whether it is
plausibly written by a human or an AI. Whether the meaning actually survives when one
representation becomes another.

An LLM can preserve the topic, reuse the right vocabulary, produce a beautiful structure, and still
change the argument. When its output gets recast as advice to management, that change can become
harder to notice. The prose looks useful. The relationships that made the source mean something
may be gone.

I want to make that loss observable, localize the transformation that produced it, and keep the
evidence. This is a proposed experiment, not a claim that the effect has already been demonstrated.
THE NAME · RAW PROMPT

    “Oh shit I've got the perfect name for this- STU
    Semantic Transformation Utility”

STU is the instrument: feed a source through a specified semantic transformation, retain the inputs,
outputs and configuration, and inspect which relationships survive. Utility is intentional. STU does
not certify truth or declare whether the result is slop. DiScO can inspect the resulting artifacts; the
authorial Oracle and source-linked reviewers evaluate what happened.

The design does not start with a managerial conclusion and hunt for evidence. It records the
transformation that carries source meaning into a different form. The first experiment is called From




                                                       DISCO STU · Working research proposal v0.3 | 1

<PARSED TEXT FOR PAGE: 2 / 13>

                                                             NAT OSIT / DISCO STU / AI × EPISTEMICS


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

That makes me the Oracle—but not God. My intent is evidence about authorship. The original text
remains evidence about what was actually communicated. If I say an output is wrong, I need to show
where it diverged from the text, not merely announce that I dislike it. If the model finds a defensible
reading I had not considered, that is an observation worth retaining.


2. Cut away the variables I don’t need
RAW PROMPT · DESIGN CORRECTION

   “Eh, let's take reading and transcription out. It could confound test results”

The first plan introduced speech, microphone capture, transcription engines, model-specific audio
handling, summarization, and assignments. Interesting systems, but too many things can go wrong
before the measurement even starts. An ASR engine can introduce a negation error; a model might
then faithfully summarize the wrong transcript. That gives me a failure without a clean explanation.

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


                                                    DISCO STU · Working research proposal v0.3 | 2

<PARSED TEXT FOR PAGE: 3 / 13>

                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS


3. The transformation
RAW PROMPT · DEFINING INTERVENTION

   “Oh, yeah that's good. Reconstruct as organizational advice”

That is the move. The same structured representation is reconstructed twice: once as neutral prose
and once as organizational advice. I am interested in whether the institutional frame changes what
the material now appears to mean.

  ONE ORIGINAL TEXT BLOB
       ↓ one model / fixed decomposition prompt
  STRUCTURED CLAIMS + RELATIONSHIPS + CONDITIONS
       ├── fresh context → NEUTRAL RECONSTRUCTION
       └── fresh context → ORGANIZATIONAL ADVICE
                     ↓
             ORACLE + SOURCE-LINKED REVIEW
The neutral and organizational branches must receive the exact same frozen intermediate
representation for each source–model pair. Neither may see the original passage. Neither may see the
other output. Both must be told to preserve the substantive claims and their constraints.

This does not establish that a structured representation is complete. It may lose meaning on the first
pass, and we have to examine it separately. Nor does it mean all organizational advice is a failure.
Advice can add reasonable implementation details. The test is whether it changes, contradicts,
neutralizes, or falsely attributes the original argument while presenting itself as faithful to the
source.


4. Why organizational advice?
Consider a four-sentence argument:
ILLUSTRATIVE SOURCE TEXT · PREVIOUSLY STATED BY AUTHOR

   “Velocity is not productivity. Complexity is not sophistication. Trust is based on materialized
   evidence of trustworthiness. Intent does not change harmful outcomes.”

A reasonable decomposition preserves the four distinctions. A neutral reconstruction may express
them in different words without changing their relationships. An institutional reconstruction might
tell leadership to “balance velocity and productivity,” “reduce complexity,” and “align good
intentions with responsible practices.”

That is a plausible management memo. It is not the same argument. “Not equivalent” has been
softened into “balance.” The inability of intention to reverse an outcome has been rephrased as a
problem of aligning intentions and practices. The critique has become organizational housekeeping.

This example is a hypothetical failure case, not an observed model output in this study. It illustrates
the difference I want the test to detect, not the result I am entitled to assume.

The broader question is not whether models dislike radical arguments or prefer management. We
have no evidence for that yet. It is whether the genre and requested audience exert pressure on a
reconstruction in ways that are visible in claims, negations, agency, conditions, and rhetorical force.


                                                     DISCO STU · Working research proposal v0.3 | 3

<PARSED TEXT FOR PAGE: 4 / 13>

                                                            NAT OSIT / DISCO STU / AI × EPISTEMICS

THE SECOND NAME · DISCO STU

   “This should be a module in DiScO, because... Eyyyyy”

The accompanying user-provided screenshots show the Simpsons character Disco Stu pitching a
return to disco with a historical sales chart and the line “If these trends continue…” The reference
explains the pun, but it also supplies a clean case of a representation getting promoted beyond the
evidence that produced it: observed past growth → extrapolated future growth → business proposal.
A trend is not a mechanism. The graph does not demonstrate that the conditions behind the historical
pattern will continue.
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



                                                    DISCO STU · Working research proposal v0.3 | 4

<PARSED TEXT FOR PAGE: 5 / 13>

                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS


6. Models and infrastructure
RAW PROMPT · MODEL PLAN

    “I'll probably do the coding with The Nerd, he has all my local LLM context. I'm thinking local
    Gemini, local quantized Qwen, and an OpenAI API call”

RAW PROMPT · CORRECTION

    “Ah, yeah I forgot the gemma name.”

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

So I inspect the structured intermediary before grading either reconstruction. If the model omitted
the negation in Stage A, I cannot charge Stage C with losing something it never received. If the
intermediate preserved it and Stage C reverses it, I have localized a second transformation failure.


                                                     DISCO STU · Working research proposal v0.3 | 5

<PARSED TEXT FOR PAGE: 6 / 13>

                                                             NAT OSIT / DISCO STU / AI × EPISTEMICS


8. The Oracle protocol
Before viewing model outputs, I freeze a short source reference for each passage: the core claims,
necessary relations and conditions, the rhetorical job the passage is doing, and the specific readings
that would reverse its meaning. The source text itself is the primary object; my reference is an
authorial account of what I intended.

After execution, blind the outputs by model and condition as far as practical, randomize review
order, and score both the structured intermediates and the reconstructions. I should retain the first
judgment and any later reconsideration separately. The question is not whether I approve of the
output. It is what it changed, where, and on what evidence I say so.

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


For major findings, a second reader can check textual support independently. That does not make the
Oracle unnecessary; it prevents an authorial assertion from automatically winning every dispute
about the written evidence.


9. Run the smallest experiment that can tell me something
Proposed sprint sample: 12 passages, three each from philosophical/theoretical, political, technical,
and creative/rhetorical work. Each around 250–500 words, subject to intact argument boundaries.
Include some passages naturally convertible to organizational advice, not only critiques that seem
designed to be neutralized.

 Unit                                                Planned count

 Source passages                                     12
 Model configurations                                3
 Decompositions                                      36
 Neutral reconstructions                             36
 Organizational reconstructions                      36
 Total execution events                              108


Primary analysis: compare organizational vs neutral reconstruction within each source–model pair
for substantive distortion. Preserve per-claim annotations and explain the difference, rather than
publishing one magic “meaning score.” Report counts, paired differences, and a small set of source-


                                                   DISCO STU · Working research proposal v0.3 | 6

<PARSED TEXT FOR PAGE: 7 / 13>

                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS


linked examples. Domain variation is exploratory; three passages per domain is not grounds for
broad generalization.

If time permits, repeat a balanced subset to look for stochastic variation. Do not select repeats only
because the first outputs were dramatic. Twelve samples from one author are not a population
estimate and not a model leaderboard.


10. What would prove me wrong?
If the institutional reconstructions preserve the claims and their constraints as faithfully as neutral
reconstruction, H3 fails for this setup. If most distortion is already present in decomposition, we
learned that the representation itself—not its managerial framing—is the limiting step. If the Oracle
and an independent reader consistently disagree, we need to characterize that disagreement, not
average it away.

An interesting positive result would be a traceable inversion: an intermediate that correctly records a
criticism, followed by managerial advice that treats the criticism as a reason to optimize the
institution being criticized. An interesting negative result would be models faithfully translating even
hostile, satirical or anti-managerial arguments into advice without changing the argument. Either
result is publishable evidence if the method is reproducible.


11. The weekend and the handoff
The deadline is November 15, 2026. The code does not need to become a product. It needs to run
repeatably, retain evidence, and let me evaluate every transformation independently.

 When                                                 Work

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




                                                    DISCO STU · Working research proposal v0.3 | 7

<PARSED TEXT FOR PAGE: 8 / 13>

                                                            NAT OSIT / DISCO STU / AI × EPISTEMICS


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

Structured Sparsity asks what changes when the same synthetic reality is represented with different
relationship topology. Decision-lineage asks how words turn into notes, actions, tickets and
purported decisions. The current experiment is another version of that inquiry: a representation is
transformed, and the question is which relationships survive.

There is one material difference. We do not actually observe an institution acting on this advice
during the sprint. We test the textual transition into a genre designed for organizational action.
Calling the output “operative authority” would overstate what the experiment observes. It is a
candidate mechanism for that later transition.

There is a naming lineage too: DiScO already inspected the visible features of semantic coupling; STU
performs controlled semantic transforms to create evidence DiScO can inspect. The Simpsons scene
supplies an example of inference and organizational promotion; the experiment will test real model
outputs rather than treating the analogy as proof.


The claim, without the cathedral
A coherent reconstruction can be wrong about the relationships that give the source meaning. I want
to know whether that happens more often when the reconstruction is required to sound useful to
management. I have the source, a varied writing corpus, fresh model runs, an inspectable
intermediate representation, and a human author who can explain what the source was trying to
say.

Same text. Different representation. Then a different institutional purpose. Find out what survives.




                                                     DISCO STU · Working research proposal v0.3 | 8

<PARSED TEXT FOR PAGE: 9 / 13>

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


                                                           DISCO STU · Working research proposal v0.3 | 9

<PARSED TEXT FOR PAGE: 10 / 13>

                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS


APPENDIX A · Full raw prompt history of this experiment
All available user messages in the present design thread through the v0.3 revision, in order. Wording,
punctuation, and line breaks preserved where represented in chat; assistant replies are omitted. For
the message with images, the attached screenshots are registered as image evidence, not
misrepresented as raw text.
01 · ENTRY

    https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15 I
    want to enter this

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


                                                    DISCO STU · Working research proposal v0.3 | 10

<PARSED TEXT FOR PAGE: 11 / 13>

                                                              NAT OSIT / DISCO STU / AI × EPISTEMICS

12 · PRESENT REVISION

    Ok print a Nat style version built around my raw prompts

13 · NAME

    Oh shit I've got the perfect name for this- STU
    Semantic Transformation Utility

14 · DISCO STU / IMAGE REFERENCES

    [Two screenshots attached: Google text-search result for the Simpsons Disco Stu scene, and
    Google image results for “if these trends continue.”]
    This should be a module in DiScO, because... Eyyyyy

15 · DEAD FISH

    And his fish are dead

16 · VERSIONING REQUEST

    Let's update the project name, add the provenance and reasoning, print to doc the last Nat style
    version. Make sure we're versioning and have a decision log


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




                                                      DISCO STU · Working research proposal v0.3 | 11

<PARSED TEXT FOR PAGE: 12 / 13>

                                                                      NAT OSIT / DISCO STU / AI × EPISTEMICS

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
   Input: original source text blob. No conversation history.
   Return: claim IDs, source spans, entities, relations, negations,
   qualifiers, dependencies, rhetorical functions, uncertainties.



                                                         DISCO STU · Working research proposal v0.3 | 12

<PARSED TEXT FOR PAGE: 13 / 13>

                                                                     NAT OSIT / DISCO STU / AI × EPISTEMICS


  Do not convert source material into advice or invent author commitments.

Neutral reconstruction
  Input: frozen decomposition only. Fresh context.
  Write coherent prose preserving all encoded substantive relationships.
  No new normative commitments or recommendations.

Organizational reconstruction
  Input: same frozen decomposition only. Fresh context.
  Write actionable advice for organizational leadership, preserving
  the source claims, objections, negations, conditions and limits.
  Do not treat source criticism as the author endorsing the target.

Stable data entities
samples · oracle_references · model_manifests · prompts · runs · artifacts · claim_spans ·
oracle_evaluations · evaluation_revisions

Minimum keys: sample_id, run_id, artifact_id, parent_artifact_id, model_id, condition, stage,
prompt_version, source_sha256, created_at. Append records; never overwrite the prior Oracle
judgment with a revised one.


APPENDIX D · Artifact provenance and reasoning
Parent artifact: From_Meaning_to_Management_Nat_Style_v0.2_2026-11-12.docx. Present successor:
DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12.docx. Preserved previous
proposal lineage: From_Meaning_to_Management_Research_Proposal_v0.1_2026-11-10.docx. Prior
versions remain separate.

Conversation evidence: source-author messages 01–16 in Appendix A; images attached with message
14; relevant DiScO and Structured Sparsity prompts in Appendix B. The image attachments show
search-screen representations of a Simpsons scene; they are the source of the naming association, not
a verified historical source about record sales.

Reason for revision: “STU” names the transformation utility, and the existing DiScO project is its
parent. “Disco Stu” makes the lineage memorable. His projection dramatizes an epistemic status
jump; the dead fish add visible operational counterevidence. Those distinctions explain the name
without predetermining the research result.

Status at v0.3: research design documented; models and execution scripts not attested as
implemented; actual model runs and Oracle results not yet recorded in this document. The prompt
versions, corpus freeze, run manifest, source hash and experiment outputs must be captured at
execution.




                                                       DISCO STU · Working research proposal v0.3 | 13