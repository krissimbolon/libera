# LIBERA ChatSim — controlled Android evidence carrier

LIBERA ChatSim is a researcher-controlled Android messaging simulator for the LIBERA forensic demonstration. **It is not WhatsApp and must never be presented as a WhatsApp acquisition tool.** It exists so the team can demonstrate actual Android app-private logical acquisition, hashing, working-copy examination, extraction, provenance, and downstream P5–P10 analysis without touching personal WhatsApp accounts or mass-sending 10,000 messages.

## Evidence identity

- Simulation device: `DEV-SIM-001`.
- Simulation acquisition: `ACQ-SIM-001`.
- App package: `id.libera.chatsim`.
- Private SQLite: `databases/libera_messages.db`.
- Source: immutable frozen P2 corpus SHA-256 `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`.
- Device seed: 9,997 Raka-participating messages.
- Three non-Raka source anomalies remain separately documented and are not silently inserted onto Raka's simulated device.
- Source-construction provenance and evaluator ground truth are excluded from the app database.

## Build seed and APK

From repository root:

    py -3 tools/build_demo_seed.py

The seed builder refuses a corpus whose SHA-256 differs from frozen P2.

Build in Android Studio, or use the GitHub Actions artifact from `Build Final ChatSim`.

## Emulator acquisition

Install the debug APK on an Android emulator, open ChatSim once so the seed is imported, then run:

    powershell -ExecutionPolicy Bypass -File scripts\acquire_chatsim.ps1

The acquisition uses `adb exec-out` + `run-as` against this researcher-controlled debuggable app. It force-stops the app, copies the private SQLite database into a MASTER location, calculates SHA-256, creates a WORKING copy, re-hashes it, and refuses a mismatch.

Acquisition type:

    LOGICAL_APP_PRIVATE_FILE_COPY

This is not a physical/full-filesystem acquisition.

## End-to-end presentation run

For acquisition + extraction + P5–P10 dry-run:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -DryRun

For real local BGE-M3 + LLaMA-3.1-8B:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1

Optional workbench:

    powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -DryRun -LaunchWorkbench

## Presentation disclosure

Describe the original 10,000-message dataset as a **synthetic WhatsApp-style case corpus**. Describe ChatSim as the **controlled Android evidence carrier used for the reproducible forensic demonstration**. Do not say that ChatSim proves extraction behavior of WhatsApp itself.
