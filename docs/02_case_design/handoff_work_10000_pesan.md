# Handoff ke ChatGPT Work — Produksi Corpus 10.000 Pesan LIBERA

Branch kerja: `p2-10k-work`

## Misi

Bangun **satu corpus final berisi tepat 10.000 pesan WhatsApp sintetis Indonesia** yang konsisten dengan adaptasi kasus Galloway.

Kerjakan seluruh pekerjaan ini menggunakan **satu GPT/Work session** agar state percakapan, gaya bahasa, kronologi, dan relasi antaraktor tetap konsisten.

## Sumber yang wajib dibaca terlebih dahulu

1. `data/adaptasi_indonesia/anchor_indonesia_500.csv`
2. `data/adaptasi_indonesia/registri_aktor_indonesia.csv`
3. `docs/02_case_design/desain_dataset_10000_pesan_indonesia.md`
4. `docs/02_case_design/peta_lokalisasi_kasus_indonesia.md`
5. `docs/02_case_design/kontrak_ekspansi_9500_pesan.md`
6. `docs/02_case_design/peta_kronologi_generasi.md`
7. `docs/02_case_design/kontrak_gaya_percakapan.md`
8. `docs/02_case_design/qa_integrasi_500_jangkar.md`

Untuk memahami pola komunikasi sumber, gunakan Document 547 yang tersedia pada workspace privat/user-provided source. Jangan memasukkan court narrative ke dataset investigator dan jangan menyalin ulang teks sumber sebagai synthetic filler.

## Komposisi final

- 500 `ADAPTED_FROM_GALLOWAY` — sudah ada dan immutable.
- 1.500 `SYNTHETIC_BRIDGE`.
- 6.500 `SYNTHETIC_CONTEXT`.
- 1.500 `SYNTHETIC_DISTRACTOR`.

Total: **10.000**.

## Cara kerja wajib

Jangan membuat 9.500 baris secara independen.

Gunakan proses berurutan:
1. baca semua 500 anchor;
2. bentuk state per conversation_id dan per aktor;
3. petakan gap waktu/kejadian antar-anchor;
4. buat bridge untuk menjaga kesinambungan;
5. tambahkan context dan distractor di sekitar state yang sudah ada;
6. setelah setiap 500–1.000 pesan, audit kronologi dan state;
7. lakukan audit penuh setelah mencapai 10.000.

## Bahasa

Bahasa Indonesia percakapan, natural, tidak formal, tidak seperti chatbot.

Gunakan variasi natural seperti:
`nggak`, `udah`, `iya`, `oke`, `bentar`, `gimana`, `di mana`, `otw`, `ntar` bila cocok dengan aktor.

Jangan memaksa semua aktor punya gaya slang yang sama.

## Output

Buat:
- `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`
- `data/adaptasi_indonesia/qa_corpus_10000.json`
- `docs/02_case_design/laporan_qa_corpus_10000.md`
- `docs/02_case_design/log_progres_generasi_10000.md`

## QA minimum

Final harus memenuhi:
- jumlah = 10.000;
- message_id unik = 10.000;
- exact duplicate row = 0;
- synthetic message_text exact duplicate = 0;
- 500 anchor tetap identik terhadap reference set;
- tidak ada unresolved source line yang diubah menjadi anchor;
- provenance valid;
- tidak ada kebocoran nama/lokasi sumber utama;
- chronological consistency;
- actor-state consistency;
- no illegal merge to `main`.

## Tracking progres

Update `log_progres_generasi_10000.md` pada checkpoint:
- 500/10.000 — anchor locked
- 2.000/10.000
- 4.000/10.000
- 6.000/10.000
- 8.000/10.000
- 10.000/10.000
- QA final

Setiap checkpoint catat:
- jumlah pesan;
- komposisi provenance;
- duplicate count;
- conversation count;
- masalah continuity yang ditemukan;
- koreksi yang dilakukan.

## Git

Commit hanya ke `p2-10k-work`.

Jangan merge ke `main` atau `proyek-uas-df` sampai QA final selesai dan hasil ditinjau.
