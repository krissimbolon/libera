# Log Progres Generasi 10.000 Pesan

Branch: `p2-10k-work`

| Checkpoint | Status | Pesan | Anchor | Bridge | Context | Distractor | Catatan |
|---|---|---:|---:|---:|---:|---:|---|
| Anchor locked | SELESAI | 500 | 500 | 0 | 0 | 0 | 500 anchor Indonesia telah QA dan dikunci |
| 2.000 | LULUS QA CHECKPOINT | 2.000 | 500 | 500 | 800 | 200 | Batch 005 +432 pesan; audit otomatis dan spot-check continuity selesai |
| 4.000 | BELUM | 500 | 500 | 0 | 0 | 0 | |
| 6.000 | BELUM | 500 | 500 | 0 | 0 | 0 | |
| 8.000 | BELUM | 500 | 500 | 0 | 0 | 0 | |
| 10.000 | BELUM | 500 | 500 | 0 | 0 | 0 | |
| QA final | BELUM | 500 | 500 | 0 | 0 | 0 | |

## Target akhir
- Anchor: 500
- Bridge: 1.500
- Context: 6.500
- Distractor: 1.500
- Total: 10.000

## Aturan update checkpoint
Pada setiap checkpoint catat:
- exact duplicate row;
- exact duplicate synthetic message_text;
- jumlah conversation;
- konflik kronologi;
- konflik state aktor;
- kebocoran provenance/identitas sumber;
- koreksi yang dilakukan.

## Draf 001 — 572/10.000 (belum checkpoint)

- Komposisi: 500 anchor, 72 bridge, 0 context, 0 distractor; 101 conversation.
- `message_id` ganda: 0; duplikat teks sintetis: 0; duplikat baris dan tabrakan waktu per conversation: 0; kandidat near-duplicate panjang: 0.
- Seluruh 500 baris anchor pada corpus kerja sama persis dengan file jangkar yang ada di branch; seluruh source line anchor berstatus terpetakan, tidak ada yang unresolved.
- Draf bridge diputar ulang menurut timestamp bersama jangkar pada 12 conversation. Koreksi saat review: buang pengulangan pertanyaan identitas sebelum jawaban anchor Kirana, buang balasan yang menyela jawaban sensitif Kirana, dan ubah pesan perjalanan yang mendahului izin dari anchor.
- Empat conversation jangkar (`KONV-GAL-P22-C`, `KONV-GAL-R013`, `KONV-GAL-R080`, `KONV-GAL-R088`) sudah berisi lebih dari satu pasangan aktor. Ini anomali baseline yang tidak diubah; draf tidak menambah pesan di keempatnya.
- Hash di `jangkar_500/manifest.json` dan `qa_integrasi_500_jangkar.md` (`63eeaac8…`) tidak cocok dengan hash byte file jangkar yang ter-commit di branch (`12859745…`). File jangkar tidak disentuh. Rekonsiliasi provenance perlu dilakukan sebelum QA final.
- Audit state aktor lintas semua conversation, kesinambungan 9.428 pesan yang belum ditulis, serta QA final masih tertunda. Jangan gunakan `corpus_whatsapp_working.csv` sebagai corpus final investigator.

## Draf 002 — 768/10.000 (belum checkpoint)

- Komposisi: 500 anchor, 168 bridge, 70 context, 30 distractor; 111 conversation. Bertambah 196 pesan dari draf 001.
- ID ganda, teks sintetis identik, tabrakan timestamp dalam conversation, kandidat near-duplicate panjang, dan kebocoran nama sumber pada pesan baru: semuanya 0.
- Bridge ditambah pada fase 2 sampai 5. Review berurutan membuang pesan yang mendahului instruksi turun, menjawab pertanyaan sebelum anchor, atau mengulangi pertanyaan Nara/Jihan. 70 context berupa tujuh dialog netral berlanjut; 30 distractor berupa tiga dialog sosial dengan aktor existing. Semua thread baru melibatkan Raka, sesuai batas telepon akuisisi.
- Ledger lintas percakapan dibuat pada `ledger_kontinuitas_aktor_10k.md`; empat conversation campuran dari anchor tetap dihindari. Hash manifest yang berbeda dari file jangkar masih terbuka.
- Audit semantik manual terhadap seluruh 768 pesan, jumlah target, dan QA final **belum selesai**. Berkas `corpus_whatsapp_working.csv` tetap draf.

