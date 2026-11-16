# Field Notes: The Dashboard Is Not the Experiment

*DiScO STU — From Meaning to Management*  
*Post-submission discussion, 15 November 2026; documented 16 November 2026*

## The conversation

After completing the Apart Research AI × Epistemics sprint, I shared DiScO STU with colleagues.

The project was available as a GitHub repository containing a Streamlit interface, Python services, experimental records, and documentation. Users could install it locally and reproduce the workflow.

A colleague suggested improving its presentation. The proposed additions included a public landing page, interactive results visualizations, adjustable parameters, browser-based execution, and more polished graphics. Claude could generate much of this quickly, potentially in less than an hour.

The suggestion wasn't unreasonable. A research repository and a public demonstration serve different purposes. Someone evaluating the project might reasonably want to inspect the results without installing Python dependencies.

But the proposed implementation introduced a different question:

**What additional work would be required to establish that the new interface accurately represented the experiment?**

## Why I deliberately built an ugly interface

My first response was practical:

> I purposefully make ugly UIs so I don't get dragged into UI/Java development 😅

That was partly a joke.

Streamlit is common among data scientists. I deliberately built the interface as a thin client over reusable Python services, so that the scientific operations weren't dependent on the interface.

The research instrument needed to capture original writing, preserve independently recorded human intention, execute controlled transformations, retain evidence, and record human assessments.

It did not need an elaborate frontend.

I explained:

> The simplicity is part of the point. Streamlit is common among data scientists, and though Claude could produce something more elegant, I'd need to review the code, test, fix, test, justify the addition, and determine if it adds any confounds. For a research project, not worth it IMHO

Generating an implementation is one activity. Establishing that it does the right thing is another.

## Assumptions don't become valid because we list them

The conversation then shifted toward hypothetical results.

One suggestion involved allowing viewers to adjust parameters and explore how results might change. Another involved documenting the assumptions behind those visualizations and asking Claude to audit them.

I asked:

> What if an assumption is missing?

An automated system can evaluate the assumptions it has been given. It may discover inconsistencies or omissions. That does not independently establish that the assumptions are complete.

There is also an important distinction between two kinds of visualization.

An interface that displays recorded experimental observations is a presentation of evidence.

An interface that allows users to change experimental parameters and produces hypothetical results is running a model of the experiment.

That model has its own assumptions, implementation, and validation requirements.

The original DiScO STU experiment does not establish how its results would change under conditions it never executed.

Presenting simulated outcomes alongside observed ones without a clear distinction would create another semantic transformation requiring evaluation.

## The downstream problem

My colleague argued that a sprint results page was unlikely to become mission-critical infrastructure and could be removed after judging.

I questioned that assumption.

Sprint participants were being encouraged to seek grants and venture funding. A demonstration intended only for judging could become material used to communicate research findings, justify investment, or support further development.

This does not mean a dashboard would inevitably cause harm.

It means the intended lifespan of a representation is not sufficient evidence of how it will eventually be used.

I recalled a question a pediatric doctor once asked me while I was installing emergency department software:

> What if it misses an assumption and a child dies as a result?

That question is not evidence that this proposed dashboard carried a comparable risk. The systems and consequences are different.

It illustrates why I've learned not to treat the absence of an identified failure as evidence that relevant failures have been excluded.

## My development method

I explained how I approach building systems:

> I approach things a bit differently, I build slow at first, interrogating everything and making sure I understand how it's wired. I end up with a bunch of reality tested components. Then I build with them, test at a larger scale, tear it apart, find new components. Repeat. Keeps me grounded, if I don't understand something I ask

This is why the original experiment began with a small amount of source material, fixed transformation conditions, and independently preserved evidence.

The apparatus expanded as requirements became concrete.

It also contracted when we discovered that unnecessary semantic structures and interface obligations were imposing additional human work.

## What DiScO STU actually measures

The initial experiment tested how meaning changed when human-authored writing was decomposed by a language model and reconstructed as neutral prose or commercial-management advice.

Its human review layer recorded the active time spent explaining differences between the original and transformed texts.

That recorded interval is not a complete measurement of human cognition. Reading, reflection, and unrecorded work remain outside it.

But the explanatory work is an observable part of the experiment.

After discussing the proposed visualizations, I wrote:

> The Disco STU experiment tests whether doing so would add value to the project, or add confounds and displace the semantic reconstruction costs. The review time at the end measures that cognitive labor time

Strictly speaking, the completed experiment tested textual reconstruction, not alternative dashboard implementations. The conversation raised an additional application of its research question.

If I add a visualization, its usefulness must be established against the work required to create, understand, validate, and maintain it.

A more elaborate interface may be worth that work.

The ability to generate it quickly does not establish that it is.

## Field observation

The discussion revealed a genuine distinction between making research accessible and changing the apparatus that produced it.

An independent presentation layer could improve access to existing results. A new interactive simulation would introduce additional scientific claims requiring independent evidence.

Those are different development tasks.

The conversation also illustrated the labor-accounting problem motivating DiScO STU. The apparent cost of generating software can be much smaller than the cost of establishing what the software actually does.

I declined to add new experimental machinery simply because it could be generated quickly.

The project already had functioning components, completed experiments, archived evidence, and human assessments.

**Velocity is not productivity.**

**Coherence is not accuracy.**

**Complexity is not sophistication.**

---

*Provenance: Field note based on screenshots of an informal discussion, with my messages quoted and the colleague's suggestions paraphrased. The colleague was not a sprint participant. Screenshots and identifying details are not included. This is a post-experiment methodological reflection, not a third controlled observation.*
