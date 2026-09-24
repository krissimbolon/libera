# Protokol Evaluasi Blind P9

Versi: 0.1-DRAFT  
Status: PERSIAPAN  
Tahap: P9 — Validasi dan Mitigasi Kesalahan

## 1. Tujuan

Protokol ini mengatur evaluasi independen terhadap hasil eksperimen P8 agar ground truth tidak memengaruhi proses generasi, retrieval, prompt, maupun output model.

Tujuan utamanya adalah menjaga pemisahan antara pipeline AI dan informasi evaluator.

## 2. Prinsip utama

- Ground truth privat tidak boleh diberikan kepada pipeline AI.
- Court narrative atau source reconstruction tidak boleh digunakan sebagai evidence investigator pada RAG.
- Output P8 harus dikunci sebelum ground truth digunakan untuk scoring.
- Hasil eksperimen yang telah dikunci tidak boleh diganti berdasarkan informasi dari ground truth.
- Setiap keputusan evaluator harus dapat diaudit.

## 3. Peran

### Tim AI / P6–P8

Tim AI bertanggung jawab untuk:

- menjalankan pipeline sesuai metodologi;
- menghasilkan output eksperimen;
- mencatat RUN-ID;
- mencatat model dan versi;
- mencatat prompt version;
- mencatat parameter eksperimen;
- mencatat retrieved evidence/chunk IDs;
- menyimpan output;
- menyerahkan paket hasil P8 yang telah dikunci.

Tim AI tidak boleh menerima ground truth privat yang digunakan untuk evaluasi P9.

### Evaluator P9

Evaluator bertanggung jawab untuk:

- menerima paket hasil P8 yang telah dikunci;
- memastikan metadata run tersedia;
- melakukan evaluasi menggunakan rubrik P9;
- mengakses ground truth hanya pada tahap evaluasi yang diizinkan;
- mencatat keputusan dan alasan;
- menjaga audit trail.

## 4. Prasyarat sebelum evaluasi final

Evaluasi final P9 belum boleh dimulai apabila salah satu prasyarat berikut belum terpenuhi:

- artefak evidence P4 belum stabil;
- baseline P5 belum dikunci;
- eksperimen P8 belum selesai;
- output P8 belum dikunci;
- RUN-ID belum tersedia;
- metadata eksperimen belum lengkap;
- evidence reference belum tersedia;
- rubrik P9 belum dikunci;
- ground truth evaluator belum tersedia secara privat.

## 5. Tahap sebelum ground truth dibuka

Sebelum ground truth digunakan, evaluator harus memastikan:

1. paket P8 telah diterima;
2. setiap output memiliki RUN-ID;
3. mode eksperimen dapat diidentifikasi;
4. output asli disimpan tanpa perubahan;
5. evidence reference tersedia jika diwajibkan oleh mode eksperimen;
6. versi rubrik telah ditetapkan;
7. checksum, version identifier, commit, atau mekanisme penguncian lain dicatat apabila tersedia.

Output P8 tidak boleh disunting untuk meningkatkan kualitas jawaban sebelum scoring.

## 6. Paket hasil P8 yang diterima evaluator

Minimal berisi:

- RUN-ID;
- mode eksperimen;
- model dan versi;
- model digest jika tersedia;
- Ollama version jika relevan;
- prompt version;
- parameter run;
- retrieved evidence/chunk IDs untuk mode yang menggunakan retrieval;
- output eksperimen;
- timestamp;
- reviewer status jika tersedia.

Mode eksperimen yang diharapkan:

- A — Local LLM only;
- B — Local LLM + RAG;
- C — Local LLM + RAG + structured forensic reasoning.

## 7. Pembukaan ground truth

Ground truth hanya boleh digunakan setelah output P8 yang akan dievaluasi dinyatakan final dan dikunci.

Ground truth digunakan hanya untuk:

- verifikasi entity;
- verifikasi event;
- verifikasi relation;
- verifikasi timeline;
- verifikasi finding;
- penghitungan metrik evaluasi;
- identifikasi kesalahan atau unsupported claim.

Ground truth tidak digunakan sebagai input untuk memperbaiki output P8 asli.

## 8. Proses evaluasi

Untuk setiap unit evaluasi:

1. catat EVAL-ID;
2. catat RUN-ID;
3. catat mode eksperimen;
4. identifikasi claim atau finding;
5. catat evidence reference;
6. periksa evidence yang relevan;
7. bandingkan dengan ground truth apabila tahap ground truth telah dibuka;
8. terapkan rubrik evaluasi;
9. catat label keputusan;
10. catat alasan evaluator;
11. tandai apabila membutuhkan adjudikasi.

## 9. Perlindungan terhadap leakage

Tidak boleh dilakukan:

- memasukkan ground truth ke prompt P8;
- memasukkan ground truth ke vector store investigator;
- memasukkan court narrative sebagai evidence investigator;
- memberikan hasil scoring sementara kepada pipeline AI lalu menjalankan ulang model untuk mengganti output yang telah dikunci;
- menyimpan ground truth privat pada repository publik.

## 10. Re-run dan reproducibility

Re-run terbatas dapat dilakukan untuk pemeriksaan reproducibility apabila memang dibutuhkan oleh metodologi.

Re-run tersebut harus:

- dicatat sebagai pemeriksaan reproducibility;
- menggunakan RUN-ID baru apabila menghasilkan run baru;
- tidak menggantikan output eksperimen P8 yang telah dikunci;
- dilakukan tanpa menggunakan ground truth sebagai input.

## 11. Adjudikasi

Finding yang tidak dapat diputuskan secara langsung diberi status membutuhkan adjudikasi.

Adjudikasi harus mencatat:

- EVAL-ID;
- evidence yang diperiksa;
- ground truth reference privat jika digunakan;
- alasan perbedaan;
- keputusan akhir;
- evaluator atau reviewer yang terlibat;
- timestamp;
- versi rubrik.

## 12. Audit trail

Seluruh proses evaluasi harus mempertahankan keterlacakan:

RUN-ID → output P8 → claim/finding → evidence reference → EVAL-ID → keputusan evaluasi.

Ground truth ID yang sensitif tetap berada di penyimpanan privat.

## 13. Penguncian protokol

Dokumen ini masih berstatus DRAFT.

Protokol harus dikunci sebelum evaluasi final P9 dimulai.

Perubahan substantif setelah output P8 mulai dinilai harus memiliki versi baru dan alasan perubahan yang terdokumentasi.
