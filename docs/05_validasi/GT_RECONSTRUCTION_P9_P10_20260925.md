# Rekonstruksi referensi evaluasi, P9, dan P10 — 25 September 2026

**Selesai untuk jalur rekonstruksi proxy. Ground truth semantik evaluator asli belum berhasil dipulihkan.**

Ground truth di workstation Chris dinyatakan hilang oleh pengguna. Repository menyimpan corpus beku dan desain generasi, tetapi tidak menyimpan keputusan evaluator `DIRECT/SUPPORTING/AMBIGUOUS/NEUTRAL` atau label bukti kunci. Mengisi ulang label tersebut seolah berasal dari evaluator lama akan mengarang data penelitian.

Yang dibuat adalah referensi proxy deterministik dari provenance, paket anotasi manusia untuk membangun ulang GT semantik, serta hasil P9/P10 pasca-eksperimen yang secara eksplisit menyebut perubahan target evaluasi. Ini bukan pengganti setara untuk studi blind yang direncanakan.

## Dasar dan aturan rekonstruksi

Generator hanya membaca corpus P2 beku dan dokumen desain. Generator tidak menerima respons P8, hasil retrieval, baseline P5, atau metrik sebagai input. Namun kebijakan ini dipilih setelah output P8 terlihat, sehingga tidak diklaim preregistered atau blind.

| Provenance | Label proxy | Makna |
|---|---|---|
| `ADAPTED_FROM_GALLOWAY` | 1 | Source anchor dalam desain sintetis; bukan otomatis bukti kunci |
| `SYNTHETIC_DISTRACTOR` | 0 | Designed distractor; bukan keputusan semantik evaluator |
| `SYNTHETIC_CONTEXT` | kosong | Tidak diasumsikan negatif |
| `SYNTHETIC_BRIDGE` | kosong | Tidak diasumsikan negatif |

Target eksplisit: `source_anchor_vs_designed_distractor_not_semantic_key_evidence`.

CSV memakai `is_key_evidence` sebagai kolom kompatibilitas evaluator lama, tetapi juga memuat `proxy_label`, `label_origin`, `reference_target`, dan `review_status`. Nilai itu **bukan klaim label bukti kunci**. Field event, strength, dan relation tidak dikarang. Verifikasi lock menolak perubahan metadata yang mencoba melaporkan proxy sebagai label blind.

## Artefak yang dibuat

Folder privat, diabaikan Git: `runtime/private/P9_reconstructed_20260925/`.

- `reconstructed_reference.csv`: 10.000 ID unik; 500 proxy positif, 1.500 proxy negatif, 8.000 tanpa label.
- `reconstruction_manifest.json`: aturan, jumlah, sumber, hash, dan batasan.
- `reconstructed_reference.csv.lock.json`: penguncian label dan metadata asal/target.
- `human_annotation_packet.csv`: 9.997 acquired messages; label semantik tetap kosong, untuk evaluator manusia.
- `human_annotation_manifest.json`: provenance paket anotasi; `labels_auto_assigned=0`.

Folder hasil: `runtime/working/P9_reconstructed_20260925/`.

- `evaluation.json`: seluruh metrik, cakupan label, verifikasi lock, dan audit karantina.
- `run_report.md`: laporan P10 dengan disclosure proxy di bagian atas.
- `citation_review.csv`: daftar referensi valid/karantina untuk audit.
- `completion_manifest.json`: hash hasil, referensi, lock, dan snapshot kode evaluasi.
- `code_snapshot/`: kode/metode yang dipakai; snapshot dipertahankan agar perubahan kode kemudian tidak mengubah bukti reproducibility run ini.

SHA-256 referensi rekonstruksi: `0c149ebf6e107cbe95ed77620eec8f5486067edd5f573804d74d78d7e379598f`.

P8 asli tidak diubah dan tidak dijalankan ulang. Sebanyak 14/14 file lock P8 terverifikasi sebelum label dibuka.

## Cakupan penilaian

- Acquired universe: 9.997 pesan.
- Labeled evaluation universe: **1.997 pesan** = 497 anchor + 1.500 distractor.
- Tiga anchor dari corpus tidak terakuisisi; tidak dihitung sebagai FN/TN.
- Sebanyak 8.000 context/bridge belum berlabel dan dikeluarkan dari universe scoring, bukan diubah menjadi negatif.
- Referensi model di luar labeled universe dihitung dan dilaporkan secara terpisah.
- Metrik menggabungkan evidence IDs unik lintas T01–T10, bukan akurasi jawaban per task, per aktor, event, atau claim.

