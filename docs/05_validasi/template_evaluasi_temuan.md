# Template Evaluasi Temuan P9

Versi: 0.1-DRAFT  
Status: PERSIAPAN  
Tahap: P9 — Validasi dan Mitigasi Kesalahan

## 1. Tujuan

Template ini digunakan untuk mencatat evaluasi setiap claim atau finding dari output eksperimen P8.

Setiap evaluasi harus dapat ditelusuri kembali ke RUN-ID, mode eksperimen, output asli, dan evidence reference yang relevan.

## 2. Identitas evaluasi

- EVAL-ID:
- RUN-ID:
- Mode eksperimen:
- Tanggal evaluasi:
- Evaluator:
- Versi rubrik:

## 3. Identitas output P8

- Model:
- Model version/tag:
- Model digest:
- Prompt version:
- Parameter run:
- Timestamp run:

## 4. Unit evaluasi

Pilih salah satu:

- ENTITY
- EVENT
- RELATION
- TIMELINE
- FINDING

Unit evaluasi:

- Unit:
- Claim/Finding:
- Evidence reference:
- Artifact ID:
- Chunk ID:
- Message ID:

Isi hanya identifier yang memang tersedia pada output atau evidence terkait.

## 5. Evaluasi

### Factual correctness

Keputusan:

- CORRECT
- PARTIALLY_SUPPORTED
- INCORRECT
- NOT_ESTABLISHED

Catatan:

### Evidence attribution

Keputusan:

- CORRECT
- PARTIALLY_CORRECT
- INCORRECT
- NOT_APPLICABLE

Catatan:

### Groundedness

Keputusan:

- SUPPORTED
- PARTIALLY_SUPPORTED
- UNSUPPORTED
- NOT_ESTABLISHED

Catatan:

### Hallucination / unsupported claim

Keputusan:

- NO
- PARTIAL
- YES
- NOT_ESTABLISHED

Catatan:

### Citation accuracy

Keputusan:

- CORRECT
- PARTIALLY_CORRECT
- INCORRECT
- NOT_APPLICABLE

Catatan:

### Contradiction detection

Keputusan:

- CORRECT
- MISSED
- FALSE_POSITIVE
- NOT_APPLICABLE

Catatan:

## 6. Ground truth

Ground truth reference tidak boleh ditulis pada repository publik apabila bersifat privat.

- Ground truth diperiksa: YA / TIDAK
- Ground truth reference privat:
- Catatan evaluator:

## 7. Keputusan akhir

Label akhir:

- CORRECT
- PARTIALLY_SUPPORTED
- INCORRECT
- NOT_ESTABLISHED

Alasan keputusan:

## 8. Adjudikasi

- Membutuhkan adjudikasi: YA / TIDAK
- Alasan:
- Reviewer tambahan:
- Keputusan adjudikasi:
- Timestamp adjudikasi:

## 9. Audit trail

Keterlacakan minimum:

RUN-ID → Claim/Finding → Evidence Reference → EVAL-ID → Keputusan Evaluasi

Output P8 asli tidak boleh diubah sebagai bagian dari proses evaluasi.
