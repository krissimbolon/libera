# Controlled AI Experiment Protocol — LIBERA

Tujuan: menjawab RQ1–RQ5 dengan perbandingan yang fair antara traditional forensic baseline dan tiga kondisi AI.

Acuan utama:
- ForensicLLM (Sharma et al., 2025; SRC-002): local LLM for digital forensics, correctness/relevance, source attribution, dan perbandingan base/RAG.
- SOLVE-IT (Hargreaves et al., 2025; SRC-003): systematic error identification dan mitigation.
- Research design LIBERA: case-design/ground truth dipisahkan dari examiner/AI pipeline.

## Experimental conditions

### BASE — Traditional forensic baseline
Tanpa LLM/RAG.
Output investigator harus mempunyai ART locator.

### A — Local LLM only
Input hanya evidence payload yang diberikan langsung pada run sesuai batas context. Tidak ada hidden ground truth.

### B — Local LLM + RAG
Evidence diindeks dari extracted/acquired artifacts. Setiap retrieved chunk harus traceable ke ART.

### C — Local LLM + RAG + structured forensic reasoning
Retrieval sama dengan B. Perbedaannya hanya reasoning/prompt protocol yang mewajibkan:
1. claim;
2. supporting evidence;
3. evidence locator;
4. uncertainty;
5. alternative explanation bila relevan;
6. no-evidence/no-conclusion bila dukungan tidak cukup.

Jangan mengubah model atau evidence corpus antar B dan C bila tujuan eksperimen adalah mengisolasi efek structured reasoning.

## Fixed investigative task set

Gunakan task yang sama pada A/B/C:

- T01 — Identifikasi aktor yang relevan dan hubungan antarnya berdasarkan evidence.
- T02 — Susun timeline peristiwa relevan dengan evidence locator.
- T03 — Temukan evidence koordinasi/rekrutmen yang didukung pesan.
- T04 — Temukan evidence transportasi, lokasi/penginapan, dan pergerakan.
- T05 — Temukan evidence tekanan/kontrol atau konflik yang didukung pesan.
- T06 — Temukan evidence pembayaran, harga, atau transaksi/negosiasi.
- T07 — Temukan evidence upaya pulang/keluar/mencari bantuan bila ada.
- T08 — Bedakan evidence substantif dari percakapan netral/distractor.
- T09 — Identifikasi kontradiksi, ambiguity, atau informasi yang belum cukup.
- T10 — Buat daftar finding prioritas dengan evidence IDs dan confidence/uncertainty.

Task wording dikunci sebelum melihat ground truth evaluation.

## Run control

Untuk setiap RUN:
- run_id;
- condition;
- task_id;
- model name/version;
- model digest;
- quantization;
- Ollama version;
- prompt version/hash;
- temperature;
- seed bila tersedia;
- context window;
- timestamp;
- evidence/chunk inputs;
- retrieved CHK IDs untuk B/C;
- raw output;
- elapsed time;
- reviewer status.

Jika seed tidak didukung, catat `NOT_AVAILABLE`, bukan mengarang nilai.

## Retrieval provenance

Untuk setiap CHK:
- chunk_id;
- source artifact_id;
- acquisition_id;
- source message IDs/range;
- text start/end locator;
- embedding model/version;
- chunking config;
- index version.

Trace minimum:
`RUN -> CHK -> ART -> ACQ -> DEV`.

## Ground-truth blinding

Sebelum semua experimental RUN dikunci:
- evaluator ground truth tidak boleh berada di RAG;
- source court narrative yang dipakai membangun skenario tidak boleh berada di evidence RAG;
- filenames/columns yang langsung membocorkan label evaluator tidak boleh diberikan ke model;
- evaluator mapping hanya dibuka pada P9.

## Evaluation dimensions

### Finding recovery
- true positive finding;
- false positive finding;
- false negative finding;
- precision;
- recall;
- F1 bila denominator memadai.

### Evidence attribution
Untuk setiap claim/finding:
- locator exists?;
- locator belongs to acquired evidence?;
- cited evidence actually supports claim?;
- claim overstates evidence?;
- attribution accuracy.

### Hallucination / unsupported claim
Hitung claim faktual yang:
- tidak didukung acquired evidence;
- bertentangan dengan acquired evidence;
- berasal dari case-design/ground truth leakage;
- mengarang actor/location/event.

### Human usefulness
Reviewer blind terhadap condition bila memungkinkan menilai:
- correctness;
- relevance;
- understandability;
- verifiability;
- detail/usefulness.

Gunakan rubric yang sama antar condition.

## Statistical/reporting discipline

Laporkan per-task dan aggregate. Jangan hanya melaporkan satu contoh sukses.

Untuk sample kecil, utamakan:
- raw counts;
- proportions;
- confidence intervals bila layak;
- paired task-level comparison;
- qualitative error taxonomy.

Jangan mengklaim superiority general di luar test corpus.

## Final comparison table

Minimal kolom:
- condition;
- findings proposed;
- TP;
- FP;
- FN;
- precision;
- recall;
- evidence-attribution accuracy;
- unsupported claims;
- mean human correctness;
- mean relevance;
- mean verifiability;
- runtime;
- notes.

## Failure handling

Setiap failure signifikan masuk ERR register:
- technique/objective;
- stage;
- symptom;
- evidence;
- root-cause hypothesis;
- mitigation;
- rerun required?;
- residual risk.

Mitigation tidak boleh mengubah condition definition setelah melihat result tanpa dicatat sebagai protocol deviation.
