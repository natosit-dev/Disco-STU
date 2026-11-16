# DiScO-STU Experiment 01 rig — accepted exploratory baseline

**Acceptance date:** 2026-11-15 (America/New_York)  
**Decision:** User: **“We're done enough—the rig works and produces usable data.”**  
**Scope:** local single-user experimental apparatus; **not** a regulated production system or an independent semantic-validity certification.

## Evidence of working end-to-end capability

1. **Human reference:** SERA records original writing and unrestricted intended meaning, freezes a versioned Oracle and exposes a four-field source-only packet without exposing private intention to the model.
2. **Independent hosted execution:** An Adaption call decomposes the source; two subsequent fresh neutral/commercial requests use the **same frozen model-visible projection bytes** without `source_support`, agents, memory or tools.
3. **Transparent lineage:** study/run/model identifiers; provider requests/responses and failures; exact prompt/schema snapshots; SHA-256 artifacts, append-only human review journals, and reproducible private ZIPs.
4. **Human observation:** The author evaluated both final conditions for **Gemma 4 31B** and **DeepSeek V4 Flash**, with free-text findings preserved independently from optional classification labels. Timing uncertainty from the first run was retained instead of imputed.
5. **Material results:** [Gemma first evaluation](../results/EXPERIMENT_01_GEMMA_FIRST_HUMAN_REVIEW_2026-11-15.md) and [DeepSeek second evaluation](../results/EXPERIMENT_02_DEEPSEEK_FIRST_HUMAN_REVIEW_2026-11-15.md), each backed by separately retained complete private archives. DeepSeek: 45/45 verified manifest entries, three completed model stages, two human reviews, ten comparisons, validated journal chains.
6. **Regression evidence:** Prior engineering checkpoint `e65a1ca81f0d401d5298290491ebf2b55227213d` passed **86 automated tests** and synthetic CLI acceptance. Current closure changes **documentation only**.

## First research finding

Both models preserved the three explicit negations. Both transformed the author's deliberately separate, compressed statements into a different reading experience, particularly under the commercial-management treatment. Gemma compressed Neutral to a single sentence; DeepSeek explained the rhetorical form instead of reproducing it.

The human observed that **preservation of propositional content did not guarantee preservation of rhetorical function**. This is an observation about two model runs on one source, not a universal conclusion or attribution solely to model architecture. Prompt, representation, and treatment also contribute.

The reviews additionally make human evaluation labor observable. Gemma's commercial timing was incomplete; DeepSeek's completed reviews passed the instrument's reported timing checks, while untimed inspection remains outside confirmed active duration.

## Boundary of the accepted milestone

- **Accepted:** usability sufficient for repeatable local experiments, observable inference and failures, independently inspectable lineage, explicit human review, deterministic regression tests and defensible evidence exports.
- **Not claimed:** model truth, semantic scoring, generalizable causal conclusions, complete capture of human cognitive labor, provider data-retention guarantees, production readiness, or PHI/security certification.
- **Deferred rather than blocking:** optional more models, streaming/timeouts for slow providers, richer rhetorical representation, formal study design and additional UI polish. Do not expand scope automatically.
- **Privacy:** full ZIPs, frozen Oracle text, complete human explanations and raw provider payloads remain only in private study storage or the user's separately held archives; Git records derived summaries, IDs and verification digests.
- **Repository:** keep the current feature branch and draft PR #1 as-is; this acceptance is not an instruction to merge, deploy or publish private materials.

**Milestone disposition:** **closed — usable exploratory research rig demonstrated.**
