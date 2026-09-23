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


## Pemeriksaan langsung 2026-09-23 19:48 WIB

### Progres
- Branch Work head: `9013a89007fb69f847d289a5904965eee640fd74`.
- Corpus kerja: **572/10.000**.
- Komposisi: **500 anchor + 72 bridge + 0 context + 0 distractor**.
- Bridge baru tersebar pada 12 conversation.
- Checkpoint 2.000 belum tercapai.

### QA terukur
- duplicate `message_id`: 0
- duplicate teks sintetis: 0
- benturan timestamp dalam conversation: 0
- near-duplicate panjang kandidat: 0
- kebocoran identitas sumber pada pesan baru: 0
- anchor row exact match terhadap reference set: 500/500
- conversation campuran baru: 0

### Review kontinuitas dan gaya
Spot-check bridge menunjukkan percakapan sudah mengikuti pesan sebelum/sesudahnya dan menggunakan Bahasa Indonesia percakapan seperti “bentar”, “nggak”, “udah”, dan pesan pendek. Ada beberapa frasa yang masih sedikit formal (mis. “beri tahu”) dan perlu dijaga supaya batch berikutnya lebih konsisten memakai gaya WhatsApp natural seperti “kasih tahu” bila cocok dengan aktor.

### Isu yang belum memblokir generasi
1. Hash manifest anchor `63eeaac8…` berbeda dengan byte hash file anchor committed `12859745…`, tetapi QA membuktikan **500/500 row anchor tetap identik**. Jangan ubah isi anchor; rekonsiliasi hash dilakukan sebagai pekerjaan provenance sebelum QA final.
2. Empat conversation anchor baseline memiliki lebih dari satu pasangan aktor: `KONV-GAL-P22-C`, `KONV-GAL-R013`, `KONV-GAL-R080`, `KONV-GAL-R088`. Work sudah benar dengan tidak menambahkan bridge ke thread ini sebelum keputusan eksplisit.
3. `corpus_whatsapp_working.csv` tetap artefak kerja, bukan dataset final investigator.

### Penilaian
**ON TRACK.** Generasi nyata sudah dimulai dan guardrail QA bekerja. Prioritas selanjutnya adalah memperluas bridge secara bertahap menuju 1.500 sambil mempertahankan replay terhadap anchor, lalu mulai context/distractor setelah state aktor stabil.


## Pemeriksaan langsung 2026-09-23 21:17 WIB

### Progres Work
- Head `p2-10k-work`: `da66ca09a693e333954edac75b88301b901a58a2`.
- Checkpoint 2.000: **LULUS QA CHECKPOINT**.
- Checkpoint 4.000: **LULUS QA CHECKPOINT**.
- Komposisi 4.000: 500 anchor, 900 bridge, 2.100 context, 500 distractor.
- 353 conversation.
- QA struktural: 4.000/4.000 message_id unik, exact duplicate row 0, duplicate synthetic text 0, timestamp collision 0, near-duplicate panjang 0, source identity leakage 0, anchor exact-match 500/500.
- Checkpoint 6.000 tercatat **DALAM PROSES**, tetapi Work sedang berhenti karena limit sesi pengguna.

### Temuan gaya
Audit gaya pada commit `da66ca0` benar-benar menemukan ritme yang terlalu seragam:
- anchor ≤3 kata: 163/500 (32,6%);
- bridge ≤3 kata: 20/900 (2,2%);
- context ≤3 kata setelah koreksi: 89/2.100 (4,2%);
- distractor ≤3 kata setelah koreksi: 35/500 (7,0%).
- 107 conversation context masih tepat 10 pesan;
- 44 conversation distractor masih tepat 10 pesan.

Koreksi manual 47 baris sudah dilakukan tanpa mengubah jumlah pesan atau anchor. Ini memperbaiki arah, tetapi gaya **belum final-lulus**. Batch 4.000–10.000 harus sengaja meningkatkan fragmen pendek, double text, unanswered message, jeda, dan variasi panjang thread.

### Temuan Git penting
PR #11 (`p2-10k-work` → `main`) ternyata **telah di-merge** pada commit `f9423970...` ketika head Work masih `5480fdc...`. PR ini membawa 38 file termasuk `corpus_whatsapp_working.csv`, draft bridge/context/distractor, QA working, log, ledger, dan script. Ini melanggar aturan bahwa Work tidak boleh di-merge ke `main` sebelum final QA.

Status dataset kanonik tetap harus mengacu ke `p2-10k-work` untuk generasi dan `proyek-uas-df` untuk integrasi final. Jangan gunakan snapshot di `main` sebagai source of truth dan jangan merge Work lagi ke `main`.

### Penilaian
**ON TRACK secara substansi pada 4.000/10.000, dengan satu isu proses Git yang nyata dan satu isu kualitas gaya yang masih terbuka.** QA struktural sangat baik; continuity telah direview secara bertahap. Fokus saat Work dapat berjalan lagi adalah memperbaiki distribusi gaya sambil menuju checkpoint 6.000, bukan sekadar menambah volume.


## Pemeriksaan langsung 2026-09-23 21:58 WIB

### State terbaru GPT pengganti
- Head `p2-10k-work`: `c03ab96d337b3f97af1313afd1f657400e87bfd3`.
- Commit terbaru: `fix: repair +07:00 bridge timestamps before 6k QA`.
- Corpus: **4.650/10.000**.
- Komposisi: 500 anchor, 1.000 bridge, 2.530 context, 620 distractor.
- Conversation: 393.
- QA struktural: message_id unik 4.650/4.650, exact duplicate row 0, duplicate synthetic text 0, timestamp collision 0, near-duplicate panjang 0, source leakage 0, anchor exact-match 500/500.

### Perkembangan gaya
Dibanding checkpoint 4.000:
- bridge <=3 kata naik dari 20/900 menjadi 112/1.000;
- context <=3 kata naik dari 89/2.100 menjadi 425/2.530;
- distractor <=3 kata naik dari 35/500 menjadi 124/620;
- context thread tepat 10 pesan turun dari 107 menjadi 77.
Perbaikan arah gaya terlihat nyata. Distractor thread tepat 10 pesan masih 44, jadi variasi panjang distractor tetap perlu diperbaiki.

### Penilaian
**ON TRACK.** GPT pengganti telah melanjutkan dari state yang benar, menambah 650 pesan, mempertahankan QA struktural, memperbaiki distribusi gaya secara signifikan, dan sedang memperbaiki timestamp +07:00 sebelum QA checkpoint 6.000.
