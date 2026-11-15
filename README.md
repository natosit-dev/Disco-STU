# Disco-STU

If these trends continue... EHHHH

...your fish is dead

**[Documentation index](docs/INDEX.md)** — current research plan, factual build record, implementation contracts, and historical archive.

## What this is

**DiScO** = **Deterministic Inspection of Semantic Coupling in Outputs**.

**DiScO STU** (Semantic Transformation Utility) is a proposed semantic-transformation research instrument within the broader DiScO work. Experiment 01, **From Meaning to Management**, examines whether intended meaning survives structured decomposition and reconstruction, including reconstruction as commercial-management advice.

**SERA** (Semantic Explication Recorded Analytics) is the proposed human explication/warmup interface: source paragraphs and the author's independently frozen intended-meaning references are produced before model testing.

**Current state:** SERA v0.1 local capture/freeze/export application implemented, with automated domain tests. STU model execution and timed human gap review are not implemented yet.

## Run SERA locally

SERA uses **progressive explication**: source paragraph → unrestricted human intention → category-level prose → semantic units/relations → immutable frozen Oracle and source-only STU export.

```bash
git clone https://github.com/natosit-dev/Disco-STU.git
cd Disco-STU
python -m venv .venv
source .venv/bin/activate     # Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Use the **SERA** page in the sidebar. Records live in `./data/` (gitignored). To use another directory, set `SERA_DATA_DIR`. The app is **local and single-user**; it does not encrypt data at rest. The model-visible export contains only the original paragraph, its hash and a sample ID—not the Oracle reference.

Run backend tests with `python -m pip install -r requirements-dev.txt && pytest -q`. The first UI walkthrough should be performed locally with Streamlit installed.

[Implementation plan](docs/sera/BUILD_PLAN_v0.1.md) · [Data contract](docs/sera/DATA_CONTRACT.md) · [Shared semantic schema](schemas/semantic_v0.1.json)

## The Nerd implementation handoff

[Complete STU pipeline handoff v0.1](docs/handoff/NERD_HANDOFF_STU_COMPLETE_PIPELINE_v0.1_2026-11-14.md) — build the remaining model runner, paired reconstructions, Review and timing, analysis and tests as one coherent system. Includes a five-step user walkthrough for later acceptance testing.

## Research documentation

- [v0.3 — pre-sprint baseline](docs/stu/DiScO_STU_From_Meaning_to_Management_Nat_Style_v0.3_2026-11-12_BASELINE.md) — archival text extraction from the November 12, 2026 Word plan; identifies work existing before the Apart AI × Epistemics sprint.
- [v0.4 — in-sprint working draft with SERA addendum](docs/stu/DiScO_STU_From_Meaning_to_Management_v0.4_REVIEW_SERA_ADDENDUM_2026-11-13.md) — research plan under review, including a proposed 200-word maximum source paragraph and SERA as the preparation stage.

These Markdown files are copied without alteration from the `feature/disco-stu-20261113` branch of the original DiScO repository. Their original DOCX filenames and SHA-256 checksums are preserved in the archived files. The documents are text extractions, not binary DOCX replicas.

**Nat Notes**
I'm building something that takes text I've written, a few paragraphs from the last 20 years (I write a lot😅), breaking down what I was trying to represent semantically by explaining the actors, relationships, assertions, etc manually and turning that explication into structured data. Then run the same text through different LLM models, have it do the same deconstruction. Wipe the LLM context, have it reconstruct the output from the structured data- one as neutral prose, one as advice to a competitive business that sells products. Then compare the outputs with my original explication. Final output is my assessment of what was lost in the process, and potentially what I failed to convey in the original translation from thought to written words. Human in the loop semantic deconstruction, transformation, and reconstruction. 

**Nat Notes, Vol II**

I'm turning prompts into source data going through transformations, then measuring the labor time required to reconstruct the meaning from LLM outputs. Goal is to see where semantic labor is displaced during generative inference.

An LLM can make a coherent inference from a prompt, I'm trying to drag it back down to reality and see how much labor is required to fill in meaning that was lost in the transformation. 
The trends look good, but the fish is dead

## License

Two licenses apply to original material that we have the rights to distribute:

- **Documentation** (`docs/`): [CC BY-NC-SA 4.0 International](LICENSE-DOCS.md). Noncommercial reuse and adaptations permitted with attribution and ShareAlike.
- **Software code:** [PolyForm Noncommercial 1.0.0](LICENSE-CODE.md) for new project-owned SERA software. STU execution and Review are future work.

These **are not OSI-approved open-source licenses**, because they restrict commercial purposes. Public availability does not give others permission to resell the work.

When existing code is imported, its authorship, copyright, provenance, and license compatibility must be checked before applying the project license. Material owned by third parties is not automatically relicensed by this repository.

Copyright © 2026 Nat Osit for original contributions unless otherwise specified.
