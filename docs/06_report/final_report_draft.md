# LIBERA — Final Report Draft (P10)

## Hasil rekonstruksi terbaru

P9/P10 untuk **post-hoc provenance proxy** telah selesai. Lihat [metode, metrik actual, dan batasan](../05_validasi/GT_RECONSTRUCTION_P9_P10_20260925.md). Ground truth semantik evaluator yang hilang tidak berhasil dipulihkan; jangan mengklaim metrik proxy sebagai akurasi bukti kunci.

## Checkpoint lokal sebelum rekonstruksi

Hasil actual dan batasannya tersedia dalam [RESULTS_LOCAL_20260925.md](RESULTS_LOCAL_20260925.md): P8 30/30 selesai, 12 citation C dikarantina, evaluasi GT final masih menunggu label independen. Parameter v2 di rancangan awal berikut bersifat historis; run actual memakai v6 yang terdokumentasi.

## Working title
**Local LLM-Assisted Digital Forensic Investigation of Synthetic WhatsApp Evidence Using Retrieval-Augmented Generation and Structured Forensic Reasoning**

## Abstract
LIBERA evaluates a reproducible local-LLM workflow for digital-forensic analysis of a controlled Indonesian synthetic WhatsApp case. The study separates source reconstruction, synthetic case construction, mobile acquisition, evidence extraction, traditional forensic analysis, RAG/local-LLM analysis, and blinded ground-truth evaluation. The final corpus contains 10,000 frozen messages and is passed downstream without modification. Three AI conditions are compared: local LLM only (A), local LLM + RAG (B), and local LLM + RAG + structured forensic output (C). Findings are evaluated only after outputs are locked, using evidence traceability and message-level TP/FP/TN/FN metrics. **Replace this final sentence with actual P9 numerical results after local execution.**

## 1. Introduction
Digital-forensic workloads increasingly involve large volumes of messenger data. Local LLMs offer potential efficiency benefits but create risks around hallucination, reproducibility, provenance, and evidence attribution. LIBERA therefore treats the LLM as an analysis assistant rather than an evidence source and requires every downstream claim to be traceable to acquired evidence identifiers.

### Research questions
- RQ1: How effectively can a local LLM identify relevant evidence from synthetic WhatsApp evidence?
- RQ2: Does RAG improve groundedness and evidence attribution compared with a local LLM without RAG?
- RQ3: Does structured forensic output improve verifiability?
- RQ4: What errors arise across acquisition, preprocessing, retrieval, and inference?
- RQ5: How consistent are AI-assisted findings with ground truth and a traditional forensic baseline?

## 2. Related work
Summarize the references in `docs/01_research_design/methodology_references.md`, emphasizing NIST/SWGDE mobile-forensics integrity, WhatsApp artifact analysis, RAG provenance, BGE-M3 multilingual retrieval, and recent LLM-forensics evaluation work.

## 3. Case and data design
- P1 reconstructs only publicly supportable source information.
- P2 adapts the structure into an Indonesian synthetic scenario.
- Frozen P2 corpus: 10,000 messages.
- Composition: 500 adapted anchors, 1,500 bridge, 6,500 context, 1,500 distractor.
- Frozen SHA-256: `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`.
- P2 is immutable after freeze.

## 4. Forensic acquisition and extraction
### P3
Document DEV-001 state contemporaneously, acquisition method/tool version, examiner interaction, chain of custody, master evidence hash, and working-copy verification. If the presentation uses ACQ-DRY-001, state explicitly that it is a software-controlled pipeline dry-run rather than a physical-device acquisition.

### P4
Normalize examiner-visible evidence into ART identifiers. The public/examiner artifact schema must exclude construction provenance and evaluator-only ground-truth fields. Preserve the original generation segment only as a segment identifier while grouping examiner chat context by participant pair.

## 5. Traditional forensic baseline (P5)
The locked baseline uses deterministic keyword search, chronological timeline reconstruction, actor frequency, and pairwise communication frequency for T01–T10. It does not use LLMs, embeddings, source reconstruction, or ground truth.

## 6. Local RAG/LLM methodology
### P6 retrieval
- chunking: merged participant chat + time window;
- target chunk size: 30–60 messages;
- evidence IDs rendered inside chunk text;
- final embedding: BGE-M3 via local Ollama;
- cosine similarity;
- top-k: 8;
- case index input: P4 ART evidence only.

### P7 local model
- model: `qwen2.5:1.5b`;
- temperature: 0.1;
- seed: 42;
- context setting: 8192;
- prompt version: `v2-forensic-grounded`;
- log Ollama version and model digest where available.

### P8 experimental conditions
- A: local LLM only; no case evidence supplied; lower-bound abstention/hallucination condition.
- B: local LLM + RAG.
- C: same retrieval as B + locked structured forensic JSON schema.
- B and C share exactly the same retrieval trace per task.
- Outputs are locked before ground truth is opened.

## 7. Evaluation (P9)
Run `src.evaluation.evaluate_experiment` after P8 lock.

### Integrity metrics
- invalid ART citations;
- retrieval references outside artifact universe;
- C structured-JSON validity;
- model/runtime errors.

### Ground-truth metrics
For each locked condition/prediction set compute TP, FP, FN, TN, precision, recall, F1, and specificity against evaluator-only key-evidence labels. Report the ground-truth coverage and explicitly state whether the private label file represents the full 10,000-message universe or a labeled subset.

## 8. Results
Populate from `runtime/working/P10/run_report.md` after local execution.

Recommended tables:
1. acquisition/extraction integrity;
2. P5 baseline evidence coverage;
3. retrieval/citation integrity per condition;
4. TP/FP/TN/FN and precision/recall/F1/specificity;
5. representative supported, partially supported, and rejected findings.

## 9. Discussion
Discuss whether RAG improves evidence attribution without overstating causal conclusions from a single synthetic case. Separate model quality from retrieval quality. Discuss false positives, missed evidence, context-window effects, and the difference between software dry-run and real mobile acquisition.

## 10. Limitations
- synthetic case design limits external validity;
- logical/selective acquisition must not be described as physical/full-file-system acquisition;
- LLM outputs are probabilistic despite locked parameters;
- ground-truth design may affect measured performance;
- one local model and one embedding model do not generalize to all model families;
- a dry-run acquisition validates software flow, not mobile-tool capability.

## 11. Conclusion
Conclude only after P9. The defensible claim should focus on reproducibility, evidence attribution, observed metric differences, and documented limitations—not on AI replacing forensic examiner judgment.

## Reproducibility appendix
- Integration branch: `p3-p10-final-integration`.
- One-command Windows runner: `scripts/run_libera_local.ps1`.
- Post-P2 CI: `.github/workflows/post-p2-integration.yml`.
- Runtime outputs are excluded from Git.
- Private ground truth and acquisition masters remain outside the public repository.
