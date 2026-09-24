# LIBERA ChatSim — DEV-001

LIBERA ChatSim is a researcher-controlled Android messaging simulator for the LIBERA digital-forensics demonstration.

It is not WhatsApp and is not presented as a WhatsApp forensic acquisition tool. It simulates the messaging evidence environment so the team can demonstrate preservation, logical acquisition, extraction, analysis, and evidence attribution without touching personal WhatsApp data.

## Evidence model

- Host: Android Emulator.
- Simulated device ID: DEV-001.
- Simulated owner: Raka Pradana.
- App package: id.libera.chatsim.
- Local evidence store: databases/libera_messages.db.
- One chat_id per Raka-counterparty pair.
- Existing corpus conversation_id is retained as segment_id.
- Evaluator-only provenance and ground-truth fields are excluded from the device.

Three non-Raka anchor rows currently present in the master reconstruction are not silently inserted as direct messages on Raka's device. The seed builder writes them to source_anomalies.jsonl pending provenance resolution.

## Build the seed

From repository root:

    python tools/build_demo_seed.py

This creates:

    apps/libera-chatsim/app/src/main/assets/messages_seed.jsonl
    apps/libera-chatsim/app/src/main/assets/source_anomalies.jsonl
    apps/libera-chatsim/app/src/main/assets/seed_manifest.json

After P2 final QA, regenerate the seed from corpus_whatsapp_10000.csv and record the final seed hash.

## Build and install

Open apps/libera-chatsim in Android Studio and use an Android Virtual Device. API 35 is the current project target.

Run the debug build. Debug is intentional because the research demo uses Android run-as for a controlled logical acquisition of the app-private SQLite database.

Launch LIBERA ChatSim once. First launch imports the seed into SQLite.

## Live acquisition on Windows

With the emulator running:

    powershell -ExecutionPolicy Bypass -File scripts/acquire_chatsim.ps1

The script:

1. records emulator/device metadata;
2. force-stops ChatSim;
3. copies libera_messages.db using adb exec-out + run-as;
4. stores a MASTER copy;
5. creates a WORKING copy;
6. SHA-256 hashes both;
7. verifies master == working;
8. writes acquisition_manifest.json and sha256_manifest.csv.

This acquisition is explicitly labelled:

    LOGICAL_APP_PRIVATE_FILE_COPY

It is not physical acquisition or full-filesystem acquisition.

## Extraction

The acquisition script prints the next command. Equivalent example:

    python tools/extract_acquired_chatsim.py "demo_evidence\ACQ-001_<time>\working\libera_messages.db" --out "demo_evidence\ACQ-001_<time>\artifacts"

Outputs:

- ART-00001_messages.csv
- ART-00002_chats.csv
- ART-00003_device_metadata.csv
- artifact_manifest.json

These extracted ART files, not the P2 design corpus, are the intended inputs to the examiner and LLM workflow.

## Demo rule

Pre-stage Android Studio/emulator and the APK before the 20-minute presentation.

Perform live:

    open DEV-001 ChatSim
    -> inspect one chat
    -> run acquisition
    -> display SHA-256
    -> run extraction
    -> open LIBERA Workbench
    -> search/analyze evidence
    -> show FND -> ART -> ACQ -> DEV trace

Do not spend presentation time compiling Android or generating embeddings.
