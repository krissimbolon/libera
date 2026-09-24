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

## 3. Case Initiation and Investigative Basis
Tetapkan sebelum examiner melihat evidence:
- alasan Raka menjadi subjek pemeriksaan berdasarkan informasi pre-device;
- investigative hypotheses;
- examination request/scope;
- simulated search authority;
- penjelasan bahwa DEV-001 adalah researcher-owned test device yang merepresentasikan handset Raka;
- pemisahan pre-device suspicion, device evidence, dan evaluator-only ground truth.

Jangan memakai temuan dari WhatsApp sebagai alasan retroaktif untuk menjelaskan mengapa HP diperiksa.

## 4. Research Questions
RQ1–RQ5 harus sama dengan `research_design.md`.

## 5. Research Design dan Separation
Jelaskan layer:
public source -> source reconstruction -> adapted synthetic scenario -> test-device staging -> acquisition -> extraction -> baseline/RAG/LLM -> human verification -> reporting.

Tegaskan ground truth tidak tersedia ke examiner/AI sebelum P9.

## 6. Source Reconstruction dan Synthetic Scenario
Laporkan:
- 543-line universe;
- mapped/unresolved count;
- 500 locked anchors;
- synthetic expansion;
- provenance categories;
- language/continuity QA;
- generator-artifact mitigation;
- keterbatasan bahwa skenario adalah synthetic adaptation, bukan komunikasi asli.

## 7. P2 Final QA
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

## 8. Forensic Preservation dan Acquisition
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

## 9. Extraction
Laporkan:
- ART inventory;
- parser/tool;
- schema;
- timestamp/timezone handling;
- row/object counts;
- output hashes;
- extraction QA.

## 10. Traditional Forensic Baseline
Metode:
- keyword/search;
- actor/entity;
- timeline;
- relationship;
- manual findings.

Laporkan baseline sebelum AI results.

## 11. Local LLM / RAG Methodology
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

## 12. Experimental Conditions
- BASE traditional;
- A LLM-only;
- B RAG;
- C RAG + structured reasoning.

Task set sama untuk A/B/C.

## 13. Metrics
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

## 14. Results
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

## 15. Error Analysis
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

## 16. Discussion per RQ
Jawab RQ dengan hasil, bukan opini.

RQ2 tidak otomatis berasumsi RAG lebih baik; laporkan jika lebih detail tetapi precision/attribution berbeda.

## 17. Limitations
Minimal:
- synthetic scenario;
- single test-device/environment;
- acquisition depth;
- local model size/hardware;
- sample/task size;
- evaluator subjectivity;
- unresolved historical provenance issue bila masih ada;
- generalizability.

## 18. Ethics dan Data Handling
- restricted source materials;
- minor-related content sanitization;
- no real victim data in synthetic corpus;
- local inference;
- raw evidence private;
- public repo hanya metadata/safe artifacts.

## 19. Reproducibility
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

## 20. Forensic Conclusion and Ground-Truth Concordance
Pisahkan dua lapis:
- blinded forensic conclusion: apa yang didukung acquired evidence;
- evaluator comparison: apakah temuan tersebut concordant dengan intended Raka case resolution yang diadaptasi dari adjudicated Galloway outcome.

Hindari kalimat bahwa HP sendiri 'membuktikan Raka bersalah'. Gunakan bahasa evidentiary support dan concordance.

## 21. Conclusion
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
