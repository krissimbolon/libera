# Model Chat Forensik dan Audit Koherensi Global — Snapshot 23938ea

Snapshot corpus yang diperiksa:
`p2-10k-work@23938ea2c18917735860c76f1fcde6fd08e2b6b2`

Dokumen ini memperluas QA dari level `conversation_id` ke level chat WhatsApp per pasangan kontak.

## Kesimpulan arsitektur

Corpus paling konsisten dimodelkan sebagai **satu acquisition perangkat/akun WhatsApp Raka** yang memuat banyak chat personal, bukan satu group chat besar.

Bukti struktur snapshot:
- total 10.000 pesan;
- rentang 1 Juli 2026 06:11:11 sampai 21 Juli 2026 23:57:45 (+07:00);
- 9.997/10.000 pesan melibatkan `AKT-RAKA`;
- 26 pasangan partisipan unik;
- 25 pasangan melibatkan Raka;
- seluruh 25 pasangan Raka memiliki minimal satu anchor `ADAPTED_FROM_GALLOWAY`;
- tidak ada pasangan Raka yang hanya muncul karena synthetic expansion;
- 842/846 `conversation_id` adalah dyadic;
- empat segment multi-participant seluruhnya berasal dari anchor immutable: `KONV-GAL-P22-C`, `KONV-GAL-R013`, `KONV-GAL-R080`, `KONV-GAL-R088`;
- tiga pesan yang tidak melibatkan Raka seluruhnya merupakan anchor Galloway (Rena ke kontak tidak diketahui).

Dengan demikian synthetic expansion tidak menciptakan jejaring sosial baru di luar relasi yang sudah didukung anchor.

## Conversation ID bukan WhatsApp chat ID

Snapshot memiliki 846 `conversation_id`, tetapi hanya 26 participant pairs.

Contoh:
- Raka–Dini: 134 segment, 1.457 pesan;
- Raka–Reza: 121 segment, 1.297 pesan;
- Raka–Rena: 101 segment, 1.417 pesan;
- Raka–Bagas: 87 segment;
- Raka–Tania: 84 segment.

Karena WhatsApp personal chat secara konseptual adalah satu thread per peer/account, `conversation_id` pada corpus harus diperlakukan sebagai **scenario/event segment ID**, bukan physical WhatsApp chat identity.

Untuk P3/P4/demo:
- derive satu `chat_id` stabil per participant pair;
- pertahankan `conversation_id` sebagai `segment_id` / `source_thread_id`;
- jangan mengubah 500 anchor hanya untuk merapikan ID;
- merged view per `chat_id` harus menjadi dasar human continuity review.

## Integrasi bridge dengan anchor Galloway

Seluruh 1.500 `SYNTHETIC_BRIDGE` berada dalam segment yang memiliki anchor.

Jarak waktu bridge ke anchor terdekat pada segment yang sama:
- median 372 detik;
- p75 1.048 detik;
- p90 1.603 detik;
- p95 2.202 detik;
- maksimum 3.393 detik;
- 683/1.500 berada <=5 menit dari anchor;
- 1.388/1.500 <=30 menit;
- 1.500/1.500 <=1 jam.

Ini mendukung fungsi bridge sebagai penghubung anchor, bukan chat independen yang ditempel jauh dari skenario.

## Rentang waktu dan volume

Corpus bukan satu minggu. Rentang aktual sekitar tiga minggu: 1–21 Juli 2026.

Volume harian berkisar sekitar 217–777 pesan. Ini dapat masuk akal untuk satu akun yang aktif di banyak chat, tetapi harus dinilai bersama state Raka agar tidak menghasilkan aktivitas fisik/lokasi simultan yang mustahil.

## Audit merged-chat manual

Membaca masing-masing `conversation_id` saja tidak cukup. Ditemukan 49 overlap interval antar-segmen untuk participant pair yang sama.

Overlap dapat natural karena manusia bisa pindah topik, tetapi juga dapat membuka artefak generator apabila dua dialog mini berjalan paralel seolah tidak saling melihat.

### Contoh cukup natural

