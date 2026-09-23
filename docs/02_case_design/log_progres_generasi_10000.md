# Log Progres Generasi 10.000 Pesan

Branch: `p2-10k-work`

| Checkpoint | Status | Pesan | Anchor | Bridge | Context | Distractor | Catatan |
|---|---|---:|---:|---:|---:|---:|---|
| Anchor locked | SELESAI | 500 | 500 | 0 | 0 | 0 | 500 anchor Indonesia telah QA dan dikunci |
| 2.000 | LULUS QA CHECKPOINT | 2.000 | 500 | 500 | 800 | 200 | Batch 005 +432 pesan; audit otomatis dan spot-check continuity selesai |
| 4.000 | LULUS QA CHECKPOINT | 4.000 | 500 | 900 | 2.100 | 500 | Batch 010 +400 pesan; QA checkpoint dan spot-check selesai |
| 6.000 | DALAM PROSES | 4.000 | 500 | 900 | 2.100 | 500 | Lanjut batch berikut tanpa menunggu konfirmasi |
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

## Batch 006 — 2.400/10.000 (menuju checkpoint 4.000)

- Tambahan 400 pesan: 80 bridge, 260 context, 60 distractor. Kumulatif 500/580/1.060/260 dan 225 conversation.
- Validator: ID ganda, duplikat baris/teks sintetis, tabrakan timestamp conversation, kandidat near-duplicate panjang, leakage sumber, dan mixed pair baru: 0. Anchor exact-match 500/500.
- Bridge pada percakapan Tania/Nara/Caca/Dini ditinjau berurutan dengan anchor. Detail jam tutup kantor Dini yang tidak didukung anchor dihapus; kalimat pembelian charger diselaraskan dengan posisi Raka yang belum berangkat.
- Context dipindah waktunya setelah ditemukan chat Rena yang bertumpuk dengan thread lain. Dialog sarapan Dini ditulis ulang karena proses memasak di kamar setelah pindah penginapan tidak terdukung. Distractor mempertahankan callback stiker ikan, kucing, dan payung tanpa outcome perkara baru.
- QA final dan hash manifest jangkar masih terbuka. Perlu 320 bridge, 1.040 context, 240 distractor lagi untuk checkpoint 4.000.

## Batch 007 — 2.800/10.000 (menuju checkpoint 4.000)

- Tambahan 400 pesan: 80 bridge, 260 context, 60 distractor. Kumulatif 500/660/1.320/320; 256 conversation.
- Validator: 0 ID/row/teks sintetis ganda, 0 collision timestamp conversation, 0 near-duplicate panjang, 0 leakage identitas sumber, 0 pasangan conversation baru bercampur. Anchor exact-match 500.
- Replay bridge R063, R065, R066, R068, R069, R071, R075, R090–R092: tidak mengarang hasil perjalanan bus Tania atau menyelesaikan tekanan pada Jihan. Konten minor tetap pada komunikasi keluarga dan waktu penjemputan.
- Reza dalam dua chat bersamaan serta Rena selama chat Nara dipisah waktunya. Dini pada 20 Juli digeser dari anchor Raka yang berdekatan. Context dan distractor menambah percakapan benda sehari-hari; ritme masih cenderung rapi dan perlu lebih banyak jeda/fragmen dalam batch selanjutnya.
- Ke checkpoint 4.000 masih perlu 240 bridge, 780 context, 180 distractor. QA final belum selesai; mismatch hash manifest jangkar tetap dilacak.

## Batch 008 — 3.200/10.000 (menuju checkpoint 4.000)

- Tambahan 400 pesan: 80 bridge, 260 context, 60 distractor. Kumulatif 500/740/1.580/380; 288 conversation.
- QA otomatis: 0 message ID ganda, duplikat baris, teks sintetis identik, collision timestamp conversation, kandidat near-duplicate panjang, leakage sumber, dan pasangan conversation baru bercampur; 500 anchor tetap exact-match.
- Saat review ditemukan tiga ID kontak yang keliru di draft R007/R009/R010; diperbaiki sebelum merge. Dua dialog Nara yang terformat sebagai Rena juga diperbaiki. Chat Caca dan Reza yang terlalu dekat dengan anchor lain digeser.
- Bridge baru pada R006/R007/R009–R012, R024, R041, R062, R113 menjawab anchor tanpa memaksakan outcome. Beberapa penutup rapi di context dipotong dan diganti pesan lanjutan agar ritme tidak seragam.
- Ke checkpoint 4.000 perlu 160 bridge, 520 context, dan 120 distractor lagi. Mismatch manifest SHA tetap terbuka.

## Batch 009 — 3.600/10.000 (menuju checkpoint 4.000)

