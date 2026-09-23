# Pelacak Progres Utama

Diperbarui: 2026-09-23

| ID | Tahap | Luaran utama | Status | Progres |
|---|---|---|---|---:|
| P0 | Penyiapan proyek & ruang lingkup | desain riset, branch, struktur folder, aturan sumber/provenance | SELESAI | 100% |
| P1 | Rekonstruksi sumber & desain kasus | skeleton 1–543, pesan terpulihkan, gap, registri sumber | BERJALAN | 60% |
| P2 | Adaptasi sintetis Indonesia | aktor, peristiwa, pesan, distractor, ground truth | BERJALAN | 25% |
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
- desain riset, provenance, pemisahan publik/privat, tim, perangkat uji, workstation, dan penyimpanan bukti privat telah dikunci.

## P1 — status saat ini
- sumber kerja kanonik: `Document 547 Galloway.md`
- SHA-256 sumber: `195a880e87f59d882e70c16b4c42a9df23a0eaec547b928f1ad1a9afae4ae889`
- 543 line Exhibit 1A dipertahankan sebagai universe rekonstruksi
- **500/543 line (92,08%)** telah memiliki mapping kerja yang dapat dipertahankan
- **43/543 line (7,92%)** tetap unresolved
- konflik 85–96 vs 382–389 diselesaikan melalui konsistensi internal dan narasi line 94
- 382–392 dipetakan dari referensi langsung yang koheren pada halaman 34–35
- typo 511–5521 disimpan sebagai source typo dengan working resolution 511–521
- artefak parsing dari konversi PDF lama dibersihkan terhadap sumber Markdown kanonik
- paket rekonstruksi verbatim v2 tetap berada di penyimpanan privat, bukan GitHub publik
- tidak ada gap yang diisi menggunakan LLM

## Sisa P1
- corroboration untuk rentang 16–27, 116–117, 168–175, 208–217, dan 531–541;
- QA manual silang oleh anggota kedua;
- bentuk actor/event/timeline ground truth yang tidak membocorkan evidence ke examiner;
- kunci versi final rekonstruksi sebelum P2.

## P2 — sudah dimulai
- target corpus ditetapkan 10.000 pesan;
- 500 pesan anchor berasal dari line Galloway yang sudah dipetakan;
- 1.500 pesan bridge, 6.500 context, dan 1.500 distractor akan dibuat dalam semesta kasus yang sama;
- latar utama dilokalisasi ke Bandung Raya dengan hotel/alamat/platform fiktif;
- peta aktor sumber → aktor Indonesia telah ditetapkan;
- aturan anti-duplikasi, provenance, ground-truth leakage, dan QA batch telah didokumentasikan.

## Tindakan P2 berikutnya
- Worker A selesai menghasilkan 239 anchor untuk source line 1–271;\n- Worker B sedang mengerjakan source line 272–543; branch saat pemeriksaan berisi 89 anchor sampai line 360;\n- selesaikan dan audit Batch B sebelum merge 500 anchor;
- validasi source_original_line dan transformation_id;
- setelah anchor lolos QA, lanjutkan bridge/context/distractor secara bertahap.

## Tugas paralel tim
Prioritaskan pencarian Doc. 382, Doc. 427, Doc. 512, exhibit list, atau Exhibit 1A. Sumber domain perdagangan orang Indonesia dapat terus dikumpulkan untuk P2/P6.

## Pembagian tim
- Chris — Anggota A — Lead Forensik Digital
- Bela — Anggota B — Lead Kasus & Data
- Meldiro — Anggota C — Lead AI/RAG
- Daffa — Anggota D — Lead Validasi & Dokumentasi
