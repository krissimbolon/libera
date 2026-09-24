# Log Progres Generasi 10.000 Pesan

Branch: `p2-10k-work`

| Checkpoint | Status | Pesan | Anchor | Bridge | Context | Distractor | Catatan |
|---|---|---:|---:|---:|---:|---:|---|
| Anchor locked | SELESAI | 500 | 500 | 0 | 0 | 0 | 500 anchor Indonesia telah QA dan dikunci |
| 2.000 | LULUS QA CHECKPOINT | 2.000 | 500 | 500 | 800 | 200 | Batch 005 +432 pesan; audit otomatis dan spot-check continuity selesai |
| 4.000 | LULUS QA CHECKPOINT | 4.000 | 500 | 900 | 2.100 | 500 | Batch 010 +400 pesan; QA checkpoint dan spot-check selesai |
| 6.000 | DALAM PROSES | 4.000 | 500 | 900 | 2.100 | 500 | Lanjut batch berikut tanpa menunggu konfirmasi |
| 8.000 | LULUS QA CHECKPOINT | 8.000 | 500 | 1.400 | 4.900 | 1.200 | Batches 015–017; structural/style checkpoint lulus |
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

## Checkpoint 6.000 — Batch 013

- Kumulatif tepat **6.000**: 500 anchor, 1.200 bridge, 3.400 context, 900 distractor; 492 conversation.
- QA struktural: message_id unik 6.000/6.000; exact duplicate row 0; duplicate synthetic text 0; timestamp collision dalam conversation 0; near-duplicate panjang 0; source identity leakage 0; anchor exact-match 500/500; timestamp di luar 1–21 Juli 0.
- Koreksi sebelum lulus: bug timezone pada bridge Batch 012–013 terdeteksi karena midpoint sempat bergeser ke 30 Juni; 200 bridge direlokasi ke gap lokal +07:00 dalam conversation GAL masing-masing, tanpa menyentuh anchor.
- Continuity/actor-state spot-check: tambahan context/distractor tetap dyadic dengan Raka, tidak menambah outcome utama atau lokasi spesifik baru; Caca tidak diperpanjang setelah baseline blokir 19 Juli; Jihan tetap netral dan tersanitasi.
- Profil gaya: <=3 kata — anchor 163/500, bridge 180/1.200, context 874/3.400, distractor 339/900. Distribusi pesan pendek membaik nyata dibanding 4k. Masalah tersisa: 80 context conversation dan 59 distractor conversation masih tepat 10 pesan; batch menuju 8k harus terutama memperpanjang thread ini secara organik dan menghindari thread baru berukuran seragam.
- Discrepancy hash manifest anchor tetap isu provenance saja; 500 anchor tidak diubah.

## Revert kualitas setelah Batch 011

- Commit `78891ad939925247fca0b8046b6f7e8d9e78b747` menghapus delta corpus Batch 012–013 yang dinilai terlalu mekanis. Source of truth kembali ke **4.650** pesan: 500 anchor, 1.000 bridge, 2.530 context, 620 distractor.
- Klaim checkpoint 6.000 yang sempat ditulis sebelum revert tidak lagi berlaku terhadap corpus kerja dan dinyatakan superseded.
- Generasi berikutnya wajib dimulai dari Batch 011, mempertahankan perbaikan gaya melalui thread yang benar-benar beragam, callback organik, dan panjang percakapan tidak seragam.

## Checkpoint 6.000 — regenerated Batches 012–014

- Setelah delta mekanis lama direvert, corpus dibangun ulang dari 4.650 melalui commit `5e3af8d`, `835f14e`, dan `33e9430` hingga tepat **6.000** pesan.
- Komposisi: 500 anchor, 1.200 bridge, 3.400 context, 900 distractor; 497 conversation.
- QA: 6.000 message_id unik; exact duplicate row 0; duplicate synthetic text 0; timestamp collision 0; near-duplicate panjang 0; source leakage 0; timestamp di luar skenario 0; anchor exact-match 500/500; mixed conversation baru 0.
- Namespace diperbaiki sesuai kontrak: CTX-A berakhir tepat di 3.250 dan context berikutnya dimulai CTX-B (saat checkpoint: CTX-B-0150).
- Profil gaya: <=3 kata — bridge 225/1.200, context 862/3.400, distractor 261/900. Conversation tepat 10 pesan turun menjadi context 3 dan distractor 0, dari 77/44 pada state 4.650.
- Perbaikan dilakukan melalui callback organik pada thread lama, variasi panjang 5–17 pesan, fragmen/double-text, dan thread baru yang tidak semuanya ditutup rapi; bukan pemotongan otomatis massal.

