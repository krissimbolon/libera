# Reproducibility manifest

Canonical reproduction guide for the archived Libera snapshot. It separates what anyone can reproduce
from a clone, what needs local tools and models, and what is intentionally not published.

## 1. Snapshot identity

| Item | Value |
|---|---|
| Repository | <https://github.com/krissimbolon/libera> |
| Snapshot | tag `v1.0.0` on `main` (resolve the exact commit with `git rev-parse v1.0.0`; a file cannot embed its own commit SHA) |
| Frozen P2 corpus | `data/adaptasi_indonesia/corpus_whatsapp_10000.csv` — 10,000 rows — SHA-256 `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6` — `FROZEN_FOR_FORENSIC_SIMULATION` |
| Corpus byte protection | `.gitattributes`: `-text` for the corpus, so Git never converts line endings (Windows checkouts keep the hash) |
| Registered config | `configs/p6_p7_config.json` v1.1.0 — the v6 parameters of the reported run (§5); the superseded v2 baseline is recorded under `history` |
| Investigation tasks | `configs/investigation_tasks.json` (T01–T10) |
| Reported experiment | P8 v6, 2026-09-25 — parameters in §5; outputs private (§4) |

## 2. Tier A — reproducible from the public repository

Requirements: Python ≥ 3.12, `pytest`. No network, no models, no Android tooling. The P3–P10 pipeline code
uses only the standard library.

```bash
git clone https://github.com/krissimbolon/libera.git && cd libera
python -m pip install -e ".[test]"        # installs pytest only; no package code is installed

# 1. Frozen-corpus integrity
python - <<'PY'
import csv, hashlib
p = "data/adaptasi_indonesia/corpus_whatsapp_10000.csv"
print(hashlib.sha256(open(p, "rb").read()).hexdigest())
print(sum(1 for _ in csv.DictReader(open(p, encoding="utf-8", newline=""))))
PY
# expected: a014a02e…467e6 and 10000

# 2. Automated tests (74 tests at v1.0.0)
python -m pytest

# 3. Pipeline smoke on a software dry-run acquisition (deterministic, no model calls)
python -m src.forensics.acquisition_simulator          # P3 ACQ-DRY-001 (NOT a device acquisition)
python -m src.forensics.extract_artifacts               # P4
python -m src.baseline.traditional_baseline             # P5
python -m src.ai_rag.chunker --input runtime/working/P4/artifacts.csv --output runtime/working/P6/chunks.jsonl --min-size 30 --max-size 60 --time-window-minutes 120
python -m src.ai_rag.leakage_check --input runtime/working/P6/chunks.jsonl
python -m src.ai_rag.retriever build --chunks runtime/working/P6/chunks.jsonl --namespace case_evidence --index runtime/working/P6/index.json --embedding-method hashing
python -m src.ai_rag.run_experiment --dry-run --index runtime/working/P6/index.json --questions configs/investigation_tasks.json --output runtime/working/P8/experiment_output.json --top-k 8
python tools/lock_p8_outputs.py          # expected to FAIL: "Refuse P8 lock" (dry-run/hashing is never a study lock)
python -m src.evaluation.evaluate_experiment   # P9 precheck only, no labels
python -m src.report.build_report              # P10; states "DRY-RUN (no model call ...)"

# 4. Documentation references
python tools/check_doc_links.py --paths

# 5. ChatSim device seed (what CI builds into the APK)
python tools/build_demo_seed.py   # seed_manifest.json: 10,000 source rows -> 9,997 device rows + 3 anomalies
```

Expected smoke values (Python 3.12–3.14, Linux): P3 dry-run SQLite SHA-256 `1e6a1c83…e21eea`; P4 10,000
artifacts / 26 chats / 846 segments, `artifacts.csv` SHA-256 `d5e6fb73…24cfd`; P6 648 chunks with
`hashing:sha256_hashing_v1`. These are **smoke values for the dry-run carrier**, not study results (the study
used the ChatSim acquisition: 9,997 artifacts, 25 chats, 645 chunks).

