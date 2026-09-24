# Register Error SOLVE-IT P9

Versi: 0.1-DRAFT  
Status: PERSIAPAN  
Tahap: P9 — Validasi dan Mitigasi Kesalahan

## 1. Tujuan

Register ini digunakan untuk mencatat error, kegagalan, ketidakpastian, dan risiko yang ditemukan selama validasi P9.

Pendekatan pencatatan mengikuti prinsip SOLVE-IT dengan menekankan:

- lokasi error dalam workflow;
- dampak error;
- bagaimana error terdeteksi;
- mitigasi yang dilakukan;
- residual risk setelah mitigasi.

## 2. Cakupan

Error dapat berasal dari:

- evidence extraction;
- baseline P5;
- chunking;
- retrieval;
- citation;
- prompt;
- model output;
- structured reasoning;
- evaluasi;
- reproducibility;
- dokumentasi.

## 3. Skema register

Setiap error minimal memiliki:

- ERR-ID;
- stage;
- RUN-ID jika relevan;
- EVAL-ID jika relevan;
- deskripsi error;
- impact;
- detection;
- mitigation;
- residual risk;
- status;
- reviewer;
- timestamp.

## 4. Format pencatatan

### ERR-ID

Identifier unik error.

Contoh:

ERR-001

### Stage

Tahap tempat error ditemukan.

Nilai yang dapat digunakan antara lain:

- P4_EXTRACTION
- P5_BASELINE
- P6_RAG
- P7_LLM
- P8_EXPERIMENT
- P9_EVALUATION
- REPRODUCIBILITY
- DOCUMENTATION

### RUN-ID

Isi apabila error terkait run P8 tertentu.

Jika tidak relevan, isi:

N/A

### EVAL-ID

Isi apabila error ditemukan pada evaluasi claim/finding tertentu.

Jika tidak relevan, isi:

N/A

### Deskripsi error

Jelaskan secara faktual apa yang terjadi.

Hindari asumsi mengenai penyebab apabila belum diverifikasi.

### Impact

Jelaskan dampak error terhadap:

- evidence;
- retrieval;
- finding;
- citation;
- metric;
- reproducibility;
- atau kesimpulan penelitian.

### Detection

Catat bagaimana error ditemukan.

Contoh:

- manual review;
- citation check;
- comparison dengan evidence;
- comparison dengan ground truth;
- automated validator;
- reproducibility test.

### Mitigation

Catat tindakan yang dilakukan untuk mengurangi atau menangani error.

Mitigasi tidak boleh mengubah output P8 yang telah dikunci secara diam-diam.

### Residual risk

Jelaskan risiko yang masih tersisa setelah mitigasi.

Contoh:

- NONE
- LOW
- MEDIUM
- HIGH
- NOT_ESTABLISHED

Jika menggunakan kategori risiko tersebut, alasan harus dicatat.

### Status

Gunakan salah satu:

- OPEN
- UNDER_REVIEW
- MITIGATED
- ACCEPTED_LIMITATION
- CLOSED

Status CLOSED hanya digunakan apabila penyelesaian error dapat dibuktikan.

## 5. Template entri

### ERR-XXX

- Stage:
- RUN-ID:
- EVAL-ID:
- Deskripsi error:
- Impact:
- Detection:
- Mitigation:
- Residual risk:
- Status:
- Reviewer:
- Timestamp:
- Evidence/reference terkait:
- Catatan:

## 6. Aturan audit

Setiap perubahan status error harus dapat ditelusuri.

Error tidak boleh dihapus hanya karena telah diperbaiki.

Riwayat error harus dipertahankan sebagai bagian dari audit trail dan dokumentasi keterbatasan penelitian.

## 7. Hubungan dengan hasil evaluasi

Jika error berkaitan dengan claim/finding tertentu, relasi berikut harus dapat ditelusuri:

RUN-ID → EVAL-ID → ERR-ID

Jika error memengaruhi lebih dari satu finding, semua EVAL-ID terkait harus dicatat.

## 8. Perlindungan data

Ground truth privat, raw evidence, dan data restricted tidak boleh disalin ke register publik.

Gunakan identifier atau reference yang aman apabila diperlukan.

## 9. Penguncian register

Dokumen ini masih berstatus DRAFT.

Struktur register harus ditetapkan sebelum evaluasi final P9 dimulai.

Entri error akan ditambahkan selama evaluasi tanpa menghapus histori sebelumnya.
