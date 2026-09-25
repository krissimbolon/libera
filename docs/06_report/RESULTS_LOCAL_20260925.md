# Hasil lokal LIBERA — 25 September 2026

## Status yang dapat dipertanggungjawabkan

P8 selesai untuk seluruh T01–T10: 30 respons nyata A/B/C, tanpa error transport/retry, dan semua generation berhenti normal. Sepuluh output C memenuhi schema JSON. Output beserta input dan konfigurasi telah dikunci; 14/14 hash terverifikasi.

P9 telah menyelesaikan validasi identifier dan penanganan referensi rusak. **Independent human semantic ground truth tidak tersedia pada studi ini; karena itu precision/recall/F1 semantik final tidak diklaim.**

## Data dan metode actual

- Akuisisi: `ACQ-SIM-001 / DEV-SIM-001`, logical acquisition ChatSim di emulator Android. Bukan akuisisi WhatsApp atau physical-device acquisition.
- P4: 9.997 message artifacts, 25 chat.
- P5: baseline dan examiner review telah dikunci sebelum AI.
- P6: 645 chunk/index entries, BGE-M3 berdimensi 1.024.
- P7/P8: Qwen2.5 1.5B, temperature 0.1, seed 42, context 8.192, top-k 8; output budget 2.048, repeat penalty 1.2, repeat window 256.
- Prompt: `v6-forensic-grounded-repeat-control`; B/C memakai retrieval yang sama pada setiap task.
- A tidak menerima evidence. C memakai schema JSON dengan batas panjang field.
- Percobaan pendahuluan yang gagal dipertahankan; perubahan prompt/parameter dan riwayat run didokumentasikan dalam [catatan P8](../04_ai_methodology/P8_REAL_RUN_20260925.md).

## Hasil integrity dan citation

| Ukuran | A | B | C |
|---|---:|---:|---:|
| Respons nyata | 10 | 10 | 10 |
| Error transport | 0 | 0 | 0 |
| Generation terpotong | 0 | 0 | 0 |
| JSON sesuai schema | N/A | N/A | 10 |
| Referensi yang diajukan | 0 | 10 | 24 |
| Referensi valid dan ada dalam input kondisi | 0 | 10 | 12 |
| Referensi dikarantina | 0 | 0 | 12 |
| Validitas identifier | N/A | 100% | 50% |

Angka di atas bukan precision/recall/F1 atau akurasi semantik. B tetap memiliki lima task tanpa citation; C memiliki dua task tanpa citation terverifikasi. Review claim perlu membedakan abstention dari claim tanpa dukungan.

## Penanganan 12 referensi C

Output asli tetap tidak diubah. Dua belas referensi yang rusak dikarantina dari pemetaan evidence dan tidak boleh menjadi temuan terverifikasi. Kesalahan tetap dicatat pada T01/T02/T03/T04/T07/T08. Universe penilaian tidak dipersempit: jika evidence positif terlewat, FN tetap dihitung ketika GT tersedia.

Kebijakan [karantina P9](../05_validasi/P9_CITATION_POLICY_20260925.md) ditambahkan setelah audit P8 dan sebelum pembukaan GT. Laporkan perubahan pasca-eksperimen ini. Hasil filtered citation tidak boleh dipresentasikan sebagai output model yang sejak awal benar.

## Kesimpulan sementara

Pipeline berhasil menuntaskan eksperimen lokal yang dapat diaudit. Schema JSON meningkatkan keteraturan format, tetapi pada run ini belum menjamin referensi evidence yang valid. Penanganan referensi mencegah identifier rusak dipakai sebagai evidence sah; temuan kesalahan tetap membatasi kesimpulan tentang kualitas model. Belum ada dasar untuk menyatakan RAG/C lebih akurat secara semantik. Hasil yang dapat dipertanggungjawabkan adalah integritas acquisition, kelengkapan eksekusi, traceability, schema validity, output locking, dan citation validation.

## Artefak lanjutan

- Paket review dan laporan actual: `runtime/working/P9_review_20260925/`.
- Eksperimen locked: `runtime/working/P8_final_v6_20260925/`.
- Script final P9: `scripts/run_p9_final.ps1` dengan parameter lock v6 dan path GT independen.

Runtime evidence dan GT tidak dimasukkan ke Git publik. Dokumentasi ini menyimpan status dan agregat saja.
