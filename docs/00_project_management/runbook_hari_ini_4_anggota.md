# Runbook Penyelesaian Hari-H — 4 Anggota LIBERA

Tanggal kerja: 2026-09-24  
Tujuan: menyelesaikan jalur eksperimen digital forensics secara akademik dan reproducible pada hari yang sama, dengan pembagian kerja paralel dan tanpa membocorkan ground truth ke examiner/AI pipeline.

## Prinsip penelitian yang tidak boleh dilanggar

1. P2 case-design/ground truth terpisah dari evidence yang akan dilihat examiner.
2. Setelah P2 final, pipeline examiner hanya menerima acquired/extracted evidence, bukan file desain kasus.
3. Semua evidence dan hasil AI harus traceable:
   - AI-assisted: `FND -> RUN -> CHK -> ART -> ACQ -> DEV`
   - non-AI: `FND -> ART -> ACQ -> DEV`
4. Raw/restricted evidence tetap di penyimpanan privat.
5. Jangan menyebut logical export sebagai physical/full-file-system acquisition.
6. Master evidence tidak diedit; analisis hanya pada working copy.
7. Hash, tool/version, prompt, model, retrieval context, parameter, output, error, dan human validation dicatat.

## Pembagian empat anggota

### Chris — Lead Forensik Digital
Fokus utama:
- P3 preservation/acquisition;
- DEV/ACQ identifier;
- device/workstation metadata;
- acquisition log;
- SHA-256 master + working copy;
- chain of custody;
- cross-review hasil P5 baseline.

Tidak boleh:
- mengubah ground truth selama menjadi examiner;
- menganalisis file case-design sebagai evidence.

### Bela — Lead Kasus & Data
Fokus utama:
- menutup P2 bersama QA Work;
- memverifikasi final corpus dan mapping evidence simulator;
- P4 extraction/schema;
- ART identifier;
- entity/timeline tables dari acquired evidence;
- menjaga separation antara source reconstruction, adapted synthetic scenario, dan acquired evidence.

Cross-review:
- dataset/chunks RAG dan provenance retrieval.

### Meldiro — Lead AI / RAG
Fokus utama:
- P6 knowledge base + retrieval;
- P7 Ollama/local model configuration;
- P8 experimental runs;
- log `RUN-#####`, model/version/quantization, prompt, temperature, seed bila tersedia;
- condition A = LLM-only;
- condition B = RAG;
- condition C = RAG + structured reasoning.

Tidak boleh:
- memasukkan ground truth/case-design ke knowledge base examiner;
- memakai corpus desain langsung bila P4 acquired/extracted artifact sudah tersedia.

### Daffa — Lead Validasi & Dokumentasi
Fokus utama:
- P9 validation;
- SOLVE-IT-inspired error register `ERR-#####`;
- hallucination/unsupported claim audit;
- evidence attribution audit;
- chain-of-custody review;
- P10 paper/report + P11 presentation/demo;
- cross-review P3 acquisition documentation.

## Critical path hari ini

### Gate 0 — P2 Finalization
Owner: Bela  
Reviewer: Chris + independent QA branch

Selesai hanya jika:
- corpus = 10.000;
- provenance = 500/1.500/6.500/1.500;
- anchor = 500/500;
- synthetic source_original_line kosong;
- duplicate = 0;
- cadence/language artifact sudah ditangani;
- chronology + actor-state audit selesai;
- near-duplicate selesai;
- hash discrepancy didokumentasikan;
- final artifacts dibuat.

Jangan lanjut menggunakan corpus sebagai evidence master sebelum Gate 0.

### Gate 1 — Test-device/evidence staging
Owner: Bela + Chris

1. Catat final corpus hash.
2. Buat satu paket evidence-simulation versioned.
3. Catat prosedur staging ke test device/environment.
4. Simpan ground-truth mapping di lokasi evaluator-only.
5. Examiner copy tidak berisi label ground truth/provenance internal yang tidak seharusnya terlihat.

### Gate 2 — P3 Preservation & Acquisition
Owner: Chris  
Reviewer: Daffa

Minimum deliverable:
- `DEV-001` device record;
- `ACQ-001` acquisition package;
- acquisition method/type;
- tool + version;
- start/end time;
- device state;
- network state;
- timezone;
- WhatsApp/app version;
- hash manifest;
- chain-of-custody entries;
- limitation statement.

