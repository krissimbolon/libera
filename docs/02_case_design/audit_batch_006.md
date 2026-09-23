# Audit Batch 006 — 2.400 pesan

Tambahan 400 pesan: 80 bridge, 260 context, 60 distractor; total 2.400 dan 225 conversation. `python src/libera_corpus_work.py` lulus pemeriksaan struktur dan provenance 500/580/1.060/260. Duplicate ID/row/teks sintetis, collision timestamp conversation, near-duplicate panjang, serta leakage sumber semuanya nol; 500 anchor exact-match.

Review manual memutar R070, R072–R074, R076, R079, R087, R089, R094, R103 dengan anchor. Tidak menyelesaikan pertikaian Tania, perpindahan hotel Dini, sakit Nara, atau konsekuensi komunikasi Caca. Koreksi: keterangan jam kantor Dini dihapus; percakapan sarapan Dini diganti karena lokasi memasak tidak pasti; beberapa thread yang terlalu berdekatan menit digeser. Chat lucu memakai callback yang sudah ada (ikan, kucing, payung), bukan event utama baru.

Audit menyeluruh kronologi lintas actor dan gaya bahasa 10.000 pesan tetap tertunda. Manifest SHA anchor lama masih berbeda dari bytes file yang sudah dikunci; tidak ada perubahan anchor.
