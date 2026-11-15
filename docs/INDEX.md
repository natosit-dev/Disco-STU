# DiScO STU · Documentation Index

**Repository:** [natosit-dev/Disco-STU](https://github.com/natosit-dev/Disco-STU)  
**Experiment 01:** *From Meaning to Management*  
**Index established:** 14 November 2026  
**Status:** SERA is on `main`; the deterministic STU pipeline is in [draft PR #1](https://github.com/natosit-dev/Disco-STU/pull/1), **not merged**. No scored LLM experiment is documented.

Use this page to find the **authoritative document for a question**. Historical plans stay intact; later documents do not silently revise earlier decisions. A planning document is not implementation evidence.

## Start here

| Question | Read this | Status / authority |
| --- | --- | --- |
| What are we trying to learn, in Nat's words? | [Nat-style research plan v0.5](stu/DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.5_2026-11-13.md) | **Current consolidated research narrative**; includes raw prompts and complete **STU-D001–D038** decision log. Working plan, **not a frozen scored protocol** |
| What has actually been built and tested? | [Deterministic Build — factual handoff](handoff/Disco_STU_Deterministic_Build_Full_Handoff_Radiant_Control_2026-11-14.md) | **As-built evidence report**, sourced to implementation commit `98f5036` and draft PR #1; reports 25 automated tests passing, deterministic fixtures only |
| What is The Nerd supposed to implement? | [The Nerd complete-pipeline handoff](handoff/NERD_HANDOFF_STU_COMPLETE_PIPELINE_v0.1_2026-11-14.md) | Original requirements/handoff; later implementation choices and current status must be checked against the factual build report |
| What did The Nerd get approval to build? | [Full deterministic build plan](stu/DISCO_STU_FULL_BUILD_PLAN_v0.1_2026-11-14.md) | **Implementation design baseline**; its pre-authorization wording records the state when written, not current authorization |
| What changed after the human caught the review-workload drift? | [**Wait, What??! — human intervention**](interventions/Wait_What_Intervention_DiScO_STU_2026-11-14.md) | **Current corrective design record**; distinguishes the 2 final-output reviews from 8 diagnostic comparisons, the 15-minute Boolean from idle-time uncertainty, and proposed changes from implemented code. Includes 21 raw prompts and decisions WWH-01–WWH-09. **Not a scored result** |
| What are SERA's original requirements? | [SERA build plan](sera/BUILD_PLAN_v0.1.md) | Adopted progressive-explication design contract |
| What does SERA save and expose? | [SERA data contract](sera/DATA_CONTRACT.md) and [shared semantic JSON Schema](../schemas/semantic_v0.1.json) | Implemented SERA structure / Oracle isolation and serialization rules |

## Human intervention and change lineage

[**Wait, What??!**](interventions/Wait_What_Intervention_DiScO_STU_2026-11-14.md) documents the author's correction of an AI-generated workflow interpretation: a deterministic rig may materialize eight comparison *types* without requiring eight manual reviews. The human baseline remains **one SERA explication per source** and **two final-output gap explanations per model**. It also records that **reaching fifteen minutes** is a candidate labor-budget Boolean and must be tracked separately from a suspect/idle review interval.

**Status:** documented intervention and proposed corrections, not implementation evidence or an empirical finding. See WWH-01–WWH-09; preserve earlier STU decision history.

## Runtime and technical evidence

The deterministic implementation lives on the unmerged branch [`feature/stu-deterministic-pipeline-20261114`](https://github.com/natosit-dev/Disco-STU/tree/feature/stu-deterministic-pipeline-20261114).

- [Implementation instructions](https://github.com/natosit-dev/Disco-STU/blob/feature/stu-deterministic-pipeline-20261114/docs/stu/IMPLEMENTATION.md) — commands, CLI, fixtures, limits.
- [Work log](https://github.com/natosit-dev/Disco-STU/blob/feature/stu-deterministic-pipeline-20261114/docs/WORK_LOG.md) — build decisions, reuse boundaries and testing notes.
- [Prompt files](https://github.com/natosit-dev/Disco-STU/tree/feature/stu-deterministic-pipeline-20261114/prompts) — candidate `decompose_v0.1`, `neutral_v0.1`, `commercial_v0.1`; versioned, **not empirically validated** against real models.
- [Implementation commit](https://github.com/natosit-dev/Disco-STU/commit/98f50367c6458f840c5fd1cf0b1ba3b22ed6c7d6) and [draft PR #1](https://github.com/natosit-dev/Disco-STU/pull/1) — source and review history.

**Evidence boundary:** Passing fixture tests demonstrate that the pipeline can execute its specified deterministic operations. They do **not** establish semantic preservation, model behavior, reviewer accuracy, or scientific validity. UI startup tests are not a complete human browser walkthrough.

## Historical research archive — preserve, don't promote

- [v0.3 pre-sprint baseline](stu/DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12_BASELINE.md) — frozen November 12 source-history record and decisions; retained for provenance.
- [v0.4 working draft and SERA addendum](stu/DiScO_STU_From_Meaning_to_Management_v0.4_REVIEW_SERA_ADDENDUM_2026-11-13.md) — working intermediate revision, including superseded length/sample guidance in its historical body.
- [Fancy AI Cathedral Plan v0.1](stu/Fancy_AI_Cathedral_Plan_v0.1.md) — earlier consolidated planning draft, **superseded as the narrative entry point by Nat-style v0.5**. Retained as a deliberate snapshot of reasoning, not the current protocol.

The Nat-style v0.5 file is a Markdown transcription of the original 20-page DOCX; the deterministic build report is a Markdown transcription of the original 12-page DOCX. Each includes the original Word file name and SHA-256. These preserve the source text, ordered tables and available hyperlinks, but **not the DOCX binary or original pagination**.

## Open gates

1. Complete a human-driven SERA → Transform → Review → Results walkthrough on the feature branch; check persistence and UI state.
2. Decide and implement real Gemma, Qwen and OpenAI adapters. **No actual model execution is established by the deterministic report.**
3. Freeze the scored study's corpus, model manifests, prompts, semantic adjudication, review masking/order and timing interpretation before claiming experimental findings.
4. Preserve exact Oracle-version pins. Do not silently compare older runs against newer explications.
5. Resolve the relationship between the 15-minute review threshold as a **labor-budget/Boolean observation** and the current implementation's `timing_uncertain` handling. The threshold is not automatically a data-quality failure; freeze its final measurement semantics before scored runs.

**Licensing:** [Docs](../LICENSE-DOCS.md) use CC BY-NC-SA 4.0 and new project-owned [code](../LICENSE-CODE.md) uses PolyForm Noncommercial 1.0.0. These are noncommercial, not OSI open source. Check code provenance before importing from other repositories.

**If only one document gets read:** Start with Nat-style v0.5 for the question, then the factual build handoff for the evidence. Don't confuse either with a completed study.