## Hasil P9 actual

Status: `P9_RECONSTRUCTED_PROXY_EVALUATION_COMPLETE_WITH_CITATION_ERRORS`.

| Set prediksi | TP | FP | FN | TN | Precision | Recall | F1 | Prediksi di luar labeled universe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A citations | 0 | 0 | 497 | 1500 | 0* | 0 | 0 | 0 |
| B citations | 0 | 3 | 497 | 1497 | 0 | 0 | 0 | 7 |
| C citations | 1 | 1 | 496 | 1499 | 0.500000 | 0.002012 | 0.004008 | 10 |
| B retrieval | 137 | 107 | 360 | 1393 | 0.561475 | 0.275654 | 0.369771 | 1119 |
| P5 baseline | 45 | 24 | 452 | 1476 | 0.652174 | 0.090543 | 0.159011 | 77 |

\* Precision A tidak terdefinisi secara matematis karena tidak ada prediksi positif. Implementasi menyimpan 0.0 sebagai konvensi zero-division, bukan klaim akurasi nol yang terukur. Interpretasi perbandingan harus memperhatikan cakupan: misalnya hanya dua citation C berada dalam subset yang memiliki label proxy.

Angka ini mengukur keterpilihan anchor dibanding distractor desain. Jangan menyebutnya accuracy/precision bukti kunci, menggunakannya untuk membuktikan temuan forensik, atau menyimpulkan keunggulan metode secara umum.

## Dua belas referensi C

C memiliki 24 kemunculan referensi: 12 identifier valid dan 12 dikarantina. Validitas identifier 50%, bukan akurasi semantik. Referensi rusak tidak dipetakan, tidak diberi kredit TP, dan tetap muncul sebagai error. Universe label tidak dikurangi untuk menghapus false negative.

P9 tetap mencatat precheck `FAIL_INVALID_EVIDENCE_REFERENCE` bersamaan dengan status komputasi selesai. Penyelesaian komputasi tidak menyembuhkan kesalahan model.

## Reproduksi

Perintah yang sudah dijalankan dari root repo:

```powershell
python tools/reconstruct_private_reference.py --output-dir runtime/private/P9_reconstructed_20260925

python tools/build_private_gt_annotation_packet.py `
  --artifacts demo_evidence/ACQ-SIM-001_20260925_010848/artifacts/artifacts.csv `
  --output runtime/private/P9_reconstructed_20260925/human_annotation_packet.csv `
  --manifest runtime/private/P9_reconstructed_20260925/human_annotation_manifest.json

powershell -ExecutionPolicy Bypass -File scripts/run_p9_final.ps1 `
  -GroundTruthPath runtime/private/P9_reconstructed_20260925/reconstructed_reference.csv `
  -LockManifest runtime/working/P8_final_v6_20260925/p8_lock_manifest.json `
  -OutputDirectory runtime/working/P9_reconstructed_20260925
```

Gunakan folder baru untuk reproduksi; generator/evaluator tidak menimpa hasil final. Jangan menjalankan ulang paket anotasi pada file yang sudah diisi reviewer. Seluruh artefak privat/runtime harus tetap di luar Git publik.

## Validasi dan pekerjaan manusia yang masih diperlukan

33 tes otomatis lulus. Tes mencakup karantina citation, FN tidak dihapus, integritas lock, asal proxy tidak dapat disamarkan, dan context/bridge tetap tanpa label. P9/P10 rekonstruksi sudah dieksekusi, bukan dry-run.

Untuk menyelesaikan tujuan penelitian awal, evaluator perlu menilai paket anotasi manusia secara independen, mendokumentasikan rubrik dan adjudikasi, lalu mengunci label baru. Karena file asli hilang, penilaian ulang tersebut tetap harus disebut ground truth baru, bukan salinan ground truth lama. Laporan saat ini sudah lengkap untuk jalur proxy dengan keterbatasan ini diungkapkan; klaim evaluasi blind semantik tetap belum terpenuhi.
