# LIBERA — UAS Digital Forensics Research v2

End-to-end, reproducible digital-forensics research project using a frozen synthetic WhatsApp case, traditional forensic baseline, local Ollama LLM, retrieval-augmented generation (RAG), structured forensic output, and blinded evaluation.

## Canonical state

- P1: complete.
- P2: **complete and frozen** on `p2-10k-work@07a33cc4c2a1fceecabe09f4bfcc01331796b46b`.
- Canonical corpus: `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`.
- Corpus SHA-256: `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`.
- P3–P10 integration branch: `p3-p10-final-integration`.

## Non-negotiable evidence separation

1. Frozen P2 is never edited downstream.
2. Case-design/source reconstruction is not examiner evidence.
3. P6/P7 ingest P4 ART evidence only.
4. Private ground truth is not exposed to P5/P6/P7/P8.
5. P8 outputs are locked before P9 opens private ground truth.
6. Raw acquisition masters, credentials, phone identifiers, and private ground truth stay outside the public repository.

## Local run

Windows PowerShell dry-run:

    powershell -ExecutionPolicy Bypass -File scripts/run_libera_local.ps1 -DryRun

Local Ollama run:

    powershell -ExecutionPolicy Bypass -File scripts/run_libera_local.ps1

Final blind evaluation after output lock:

    powershell -ExecutionPolicy Bypass -File scripts/run_libera_local.ps1 -ArtifactsPath runtime/working/P4/artifacts.csv -GroundTruthPath D:\PRIVATE\ground_truth_final.csv

## Locked AI configuration

- Embedding: `bge-m3` via Ollama.
- LLM: `llama3.1:8b`.
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

## Important disclosure

`ACQ-DRY-001` is a controlled software pipeline dry-run. It is intentionally labeled differently from the real mobile acquisition `ACQ-001` and must not be presented as physical-device evidence.
