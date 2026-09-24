# P6/P7/P8 Implementation Plan — LIBERA AI/RAG Track

Status: draft pendukung, melengkapi `docs/04_ai_methodology/ai_methodology.md`
(dokumen tersebut TIDAK diubah oleh file ini).

Sumber: `Rencana_Kerja_4_Anggota_LIBERA.pdf` (versi kerja 23 September 2026) +
snapshot repository yang diberikan owner branch `p6-p7-rag-ollama-meldiro`.

> Catatan: dokumen ini disusun tanpa akses langsung ke repository GitHub.
> Semua asumsi status berasal dari PDF dan snapshot yang diberikan, bukan
> hasil audit repo.

## 1. Lingkup yang dikerjakan sekarang

Sesuai PDF Bab 2 (P6 = "Infrastruktur boleh", P7 = "Infrastruktur boleh",
P8 = "Harness boleh; run final menunggu"), dan Bab 6.1, pekerjaan yang
dikerjakan pada tahap ini adalah **infrastruktur**, bukan hasil eksperimen
final. Semua dikembangkan di atas **toy/sanitized evidence**, bukan:

- corpus 10.000 pesan (masih di branch `p2-10k-work`, belum LOCKED)
- Ground Truth privat (`data/adaptasi_indonesia/skema_ground_truth_privat.csv`)
- court narrative / Document 547

## 2. Pipeline (PDF Bab F / Bab 6.1)

```
TOY / SANITIZED EVIDENCE
        |
PREPROCESSING (baca CSV, validasi field wajib)
        |
EVIDENCE-AWARE CHUNKING (per conversation + time window, target 30-60 pesan/chunk)
        |
REPRESENTATION / EMBEDDING (placeholder hashing-vector, lihat catatan di bawah)
        |
VECTOR STORE / RETRIEVAL INDEX (JSON store lokal, 2 namespace: domain_knowledge, case_evidence)
        |
RETRIEVAL (top-k, cosine similarity, log query+scores+chunk_ids+evidence_ids+latency)
        |
RETRIEVED EVIDENCE + PROVENANCE
        |
OLLAMA (HTTP API lokal, ada mode --dry-run tanpa Ollama)
        |
STRUCTURED FINDING (Question -> Relevant Evidence -> Observed Facts ->
                     Possible Interpretation -> Contradicting Evidence ->
                     Confidence/Uncertainty -> Finding)
        |
RUN LOG (JSONL append-only, 1 baris per run)
```

## 3. Catatan penting soal embedding (batasan prototype)

Prototype ini memakai **hashing-vector sederhana berbasis stdlib Python**
(character n-gram hashing -> vektor tetap, dinormalisasi), BUKAN model
embedding sungguhan (mis. sentence-transformers). Ini sesuai arahan PDF
Bab 6.1 poin 2-4: "Prototype boleh menggunakan pendekatan sederhana
terlebih dahulu. Tidak wajib langsung menggunakan vector database berat."

Ketika model embedding sungguhan sudah dipilih (PDF 6.1 poin 3: "Pilih
embedding model. Catat model, dimensi, normalisasi, perangkat, dan versi"),
ganti fungsi `embed()` di `src/ai_rag/retriever.py` — interface lain
(chunking, indexing, retrieval, logging) tidak perlu berubah.

## 4. Dua knowledge layer (PDF 6.1 poin 6)

`retriever.py` memisahkan index menjadi dua *namespace* terpisah:

- `domain_knowledge` — materi umum forensik digital (bukan bukti kasus)
- `case_evidence` — hasil ekstraksi P4 dari Chris (working evidence), TIDAK
  PERNAH berisi court narrative / Document 547 / Ground Truth

`leakage_check.py` melakukan pengecekan dasar sebelum ingest ke index
`case_evidence`, menolak file yang mengandung penanda Ground Truth
(kolom schema privat) atau penanda narasi pengadilan.

Ini adalah **guard sederhana**, bukan jaminan mutlak — review manusia
tetap wajib sebelum data masuk index produksi, sesuai prinsip "Tujuan 3"
di PDF (blind evaluation).

## 5. Traceability (PDF 6.3 Definition of Done Meldiro)

Setiap `structured finding` harus bisa ditelusuri:

```
FND -> RUN -> CHK -> ART -> ACQ -> DEV
```

Prototype ini mengimplementasikan bagian `FND -> RUN -> CHK` (finding,
run log, chunk provenance). Bagian `ART -> ACQ -> DEV` bergantung pada
output P4 milik Chris dan **belum tersedia** — field-field itu disiapkan
sebagai *pass-through* opsional di schema (`source_reference` per pesan),
diisi kosong/`TOY` selama memakai data mainan.

## 6. Tiga kondisi eksperimen (PDF Bab 6.1 poin 11, P8)

| Kondisi | Deskripsi | Retrieval? | Structured reasoning prompt? |
|---|---|---|---|
| A | LLM only | Tidak | Tidak |
| B | LLM + RAG | Ya | Tidak (jawaban bebas + evidence IDs) |
| C | LLM + RAG + structured reasoning | Ya | Ya (format finding penuh) |

Implementasi: `src/ai_rag/run_experiment.py`. Pertanyaan yang sama
dijalankan pada ketiga kondisi dengan `prompt_version`, `model`, `seed`
yang dikunci sebelum run — tidak ada perubahan prompt berdasarkan hasil,
sesuai larangan PDF di Bab F: "Jangan membuat klaim bahwa salah satu
kondisi lebih baik sebelum eksperimen dilakukan."

## 7. Yang sengaja TIDAK dibuat di sini

Sesuai batasan eksplisit dari owner:

- Tidak membuat ulang sistem reconstruction/QA P1 (`data/reconstruction/`)
- Tidak membuat Ground Truth schema baru / mengubah
  `skema_ground_truth_privat.csv`
- Tidak membuat ulang `anchor_indonesia_500.csv`
- Tidak membuat dataset final 10.000 sebagai bagian prototype ini
- Tidak membuat hasil evaluasi P9 (itu milik Daffa, setelah P8 final)
- Tidak memasukkan court narrative ke RAG

## 8. Definition of Done untuk P6/P7 infra (dikutip ulang dari PDF 6.3)

- [ ] Pipeline dapat dibangun ulang dari environment + config
- [ ] Chunk memiliki evidence provenance lengkap
- [ ] LLM-only, RAG, dan RAG+structured reasoning memakai protokol yang setara
- [ ] Tidak ada ground-truth leakage
- [ ] Setiap finding AI dapat ditelusuri FND -> RUN -> CHK -> ART -> ACQ -> DEV

Status saat ini: **infrastruktur + toy dry-run**, belum memenuhi seluruh
poin di atas (bagian ART->ACQ->DEV menunggu handoff P4 dari Chris).