CI (`.github/workflows/post-p2-integration.yml`, "Libera CI") runs exactly these checks on Python 3.12 and
3.14, including the assertion that the lock refuses the smoke output.

Also reproducible publicly: the P2 corpus audits (`python src/audit_final_corpus.py` etc., manual workflow
`p2-final-audit.yml`). Note that re-running them rewrites the committed `qa_*_working.json` snapshots with
some different style counts (e.g. `context_B.comma_phrase_ya_ending`); the committed files are historical
snapshots from corpus construction and the automated gate result (`automated_gate_passed: true`) is unchanged.

## 3. Tier B — reproducible locally with tools and models

Tested team environment (as recorded in `docs/03_forensic_protocol/persiapan_p3_p4/`): Windows 10/11
(build 26200, 64-bit), Python 3.14 via the `py` launcher, Android SDK Platform-Tools 37.0.1 (ADB 1.0.41),
Android emulator, Ollama with `qwen2.5:1.5b` and `bge-m3`. The exact Ollama version and model digests were
recorded per call in the private run log (`ollama_version`, `model_digest`) and are not published.
The APK is built by CI (`build-chatsim-final.yml`: Java 17, Gradle 8.9). Other platforms are untested.

```powershell
# 1. Android carrier: install the CI-built APK on the emulator (ChatSim, NOT WhatsApp)
powershell -ExecutionPolicy Bypass -File scripts\install_chatsim.ps1 -ApkPath .\Libera-ChatSim-final-debug.apk

# 2. P3 logical acquisition + hash check + P4 extraction, then stop for examiner QC
powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -StopAfterP4

# 3. P5 baseline with time-boxed human examiner QC, locked before any AI step
powershell -ExecutionPolicy Bypass -File scripts\run_p5_examiner_review.ps1 -ArtifactsPath demo_evidence\ACQ-SIM-001_<timestamp>\artifacts\artifacts.csv

# 4. P6–P10 on the acquired artifacts. -DryRun: hashing embedding, no model calls, no lock.
#    Without -DryRun: pulls bge-m3 + qwen2.5:1.5b, runs A/B/C with the registered v6 parameters and locks P8.
powershell -ExecutionPolicy Bypass -File scripts\run_libera_local.ps1 -ArtifactsPath demo_evidence\ACQ-SIM-001_<timestamp>\artifacts\artifacts.csv -UseLockedP5 -DryRun

# Examiner workbench (python -m pip install -e ".[workbench]" into .venv first)
powershell -ExecutionPolicy Bypass -File scripts\run_workbench.ps1
```

The reported v6 experiment command, its audit, lock and report steps are recorded verbatim in
[04_ai_methodology/P8_REAL_RUN_20260925.md](04_ai_methodology/P8_REAL_RUN_20260925.md). Locked-output
evaluation (never reruns P8):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_p9_final.ps1 `
  -GroundTruthPath <private labels.csv> -LockManifest <run>\p8_lock_manifest.json `
  -OutputDirectory <new folder> -CitationPolicy quarantine   # default "refuse" stops on any invalid citation
