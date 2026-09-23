# Audit Checkpoint 6.000 — Regenerated Batches 012–014

Corpus source of truth pada checkpoint ini berisi tepat **6.000** pesan: 500 anchor, 1.200 bridge, 3.400 context, dan 900 distractor dalam 497 conversation.

## QA struktural

- message_id unik: 6.000/6.000
- exact duplicate row: 0
- exact duplicate synthetic message_text: 0
- timestamp collision dalam conversation: 0
- near-duplicate panjang: 0
- source identity leakage: 0
- timestamp di luar 1–21 Juli 2026 +07:00: 0
- anchor exact-match: 500/500
- mixed conversation baru: 0

## Continuity dan actor-state

Bridge hanya ditambahkan pada gap conversation GAL dan empat mixed baseline conversation tetap tidak disentuh. Context/distractor baru tetap dyadic dengan Raka, tidak menambah outcome perkara atau lokasi spesifik baru. Jihan hanya menerima percakapan netral/nonseksual. Tidak ada penggunaan Caca baru setelah state pemblokiran baseline 19 Juli.

## Gaya

Delta lama yang direvert di `78891ad` tidak dipulihkan. Batches 012–014 dibangun ulang. Pesan <=3 kata: bridge 225/1.200, context 862/3.400, distractor 261/900. Thread tepat 10 pesan turun menjadi 3 context dan 0 distractor. Variasi berasal dari callback pada thread lama, panjang thread 5–17, fragmen, double-text, jeda, dan akhir yang tidak selalu rapi.

Discrepancy hash manifest anchor tetap dicatat sebagai provenance-only dan tidak digunakan untuk mengubah anchor.