Jika metode yang tersedia hanya export/logical copy, dokumentasikan secara eksplisit sebagai logical acquisition. Jangan mengklaim bit-for-bit image.

### Gate 3 — P4 Extraction
Owner: Bela  
Reviewer: Chris

Minimum:
- extracted message table;
- preserved original timestamps/timezone;
- sender/recipient/conversation mapping;
- artifact IDs `ART-#####`;
- traceability ke ACQ-001;
- attachment index bila ada;
- extraction script/tool/version;
- row-count/hash QA.

### Gate 4 — P5 Traditional forensic baseline
Owner: Chris + Bela

Tanpa LLM:
- keyword search;
- actor/entity inventory;
- event/timeline reconstruction;
- relationship/link table;
- evidence relevance decisions;
- setiap finding memiliki ART locator.

Output:
- `FND-BASE-...`;
- baseline findings table;
- baseline false-positive/uncertain notes.

Baseline ini wajib selesai sebelum membandingkan AI.

### Gate 5 — P6/P7 RAG + Local LLM
Owner: Meldiro  
Reviewer: Bela

RAG chunks harus berasal dari:
- acquired/extracted evidence;
- public digital-forensic methodology/domain KB bila desain eksperimen membolehkan.

Jangan memasukkan:
- ground truth;
- hidden evaluator mapping;
- source court narrative yang tidak hadir di acquired evidence, kecuali diposisikan eksplisit sebagai external domain KB dan eksperimen memisahkannya.

Simpan:
- CHK IDs;
- source ART;
- chunk offsets;
- embedding model/version;
- index config;
- local LLM model/version/quantization;
- prompt template.

### Gate 6 — P8 Experiment
Owner: Meldiro  
Reviewer: Daffa

Jalankan pertanyaan/investigative tasks yang sama pada:
A. local LLM only;
B. RAG + local LLM;
C. RAG + structured reasoning.

Minimal outcome yang dicatat per RUN:
- answer;
- cited evidence IDs;
- retrieved chunks;
- runtime;
- unsupported claims;
- investigator usefulness;
- whether expected finding was recovered.

### Gate 7 — P9 Validation
Owner: Daffa  
Reviewer: Chris

Gunakan evaluator-only ground truth setelah run dikunci.

Metrik minimum:
- finding recall/sensitivity;
- precision/false-positive rate untuk finding;
- evidence attribution accuracy;
- unsupported/hallucinated claim count/rate;
- citation/ART correctness;
- actor/event/timeline correctness;
- human verification status.

SOLVE-IT-inspired error register:
- technique/objective;
- observed failure;
- cause hypothesis;
- impact;
- mitigation;
- residual risk.

### Gate 8 — P10/P11 Report & Demo
Owner: Daffa  
Semua anggota review

Paper/report harus memisahkan:
1. source reconstruction;
2. synthetic case design;
3. forensic acquisition;
4. extraction;
5. traditional baseline;
6. LLM-only;
7. RAG;
8. structured reasoning;
9. ground-truth evaluation;
10. errors/limitations.

Demo harus bisa menunjukkan satu trace lengkap:
`FND -> RUN -> CHK -> ART -> ACQ -> DEV`.

## Stop conditions

Hentikan sign-off, bukan seluruh kerja, bila:
- P2 final hash berubah tanpa change log;
- acquired evidence hash tidak cocok;
- master evidence pernah diedit;
- ground truth bocor ke examiner/RAG;
- tool/version tidak tercatat;
- AI finding tidak dapat ditelusuri ke ART;
- acquisition type diklaim lebih kuat daripada metode sebenarnya.

Temuan seperti ini masuk `ERR-#####` dan harus dimitigasi/didokumentasikan.

## Definition of Done hari ini

Proyek dianggap selesai secara eksperimen bila:
- P2 final frozen;
- satu acquisition package tervalidasi dan hashed;
- extraction dapat direproduksi;
- traditional baseline tersedia;
- tiga experimental conditions memiliki run logs;
- ground-truth evaluation selesai;
- error/mitigation register selesai;
- paper memiliki hasil aktual, bukan placeholder;
- presentation/demo memiliki satu end-to-end trace;
- semua raw sensitive evidence tetap berada di storage privat.

Jika waktu menjadi bottleneck, prioritaskan validitas metodologis dan traceability daripada jumlah model/prompt/visualisasi.
