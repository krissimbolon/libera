# Ledger kontinuitas aktor untuk ekspansi corpus

Status: catatan kerja berbasis anchor terkunci; **bukan** fakta tambahan perkara asli. Setiap pesan baru harus diuji terhadap anchor sesudahnya, termasuk ketika `conversation_id` berbeda.

| Aktor | Perubahan state yang tampak pada anchor | Batas ekspansi |
|---|---|---|
| Raka | Pusat komunikasi sepanjang 1–21 Juli; sesekali mengatakan sedang di luar, berkendara, atau menjemput. | Jangan tempatkan dia di lokasi berbeda pada menit yang sama. Pesan netral saat perjalanan boleh berupa chat singkat, bukan aktivitas fisik simultan. |
| Kirana | 1 Juli meminta bantuan; 3–4 Juli sakit dan meminta obat; 10–12 Juli terlibat konflik soal kembali/pergi; 13 Juli ada rencana penjemputan; 20 Juli menyatakan berada di Cirebon dan ingin pulang. | Jangan membuat kesehatan, keberangkatan, atau konflik selesai sebelum anchor berikutnya. Anchor 20 Juli kemudian menyebut permintaan bantuan keluar dari tahanan melalui telepon lain (`R098`); urutan dan lokasinya belum cukup jelas untuk diisi dengan adegan baru. |
| Tania | 2 Juli mengalami hambatan jaringan dan koordinasi penginapan; 11 Juli ingin pulang dan sulit menelepon; 12 Juli menunggu tiket dan naik bus; 15 Juli masih berhubungan dengan Raka, termasuk perselisihan. | Jangan menyatakan perjalanan bus atau rekonsiliasi berakhir permanen; jangan tambahkan orang baru sebagai hasil permintaan Raka di `R075`. |
| Rena | 6–11 Juli sering berkomunikasi tentang kesiapan, kamar, penjemputan, makanan, dan uang. | Pertahankan jeda antarpesan dan pekerjaan yang belum selesai; jangan membuat outcome baru dari jadwal yang disebut anchor. |
| Nara | 16–17 Juli menjawab koordinasi jadwal; `R080` sudah bercampur dengan pasangan Maya. | Gunakan percakapan Nara yang dyadic (`R079`, `R087`, `R089`); hindari menambah baris pada `R080` sebelum anomali pasangan diselesaikan. |
| Maya | 16 Juli memiliki pesan tersendiri; 18 Juli Jihan memberi informasi tentang keberadaannya. | Jangan mengarang penangkapan, penemuan, atau hasil pencarian. |
| Jihan | 16–17 Juli menyampaikan ketakutan; 18 Juli bersama keluarga; 18–19 Juli muncul tekanan soal kembali; 20–21 Juli berkomunikasi lagi soal bantuan dan penjemputan. | Aktor di bawah umur: jangan membuat konten seksual eksplisit. Jangan menyelesaikan ketakutan atau perpindahan tempat tanpa dukungan anchor. `R088` memiliki pasangan aktor campuran. |
| Dini | 17 Juli membahas pemindahan hotel, 18 Juli sulit menghubungi Raka; anchor lain menyebut fungsi logistiknya. | Pesan kehidupan sehari-hari boleh, tetapi jangan mengubahnya menjadi pengambil keputusan kriminal baru. |
| Reza | 5 Juli menyatakan tidak dapat bicara; 11 Juli disebut Kirana, 14 Juli berkabar dari lobi. | Jangan menetapkan lokasi/penjelasan percakapannya lebih rinci daripada yang terlihat. |
| Bagas | 16 dan 19 Juli memiliki percakapan langsung dengan Raka; ada referensi lebih awal dalam ancaman. | Percakapan netral boleh; jangan menambah tindakan kekerasan atau outcome ancaman. |
| Caca | 19 Juli meminta kebutuhan sehari-hari dan berkoordinasi; sore hari muncul pesan pemblokiran nomor. | Percakapan sebelum pemblokiran boleh. Jangan lanjutkan chat dua arah setelah `R096` tanpa alasan yang didukung. |

## Anomali dan aturan pengambilan keputusan

- Empat conversation jangkar berisi lebih dari satu pasangan: `P22-C`, `R013`, `R080`, dan `R088`. Pesan baru tidak ditempatkan dalam conversation tersebut.
- Nama yang muncul dalam teks anchor tetapi tidak memiliki ID aktor utama dalam registri, seperti Tara, tidak otomatis menjadi aktor pengirim baru.
- Timestamp anchor adalah waktu skenario sintetis, bukan waktu sebenarnya dari Exhibit 1A. Jangan mengubahnya untuk mengatasi anomali narasi.
- Lokasi spesifik pada pesan baru harus diperiksa juga terhadap conversation lain pada waktu yang sama. Saat tidak perlu, gunakan penanda umum seperti "di kamar", "di luar", atau "di jalan" tanpa membuat alamat baru.
- Context dan distractor tetap pada akuisisi telepon Raka: seluruh percakapan baru pada draf pertama berpasangan dengan `AKT-RAKA`.
