# Experiment 02 — DeepSeek V4 Flash — First human evaluation

**Date:** 2026-11-15 (America/New_York)  
**Mode:** live, direct Adaption hosted model `deepseek-v4-flash`  
**Source:** “Velocity is not productivity. / Coherence is not accuracy. / Complexity is not sophistication.”  
**Study:** `a5cac708-c971-4d5b-9317-61e1b387f228`  
**Run:** `18f7c5c0-45e3-40e1-983b-d32880d7dbf6`  
**Interpretation status:** Two completed *authorial* assessments, not independently established model correctness.

## Evidence custody and verification

This is a **derived, intentionally limited research summary**. Keep the complete private ZIP, original Oracle, full review explanations, requests/responses and event journals out of Git.

- Full private ZIP SHA-256: `fadc3b06d8965e32f03fe503d1a8ad3a3ff5e2294d12d7299449a7fd0570bd0a`.
- Safe JSON export SHA-256: `7f13d057a6c12635872b8b9f4c17ad1583148e5f690d771a1bcc18db511a3295`.
- ZIP evidence manifest: **45/45** files passed actual byte-length and SHA-256 verification; 46 ZIP entries including `BUNDLE_MANIFEST.json`.
- Both primary Review event journals passed complete sequence, hash and previous-hash chain verification (**7** Neutral events, **3** Commercial events).
- **Three/three** model stages completed; **ten** comparison records; **two/two** primary human reviews completed; recorded study validation `valid=true`; `synthetic=false`.
- Frozen Oracle artifact hash: `83ce07444d88c3553a1a65b0f8f3a62e7b791bf74378bdd516a0c717e707af09`. Source-only SHA-256: `117282db49c12ce45ba36c57c5b7ba9f4d65e152cb48664ab538163aed059228`.
- Saved reconstruction projection SHA-256: `09c4d0976bcb9509c3a4958b5c12cf58d9d28f528d177ffb60c7d98c935feac2`. I compared the actual archived provider requests: both reconstruction inputs **exactly equal the saved projection bytes**, which omit `source_support`; no original source packet or private human Oracle was sent to reconstruction.
- Direct hosted requests use `store=false`, `agentic_memory=false`, `tools=[]`; no inference stack was substituted. These request flags do not independently prove the provider's internal retention policy.

## Transformation record

**Neutral**: DeepSeek retained the three explicit non-equivalences but expanded them into explanatory paragraphs. It described their ambiguity and rhetorical form as “corrective aphoristic distinctions”. The author recorded that this introduced terminology requiring a lookup; the finished assessment called the result **“sterile but mostly accurate.”** The model characterized the source's rhetorical operation while failing to reproduce its intentionally separate, compressed presentation.

**Commercial**: DeepSeek produced an extensive management analysis that began by calling the assertions “negative definitions”, claimed they cannot support a positive management program, attached business metrics to the distinctions and heavily qualified their possible implications. The author's assessment distinguished **negations from definitions**, argued the statements can act as a critical method inviting reflection, and identified lost emphasis on the larger reality-feedback loop, recursive testing, and task-specific requirements/constraints. The author also judged the coherence/accuracy treatment relatively useful and found merit in the conclusion about definitions, evidence and strategy.

The commercial style was partly **induced by the frozen commercial-management prompt**. These observations do not establish a general model failure or a model-independent causal attribution. The authoritative human findings remain the exact private review journals.

**Representation-level observation:** The decomposition had three units, all `kind=negation` and `polarity=affirmed`, with zero relation edges. This is permitted by the current semantic schema; schema validity does not establish a normalized equivalence across models. Gemma's archived decomposition used different field encodings for comparable source negations.

## Recorded work and cost

| Stage | Provider elapsed | Provider tokens (input/output/total) |
| --- | ---: | ---: |
| Decomposition | 29.03 s | 563 / 2,783 / 3,346 |
| Neutral | 6.26 s | 494 / 481 / 975 |
| Commercial | 12.18 s | 520 / 1,145 / 1,665 |
| **All stages** | **47.49 s overall** | **1,577 / 4,409 / 5,986** |

Provider reported total cost as `0.00065788976` in unlabelled cost units; no currency is asserted.

| Human review | Confirmed active time | Quality |
| --- | ---: | --- |
| Original → Neutral | 144.961703 s (~2m25s) | Completed, amended with changed text, completed again; no timing-quality flag |
| Original → Commercial | 866.747966 s (~14m27s) | Completed; no timing-quality flag |
| **Combined confirmed active** | **1,011.709669 s (~16m52s)** | Neither review independently reached 900s; not a measure of all untimed inspection/lookup work |

`free_text_findings_count=2`, `explicit_no_gap_reviews=0`, `review_gap_labels={}`. The empty optional-label map **does not mean no differences were reported**.

## Comparison with the first Gemma run

The earlier [Gemma evaluation](EXPERIMENT_01_GEMMA_FIRST_HUMAN_REVIEW_2026-11-15.md) used the same original writing and frozen human baseline, as verified in the preceding cross-model inspection. Both models retained the explicit non-equivalences yet transformed the intended rhetorical intervention in different ways:

- Gemma's neutral output compressed three declarations into a single fluent sentence; DeepSeek's expanded them into commentary about the declarations.
- Both commercial outputs made a jarring, reflective intervention into accessible business guidance, a transformation partly requested by the commercial treatment prompt.
- DeepSeek spent substantially more provider tokens and time; this is **not** evidence of greater rhetorical preservation.
- The author's second evaluation was richer and more qualified; differences in judgment may also reflect review experience and the changed Review interface, not solely model behavior.

**Working observation, not generalization:** preservation of explicit propositions is not equivalent to preservation of rhetorical purpose, intended cognitive work, or the work transferred back to the human reader. The comparison has one authored source, two completed models, and one accepted run per model; model-generated decompositions are not held constant between runs.

## Closure

The user has explicitly accepted the current rig as **working and producing usable exploratory research evidence**. The instrument supports source/intention freezing, live model inference, exact projection lineage, human review, immutable audit records, and validated private exports. No further development or model runs are required for this phase. Refer to the [accepted rig checkpoint](../checkpoints/DISCO_STU_RIG_ACCEPTED_2026-11-15.md).

**Do not** commit or modify the original ZIP, full human explanations, frozen Oracle, or provider responses. This summary is a deliberately reduced derivative of that evidence.
