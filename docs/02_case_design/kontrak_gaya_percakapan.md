# Kontrak Gaya Percakapan — Corpus 10.000 Pesan

Tanggal dikunci: 2026-09-23

Tujuan dokumen ini adalah menjaga 10.000 pesan terasa seperti satu rangkaian percakapan WhatsApp yang hidup, bukan kumpulan baris sintetis yang berdiri sendiri.

## Prinsip utama

1. **Konteks harus mengalir.** Setiap pesan baru harus punya hubungan dengan percakapan sebelumnya: membalas, mengonfirmasi, menunda, mengalihkan topik, menindaklanjuti, atau menutup percakapan.
2. **500 anchor tidak boleh diubah.** Anchor adalah tulang punggung skenario.
3. Pesan sintetis ditulis untuk mengisi ruang antar-anchor dan memperkaya kehidupan percakapan, bukan membuat kasus baru.
4. Struktur relasi, pola kontrol, koordinasi, pergerakan, penginapan, transportasi, pencarian, tekanan, dan komunikasi calon pelanggan tetap mengikuti pola yang tercermin pada Document 547.
5. Jangan mengklaim pesan sintetis sebagai pesan asli Galloway.

## Bahasa Indonesia

Bahasa harus:
- percakapan sehari-hari;
- tidak terlalu formal;
- boleh menggunakan bentuk seperti `nggak`, `udah`, `bentar`, `gimana`, `iya`, `oke`, `ntar`, `lagi di mana`, dan sejenisnya;
- menyesuaikan gaya tiap aktor;
- sesekali memiliki typo ringan, singkatan, emoji sederhana, atau pesan sangat pendek bila natural;
- tidak dibuat terlalu rapi seperti narasi buku atau jawaban AI.

Bahasa tidak boleh:
- sengaja dibuat sulit dibaca;
- memakai slang berlebihan pada semua pesan;
- mengulang template dengan hanya mengganti nama/angka;
- berubah menjadi bahasa laporan atau bahasa hukum.

## Ritme percakapan

Corpus harus mengandung campuran:
- pesan 1–5 kata;
- pesan satu kalimat;
- pesan lebih panjang saat konflik/penjelasan;
- unanswered message;
- double text;
- koreksi setelah salah kirim;
- jeda beberapa menit/jam;
- perubahan topik alami;
- check-in singkat;
- percakapan netral di antara percakapan relevan.

Tidak semua percakapan harus memiliki pola tanya-jawab sempurna.

## Kontinuitas aktor

Untuk setiap conversation_id, model harus mempertahankan:
- siapa sedang berbicara dengan siapa;
- lokasi terakhir yang diketahui;
- apa yang sedang ditunggu;
- pekerjaan/jadwal yang sedang berlangsung;
- emosi atau konflik yang belum selesai;
- barang/transportasi/penginapan yang sedang dibahas.

Model tidak boleh membuat aktor tiba-tiba mengetahui informasi yang belum pernah diterima.

## Kontinuitas waktu

Pesan harus mengikuti urutan timestamp. Pesan baru yang ditempatkan di antara dua anchor:
- tidak boleh membalik sebab-akibat;
- tidak boleh membuat aktor berada di dua lokasi yang bertentangan;
- tidak boleh menyelesaikan konflik yang pada anchor berikutnya masih berlangsung.

## Kesetiaan terhadap kasus

Ekspansi boleh menambahkan:
- sapaan;
- makanan;
- baterai/charger;
- perjalanan;
- check-in;
- keterlambatan;
- pertanyaan lokasi;
- percakapan keluarga;
- percakapan sosial;
- koordinasi harian;
- gangguan/noise.

Ekspansi tidak boleh menambahkan:
- korban utama baru;
- kematian;
- penangkapan baru;
- tindak pidana utama baru;
- hubungan inti baru;
- outcome baru yang mengubah kasus.

## Aktor di bawah umur

Jangan membuat konten seksual eksplisit untuk aktor di bawah umur. Signal forensik cukup melalui konteks koordinasi, kontrol, pergerakan, uang, jadwal, dan relasi.

## Target akhir

Corpus final harus terasa seperti hasil ekstraksi WhatsApp dari satu periode kehidupan nyata, bukan data tabular yang dikarang per baris.
