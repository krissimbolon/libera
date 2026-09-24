# Checklist Gate P9

Versi: 0.1-DRAFT  
Status: PERSIAPAN  
Tahap: P9 — Validasi dan Mitigasi Kesalahan

## 1. Tujuan

Checklist ini digunakan untuk menentukan apakah evaluasi final P9 sudah boleh dimulai.

P9 final hanya boleh dijalankan apabila seluruh prerequisite kritis telah terpenuhi.

## 2. Gate evidence dan baseline

- [ ] Artefak evidence hasil P4 telah tersedia.
- [ ] Evidence ID telah stabil.
- [ ] Artifact ID telah stabil.
- [ ] Timestamp evidence telah diverifikasi.
- [ ] Chain of custody dan hash yang relevan tersedia.
- [ ] Baseline forensik tradisional P5 telah selesai.
- [ ] Baseline P5 telah dikunci.
- [ ] Finding baseline dapat ditelusuri ke evidence ID terkait.

## 3. Gate pipeline AI

- [ ] P6 RAG pipeline telah selesai pada data final.
- [ ] P7 local LLM pipeline telah selesai pada data final.
- [ ] Model dan versi telah dicatat.
- [ ] Ollama version telah dicatat jika digunakan.
- [ ] Embedding model telah dicatat.
- [ ] Vector store/configuration telah dicatat.
- [ ] Chunking schema telah dikunci.
- [ ] Retrieval configuration telah dikunci.
- [ ] Evidence citation/retrieval trace tersedia.

## 4. Gate eksperimen P8

- [ ] Mode A — Local LLM only telah selesai.
- [ ] Mode B — Local LLM + RAG telah selesai.
- [ ] Mode C — Local LLM + RAG + structured forensic reasoning telah selesai.
- [ ] Setiap eksperimen memiliki RUN-ID.
- [ ] Model tag/version tersedia.
- [ ] Model digest tersedia jika didukung.
- [ ] Prompt version tersedia.
- [ ] Parameter run tersedia.
- [ ] Retrieved evidence/chunk IDs tersedia untuk mode retrieval.
- [ ] Timestamp run tersedia.
- [ ] Output asli setiap RUN-ID tersedia.
- [ ] Output P8 telah dinyatakan final.
- [ ] Output P8 telah dikunci sebelum ground truth digunakan.

## 5. Gate instrumen P9

- [ ] Rubrik evaluasi P9 tersedia.
- [ ] Rubrik evaluasi telah ditinjau.
- [ ] Rubrik evaluasi telah dikunci.
- [ ] Protokol evaluasi blind tersedia.
- [ ] Protokol evaluasi blind telah ditinjau.
- [ ] Protokol evaluasi blind telah dikunci.
- [ ] Template evaluasi temuan tersedia.
- [ ] Template CSV evaluasi tersedia.
- [ ] Register error SOLVE-IT tersedia.
- [ ] Template CSV register error tersedia.
- [ ] Aturan adjudikasi telah ditetapkan.
- [ ] Audit trail telah ditetapkan.

## 6. Gate ground truth

- [ ] Ground truth evaluator telah tersedia secara privat.
- [ ] Ground truth tidak berada di repository publik.
- [ ] Ground truth tidak diberikan kepada pipeline AI.
- [ ] Ground truth belum digunakan untuk memperbaiki output P8.
- [ ] Ground truth dapat ditelusuri menggunakan identifier privat yang stabil.

## 7. Gate blind evaluation

- [ ] Output P8 telah dikunci sebelum ground truth dibuka.
- [ ] Evaluator mengetahui versi output P8 yang dinilai.
- [ ] RUN-ID yang dinilai telah ditetapkan.
- [ ] Tidak ada output P8 yang diganti setelah ground truth dibuka.
- [ ] Re-run, jika dilakukan, dipisahkan sebagai reproducibility check.
- [ ] Re-run tidak menggantikan hasil eksperimen P8 asli.

## 8. Gate keamanan dan provenance

- [ ] Raw evidence privat tidak masuk repository publik.
- [ ] Ground truth privat tidak masuk repository publik.
- [ ] Court narrative tidak digunakan sebagai evidence investigator.
- [ ] Source reconstruction tidak digunakan sebagai input tersembunyi ke pipeline AI.
- [ ] Setiap finding dapat ditelusuri ke evidence reference yang diizinkan.

## 9. Keputusan gate

Status:

- [ ] READY_FOR_P9
- [ ] NOT_READY_FOR_P9

Tanggal pemeriksaan:

Reviewer:

Catatan:

## 10. Aturan keputusan

Status READY_FOR_P9 hanya boleh dipilih apabila seluruh prerequisite kritis telah terpenuhi.

Jika terdapat item kritis yang belum terpenuhi, status harus tetap NOT_READY_FOR_P9.

Item yang belum terpenuhi harus dicatat sebagai blocker dan tidak boleh diabaikan tanpa justifikasi metodologis yang terdokumentasi.
