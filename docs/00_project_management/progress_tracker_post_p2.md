# LIBERA Post-P2 Progress Tracker

Baseline immutable: `p2-10k-work@07a33cc4c2a1fceecabe09f4bfcc01331796b46b`.
Integration branch: `p3-p10-final-integration`.
Frozen corpus SHA-256: `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`.

| Phase | Repository implementation | Final execution status | Blocker / next action |
|---|---|---|---|
| P1 | Complete | COMPLETE | none |
| P2 | Frozen + final QA + CI | COMPLETE/FROZEN | never edit |
| P3 | Device prep docs + controlled ACQ dry-run + local runner | READY | real DEV-001/ACQ-001 requires physical local device/account/tool |
| P4 | Normalized SQLite extractor + ART manifest | READY | run on real ACQ-001 working copy for final evidence |
| P5 | Deterministic baseline implementation | READY | lock outputs after P4 final |
| P6 | Chunking + leakage guard + BGE-M3/Ollama retrieval | READY | local BGE-M3 index run |
| P7 | Local LLM runner + model/version/digest logging | READY | local Ollama `llama3.1:8b` run |
| P8 | Locked T01–T10 A/B/C harness | READY | execute after P6/P7 local setup |
| P9 | Citation precheck + blind TP/FP/TN/FN evaluator | READY | open private GT only after P8 output lock |
| P10 | Runtime report builder + methodology refs | READY | populate with actual P9 results |
| P11 | One-command local run + presentation disclosure | READY | execute/rehearse locally |

## Gate definitions

### Gate A — software dry-run
- P2 hash exactly matches canonical.
- ACQ-DRY-001 built and hashed.
- P4 extracts 10,000 unique ART rows.
- P5 creates timeline/entities/relationships/T01–T10 baseline.
- P6 chunks pass leakage guard.
- hashing retrieval + P8 dry-run completes.
- P9 precheck has zero invalid ART references.
- P10 runtime report generated.

### Gate B — real local AI run
- Ollama available.
- `bge-m3` pulled.
- `llama3.1:8b` pulled.
- model/version/digest logged.
- P8 real outputs generated and then locked.

### Gate C — final blind evaluation
- Private ground truth stays outside repository.
- P8 outputs locked first.
- P9 runs with `--outputs-locked --ground-truth <private path>`.
- TP/FP/TN/FN + precision/recall/F1/specificity saved.

### Gate D — real mobile acquisition
- Dedicated research WhatsApp account/SIM.
- DEV-001 documented contemporaneously.
- actual WhatsApp scenario staging/replay completed.
- selected acquisition tool/version documented.
- master acquisition hash + read-only preservation.
- working copy hash verified.
- P4 rerun from real ACQ-001.
