# LIBERA — UAS Digital Forensics Research v2

End-to-end, reproducible digital-forensics research project using a frozen synthetic WhatsApp case, traditional forensic baseline, local Ollama LLM, retrieval-augmented generation (RAG), structured forensic output, and blinded evaluation.

## Canonical state

- P1: complete.
- P2: **complete and frozen** at commit `07a33cc4c2a1fceecabe09f4bfcc01331796b46b`.
- Canonical corpus: `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`.
- Corpus SHA-256: `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`.
- Canonical release branch: `main`.

## Non-negotiable evidence separation

1. Frozen P2 is never edited downstream.
2. Case-design/source reconstruction is not examiner evidence.
3. P6/P7 ingest P4 ART evidence only.
4. Private ground truth is not exposed to P5/P6/P7/P8.
5. P8 outputs are locked before P9 opens private ground truth.
6. Raw acquisition masters, credentials, phone identifiers, and private ground truth stay outside the public repository.

## Recommended controlled Android demo

The presentation-ready acquisition carrier is **LIBERA ChatSim** on an Android emulator. It is not WhatsApp and is explicitly separated as `DEV-SIM-001 / ACQ-SIM-001`.

Install the CI-built APK:

    powershell -ExecutionPolicy Bypass -File scripts\install_chatsim.ps1 -ApkPath .\LIBERA-ChatSim-final-debug.apk

Then run acquisition -> extraction -> P5–P10:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -DryRun

Remove `-DryRun` for the real local BGE-M3 + Qwen2.5-7B run.

## Local software-only fallback

Windows PowerShell dry-run:

    powershell -ExecutionPolicy Bypass -File scripts/run_libera_local.ps1 -DryRun

Local Ollama run:

    powershell -ExecutionPolicy Bypass -File scripts/run_libera_local.ps1

Final blind evaluation after output lock:

    powershell -ExecutionPolicy Bypass -File scripts/run_p9_final.ps1 -GroundTruthPath D:\PRIVATE\ground_truth_final.csv

## Locked AI configuration

- Embedding: `bge-m3` via Ollama.
- LLM: `qwen2.5:7b`.
- Temperature: 0.1.
- Seed: 42.
- Context setting: 8192.
- Retrieval top-k: 8.
- Prompt: `v2-forensic-grounded`.

## Key docs

- `docs/00_project_management/progress_tracker_post_p2.md`
- `docs/01_research_design/methodology_references.md`
- `docs/03_forensik_persiapan/FINAL_ACQUISITION_CHECKLIST.md`
- `docs/06_report/final_report_draft.md`
- `docs/07_demo/PRESENTATION_RUNBOOK.md`
- `docs/07_demo/PRESENTATION_OUTLINE.md`

## Blind-evaluation lock

Final P9 never reruns P8 after the evaluator ground truth is opened. `tools/lock_p8_outputs.py` hashes P4/P5/config/tasks/P8 outputs, and `scripts/run_p9_final.ps1` verifies that lock before scoring.

## Important disclosure

`ACQ-DRY-001` is a controlled software pipeline dry-run. It is intentionally labeled differently from the real mobile acquisition `ACQ-001` and must not be presented as physical-device evidence.