## Batch 003 — 1.171/10.000 (belum checkpoint)

- Bertambah 403 pesan: 75 bridge, 238 context, 90 distractor. Kumulatif 500/243/308/120, 142 conversation.
- ID ganda, exact duplicate row, teks sintetis identik, benturan timestamp dalam conversation, kandidat near-duplicate panjang, dan kebocoran identitas sumber pada pesan baru: 0.
- Review bridge bersama anchor membuang tujuh baris yang mendahului jawaban, mengulang penutup, atau menciptakan posisi tidak konsisten. Lima penutup context yang terlalu seragam dihapus untuk memperbaiki ritme. Distractor membuat callback sosial pada stiker, kucing, dan percakapan kecil sebelumnya; tidak menambah event utama.
- Anchor 500/500 exact-match. Empat conversation anchor yang bercampur pasangan tetap dihindari. Hash manifest jangkar masih berbeda dari file ter-commit dan tetap dicatat tanpa mengubah anchor.
- Target checkpoint 2.000 belum tercapai; batch berikutnya perlu menjaga variasi bentuk dialog dan memperbanyak context yang berhubungan dengan state, bukan hanya masalah benda kecil.

## Batch 004 — 1.568/10.000 (belum checkpoint)

- Bertambah 397 pesan: 69 bridge, 258 context, 70 distractor. Kumulatif 500/312/566/190, 169 conversation.
- ID ganda, exact duplicate row, teks sintetis identik, tabrakan timestamp conversation, near-duplicate panjang, dan kebocoran identitas sumber pada tambahan: 0. Jangkar 500/500 exact-match.
- Review menghapus lima bridge yang membingungkan urutan pertanyaan akun, menggandakan permintaan daftar belanja, atau tidak menyambung setelah peringatan. Context menambah percakapan Kirana saat kondisi badan mulai kurang nyaman dan dialog Tania yang masih menyisakan soal kepulangan; tidak menutup konflik anchor. Distractor sosial tetap pada aktor yang telah dikenal.
- Komposisi menuju checkpoint 2.000 masih memerlukan 188 bridge, 234 context, dan 10 distractor. Audit state penuh dan mismatch hash manifest tetap terbuka.

## Checkpoint 2.000 — Batch 005

- Tambahan 432 pesan: 188 bridge, 234 context, 10 distractor. Kumulatif tepat 500/500/800/200; 194 conversation.
- ID ganda, exact duplicate row, teks sintetis identik, benturan timestamp dalam conversation, near-duplicate panjang, kebocoran identitas sumber pada tambahan, dan conversation pasangan baru bercampur: semuanya 0. Seluruh 500 anchor cocok persis dengan file anchor pada branch.
- Spot-check bridge diputar dengan anchor pada 25 conversation yang baru diisi; koreksi pada urutan menunggu penjemputan Rena, jawaban setelah instruksi turun, pengulangan alarm, serta level baterai Kirana. Kandidat near-duplicate tentang menyiram tanaman direvisi. Context Reza dan Rena yang bertabrakan menit pada dua chat dipisahkan waktunya.
- Hash manifest lama (`63eeaac8…`) masih tidak sama dengan file anchor ter-commit (`12859745…`); belum direkonsiliasi dan tidak diubah. Audit actor-state atas corpus final 10.000 belum selesai; checkpoint ini hanya QA draf 2.000. Lanjut batch berikut tanpa menjadikan berkas kerja sebagai output final.
