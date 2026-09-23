# QA Integrasi 500 Jangkar Indonesia

Tanggal: 2026-09-23

## Hasil integrasi
- Total pesan: **500**
- Source line unik: **500**
- `message_id` unik: **500**
- `transformation_id` unik: **500**
- Conversation ID unik: **101**
- Exact duplicate row: **0**
- Unresolved source line yang masuk: **0**
- Source line terpetakan yang hilang: **0**
- Kebocoran nama utama sumber (Cornelius/Galloway/Matthew Woods/Marcus Taylor/Danielle Galloway/Backpage/Albuquerque): **0**

## Duplikasi teks
Ada respons pendek alami yang berulang (misalnya “Oke”), dan dua teks lebih panjang yang muncul dua kali. Ini tidak dianggap duplicate row karena `message_id`, konteks, waktu, dan source line berbeda. Dataset tidak menggunakan copy-paste blok untuk menambah volume.

## Harmonisasi lintas-worker
- Actor ID dinormalisasi ke namespace `AKT-...`.
- Conversation ID dinormalisasi dari cluster rekonstruksi sumber.
- Timestamp dibuat deterministik sebagai **timestamp skenario sintetis +07:00**, bukan timestamp asli Exhibit 1A.
- Nilai moneter anchor dinormalisasi secara sintetis dengan faktor kerja 15.000 rupiah per satuan nilai dolar sumber untuk konsistensi internal; ini **bukan klaim kurs historis**.
- Wording untuk aktor di bawah umur disanitasi bila detail eksplisit tidak diperlukan, tanpa menghapus signal forensik utama.

## Integritas
SHA-256 `anchor_indonesia_500.csv`:
`63eeaac83bfd3b9145bbc1d99f3b7bfcce447face3f9cf7e20aa5231d55b0d24`

SHA-256 `registri_aktor_indonesia.csv`:
`1d42ea3fe3dfd356a7c03ca9fcd39604e63e04681db27d3941be3d47685277ca`

## Keputusan
Set 500 jangkar dinyatakan **LOCKED** sebagai reference set P2. Ekspansi 9.500 pesan tambahan tidak boleh mengubah pesan anchor; koreksi anchor berikutnya harus melalui perubahan versi dan QA eksplisit.