```

Guards that make reruns safe: `run_experiment.py` refuses to overwrite an output or a folder with a lock;
`lock_p8_outputs.py` refuses existing locks and any dry-run, errored, incomplete, unregistered or
provenance-less execution; `run_p9_final.ps1` refuses existing evaluation folders and verifies every locked
hash before opening labels; `lock_private_ground_truth.py` refuses relabelled files.

## 4. Tier C — intentionally excluded

| Excluded | Why | Where it lived |
|---|---|---|
| ChatSim master/working SQLite, extracted `ART` files (`ACQ-SIM-001_20260925_010848`) | Raw acquisition evidence; custody kept outside Git | `demo_evidence/` (git-ignored) |
| P5 lock, P6 index, P8 v6 outputs, run log, lock manifest, code snapshots | Machine-specific runtime evidence of the study | `runtime/working/` (git-ignored) |
| Original private semantic ground truth | Evaluator-only; reported lost on the team workstation; not recreated | — |
| P9 provenance-proxy reference + lock + annotation packet | Evaluator-only label material | `runtime/private/P9_reconstructed_20260925/` |
| Document 547 originals (PDF/Markdown) | Sensitive court record (trafficking, minors) | restricted local storage; hashes in `references/` |
| Credentials, device serials/IMEI, phone numbers | Never collected into the repo | — |

Consequently the reported numbers in [final_state.md](final_state.md) can be **checked for internal
consistency and traced to their recorded hashes**, but cannot be recomputed from a public clone.

## 5. Parameters of the reported run (P8 v6, 2026-09-25)

| Parameter | Value |
|---|---|
| LLM / embedding | `qwen2.5:1.5b` / `bge-m3` (1,024-dim), both through local Ollama on loopback |
| temperature / seed | 0.1 / 42 |
| num_ctx / top-k / similarity | 8,192 / 8 / cosine |
| chunking | 30–60 messages, 120-minute window, grouped by merged participant chat |
| num_predict / timeout / retries | 2,048 / 600 s / 2 (transport errors only) |
| repeat_penalty / repeat_last_n | 1.2 / 256 |
| prompt | `v6-forensic-grounded-repeat-control`; C uses an Ollama JSON schema (7 fields, ≤ 8 evidence IDs, ≤ 240 chars per field) |
| retrieval sharing | B and C use the identical retrieval per task |

## 6. Known non-determinism

- Ollama generation with a fixed seed and low temperature is repeatable on the same model digest, runtime
  and hardware, but not guaranteed across Ollama versions, quantizations or GPUs/CPUs.
- Wall-clock fields (timestamps, durations, `run_id`) differ on every run.
- The hashing embedding used in CI is deterministic; BGE-M3 vectors depend on the Ollama build.
- P5 human QC decisions and any future human annotation are, by nature, not machine-reproducible.

## 7. Output locations

| Path | Produced by | Tracked |
|---|---|---|
| `runtime/private/ACQ-DRY-001/` | P3 dry-run | no |
| `runtime/working/P4…P10/` | pipeline stages | no |
| `runtime/chatsim_snapshots/` | workbench acquisitions | no |
| `demo_evidence/ACQ-SIM-001_*/` | `acquire_chatsim.ps1` | no |
| `apps/libera-chatsim/app/src/main/assets/{messages_seed.jsonl,seed_manifest.json,source_anomalies.jsonl}` | `tools/build_demo_seed.py` | no (built in CI) |


## 8. Final fresh-run evaluation hardening

For the final report run, the real local path additionally captures and hash-locks
`runtime/working/P8/run_environment.json`, `runtime/working/P8/runtime_metrics.json`,
and the BGE-M3 retrieval index. The environment manifest records repository HEAD,
registered-input hashes, Python/OS information, Android emulator metadata, Ollama
version, and the exact generation/embedding model digests without recording a username,
hostname, arbitrary environment variables, or private evidence contents.

After the P8 lock exists, `src.evaluation.postlock_review` creates two evaluator packets:

- `retrieval_relevance_review.csv`: 10 registered tasks × top-8 ranked chunks (80 judgments in the final design), graded 0/1/2. Completed packets can report Precision@8, MRR@8 and nDCG@8. Recall@8 remains explicitly unavailable unless a complete independently judged relevant set exists.
- `claim_supportedness_review.csv`: B/C outputs, only citations that survived strict identifier/supplied-evidence validation, and the underlying cited ART text. Human review separates semantic support from identifier validity using SUPPORTED/PARTIAL/UNSUPPORTED/CONTRADICTED/ABSTAINED plus four 0–2 task-component dimensions.

Complete the packets manually, then run:

```powershell
py -3 -m src.evaluation.score_postlock_review
```

The resulting `runtime/working/P9/human_review_metrics.json` is a post-lock human
evaluation layer. It must not be conflated with private message-level ground truth.
The design intentionally keeps four questions separate: whether retrieval was relevant,
whether a citation identifier was valid, whether cited evidence semantically supported
the generated claim, and whether the answer completed the registered investigative task.
