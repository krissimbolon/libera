# LIBERA

**LIBERA is an offline-first digital-forensics research workbench for controlled conversational evidence.**

The project follows a forensic-first workflow:

**controlled Android evidence carrier → logical acquisition → SHA-256 preservation → read-only artifact examination → traditional examiner baseline → optional local AI assistance → evidence validation → report**

The AI component is intentionally downstream. It does not create the evidence source, replace acquisition, or replace examiner judgment.

## Current presentation build

The presentation scenario uses **LIBERA ChatSim** on an Android emulator as a researcher-controlled evidence carrier (`DEV-SIM-001`). ChatSim is **not WhatsApp** and the experiment is **not a physical-device or real seized-device acquisition**.

Actual local run documented on 25 September 2026:

- Acquired evidence: **9,997 message artifacts across 25 chats**.
- P5 examiner QC: **12 candidate artifacts** — 6 `SUPPORTED`, 4 `NOT_SUPPORTED`, 2 `UNCERTAIN`.
- P6 local retrieval: **645 BGE-M3 index entries**, 1,024-dimensional embeddings, leakage check PASS.
- P8: **30/30 real A/B/C responses**, no transport error, 10/10 structured C outputs passed schema validation.
- P8 lock: **14/14 hashes verified**.
- P9 citation validation: condition B produced no invalid citation references; condition C produced **12 invalid references out of 24 submitted references**. These are quarantined and remain visible as model errors.
- Independent human semantic ground truth is **not available**. Provenance-proxy results are reported separately and are not presented as semantic accuracy.

## Run the local forensic workbench

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_workbench.ps1
```

Then open the local Streamlit address, usually `http://127.0.0.1:8501`.

The workbench is organised around the examiner workflow:

1. **Kasus & Integritas** — acquisition identity, source, SHA-256, master/working verification.
2. **Percakapan** — chronological examination of acquired messages.
3. **Pencarian** — deterministic literal search and sender filtering.
4. **Timeline** — date-scoped artifact review.
5. **Jejak Bukti** — trace an `ART-*` identifier back to the acquired SQLite snapshot.
6. **Pemeriksaan Tradisional** — actor/pair activity and P5 human examiner QC before AI.
7. **Asisten AI** — view the locked A/B/C experiment as an optional analytical copilot.
8. **Validasi & Laporan** — citation integrity, quarantined references, limitations, and P10 report.

The dashboard itself does not call a cloud LLM. Case messages are read from the local ChatSim SQLite acquisition. Historical P8 results were produced locally using Ollama.

## A/B/C experiment

A/B/C is an **experiment inside the forensic workflow**, not the workflow itself.

- **A — AI without case evidence**: negative-control condition. The model receives the investigation question but no case artifacts.
- **B — AI + retrieved evidence**: BGE-M3 retrieves local evidence and Qwen receives the retrieved artifact context.
- **C — AI + the same retrieved evidence + structured output**: same retrieval as B, but the answer is constrained to a structured forensic-oriented schema.

The important measured result is that **structured format did not guarantee valid evidence references**. In the final locked run, all 10 C outputs satisfied the JSON schema, but only 12 of 24 submitted C evidence references were valid.

## Actual local AI configuration

- LLM: `qwen2.5:1.5b` through local Ollama.
- Embedding: `bge-m3` through local Ollama.
- Temperature: `0.1`.
- Seed: `42`.
- Context: `8192`.
- Retrieval top-k: `8`.
- Output budget: `2048`.
- Repeat penalty: `1.2`.
- Repeat window: `256`.
- Final prompt version: `v6-forensic-grounded-repeat-control`.

## Evidence separation

1. The frozen P2 corpus is never edited downstream.
2. Case-design/source reconstruction is not examiner evidence.
3. P4 acquired artifacts are the evidence input used downstream.
4. P5 is performed and locked before AI-assisted analysis.
5. P8 output is locked before post-run validation.
6. Invalid model citations are recorded and quarantined, not silently corrected.
7. Human semantic ground truth was planned but not completed; no final semantic precision/recall/F1 claim is made.
8. Raw acquisition masters, machine-specific runtime outputs, credentials, and private annotations stay outside the public repository.

## Corpus

- Canonical synthetic corpus: `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`.
- Status: **FROZEN_FOR_FORENSIC_SIMULATION**.
- SHA-256: `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`.
- ChatSim device seed contains 9,997 messages; three source anomalies are deliberately excluded from the simulated Raka device.

## Research positioning

LIBERA should be interpreted as a **controlled forensic simulation and research workbench**, not a validated commercial forensic suite and not evidence of legal admissibility.

Its main research question is practical: **can local AI assistance be inserted after acquisition and traditional examination while keeping every analytical claim traceable back to acquired evidence?**

The final run demonstrates both the opportunity and the limitation: local retrieval can support evidence-grounded analysis, but structured LLM output still requires independent citation validation and human oversight.

## Key documentation

- `docs/01_research_design/research_design.md`
- `docs/01_research_design/methodology_references.md`
- `docs/04_ai_methodology/P8_REAL_RUN_20260925.md`
- `docs/05_validasi/P9_CITATION_POLICY_20260925.md`
- `docs/06_report/RESULTS_LOCAL_20260925.md`
- `docs/06_report/STREAMLIT_CHATSIM.md`
- `docs/07_demo/PRESENTATION_FLOW_10MIN.md`

## Important disclosure

The research case is a synthetic WhatsApp-style conversation corpus. **ChatSim is a researcher-controlled Android evidence carrier used to demonstrate reproducible logical acquisition.** The project does not claim real WhatsApp acquisition, physical imaging, or court-ready forensic validation.