**Dini — 12 Juli**
Dua topik, pesan keluarga/makan dan gelas plastik, saling berselang dalam chat. Walau berasal dari dua segment ID, jika digabung kronologis masih terbaca seperti multitopic WhatsApp yang realistis.

**Reza — 19 Juli**
Topik laundry dan buku pinjaman berjalan berselang. Pergantian topik masih dapat diikuti dan tidak otomatis menunjukkan konflik.

**Jihan — 18 Juli**
Anchor Galloway tentang berada bersama keluarga, waktu pulang, Wi-Fi, dan rencana jemput disambung bridge tentang dapur, charger, HP, makan, dan jadwal. Ini menunjukkan contoh integrasi synthetic-to-anchor yang cukup kuat.

### Contoh belum natural

**Kirana — 10 Juli**
Merged timeline masih memiliki pola seperti:
- “eh kipas kecil”;
- “aku lupa tadi sebentar”;
- “lupa apa? sebentar”;
- “naruhnya barusan”;
- “dekat banget ternyata kok”;
- pengulangan topik wadah yang restart.

Ini masih terlihat seperti dua mini-thread generator yang ditumpuk dan belum layak final.

**Jihan — 18 Juli**
Walau alur utamanya koheren, masih ada bridge seperti “iya, nanti barusan.” yang tidak natural.

Karena itu snapshot ini belum dapat dinyatakan natural/koheren secara global hanya berdasarkan structural QA.

## Gate baru sebelum P2 final

Selain QA yang sudah ada, final sign-off harus mencakup:

1. **Merged-chat review**
   - gabungkan semua segment untuk participant pair yang sama;
   - sort timestamp;
   - review aliran topik, callback, dan state;
   - prioritas 49 overlap segment.

2. **Global Raka timeline**
   - merge seluruh 9.997 pesan yang melibatkan Raka;
   - audit lokasi, perjalanan, tidur, availability, dan simultaneous action;
   - chat simultan boleh, aktivitas fisik/lokasi kontradiktif tidak.

3. **Anchor neighborhood review**
   - untuk setiap anchor, periksa synthetic messages sebelum/sesudah;
   - bridge tidak boleh mengubah makna, sebab-akibat, atau outcome anchor;
   - context/distractor tidak boleh menyelesaikan konflik lebih awal.

4. **Forensic chat identity mapping**
   - `chat_id`: stable peer/pair identity untuk demo/extraction;
   - `segment_id`: existing `conversation_id`;
   - `message_id`: tetap immutable;
   - provenance tetap tersedia evaluator-side tetapi jangan bocorkan ground-truth-only fields ke examiner.

5. **Human sign-off**
   - sample per phase 1–5;
   - sample seluruh aktor utama;
   - sample bridge-heavy anchor chat;
   - sample context/distractor overlap;
   - catat PASS/REPAIR beserta message IDs.

## Implikasi untuk demonstrasi digital forensics

Demo sebaiknya menggambarkan satu telepon Raka yang berisi daftar chat seperti:
- Kirana
- Tania
- Maya
- Rena
- Nara
- Jihan
- Dini
- Reza
- Bagas
- Caca
- beberapa kontak fiktif/peripheral

Ketika sebuah chat dibuka, semua pesan pada participant pair tersebut ditampilkan dalam satu timeline, walaupun internal dataset menyimpan beberapa `segment_id`.

Empat mixed-pair anchor anomalies jangan ditampilkan seolah-olah otomatis merupakan WhatsApp group. Perlakukan sebagai provenance/reconstruction anomaly sampai ada bukti bahwa sumber memang group chat.

## Status snapshot

**BELUM FINAL secara chat-level coherence.**

Yang sudah kuat:
- anchor immutable;
- synthetic relationships anchored ke Galloway;
- bridge dekat secara temporal ke anchor;
- struktur acquisition sangat Raka-centric;
- beberapa merged chats sudah natural.

Yang masih menghalangi sign-off:
- cadence generator Context B;
- language-template tersisa;
- 49 overlapping segment pairs perlu human merged-chat review;
- global Raka chronology/actor-state;
- sejumlah filler bridge;
- provenance hash discrepancy historis.
