# Rubrik Evaluasi P9

Versi: 0.1-DRAFT  
Status: PERSIAPAN  
Tahap: P9 — Validasi dan Mitigasi Kesalahan

## 1. Tujuan

Rubrik ini digunakan untuk mengevaluasi hasil eksperimen P8 secara konsisten, terukur, dan dapat diaudit.

Rubrik harus dikunci sebelum evaluator melihat hasil eksperimen final dan ground truth evaluasi.

## 2. Objek evaluasi

Evaluasi dilakukan terhadap:

- entity;
- event;
- relation;
- timeline;
- finding;
- evidence citation/reference yang menyertai finding.

Setiap unit evaluasi harus dapat ditelusuri ke RUN-ID P8 dan evidence ID terkait.

## 3. Label keputusan utama

Setiap claim atau finding diberi salah satu label berikut.

### CORRECT

Claim sesuai dengan evidence yang diizinkan dan, setelah tahap ground truth dibuka, sesuai dengan ground truth evaluator.

### PARTIALLY_SUPPORTED

Sebagian claim didukung evidence, tetapi terdapat bagian yang tidak lengkap, terlalu luas, kurang tepat, atau hanya didukung sebagian.

### INCORRECT

Claim bertentangan dengan evidence atau ground truth yang relevan.

### NOT_ESTABLISHED

Evidence yang tersedia tidak cukup untuk menetapkan claim sebagai benar atau salah.

Label NOT_ESTABLISHED tidak boleh otomatis dianggap sebagai INCORRECT.

## 4. Dimensi evaluasi

### 4.1 Factual correctness

Menilai apakah isi faktual pada output P8 benar.

Yang diperiksa antara lain:

- identitas aktor;
- peristiwa;
- waktu;
- lokasi;
- relasi;
- urutan kejadian;
- detail material lain.

### 4.2 Evidence attribution

Menilai apakah finding merujuk pada evidence yang benar.

Finding harus dapat ditelusuri ke evidence ID, artifact ID, chunk ID, atau message ID yang relevan sesuai keluaran pipeline.

### 4.3 Groundedness

Menilai apakah claim benar-benar dapat diturunkan dari evidence yang tersedia.

Claim tidak boleh menambahkan fakta material yang tidak didukung evidence.

### 4.4 Hallucination / unsupported claim

Menilai keberadaan claim faktual yang tidak mempunyai dukungan evidence yang memadai.

Evaluasi dilakukan pada tingkat claim, bukan hanya pada tingkat jawaban keseluruhan.

### 4.5 Citation accuracy

Menilai apakah evidence reference yang diberikan benar-benar mendukung claim yang dirujuk.

Citation dinilai tidak akurat apabila:

- evidence tidak relevan;
- evidence tidak mendukung claim;
- identifier salah;
- claim lebih kuat daripada isi evidence.

### 4.6 Contradiction detection

Menilai kemampuan output P8 dalam mendeteksi kontradiksi yang memang ada dan menghindari kontradiksi palsu.

### 4.7 Reproducibility

Menilai apakah hasil eksperimen dapat diaudit menggunakan metadata yang tersedia, termasuk:

- RUN-ID;
- mode eksperimen;
- model dan versi;
- prompt version;
- parameter yang digunakan;
- retrieved evidence/chunk IDs;
- timestamp;
- output yang dikunci.

## 5. Evaluasi entity, event, relation, dan timeline

Untuk unit yang mempunyai ground truth terstruktur, gunakan:

- TP — item benar ditemukan;
- FP — item dilaporkan tetapi tidak didukung;
- FN — item ground truth yang seharusnya ditemukan tetapi tidak ditemukan.

Metrik:

Precision = TP / (TP + FP)

Recall = TP / (TP + FN)

F1 = 2 × Precision × Recall / (Precision + Recall)

Jika penyebut bernilai nol, hasil tidak boleh ditentukan secara arbitrer. Kondisi tersebut harus dicatat sebagai tidak terdefinisi atau tidak berlaku sesuai konteks evaluasi.

## 6. Aturan evidence

Setiap finding material harus:

- memiliki evidence reference apabila mode eksperimen menyediakan citation;
- tidak mengandalkan court narrative sebagai evidence investigator;
- tidak menggunakan ground truth sebagai input ke pipeline AI;
- mempertahankan keterlacakan ke artefak forensik yang diizinkan.

## 7. Aturan blinded evaluation

Sebelum ground truth dibuka:

- output P8 harus sudah final dan dikunci;
- RUN-ID dan metadata eksperimen harus sudah dicatat;
- tidak boleh ada perubahan output berdasarkan ground truth.

Setelah ground truth dibuka:

- ground truth hanya digunakan untuk evaluasi;
- output P8 tidak boleh diperbaiki dan dijalankan ulang untuk mengganti hasil eksperimen yang telah dikunci.

## 8. Audit trail

Setiap keputusan evaluator minimal harus mencatat:

- EVAL-ID;
- RUN-ID;
- mode eksperimen;
- unit evaluasi;
- claim/finding;
- evidence ID;
- label keputusan;
- alasan evaluator;
- evaluator;
- timestamp evaluasi;
- versi rubrik.

Ground truth ID disimpan secara privat apabila termasuk informasi yang tidak boleh masuk repository publik.

## 9. Adjudikasi

Kasus yang ambigu atau diperselisihkan harus ditandai untuk adjudikasi.

Adjudikasi harus:

- mengacu pada evidence;
- mencatat alasan keputusan;
- tidak mengubah output P8 asli;
- menjaga versi dan audit trail.

## 10. Kebijakan penguncian rubrik

Rubrik ini masih berstatus DRAFT.

Rubrik harus ditinjau dan dikunci sebelum evaluasi final P9 dimulai.

Setelah rubrik dikunci dan output P8 final mulai dinilai, perubahan substantif terhadap kriteria evaluasi harus didokumentasikan sebagai perubahan versi dan tidak boleh dilakukan hanya untuk menyesuaikan hasil eksperimen.
