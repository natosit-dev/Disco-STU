# Experiment 01 — Gemma 4 31B — First human evaluation

**Date:** 2026-11-15 (America/New_York)
**Mode:** live · Adaption `gemma-4-31b-it`
**Source:** “Velocity is not productivity. / Coherence is not accuracy. / Complexity is not sophistication.”
**Study:** `9267fc4d-4273-4e66-8b24-6d6dde6b8e38`
**Run:** `78e82cc2-ec2b-440e-a36d-72b8963be8a8`
**Research status:** First authorial assessment; **not** an independently established semantic verdict.

## Evidence identity and custody

This document is a **reviewed, intentionally limited research summary**, not the private experiment archive. The author's complete private ZIP and locally created Oracle must remain outside Git.

- Original full private ZIP SHA-256: `9e6316f7378c97bd00953790a7db09f4743e19dbd16f8b6c4df7eca9c7e8ccff`.
- Original safe JSON export SHA-256: `bc10b828a3546e8390ee159bc3f41e3205ec603caada191df9147ef6856ea8c7`.
- Verified 45/45 files in the ZIP evidence manifest by recalculating byte lengths and SHA-256. The ZIP has 46 entries including `BUNDLE_MANIFEST.json`.
- One live model, three `completed` inference stages, ten comparisons, two completed original-to-final human reviews, and passing recorded evidence validation.
- Both review journals' per-event SHA-256 and chain links verify; seven events in each. They are unchanged by this summary.
- Actual provider model: `gemma-4-31b-it`; same saved reconstruction-projection digest provided to both branches: `375f91c788200fad48875a4fa37be6d78c6dc727a1156f367c350e7544a22339`.
- Private Oracle content, complete human explanations, provider requests/responses, authorization credentials, raw review journals, and patient or clinical data are **not included** in this repository record.

## Human observation 1 — Original → Neutral

The neutral reconstruction reproduced all three explicit negations but combined the deliberately separate lines into a single fluent sentence. The author observed (quoted from author-approved review text shared for this work):

> “Only difference is the 3 lines were mashed into 1 sentence.”

The author's explanation identifies **loss of rhetorical separation and the reading work prompted by high semantic compression**, rather than a failure to reproduce the three explicit propositions. This observation is an authorial assessment; it is not an automated accuracy measurement.

## Human observation 2 — Original → Commercial

The commercial reconstruction converted the three negations into conventional sections on performance metrics, quality, product design and limits. The author's reported observation:

> “What was intended as a jarring intervention has become a smoothed corporate memo.”

And:

> “It missed the purpose of the intervention- that management must stop and think hard about what each sentence means, not make a plausible observation.”

The author described loss of the intended challenge to management's assumptions, particularly around human needs, specifications/requirements and definitions. The commercial-response style was partly induced by the experiment's explicit **commercial-management advice** prompt. It is an observed treatment effect, not proof of an unexplained model failure.

**Working research distinction:** preserving explicit propositions is not necessarily preserving *rhetorical function*. One run cannot establish a general tendency across models, prompts, or authors.

## Human time instrument — incomplete/uncertain

| Primary review | Confirmed active intervals | Evidence status |
| --- | ---: | --- |
| Original → Neutral | 171.808 seconds (~2m52s) | Text preserved; completed, amended, completed again; duplicate identical saves |
| Original → Commercial | 51.713 seconds (~52s) | Text preserved; two active intervals; paused during substantial subsequent unmeasured work |
| **Total recorded active** | **223.521 seconds (~3m44s)** | **Not a reliable measure of total human effort** |

Commercial was paused at **15:07:42 EST**; the first substantive saved explanation occurred at **15:14:11 EST**, an approximately **6m29s gap** that cannot be attributed to writing, reading, troubleshooting or absence without additional evidence. Neutral was reopened for amendment after Commercial began, and its saved explanation remained text-identical.

The empty `review_gap_labels` map only means that no *optional typed labels* were selected. Both completed human reviews contain meaningful written explanations with `no_gap=false`. A status report must not represent missing labels as absence of observed differences.

**Data-quality action:** preserve the raw event journals unchanged; mark review-labor measurement incomplete/uncertain. Do not backfill or manufacture duration from wall-clock gaps.

## Instrument correction required before next model

1. Stable selected study/run/comparison and unsaved text across Streamlit reruns.
2. Explicit untimed inspection, then one timed explanation; prevent switching from an active explanation without deliberate pause.
3. Paused work must not silently become unmeasured editing. Re-enable editing by resuming timing, or explicitly document intervals not measured.
4. One primary **Save & Complete** action; optional Save Draft; skip identical redundant saves.
5. Show pending, active, paused, completed and uncertain status beside each comparison.
6. Count confirmed cumulative active duration separately from the >=15-minute labor-budget Boolean and the >15-minute **single-interval** uncertainty flag.
7. Report free-text findings/no-gap status separately from optional labels.
8. Regression test Neutral → Commercial → Amend → Complete, reruns, multi-review overlap and private-archive preservation.

**Historical integrity:** this summary does not modify, overwrite, redact, repair or reissue the original private ZIP, the frozen SERA Oracle, or either review event journal.
