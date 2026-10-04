# Konvensi Bahasa dan Penamaan Proyek

Mulai 2026-09-23, proyek Libera UAS Digital Forensics mengutamakan Bahasa Indonesia untuk artefak baru.


## Penulisan nama proyek
- Bentuk kanonik nama proyek adalah **Libera**. Walaupun berasal dari akronim/nama proyek, ia diperlakukan sebagai satu kata dan **bukan** ditulis `LIBERA`.
- Bentuk turunan mengikuti gaya yang sama, misalnya **Libera ChatSim**, **Libera CI**, dan **proyek Libera**.
- Rekaman historis/raw yang sudah dibekukan boleh mempertahankan ejaan lama demi fidelity arsip; dokumen aktif, README, antarmuka, dan laporan baru wajib memakai **Libera**.

## Aturan
1. Nama folder baru diutamakan Bahasa Indonesia.
2. Nama dokumen baru diutamakan Bahasa Indonesia.
3. Judul, komentar dokumentasi, tracker, dan template baru ditulis dalam Bahasa Indonesia.
4. Istilah teknis yang lebih jelas atau baku dalam bahasa Inggris boleh dipertahankan, misalnya `RAG`, `ground truth`, `chain of custody`, `hash`, `retrieval`, `prompt`, dan nama skema/field kode.
5. Nama branch proyek aktif tetap `proyek-uas-df`.
6. Path lama tidak langsung diganti apabila perubahan berisiko memutus referensi, script, atau histori Git. Migrasi nama dilakukan terkontrol bila memang bermanfaat.
7. Nama field data dan identifier yang sudah digunakan lintas pipeline dipertahankan jika penggantian dapat menimbulkan inkonsistensi.
8. Dokumen sumber asli tidak diterjemahkan atau diganti namanya secara destruktif; metadata Bahasa Indonesia dibuat sebagai lapisan dokumentasi.

## Prioritas
Konsistensi, reproducibility, dan provenance lebih penting daripada menerjemahkan semua istilah secara paksa.
