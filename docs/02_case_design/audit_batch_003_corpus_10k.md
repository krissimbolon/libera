# Audit batch 003 — corpus kerja 1.171 pesan

Branch `p2-10k-work`. Draf, bukan corpus final.

Batch ini menambah 403 pesan yang ditulis sebagai rangkaian: 75 bridge pada percakapan jangkar, 238 context dalam thread yang mempertahankan topik, dan 90 distractor sosial. Kumulatif menjadi 500 anchor, 243 bridge, 308 context, 120 distractor; 142 conversation.

QA otomatis: 1.171 ID unik; exact duplicate row 0; duplikat teks sintetis 0; tabrakan timestamp per conversation 0; kandidat near-duplicate panjang 0; source-line unresolved yang dijadikan anchor 0; kebocoran nama utama sumber pada tambahan 0; semua 500 anchor sama persis dengan file branch. Timestamp tambahan berada di 1–21 Juli 2026 +07:00 dan aktornya sudah dikenal.

Review manual dilakukan dengan replay seluruh tambahan bridge terhadap pesan sebelum/sesudahnya di conversation yang sama. Pesan yang membuat salam muncul setelah percakapan berjalan, pertanyaan dijawab terlalu dini, atau perpindahan aktor terkesan selesai tanpa anchor dihapus. Sampel context/distractor dicek melintasi conversation; callback stiker ikan pada Dini (1→16 Juli) dan kucing pada Caca (4→11 Juli) konsisten. Penutup dialog yang terlalu rapi dikurangi. Audit aktor lintas keseluruhan corpus dan review bahasa final masih terbuka.

Catatan baseline tetap: hash manifest jangkar tidak cocok dengan byte jangkar ter-commit dan empat conversation anchor mencampur pasangan aktor. Jangan mengubah anchor untuk menyembunyikan masalah tersebut. Lanjutkan batch berikutnya hingga checkpoint 2.000 dengan komposisi 500/500/800/200.
