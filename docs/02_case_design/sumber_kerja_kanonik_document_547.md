# Sumber Kerja Kanonik Document 547

Mulai 2026-09-23, proyek menggunakan **Document 547 Galloway.md** sebagai sumber kerja utama untuk tahap P1.

## Status sumber
- ID sumber: `SRC-001`
- Nama file kerja: `Document 547 Galloway.md`
- SHA-256: `195a880e87f59d882e70c16b4c42a9df23a0eaec547b928f1ad1a9afae4ae889`
- Panjang hasil parse: 1014 baris
- Peran: sumber kerja kanonik untuk ekstraksi dan pemetaan referensi Government Exhibit 1A.

## Alasan penggunaan
Versi Markdown mempertahankan struktur halaman, heading, penekanan bold/underline, serta referensi line Exhibit 1A dengan lebih nyaman untuk ekstraksi terstruktur dibanding membaca PDF secara langsung.

## Aturan kerja
1. Semua ekstraksi P1 berikutnya memakai versi Markdown ini.
2. PDF sebelumnya tidak digunakan lagi sebagai sumber kerja utama.
3. PDF tetap boleh disimpan sebagai arsip/verifikasi sumber asli, tetapi tidak dijadikan basis line-mapping harian.
4. Jika terdapat konflik internal di versi Markdown, konflik tidak diselesaikan dengan tebakan atau LLM.
5. Corroboration harus berasal dari filing lain, Exhibit 1A asli, atau sumber publik lain yang dapat diaudit.
6. Materi sensitif tidak dipindahkan ke repositori publik; yang disimpan di GitHub hanya metadata, skema, QA, dan hasil yang sudah disanitasi.

## Konfirmasi isi penting
Versi Markdown menyatakan bahwa Government Exhibit 1A mengatalogkan pesan masuk dan keluar dari ponsel Cornelius Galloway dan menggunakan sistem warna untuk mengidentifikasi penulis. Dokumen juga menyatakan bahwa Government hanya memilih sebagian percakapan untuk dipresentasikan kepada juri. Karena itu, P1 tetap diperlakukan sebagai rekonstruksi parsial berbasis sumber publik, bukan sebagai salinan penuh Exhibit 1A.
