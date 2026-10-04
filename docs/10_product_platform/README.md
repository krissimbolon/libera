# Libera Operational Platform

Libera now has two deliberately separate modes:

1. **Operational investigator mode** — install once, reuse the same verified runtime/models, and create an isolated workspace for every case.
2. **Research validation mode** — the frozen P2 + ChatSim benchmark used to evaluate Libera scientifically.

The operational mode is a **beta forensic platform**, not a validated commercial forensic suite. It does not claim legal admissibility and it does not replace upstream acquisition tools.

## Supported host model

The CLI is pure Python 3.12+ and is smoke-tested on Windows, macOS, and Linux. Deterministic case management, trusted-hash import, P4 extraction, P5 baseline, verification, and archive do not require an LLM.

AI assistance additionally requires a local Ollama installation with `bge-m3` and `qwen2.5:1.5b`. Models are cached by Ollama and are **not downloaded per case**.

Hardware/OS support is therefore capability-based rather than a claim that every physical device can execute every model:

- Python 3.12+ for the platform;
- local writable case storage;
- Ollama for AI assistance;
- enough RAM/disk for the selected local models.

## Install once

From a tagged/release source or wheel:

```bash
python -m pip install .
libera doctor --json --skip-models
```

Optional AI setup, once per machine:

```bash
libera setup-models
```

## Case lifecycle

```bash
libera case create CASE-2026-001 --title "Example examination"
libera case import-sqlite CASE-2026-001 evidence.sqlite --sha256 <trusted_sha256>
libera case extract CASE-2026-001
libera case baseline CASE-2026-001
libera case review-p5 CASE-2026-001
libera case assist CASE-2026-001
libera case verify CASE-2026-001
libera case archive CASE-2026-001
```

By default cases live under `~/.libera/cases/<CASE-ID>/`. Set `LIBERA_HOME` or pass `--root` to place case storage on a dedicated forensic volume.

## Case isolation

Each case has its own:

```text
CASE-ID/
├── case.json
├── configs/
├── evidence/
│   ├── master/
│   └── working/
├── runtime/
│   └── working/
│       ├── P4/
│       ├── P5/
│       ├── P6/
│       └── AI/
├── logs/
└── exports/
```

The software, Python installation, Ollama runtime, and model cache are machine-level resources and are reused across cases.

## Evidence adapter boundary

The first operational adapter accepts a **normalized SQLite chat export** with the documented `messages` schema. The examiner supplies a trusted SHA-256. Libera:

- verifies the source hash before import;
- makes master and working copies;
- never claims it performed the upstream device acquisition;
- refuses a hash mismatch;
- derives P4 ART artifacts from the verified working copy.

Future adapters can add UFDR/AXIOM/other exports without changing the case lifecycle.

## AI boundary

Operational mode runs only the useful structured RAG assistant; it does not waste time on the A/B/C research ablation for every case. The research benchmark remains available separately.

AI output is always an **investigative aid**, never evidence. Outputs, retrieval index, run log, task/config files, and P5/P4 inputs are hash-locked after the assistance run. Examiners must verify cited ART artifacts before using a claim in a report.

## Archive

`libera case archive` verifies custody/lock hashes before creating an archive. The default archive is **report-only** and excludes message-level artifacts, chunks, AI text, and raw evidence. Use `--include-derived` for a sensitive derived-evidence archive; use `--include-derived --include-evidence` only when policy and storage rules permit a full case package.

## Current production limitations

- normalized chat SQLite is the only operational evidence adapter in v1;
- upstream mobile/disk acquisition remains the responsibility of established forensic tools;
- no legal/court validation claim;
- no central multi-user server/RBAC yet;
- local small-model quality remains an empirical limitation;
- public redistribution/reuse still depends on the repository's licensing decision.

These are product roadmap constraints, not hidden capabilities.
