# Audit Batch 013 — Checkpoint 6.000

**Kumulatif:** 6.000 pesan; 492 conversation; komposisi 500/1.200/3.400/900.

QA struktural lulus: 6.000 message_id unik, exact duplicate row 0, duplicate synthetic text 0, collision timestamp 0, near-duplicate panjang 0, source identity leakage 0, anchor exact-match 500/500, seluruh timestamp dalam 1–21 Juli 2026 +07:00.

Sebelum checkpoint dinyatakan lulus, audit menangkap pergeseran timezone pada bridge baru yang sempat menghasilkan timestamp 30 Juni. Sebanyak 200 bridge Batch 012–013 direlokasi ulang menggunakan waktu lokal skenario dan gap conversation GAL masing-masing. Empat mixed baseline conversation tetap tidak disentuh.

Continuity/actor-state: sampled bridge direplay terhadap tetangga pesan dalam conversation; context/distractor baru tidak menambah outcome utama, lokasi spesifik baru, atau pengetahuan yang jelas belum diterima. Caca tidak diperpanjang setelah blokir baseline 19 Juli. Jihan hanya menerima percakapan netral dan tersanitasi.

Style: pesan <=3 kata kini 180/1.200 bridge, 874/3.400 context, 339/900 distractor. Ini memperbaiki ritme dibanding 4k. Namun 80 context conversation dan 59 distractor conversation masih tepat 10 pesan; isu ini belum ditutup dan menjadi sasaran batch 014–016 dengan callback organik, double text, jeda, dan thread bervariasi.
