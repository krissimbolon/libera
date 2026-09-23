# QA Batch Anchor A

Tanggal: 2026-09-23

## Lingkup
- Worker: A (chat utama)
- Branch kerja: `p2-paralel-a`
- Source line yang menjadi tanggung jawab: 1–271
- Hanya line dengan status rekonstruksi `COURT_VERBATIM`

## Hasil
- Jumlah anchor: **239**
- Minimum `source_original_line`: 1
- Maksimum `source_original_line`: 271
- `message_id` unik: 239/239
- `source_original_line` unik: 239/239
- Exact duplicate row: 0
- Exact duplicate `message_text`: 0
- Conversation ID: 47
- Recipient belum dapat dipastikan dari sumber: 9 pesan
- Provenance seluruh anchor: `ADAPTED_FROM_GALLOWAY`
- SHA-256 `batch_anchor_a.csv`: `c5d11462e012887ee5447dff07a68ec824752f5a5a4d34c4efdb5e71dd4cd3e4`

## Transformasi
- Bahasa dilokalisasi ke Bahasa Indonesia percakapan.
- Cornelius Galloway → Raka Pradana.
- Marcus Taylor → Reza Mahendra.
- K.T. → Kirana.
- T.S. → Tania.
- Renee 1 → Rena.
- Backpage → Forum Iklan X (fiktif).
- Motel/hotel/lokasi spesifik sumber diganti dengan lokasi fiktif di skenario Bandung Raya.
- Nominal dolar dilokalisasi ke nilai rupiah sintetis secara konsisten untuk mempertahankan pola negosiasi.
- Kredensial sumber diganti dengan kredensial uji fiktif.
- Detail seksual eksplisit yang tidak diperlukan untuk signal forensik disanitasi.

## Catatan
Sembilan recipient yang belum pasti sengaja diberi `AKT-TIDAK-DIKETAHUI`; tidak dilakukan tebakan hanya untuk membuat data terlihat lengkap.

File CSV saat ini dihasilkan sebagai artefak kerja dan akan diintegrasikan ke branch canonical setelah Batch B lengkap dan audit silang selesai.
