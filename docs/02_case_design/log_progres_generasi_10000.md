# Log Progres Generasi 10.000 Pesan

Branch: `p2-10k-work`

| Checkpoint | Status | Pesan | Anchor | Bridge | Context | Distractor | Catatan |
|---|---|---:|---:|---:|---:|---:|---|
| Anchor locked | SELESAI | 500 | 500 | 0 | 0 | 0 | 500 anchor Indonesia telah QA dan dikunci |
| 2.000 | DALAM PROSES | 768 | 500 | 168 | 70 | 30 | Draf 002, context 001, distractor 001; belum mencapai checkpoint 2.000 |
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
