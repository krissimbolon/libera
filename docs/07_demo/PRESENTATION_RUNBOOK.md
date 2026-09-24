# LIBERA Presentation Runbook

## Recommended presentation track: Android ChatSim acquisition

Use this track to demonstrate a real Android logical acquisition without touching personal WhatsApp accounts. ChatSim is a controlled messaging simulator, **not WhatsApp**.

### 1. Preflight

    git switch p3-p10-final-integration
    git pull
    powershell -ExecutionPolicy Bypass -File scripts\preflight_local_windows.ps1

### 2. Install the CI-built ChatSim APK on an Android emulator

Download the `libera-chatsim-final-debug` artifact from the latest successful `Build Final ChatSim` GitHub Actions run, unzip it, then:

    powershell -ExecutionPolicy Bypass -File scripts\install_chatsim.ps1 -ApkPath .\app-debug.apk

This resets the app state, launches ChatSim, and verifies the app-private SQLite database exists.

### 3. Acquire -> extract -> P5–P10

Fast rehearsal without model calls:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -DryRun

Real local RAG + LLM:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1

The demo acquisition uses `DEV-SIM-001` and `ACQ-SIM-001`, preserves a hashed MASTER and verified WORKING copy, then emits normalized message-level `ART-*` evidence for the same P5–P10 pipeline.

## Software-only fallback

If the emulator cannot be prepared, the full software path can still be rehearsed with:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_local.ps1 -DryRun

This produces `ACQ-DRY-001`; explicitly disclose that it is not an Android/WhatsApp acquisition.

## Locked local AI configuration

- embedding: `bge-m3` via local Ollama;
- LLM: `llama3.1:8b`;
- seed: 42;
- temperature: 0.1;
- context: 8192;
- retrieval top-k: 8;
- prompt: `v2-forensic-grounded`.

## Final blind evaluation

Only after the real P8 outputs have been saved/locked:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -GroundTruthPath D:\PRIVATE\ground_truth_final.csv

Ground-truth messages not present on the acquired device are reported as `unacquired` and excluded from the metric denominator rather than silently treated as negatives.

## Files to show

- P3: `demo_evidence\ACQ-SIM-001_*\acquisition_manifest.json` and `sha256_manifest.csv`;
- P4: `demo_evidence\ACQ-SIM-001_*\artifacts\artifact_manifest.json` and `artifacts.csv`;
- P5: `runtime\working\P5\baseline_findings.json`;
- P8: `runtime\working\P8\experiment_output.json`;
- P9: `runtime\working\P9\evaluation.json`;
- P10: `runtime\working\P10\run_report.md`.

## Presentation wording

Say: the research case is a **synthetic WhatsApp-style conversation corpus**, while ChatSim is a **researcher-controlled Android evidence carrier used to demonstrate reproducible logical acquisition**. Do not say ChatSim is WhatsApp or that `run-as` reproduces WhatsApp protected-database acquisition.

Show the trace:

`P2 frozen design -> DEV-SIM-001 -> ACQ-SIM-001 -> ART-* -> CHK-* -> RUN-* -> finding -> P9 validation`.