- Tambahan 400 pesan: 80 bridge, 260 context, 60 distractor. Kumulatif 500/820/1.840/440; 320 conversation.
- QA otomatis: 0 ID/row/teks sintetis duplikat, 0 collision timestamp conversation, 0 kandidat near-duplicate panjang, 0 leakage sumber; 500 anchor exact-match.
- Satu teks identik pada bridge R062/P34-YY tertangkap validator lalu diubah. Review lintas chat menemukan Dini pada dua conversation di menit sama, serta Raka berbalas dalam percakapan netral saat anchor lain sedang aktif; empat thread netral digeser.
- Bridge R001/R002 menandai informasi tentang Maya sebagai belum pasti; tidak menambah penemuan atau hasil pencarian. Bridge R100 tentang Jihan tetap terkait komunikasi keluarga dan telepon, tanpa memperinci rokok atau aktivitas terlarang.
- Ke checkpoint 4.000 tinggal 80 bridge, 260 context, dan 60 distractor. Audit final 10.000 masih tertunda.

## Checkpoint 4.000 — Batch 010

- Tambahan 400 pesan: 80 bridge, 260 context, 60 distractor. Kumulatif tepat 500/900/2.100/500; 353 conversation.
- `message_id` unik 4.000/4.000; exact duplicate row 0; exact duplicate teks sintetis 0; tabrakan timestamp per conversation 0; kandidat near-duplicate panjang 0; kebocoran identitas sumber 0; seluruh 500 anchor exact-match. Empat conversation pasangan campur yang ada pada anchor baseline tidak diisi.
- Replay bridge R048–R051, R058/R060/R061, R070, R093, R095: R050 menyambung keluarnya orang yang sebelumnya disebut belum selesai, tanpa mengubah janji berikutnya; R093 tetap berada pada percakapan penjemputan Jihan dari rumah ibu tanpa mengklaim perpindahan terjadi.
- Audit lintas thread menemukan context Rena seolah sudah tidur/mute HP tepat sebelum anchor memintanya siap-siap; dipindah ke dini hari. Lima pasang pesan Dini yang terjadi hampir bersamaan di dua conversation dipisahkan waktunya. Balasan Raka tentang pintu lemari tidak lagi menempel pada chat Bagas. Tidak ditemukan konflik kronologi/state baru pada potongan yang ditinjau setelah koreksi. Audit semantik menyeluruh 4.000 baris belum setara dengan QA final 10.000.
- Hash pada manifest anchor lama (`63ee…`) tetap berbeda dari bytes anchor di branch (`1285…`), sementara baris anchor pada corpus sama persis. Perlu rekonsiliasi provenance sebelum final. Lanjut ke batch 6.000: butuh 300 bridge, 1.300 context, 400 distractor sampai checkpoint berikutnya.

## Audit gaya setelah checkpoint 4.000

- Profil awal mengungkap kelemahan: dari 2.100 context hanya 61 pesan (2,9%) berisi paling banyak tiga kata, sedangkan anchor 163/500 (32,6%); 107 dari 202 conversation context berukuran tepat 10 pesan dan 44 dari 50 distractor juga tepat 10. Ini ritme terlalu seragam untuk WhatsApp. Status checkpoint di atas berarti QA **struktur** lulus, bukan gaya final.
- 47 baris pada draf context/distractor ditinjau dan disingkat secara manual, sambil memastikan balasan sebelum/sesudah tetap masuk akal. Setelah koreksi, context pendek 89/2.100 dan distractor pendek 35/500; masih jauh dari ritme anchor. Profil gaya kuantitatif kini ditulis ke JSON QA kerja untuk pemantauan batch berikutnya.
- Batch baru harus berisi lebih banyak sapaan singkat, pesan ganda, jeda, respons yang tak dibalas, dan panjang thread beragam. Jangan mengubah 500 anchor atau mengisi target dengan pemotongan otomatis. Audit gaya final 10.000 tetap wajib.

## Batch 011 — continuity/style expansion ke 4.650

- Ditambahkan 650 pesan: +100 bridge, +430 context, +120 distractor.
- Kumulatif: **4.650** = 500 anchor + 1.000 bridge + 2.530 context + 620 distractor; 393 conversation.
- Structural QA: ID unik 4.650/4.650; exact duplicate row 0; duplicate synthetic text 0; timestamp collision 0; near-duplicate panjang 0; source leakage 0; anchor exact-match 500/500.
- Style correction dilakukan secara organik: 30 context conversation yang sebelumnya 10 pesan dilanjutkan, bukan dipotong; batch memuat pesan pendek, double-text, jeda, typo/singkatan ringan, dan beberapa thread tanpa penutupan eksplisit.
- Spot-check bridge: R029–R071 yang dipilih direplay dengan anchor terdekat; empat mixed baseline conversation tetap tidak disentuh.
- Hash manifest anchor lama tetap dicatat sebagai provenance discrepancy, tanpa perubahan anchor.
