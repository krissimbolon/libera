# LIBERA Post-P2 Progress Tracker

## Streamlit ChatSim selesai — 25 September 2026

- Sumber percakapan langsung SQLite ChatSim melalui ADB; tanpa impor CSV.
- Akuisisi lewat browser teruji: 9.997 pesan, 25 chat, hash cocok dengan sumber P8.
- Tujuh tab mencakup percakapan, pencarian, timeline, trace, A/B/C, evaluasi dan laporan.
- 12 referensi C dikarantina; status proxy rekonstruksi ditampilkan eksplisit.
- 38 tes lulus; browser dan Streamlit AppTest terverifikasi.
- Panduan: [STREAMLIT_CHATSIM.md](../06_report/STREAMLIT_CHATSIM.md).

## Latest reconstructed-reference evaluation ? 25 September 2026

- Pengguna mengonfirmasi GT asli di Chris hilang. Corpus beku digunakan untuk membuat referensi **provenance proxy**, bukan memulihkan label bukti kunci manusia.
- Referensi privat: 10.000 rows; 500 anchor-positive, 1.500 distractor-negative, 8.000 unlabeled.
- P9/P10 jalur proxy **SUDAH DIEKSEKUSI DAN SELESAI**: 1.997 acquired labeled messages; 3 anchor unacquired; 12 citation C tetap dikarantina.
- Status `P9_RECONSTRUCTED_PROXY_EVALUATION_COMPLETE_WITH_CITATION_ERRORS`; tidak diklaim sebagai final blind semantic evaluation.
- Paket anotasi ulang manusia juga dibuat, 9.997 rows dengan label kosong.
- [Dokumentasi lengkap, metrik, dan batasan](../05_validasi/GT_RECONSTRUCTION_P9_P10_20260925.md). Hasil: `runtime/working/P9_reconstructed_20260925/`.
- Checkpoint di bawah bersifat historis.

## Latest P9 review ? 25 September 2026

- P8 v6 tetap locked dan tidak diubah; 14/14 hashes terverifikasi.
- Penanganan referensi selesai: C 24 referensi, 12 valid dan 12 dikarantina (50% identifier validity). Tidak ada ID yang diperbaiki atau dipetakan otomatis.
- Scoring hanya memakai exact P4 IDs yang diberikan ke kondisi; seluruh universe GT tetap dipertahankan sehingga FN tidak disembunyikan.
- Paket evaluasi dan laporan tersedia di `runtime/working/P9_review_20260925/`.
- 31 tes lulus, termasuk bukti invalid reference tidak diberi kredit dan FN tetap dihitung.
- **P9 final belum selesai: path GT independen belum diberikan.** Script final sudah mengambil eksperimen dari lock v6 dan memverifikasi seluruh file sebelum GT dibuka.
- [Kebijakan dan perintah P9](../05_validasi/P9_CITATION_POLICY_20260925.md) | [Hasil lokal untuk laporan](../06_report/RESULTS_LOCAL_20260925.md).

## Latest local execution ? 25 September 2026

- P3/P4 ChatSim: actual ACQ-SIM-001 tersedia; 9.997 ART, 25 chat.
- P5 lock v2 verified; P6 real BGE-M3 index 645 entries.
- P8 final v6: **T01?T10 selesai, A/B/C 30/30 respons nyata**, 0 transport error/retry, 30 normal stop, 10/10 schema C valid.
- P8 output locked: **14/14 file hashes PASS**. Folder: `runtime/working/P8_final_v6_20260925/`.
- P9 precheck: **FAIL_INVALID_EVIDENCE_REFERENCE**; 12 invalid reference strings pada 6 output C. Private GT belum dibuka; final metrics belum dikerjakan.
- P10 runtime report tersedia, actual ChatSim acquisition sudah tercatat.
- Dokumentasi, perintah, hash, batasan, dan riwayat percobaan: [P8 real run](../04_ai_methodology/P8_REAL_RUN_20260925.md).
- Ringkasan/checkpoint di bawah adalah status historis sebelum eksekusi lokal ini.

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
| P7 | Local LLM runner + model/version/digest logging | READY | local Ollama `qwen2.5:1.5b` run |
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
- `qwen2.5:1.5b` pulled.
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

