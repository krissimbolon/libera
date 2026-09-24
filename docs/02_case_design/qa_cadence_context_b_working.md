# QA cadence Context B — checkpoint kerja, belum final

Baseline sebelum model: 2.757/2.954 gap Context B (93,33%) memenuhi `seconds % 60 == 7`; 718 gap tepat 247 detik. Context A tetap 75/2.957 (2,54%).

`src/naturalize_context_b_timing.py` versi `thread-weights-v1` mengubah **2.220 timestamp Context B sintetis**. Bobot waktu didasarkan pada pengirim yang double text atau berganti, panjang pesan, pertanyaan, tindakan mencari/mengambil, dan jeda eksplisit. Tidak ada random seed atau jitter acak. Model bekerja pada run satu segment dalam satu chat pasangan yang digabung, mempertahankan urutan chat, waktu anchor, posisi terhadap anchor yang melibatkan salah satu aktor, batas hari, reply, dan endpoint run bila topik/segment lain segera menyusul. Enam thread dengan waktu manual sebelumnya tidak diolah ulang. Tiga collision lintas chat yang baru ditemukan setelah transform diperbaiki secara terpisah di `koreksi_waktu_manual_003.tsv`; kejadiannya dan alasan per pesan tercatat.

| Metrik Context B | Sebelum | Sesudah |
|---|---:|---:|
| Adjacent gaps | 2.954 | 2.954 |
| Remainder 7 detik | 2.757 (93,33%) | 383 (12,97%) |
| Exact 247 detik | 718 | 105 |
| Exact 307 detik | 584 | 84 |
| Exact 127 detik | 642 | 81 |
| Exact 187 detik | 644 | 76 |

Top exact gaps sesudah: 247 s (105), 307 s (84), 127 s (81), 187 s (76), 92 s (19). Remainder sesudah: 7 (383), 14 (145), 23 (120), lalu tersebar; **remainder 7 masih yang terbesar**, meski tidak lagi mayoritas. Distribusi lengkap sebelum/sesudah ada di `qa_cadence_proposal_working.json`. Sisa 105 gap 247 dan proporsi 12,97% tetap perlu ditinjau pada packet semantik; angka ini sendiri belum menjadi sign-off.

Rerun auditor struktur sesudah transform: 10.000 pesan, anchor 500/500, provenance tetap, duplikat synthetic 0, suffix berulang 0, timestamp/reply bersih. Auditor chat fisik masih mencatat 49 overlap. Auditor actor timeline: 0 collision lintas chat sesudah tiga koreksi, 0 Caca setelah blokir, 0 perubahan manual yang melewati anchor aktor. Spot-check Dini 7 Juli menemukan bahwa percobaan model yang sempat memampatkan awal thread meninggalkan jeda tidak masuk akal di tengah dialog; percobaan itu **dibatalkan**. Model yang dipakai mempertahankan endpoint sebelum topik lain sehingga dialog tersebut tidak memiliki jeda buatan tadi. Pemeriksaan actor-state dan merged chat seluruh corpus masih terbuka; status final tetap gagal.
