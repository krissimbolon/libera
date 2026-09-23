# Pendataan Tim dan Lingkungan Uji

Dokumen ini digunakan untuk mengunci informasi tim, perangkat uji, workstation, dan penyimpanan bukti sebelum P0 ditutup.

## Tim
| Kode | Nama | Peran utama | Peran penelaah |
|---|---|---|---|
| Anggota A | Chris | Lead Forensik Digital | Telaah baseline / validasi |
| Anggota B | Bela | Lead Kasus & Data | Telaah RAG / data |
| Anggota C | Meldiro | Lead AI / RAG | Telaah eksperimen |
| Anggota D | Daffa | Lead Validasi & Dokumentasi | Telaah forensik / laporan |

## Perangkat uji
- Jenis perangkat: ponsel Android
- Produsen/model: OPPO / CPH2819
- SoC: Qualcomm Snapdragon 685 Octa-core
- Versi Android: Android 16
- Versi perangkat lunak: CPH2819_16.0.5.1201 (EX01B110P02)
- Versi kernel: 5.15.197
- RAM: 6 GB
- Baterai: 6500 mAh
- Kapasitas penyimpanan: BELUM DIKONFIRMASI
- Versi WhatsApp: BELUM DIKONFIRMASI
- Akun/SIM uji: BELUM DIKONFIRMASI
- Zona waktu: BELUM DIKONFIRMASI
- Sinkronisasi jam perangkat: BELUM DIKONFIRMASI
- Status root: BELUM DIKONFIRMASI
- Status jaringan saat akuisisi: BELUM DIKONFIRMASI
- Catatan: perangkat kandidat diberikan oleh Chris pada 2026-09-23. Jangan melakukan root, reset, atau perubahan sistem sebelum protokol akuisisi dikunci.

## Workstation akuisisi dan Ollama
- Nama perangkat: DESKTOP-SKF40M7
- Sistem operasi: 64-bit, arsitektur x64; edisi/versi Windows belum dicatat
- Prosesor: 12th Gen Intel(R) Core(TM) i7-1255U @ 1.70 GHz
- RAM: 16.0 GB (15.7 GB usable)
- GPU: Intel(R) Iris(R) Xe Graphics
- Memori grafis yang dilaporkan: 128 MB
- Penyimpanan total: 477 GB
- Penyimpanan terpakai: 150 GB
- Perkiraan ruang kosong: 327 GB
- Dukungan pen/touch: tidak tersedia
- Versi Python: BELUM DIKONFIRMASI
- Versi Ollama: BELUM DIKONFIRMASI
- Model kandidat: BELUM DITETAPKAN
- Dapat diisolasi offline?: BELUM DIKONFIRMASI
- Alat hashing: BELUM DITETAPKAN
- Alat akuisisi/ekstraksi: BELUM DITETAPKAN

## Identitas sistem yang tidak disimpan di repositori publik
Device ID dan Product ID sengaja tidak dicatat pada dokumen repositori karena tidak diperlukan untuk reproduksibilitas eksperimen dan dapat mengidentifikasi instalasi/perangkat secara lebih spesifik.

## Penyimpanan bukti privat
- Lokasi utama: `D:\KSI\Libera Private Evidence`
- Pemilik/host: workstation Chris
- Status: DIKONFIRMASI
- Enkripsi/cadangan: AKAN DITETAPKAN SEBELUM AKUISISI

### Struktur lokal yang disarankan
```text
D:\KSI\Libera Private Evidence\
├── 01_sumber_asli\
├── 02_master_evidence\
├── 03_working_copy\
├── 04_ground_truth\
├── 05_log_akuisisi\
└── 06_rekonstruksi_terbatas\
```

Aturan: file master tidak diedit; analisis dilakukan pada working copy; hash dan metadata aman dapat dicatat di GitHub publik.

## Status P0
P0 SELESAI pada 2026-09-23. Metadata operasional perangkat dan versi alat yang belum ada akan dikunci tepat sebelum tahap akuisisi P3 dan tidak menghambat penutupan desain proyek.
