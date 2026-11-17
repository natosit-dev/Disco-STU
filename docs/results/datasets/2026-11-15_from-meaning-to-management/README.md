# DiScO STU — Experiment 01–02 unredacted evidence release

This folder contains the **unmodified full evidence exports** and corresponding privacy-safe summary exports for two real 15 November 2026 live inference studies of one source (Experiment 01, *From Meaning to Management*).

The author elected to publish all exports without redactions, including the retrospective SERA authorial Oracle, exact review journals, hosted model response identifiers, timestamps, and raw DeepSeek reasoning responses. This README does not assert scientific correctness of the outputs or independent validation of the human interpretation.

## Contents

| Study | Hosted model | Raw full export | Privacy-safe export |
|---|---|---|---|
| 01 | gemma-4-31b-it | `01-gemma/9267fc4d-4273-4e66-8b24-6d6dde6b8e38-full.zip` | `01-gemma/9267fc4d-4273-4e66-8b24-6d6dde6b8e38-safe.json` |
| 02 | deepseek-v4-flash | `02-deepseek/a5cac708-c971-4d5b-9317-61e1b387f228-full.zip` | `02-deepseek/a5cac708-c971-4d5b-9317-61e1b387f228-safe.json` |

Both original full ZIPs include their own file manifests, saved model requests and responses, source-only packet, frozen authorial record, prompts, reconstructed outputs, and human-review events. The same frozen SERA Oracle occurs in both archives. Archive-internal paths containing `private` reflect the original local storage layout and are **public upon publication**.

**Later authorial clarification (17 November 2026):** [The Human Oracle Forgot the INSERT Statement](../../../field-notes/2026-11-17_SERA_POST_FREEZE_CLARIFICATION_FINGER_IMPRINT_UIDS.md) documents a finger-imprint UID mechanism omitted from the original SERA prose. This is post-freeze commentary, not an amendment to the two original evidence ZIPs or a new experimental finding.

## Provenance and verification

Files were copied byte-for-byte from original export artifacts. `RELEASE_MANIFEST.json` records SHA-256 and byte length for each copied file. `SHA256SUMS` provides command-line verification. The original archive contents were audited separately for credential and personal-data exposure before an affirmative unredacted-release decision.

Original archive SHA-256:

- Gemma full ZIP: `9e6316f7378c97bd00953790a7db09f4743e19dbd16f8b6c4df7eca9c7e8ccff`
- DeepSeek full ZIP: `fadc3b06d8965e32f03fe503d1a8ad3a3ff5e2294d12d7299449a7fd0570bd0a`

The structured intermediate includes model-generated content, and human-written reviews are interpretive annotations. Structural validity and matching file hashes are **not** proof of semantic preservation or model accuracy. The first Gemma commercial-review timing has an unmeasured interval; preserved event logs are not edited to hide that limitation.

## Scope

The deterministic fixture bundle and earlier incomplete snapshots are **not included** in this two-study empirical dataset; those are separate implementation/testing artifacts and should be labeled as such if published. No model re-execution is implied by publishing these exports.

## License

Consult the parent repository license files for author-owned text and code. Publication of model/provider-origin response data does not itself assert exclusive authorship or override applicable API/provider terms.

