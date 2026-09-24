# LIBERA Presentation Runbook

## Fastest rehearsal (no Ollama needed)

PowerShell from repository root:

    git switch p3-p10-final-integration
    py -3 -m pytest tests/test_p6_p7_pipeline.py -v
    powershell -ExecutionPolicy Bypass -File scripts/run_libera_local.ps1 -DryRun

Expected final files:
- `runtime/working/P4/artifacts.csv`
- `runtime/working/P5/baseline_findings.json`
- `runtime/working/P6/chunks.jsonl`
- `runtime/working/P8/experiment_output.json`
- `runtime/working/P9/evaluation.json`
- `runtime/working/P10/run_report.md`

## Real local LLM demo

Start Ollama first, then:

    powershell -ExecutionPolicy Bypass -File scripts/run_libera_local.ps1

The script pulls/uses:
- embedding: `bge-m3`
- LLM: `llama3.1:8b`

## Final blind evaluation

Only after P8 output is frozen:

    powershell -ExecutionPolicy Bypass -File scripts/run_libera_local.ps1 -ArtifactsPath runtime/working/P4/artifacts.csv -GroundTruthPath D:\PRIVATE\ground_truth_final.csv

Do not commit the private ground-truth path/file or runtime outputs.

## What to say in the presentation

1. P2 is a frozen 10,000-message synthetic case corpus with a pinned SHA-256 and final QA.
2. The software pipeline enforces DEV -> ACQ -> ART -> CHK -> RUN -> FND traceability.
3. Traditional P5 baseline is deterministic and locked before AI evaluation.
4. P6/P7 run locally: BGE-M3 retrieval + LLaMA-3.1-8B.
5. Conditions A/B/C are run on the same T01–T10 questions; B/C share identical retrieval.
6. P9 opens private ground truth only after P8 is locked.
7. If showing ACQ-DRY-001, explicitly call it a controlled dry-run, not a physical-device acquisition.