## Verified integration checkpoint — 24 September 2026

GitHub Actions `Post-P2 Integration Audit` run **36019711196** completed with **success** on commit `5286fb372cc1b54c80d869491a911bd56b99e7b2`.

Verified results:

- 12/12 automated tests passed.
- Frozen P2 SHA-256 gate passed.
- P3 controlled dry-run: 10,000 rows -> `ACQ-DRY-001` PASS.
- P4: 10,000 unique ART artifacts, 26 merged participant chats, 846 retained source segments.
- P5: 10,000 messages, 10 investigation tasks, 26 actors.
- P6: 648 evidence-aware chunks; leakage guard PASS; 648-entry deterministic CI index.
- P8: all 10 T01–T10 tasks completed in A/B/C dry-run harness.
- P9: `P9_PRECHECK_PASS`; no invalid evidence-reference blocker.
- P10: runtime report generated and all expected runtime outputs non-empty.

### Interpretation of this checkpoint

This closes the **software/integration implementation** of P3–P10 and proves the full pipeline is executable from the frozen P2 corpus.

It does **not** claim the following machine-bound work has already occurred:

1. real WhatsApp/device staging on DEV-001;
2. real mobile acquisition ACQ-001 with Oxygen/selected tool;
3. real BGE-M3 embeddings through local Ollama;
4. real Qwen2.5-1.5B inference;
5. final P9 ground-truth metrics.

Those five items are local execution gates and must remain distinguishable from the controlled dry-run.

## Presentation-ready checkpoint

Latest verified platform audit:

- GitHub Actions `Post-P2 Integration Audit` run **36020816999**: **SUCCESS**.
- Python 3.12 job: PASS.
- Python 3.14 job: PASS.
- This verifies the repository software path against the Python version family used by the local workstation.

Controlled Android evidence carrier:

- GitHub Actions `Build Final ChatSim` run **36020547705**: **SUCCESS**.
- Build source corpus SHA-256: `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`.
- Source rows: 10,000.
- `DEV-SIM-001` device rows: 9,997.
- Source anomalies excluded from Raka device: 3.
- Chats on simulated device: 25.
- APK artifact: `libera-chatsim-final-debug`.
- Artifact ZIP digest reported by GitHub: `sha256:4f075c86020790d015fc029cce0f55cfab99102e5ebb564f4f857a50e73c9fc8`.
- Extracted debug APK SHA-256 independently checked after download: `50ad5ee93b162d87cac562a41f7f2d28c982ec1c88146e44442b907ae4d43fb4`.

### Operational status for the presentation

The reproducible **simulation research track** is now implementation-complete:

`P2 frozen -> DEV-SIM-001 -> ACQ-SIM-001 -> P4 ART -> P5 -> P6 -> P7 -> P8 -> P9 -> P10/P11`.

The remaining actions are execution on the team's local machine/emulator:

1. install the already-built APK;
2. run the ChatSim acquisition command;
3. run real Ollama BGE-M3/Qwen2.5-1.5B instead of dry-run;
4. optionally run final P9 with the evaluator-only private ground truth after P8 output lock.

A separate physical-WhatsApp-device acquisition remains an optional/extended validation track and must not be conflated with ChatSim.


## Branch consolidation checkpoint — 24 September 2026

- Canonical branch: `main`.
- All former project branch histories were consolidated into merge commit `7453c192aa156fdb43223fc660028c29d7427d71`.
- Each former branch was verified with `ahead_by = 0` against `main` before cleanup.
- Post-P2 Integration Audit is configured to run on `main`.
- Final ChatSim build is configured to run on `main`.
