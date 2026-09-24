# LIBERA Presentation Runbook

## Recommended presentation track: Android ChatSim acquisition

Use this track to demonstrate a real Android logical acquisition without touching personal WhatsApp accounts. ChatSim is a controlled messaging simulator, **not WhatsApp**.

### 1. Preflight

    git switch main
    git pull
    powershell -ExecutionPolicy Bypass -File scripts\preflight_local_windows.ps1

### 2. Install the CI-built ChatSim APK on an Android emulator

Download the `libera-chatsim-final-debug` artifact from the latest successful `Build Final ChatSim` GitHub Actions run, unzip it, then:

    powershell -ExecutionPolicy Bypass -File scripts\install_chatsim.ps1 -ApkPath .\app-debug.apk

This resets the app state, launches ChatSim, and verifies the app-private SQLite database exists.

### 3. Acquire -> extract -> examiner-reviewed P5 -> P6–P10

For the presentation-grade forensic path, stop after P4 first:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -StopAfterP4

Then run the deterministic P5 baseline plus time-boxed human QC:

    powershell -ExecutionPolicy Bypass -File scripts\run_p5_examiner_review.ps1 -ArtifactsPath "<ACQ-SIM folder>\artifacts\artifacts.csv"

The examiner packet contains at most 12 unique evidence items, covers T01–T10 where candidates exist, records SUPPORTED / NOT_SUPPORTED / UNCERTAIN decisions, measures actual review time, and cryptographically locks P5 before AI.

Continue from the reviewed/locked P5 without rerunning it:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_local.ps1 -ArtifactsPath "<ACQ-SIM folder>\artifacts\artifacts.csv" -UseLockedP5 -DryRun

Remove `-DryRun` for the real local embedding/LLM experiment.

For a fast rehearsal that skips the human P5 gate, the original one-command path remains:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -DryRun

The demo acquisition uses `DEV-SIM-001` and `ACQ-SIM-001`, preserves a hashed MASTER and verified WORKING copy, then emits normalized message-level `ART-*` evidence for the same downstream pipeline.

## Software-only fallback

If the emulator cannot be prepared, the full software path can still be rehearsed with:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_local.ps1 -DryRun

This produces `ACQ-DRY-001`; explicitly disclose that it is not an Android/WhatsApp acquisition.

## Locked local AI configuration

- embedding: `bge-m3` via local Ollama;
- LLM: `qwen2.5:1.5b`;
- seed: 42;
- temperature: 0.1;
- context: 8192;
- retrieval top-k: 8;
- prompt: `v2-forensic-grounded`.

## Final blind evaluation

Only after the real P8 outputs have been saved and cryptographically locked. **Do not rerun P8 after opening ground truth:**

    powershell -ExecutionPolicy Bypass -File scripts\run_p9_final.ps1 -GroundTruthPath D:\PRIVATE\ground_truth_final.csv

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

## Private ground-truth completion workflow

The final key-evidence labels are **not** stored in the public repo. After the ChatSim P4 acquisition/extraction and after P8 output is produced:

    py -3 tools\build_private_gt_annotation_packet.py --artifacts "<ACQ-SIM folder>\artifacts\artifacts.csv"

This creates a private annotation packet with blank evaluator labels and reviewer hints. It does **not** auto-label evidence.

Bela/evaluator then completes at least:
- `is_key_evidence` explicitly as positive/negative for the chosen evaluation set;
- `event_id`;
- expected entities/relations where established;
- annotation/review status.

Lock the private GT:

    py -3 tools\lock_private_ground_truth.py runtime\private\P9\ground_truth_annotation_packet.csv

P8 is independently hash-locked by `tools/lock_p8_outputs.py`. Final evaluation uses `scripts/run_p9_final.ps1`, which does not rerun retrieval/model inference. P9 refuses to run if the current P4/P5/P8 files no longer match that lock.

Partial annotation is permitted for an explicitly declared evaluation subset: unlabeled and unacquired messages are reported separately and excluded from the confusion-matrix denominator. Do not describe a partial labeled subset as full-corpus evaluation.