## Checkpoint 8.000 — Batches 015–017

- Tepat **8.000** pesan: 500 anchor, 1.400 bridge, 4.900 context, 1.200 distractor; 668 conversation.
- QA: message_id unik 8.000/8.000; exact duplicate row 0; duplicate synthetic text 0; collision timestamp 0; near-duplicate panjang 0; source leakage 0; timestamp di luar skenario 0; anchor exact-match 500/500; mixed conversation baru 0.
- Profil gaya <=3 kata: bridge 354/1.400, context 1.441/4.900, distractor 427/1.200. Thread tepat 10 pesan: context 0, distractor 1.
- Namespace context: CTX-A tetap terkunci di 3.250; CTX-B mencapai 1.650. Tidak ada modifikasi anchor.

## Audit snapshot 10.000 baris — QA final gagal

- Branch mencapai hitungan 10.000 dan komposisi target, tetapi audit pada snapshot `0ab74a3` menemukan 188 jendela empat pesan beruntun yang mengulang dua kata akhir identik di 66 conversation; ada 890 context B berakhir pola koma/frasa/`ya`.
- QA kerja 8.000 yang sebelumnya tersimpan sudah tidak sesuai jumlah saat ini. Auditor baru menghasilkan status `FAILED_LANGUAGE_CONTINUITY_QA` dan laporan `audit_kualitas_10000_belum_lulus.md`.
- **Progres konten terverifikasi tetap 4.000/10.000**, sedangkan 10.000 adalah jumlah baris yang memerlukan revisi isi. Final artifact dan QA final belum boleh diterbitkan sampai dialog repetitif diperbaiki dan audit actor-state menyeluruh lulus. Anchor 500/500 tetap identik.
- Koreksi manual putaran pertama menulis ulang 80 pesan pada lima thread utuh tanpa mengubah ID/waktu/anchor; indikator pengulangan turun dari 188 jendela di 66 conversation menjadi 152 jendela di 61 conversation. QA final masih gagal.
- Empat timestamp `24:xx` di thread Kirana dikoreksi ke dini hari 20 Juli; auditor kini memeriksa parse timestamp dan menghitung 731 jeda context yang tepat 247 detik. Ritme ini tetap menjadi alasan QA gaya belum lulus.
- Koreksi manual kedua: 131 pesan pada sepuluh thread ditulis ulang, total revisi manual 211 pesan. Jendela pengulangan tersisa 93 pada 51 conversation; validasi teks sintetis identik tetap 0. QA final masih gagal dan perbaikan dilanjutkan.
- Koreksi manual ketiga: 67 pesan pada lima thread ditulis ulang; total 278 pesan. Indikator tersisa 73 jendela pada 46 conversation. QA final tetap gagal, termasuk audit ritme waktu.
- Checkpoint koreksi 400 pesan: putaran keempat menambah 122 pesan pada sepuluh thread; total 400 pesan/30 thread diperbaiki. Pola akhir berulang kini 46 jendela pada 36 conversation; cadence 247 detik 731 kejadian. Hitungan corpus tetap 10.000, tetapi QA final belum lulus.
- Koreksi kelima: 127 pesan di sepuluh thread, total revisi 527 pesan. Pola empat akhiran identik masih 26 jendela/26 thread; cadence dan review semantik penuh belum selesai. QA final tetap gagal.
- Koreksi keenam dan ketujuh: 288 pesan tambahan, total revisi manual 815 pesan di 66 thread. Detektor empat akhiran identik kini 0, namun context B masih 484 pola koma/frasa/`ya` dan 731 jeda 247 detik. Corpus tetap 10.000/10.000 secara jumlah; status QA final `FAILED_LANGUAGE_CONTINUITY_QA`, belum ada artefak final.

