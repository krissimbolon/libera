# Monitoring ChatGPT Work — Corpus 10.000 Pesan

Mulai dipantau: 2026-09-23

Branch yang dipantau: `p2-10k-work`

## Baseline monitoring
- 500 anchor: **LOCKED**
- Target berikutnya: **2.000 pesan**
- File final yang diharapkan nanti: `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`
- Log checkpoint: `docs/02_case_design/log_progres_generasi_10000.md`

## Status saat pemeriksaan 2026-09-23 19:36 WIB
- Branch `p2-10k-work` masih pada checkpoint **500/10.000**.
- Belum ada `corpus_whatsapp_10000.csv` atau batch generasi baru yang committed.
- 500 anchor dan registri aktor tersedia di branch Work.
- Log progres masih menunjukkan checkpoint 2.000 sebagai BELUM.
- Tidak ada indikasi perubahan pada 500 anchor.

## Pemeriksaan on-track yang wajib
1. 500 anchor tidak berubah.
2. Checkpoint harus bergerak 500 → 2.000 → 4.000 → 6.000 → 8.000 → 10.000 → QA final.
3. Bahasa sintetis harus natural/tidak formal sesuai `kontrak_gaya_percakapan.md`.
4. Bridge/context/distractor tetap di semesta kasus adaptasi Galloway.
5. Tidak ada victim utama/tindak pidana/outcome baru.
6. Exact duplicate row final = 0.
7. Exact duplicate synthetic `message_text` = 0.
8. `source_original_line` hanya terisi untuk 500 anchor.
9. Tidak ada nama/lokasi sumber utama yang bocor kembali.
10. Jangan merge hasil generasi ke `main` sebelum QA final.

## Temuan Git yang perlu diawasi
PR #6 dari `p2-10k-work` sempat di-merge ke `main` pada 2026-09-23. PR tersebut hanya berisi tiga dokumen instruksi/log, bukan data corpus, sehingga belum merusak dataset. Namun mulai sekarang **jangan merge branch Work ke main**. Integrasi final hanya ke `proyek-uas-df` setelah QA.

## Status penilaian
**ON TRACK, tetapi belum ada progres generasi setelah 500 anchor pada pemeriksaan ini.**
