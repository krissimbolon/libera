# Pelacak Progres Utama

Diperbarui: 2026-09-23

| ID | Tahap | Luaran utama | Status | Progres |
|---|---|---|---|---:|
| P0 | Penyiapan proyek & ruang lingkup | desain riset, branch, struktur folder, aturan sumber/provenance | SELESAI | 100% |
| P1 | Rekonstruksi sumber & desain kasus | skeleton 1–543, pesan terpulihkan, gap, registri sumber | BERJALAN | 35% |
| P2 | Adaptasi sintetis Indonesia | aktor, peristiwa, pesan, distractor, ground truth | BELUM MULAI | 0% |
| P3 | Penyitaan & akuisisi | catatan penyitaan, dokumentasi perangkat, akuisisi, hash | BELUM MULAI | 0% |
| P4 | Ekstraksi bukti | artefak WhatsApp terstruktur, lampiran, timestamp, evidence ID | BELUM MULAI | 0% |
| P5 | Baseline forensik tradisional | kata kunci, timeline, entitas, analisis relasi | BELUM MULAI | 0% |
| P6 | RAG | knowledge base domain, indeks bukti, retrieval berprovenance | BELUM MULAI | 0% |
| P7 | LLM lokal | konfigurasi Ollama, prompt, log run | BELUM MULAI | 0% |
| P8 | Eksperimen | LLM-only vs RAG vs RAG + structured reasoning | BELUM MULAI | 0% |
| P9 | Validasi & mitigasi kesalahan | metrik, audit hallucination, error register berbasis SOLVE-IT | BELUM MULAI | 0% |
| P10 | Laporan akhir | temuan terverifikasi, keterbatasan, chain of custody, lampiran | BELUM MULAI | 0% |
| P11 | Presentasi/demo | demo yang dapat direproduksi dan materi pertahanan | BELUM MULAI | 0% |

## P0 — SELESAI
- branch aktif: `proyek-uas-df`
- README v2 tersedia
- pertanyaan penelitian dan alur bukti terdokumentasi
- aturan provenance terdokumentasi
- batas data publik/privat terdokumentasi
- `.gitignore` diperkeras untuk kebutuhan forensik
- checklist pengumpulan sumber tersedia
- konvensi ID bukti/artefak tersedia
- peran tim: Chris, Bela, Meldiro, Daffa
- perangkat uji: OPPO CPH2819 / Android 16 / Snapdragon 685 / RAM 6 GB
- workstation: Intel Core i7-1255U / RAM 16 GB / Intel Iris Xe / ruang kosong sekitar 327 GB
- penyimpanan bukti privat: `D:\KSI\Libera Private Evidence`

Metadata operasional perangkat dan versi alat yang belum ada akan dikunci sebelum P3.

## P1 yang sudah selesai
- skeleton rekonstruksi 1–543 dibuat
- tabel coverage rekonstruksi dibuat
- log QA rekonstruksi dibuat
- log intake sumber dan ekstraksi dibuat
- registri sumber dibuat
- validator provenance rekonstruksi dibuat
- pengujian skema rekonstruksi dibuat
- Document 547 diingest sebagai SRC-001 dan di-hash
- audit awal referensi line Exhibit 1A selesai
- anomali internal referensi sumber didokumentasikan
- aturan eksplisit: tidak ada pengisian gap dengan LLM pada rekonstruksi sumber

## Tindakan P1 berikutnya
- ekstrak klaster pesan ke ruang kerja rekonstruksi terbatas;
- petakan hanya pesan dengan line yang tidak ambigu;
- biarkan referensi konflik/ambigu tetap unresolved;
- cari corroboration dari Doc. 382, 427, 512, daftar exhibit, atau Exhibit 1A;
- hitung coverage publik yang benar-benar terverifikasi.

## Tugas paralel tim
Kumpulkan court record tambahan, sumber domain perdagangan orang yang otoritatif, dan sumber metodologis tambahan yang relevan.

## Pembagian tim
- Chris — Anggota A — Lead Forensik Digital
- Bela — Anggota B — Lead Kasus & Data
- Meldiro — Anggota C — Lead AI/RAG
- Daffa — Anggota D — Lead Validasi & Dokumentasi