## Lanjutan setelah pemulihan state 815

- State lokal 815 ditemukan di commit `8a337c2`; enam commit sebelumnya memiliki tree sama persis dengan remote `1f453f9` meskipun hash commit berbeda. Perubahan terakhir dipasang sebagai fast-forward di atas remote dan diverifikasi pada commit GitHub `59d8297`. Tidak ada regenerasi corpus atau perubahan anchor saat recovery.
- Koreksi kedelapan dan kesembilan menulis ulang 142 pesan lagi pada sepuluh thread netral sebagai dialog berurutan (`koreksi_dialog_manual_008.tsv` dan `_009.tsv`). Total kumulatif **957 pesan di 76 thread**. Context B berpola koma/frasa/`ya` turun dari 484 ke **428**; 731 jeda 247 detik belum disentuh. Detektor empat akhiran tetap 0, 10.000 ID unik, 500 anchor exact. QA final masih **FAILED_LANGUAGE_CONTINUITY_QA**; isi dan ritme thread lain belum dinyatakan lulus.
- Koreksi kesepuluh menulis ulang 69 pesan pada lima thread (`TANIA-B19-004`, `REZA-B19-010`, `BAGAS-B20-019`, `JIHAN-B20-007`, `NARA-B16-026`). Kumulatif **1.026 pesan di 81 thread**; pola context B tersisa **403**, cadence 247 detik tetap 731, duplikat teks sintetis 0, anchor 500/500. QA tetap **FAILED_LANGUAGE_CONTINUITY_QA**.
- Koreksi kesebelas dan kedua belas menulis ulang **160 pesan pada 12 thread** tentang selimut, pakaian, makanan, alarm, barang lembap, dan kebutuhan harian (`koreksi_dialog_manual_011.tsv` serta `_012.tsv`). Kumulatif **1.186 pesan pada 93 thread**; pola context B tersisa **349**, cadence 247 detik tetap **731**, duplikat teks sintetis dan detektor empat akhiran tetap 0, anchor 500/500. Thread lain yang belum ditinjau, kronologi lintas aktor, dan ritme waktu masih menghalangi signoff QA.

## QA convergence setelah auditor independen `1ea95c1`

- Baseline sebelum edit: `python src/audit_repetisi_corpus.py` dan `python src/audit_final_corpus.py` dijalankan dari remote terbaru; pemeriksaan struktur lulus, tetapi QA semantik gagal. Context B memiliki 349 akhiran berpola koma/frasa/`ya` dalam 169 conversation; 2.818/2.954 adjacent gap (95,40%) mempunyai `seconds % 60 == 7`, sedangkan Context A 75/2.957 (2,54%). Spike 127/187/247/307/367 detik menunjukkan fingerprint generator yang lebih luas dari satu gap 247. Kandidat near-duplicate panjang dari auditor: 1 pasangan, belum ditinjau manual.
- Koreksi ke-13 dan ke-14 menulis ulang **219 pesan pada 16 thread** sebagai dialog lengkap; TSV memetakan ID ke teks. Akumulasi **1.405 revisi manual pada 109 thread**. Akhiran Context B tersisa **285**. Dua exact duplicate teks yang muncul saat repair diperbaiki sebelum checkpoint; pemeriksaan struktur auditor kembali lulus dengan 10.000 pesan, 500 anchor exact, provenance 500/1.500/6.500/1.500, duplikat teks sintetis 0, reply dan timestamp valid. Cadence `60n + 7` masih **2.818/2.954** dan belum disentuh. Status final tetap gagal; tidak ada artefak final.
- Koreksi ke-15 dan ke-16 menulis ulang **188 pesan pada 16 thread** (`koreksi_dialog_manual_015.tsv` dan `_016.tsv`), sehingga akumulasi **1.593 pesan pada 125 thread**. Akhiran Context B tersisa **238**, dua duplikat baru diperbaiki sebelum audit, dan pemeriksaan struktur kembali lulus. Seluruh 2.818 gap Context B dengan remainder 7 detik belum diubah; gate semantik tetap gagal.
- Koreksi ke-17 dan ke-18 menulis ulang **172 pesan pada 16 thread** (`_017.tsv`, `_018.tsv`), total **1.765 pesan pada 141 thread**. Pola akhiran Context B tersisa **190**, satu duplikat baru diperbaiki; pemeriksaan struktur kedua auditor lulus. Cadence generator tetap 2.818/2.954 gap `60n + 7` dan QA akhir tetap gagal.

