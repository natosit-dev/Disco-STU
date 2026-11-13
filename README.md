# Disco-STU

If these trends continue... EHHHH

...your fish is dead

## What this is

**DiScO STU** (Semantic Transformation Utility) is a proposed semantic-transformation research instrument within the broader DiScO work. Experiment 01, **From Meaning to Management**, examines whether intended meaning survives structured decomposition and reconstruction, including reconstruction as commercial-management advice.

**SERA** (Semantic Explication Recorded Analytics) is the proposed human explication/warmup interface: source paragraphs and the author's independently frozen intended-meaning references are produced before model testing.

**Current state:** Documentation only. No executable STU or SERA implementation is claimed in this repository yet.

## Research documentation

- [v0.3 — pre-sprint baseline](docs/stu/DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12_BASELINE.md) — archival text extraction from the November 12, 2026 Word plan; identifies work existing before the Apart AI × Epistemics sprint.
- [v0.4 — in-sprint working draft with SERA addendum](docs/stu/DiScO_STU_From_Meaning_to_Management_v0.4_REVIEW_SERA_ADDENDUM_2026-11-13.md) — research plan under review, including a proposed 200-word maximum source paragraph and SERA as the preparation stage.

These Markdown files are copied without alteration from the `feature/disco-stu-20261113` branch of the original DiScO repository. Their original DOCX filenames and SHA-256 checksums are preserved in the archived files. The documents are text extractions, not binary DOCX replicas.

**Nat Notes**
I'm building something that takes text I've written, a few paragraphs from the last 20 years (I write a lot😅), breaking down what I was trying to represent semantically by explaining the actors, relationships, assertions, etc manually and turning that explication into structured data. Then run the same text through different LLM models, have it do the same deconstruction. Wipe the LLM context, have it reconstruct the output from the structured data- one as neutral prose, one as advice to a competitive business that sells products. Then compare the outputs with my original explication. Final output is my assessment of what was lost in the process, and potentially what I failed to convey in the original translation from thought to written words. Human in the loop semantic deconstruction, transformation, and reconstruction. 

## License

Two licenses apply to original material that we have the rights to distribute:

- **Documentation** (`docs/`): [CC BY-NC-SA 4.0 International](LICENSE-DOCS.md). Noncommercial reuse and adaptations permitted with attribution and ShareAlike.
- **Software code** (when added): [PolyForm Noncommercial 1.0.0](LICENSE-CODE.md). The repository does not yet contain STU/SERA software.

These **are not OSI-approved open-source licenses**, because they restrict commercial purposes. Public availability does not give others permission to resell the work.

When existing code is imported, its authorship, copyright, provenance, and license compatibility must be checked before applying the project license. Material owned by third parties is not automatically relicensed by this repository.

Copyright © 2026 Nat Osit for original contributions unless otherwise specified.
