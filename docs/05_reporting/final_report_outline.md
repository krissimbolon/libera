# LIBERA Final Report Outline

Dokumen ini adalah struktur laporan akhir. Isi hasil hanya boleh diambil dari run/artifact yang sudah dilock; jangan mengisi angka yang belum diverifikasi.

## 1. Judul dan Abstrak
Working title:
**Local LLM-Assisted Digital Forensic Investigation of Synthetic Human-Trafficking Evidence Using RAG and Structured Reasoning**

Abstrak harus memuat:
- tujuan;
- synthetic test scenario;
- acquisition/extraction;
- baseline;
- tiga kondisi AI;
- metrik utama;
- hasil inti;
- limitation.

## 2. Latar Belakang
Bahas:
- kebutuhan local LLM pada digital forensics;
- privacy/confidentiality;
- hallucination dan source attribution;
- peran RAG;
- kebutuhan systematic error mitigation.

Referensi inti:
- ForensicLLM — SRC-002;
- SOLVE-IT — SRC-003;
- NIST SP 800-101 Rev.1 — SRC-004;
- NIST SP 800-86 — SRC-005.

## 3. Research Questions
RQ1–RQ5 harus sama dengan `research_design.md`.

## 4. Research Design dan Separation
Jelaskan layer:
public source -> source reconstruction -> adapted synthetic scenario -> test-device staging -> acquisition -> extraction -> baseline/RAG/LLM -> human verification -> reporting.

Tegaskan ground truth tidak tersedia ke examiner/AI sebelum P9.

## 5. Source Reconstruction dan Synthetic Scenario
Laporkan:
- 543-line universe;
- mapped/unresolved count;
- 500 locked anchors;
- synthetic expansion;
- provenance categories;
- language/continuity QA;
- generator-artifact mitigation;
- keterbatasan bahwa skenario adalah synthetic adaptation, bukan komunikasi asli.

## 6. P2 Final QA
Masukkan tabel final:
- total;
- provenance;
- duplicate;
- anchor exact match;
- source line blank synthetic;
- chronology;
- actor-state;
- near-duplicate;
- cadence QA;
- hash/provenance note;
- human spot-check.

## 7. Forensic Preservation dan Acquisition
Laporkan:
- DEV-001;
- device metadata;
- acquisition type;
- ACQ-001;
- tool/version;
- hash;
- chain of custody;
- master/working separation;
- acquisition limitations.

Jangan menggunakan istilah physical/full-file-system jika acquisition hanya logical.

## 8. Extraction
Laporkan:
- ART inventory;
- parser/tool;
- schema;
- timestamp/timezone handling;
- row/object counts;
- output hashes;
- extraction QA.

## 9. Traditional Forensic Baseline
Metode:
- keyword/search;
- actor/entity;
- timeline;
- relationship;
- manual findings.

Laporkan baseline sebelum AI results.

## 10. Local LLM / RAG Methodology
Catat:
- hardware;
- Ollama version;
- model/version/digest;
- quantization;
- embedding;
- chunking;
- index;
- prompt versions;
- run parameters.

## 11. Experimental Conditions
- BASE traditional;
- A LLM-only;
- B RAG;
- C RAG + structured reasoning.

Task set sama untuk A/B/C.

## 12. Metrics
Finding-level:
- TP/FP/FN;
- precision;
- recall;
- F1.

Attribution:
- evidence locator validity;
- support correctness;
- attribution accuracy.

Safety/quality:
- unsupported/hallucinated claims;
- contradictions;
- reviewer correctness/relevance/verifiability.

Operational:
- runtime;
- retrieval depth;
- human verification effort.

## 13. Results
Isi setelah runs selesai.

### Table A — Overall
| Condition | TP | FP | FN | Precision | Recall | Attribution accuracy | Unsupported claims |
|---|---:|---:|---:|---:|---:|---:|---:|
| BASE | | | | | | | |
| A LLM-only | | | | | | | |
| B RAG | | | | | | | |
| C RAG + structured | | | | | | | |

### Table B — Human review
| Condition | Correctness | Relevance | Understandability | Verifiability |
|---|---:|---:|---:|---:|
| A | | | | |
| B | | | | |
| C | | | | |

## 14. Error Analysis
Gunakan ERR register.

Kelompokkan:
- acquisition;
- extraction;
- retrieval;
- context truncation;
- hallucination;
- evidence misattribution;
- chronology error;
- over-inference;
- ground-truth leakage risk;
- tool/reproducibility issue.

Untuk tiap kategori: failure -> impact -> mitigation -> residual risk.

## 15. Discussion per RQ
Jawab RQ dengan hasil, bukan opini.

RQ2 tidak otomatis berasumsi RAG lebih baik; laporkan jika lebih detail tetapi precision/attribution berbeda.

## 16. Limitations
Minimal:
- synthetic scenario;
- single test-device/environment;
- acquisition depth;
- local model size/hardware;
- sample/task size;
- evaluator subjectivity;
- unresolved historical provenance issue bila masih ada;
- generalizability.

## 17. Ethics dan Data Handling
- restricted source materials;
- minor-related content sanitization;
- no real victim data in synthetic corpus;
- local inference;
- raw evidence private;
- public repo hanya metadata/safe artifacts.

## 18. Reproducibility
Sertakan:
- repository commit;
- final corpus SHA-256;
- ACQ hash;
- ART hashes;
- scripts;
- model digest;
- prompt hashes;
- index version;
- run logs;
- environment versions.

## 19. Conclusion
Ringkas temuan terhadap RQ1–RQ5 tanpa memperluas klaim melampaui eksperimen.

## Appendices
A. Evidence inventory  
B. Hash manifest  
C. Chain of custody  
D. Extraction schema  
E. Fixed task/prompt set  
F. RUN register  
G. FND register  
H. ERR register  
I. Ground-truth scoring rubric (evaluator-only version bila sensitif)  
J. Full trace example `FND -> RUN -> CHK -> ART -> ACQ -> DEV`