## Review QA lanjutan dari remote `47dac82`

- Baseline kedua auditor sebelum edit: 10.000 pesan, provenance 500/1.500/6.500/1.500, anchor 500/500, duplikat sintetis 0, suffix empat pesan 0, Context B **190** kandidat koma/frasa/`ya` dalam 122 conversation dan **74** akhiran `barusan` dalam 38 conversation. Cadence Context B **2.818/2.954** gap `60n + 7`, termasuk 731 gap 247 detik. Pemeriksaan struktur lulus; sign-off manual belum.
- Review manual thread `NARA-B20-047` dan `TANIA-B20-015` mempertahankan dua pesan `ya` yang memang mengingatkan soal tutup toples dan penyimpanan gula. Perbaikan `_019.tsv` menulis ulang **36 pesan context pada tiga thread** (`TANIA-B14-012`, `MAYA-B16-001`, `BAGAS-B20-001`) dan empat pesan bridge pada dua pasangan near-duplicate. Akumulasi revisi unik **1.805 pesan pada 148 thread**. Setelah audit: pola koma/frasa/`ya` **186**, `barusan` ending **57**, near-duplicate panjang yang terdeteksi auditor 0, struktur tetap lulus. Ini hanya review parsial: **184 kandidat pola bahasa dan 57 kandidat `barusan` belum diputuskan lewat pembacaan thread penuh**. Cadence belum diubah.
- Audit provenance baca-saja `python src/audit_anchor_provenance.py`: 500 baris bagian dan file gabungan identik dalam urutan yang sama. Hash current anchor `12859745a88aecca306b9f149661361ec2b8da8cd1f7c41c70ead1329b3e5e50`; historis `63eeaac83bfd3b9145bbc1d99f3b7bfcce447face3f9cf7e20aa5231d55b0d24` tidak cocok pada varian sederhana yang diuji. Hanya hash `bagian_01.csv` terbukti cocok setelah CRLF; bagian 02–05 belum. Perbedaan byte historis tetap terbuka, tidak digunakan untuk mengubah anchor.

## QA convergence berikutnya — dialog dan waktu sintetis

- `_020.tsv` menulis ulang 41 pesan dalam tiga percakapan lengkap (`REZA-B15-027` kartu kamar, `RENA-B16-006` pulpen, `MAYA-B19-016` sepatu). Kumulatif revisi teks unik menjadi **1.846 pesan pada 151 conversation**. Pola koma/frasa/`ya` Context B kini **182** dan akhiran `barusan` **48**. Dari 190 kandidat awal pada putaran ini, **8 diperbaiki**, **2 dipertahankan** setelah membaca thread lengkap, dan **180 belum direview sampai tuntas**. Dari 74 `barusan` awal, 26 hilang lewat perbaikan percakapan; 48 tersisa untuk review. Tidak ada replacement massal.
- `koreksi_waktu_manual_001.tsv` mencatat 71 perubahan timestamp yang dipilih menurut langkah percakapan pada enam thread utuh (nota, sarung bantal, termos, kartu kamar, pulpen, sepatu). Ini **QA pada skenario sintetis**, bukan perubahan acquired forensic evidence. Setiap baris menyimpan waktu lama, waktu baru, dan alasan. Tidak ada timestamp anchor berubah ataupun anchor per aktor yang dilewati; urutan, reply, timezone, jendela skenario, dan collision diuji ulang. Context B `seconds % 60 == 7` turun dari **2.818/2.954 (95,40%)** menjadi **2.759/2.954 (93,40%)**; gap tepat 247 detik dari 731 ke **718**. Fingerprint generator masih dominan dan audit lintas aktor penuh belum lulus. QA final tetap `FAILED_LANGUAGE_CONTINUITY_QA`.
