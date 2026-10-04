# P9 — Penanganan referensi rusak dan kesiapan evaluasi final

Versi: `p9-strict-citation-quarantine-v1`.

Status: penanganan referensi dan paket evaluasi selesai; **metrik final menunggu ground truth privat evaluator**. Kebijakan ini ditambahkan setelah audit output P8 dan sebelum ground truth dibuka. Ini adalah perubahan pasca-eksperimen yang harus diungkapkan, bukan protokol yang diklaim telah ditetapkan sebelum generasi.

## Keputusan

Output P8 v6 tetap menjadi hasil penelitian yang dikunci. Tidak ada model yang dijalankan ulang, jawaban yang disunting, atau ID yang diperbaiki berdasarkan hasil yang diinginkan.

Hanya referensi yang memenuhi semua syarat berikut boleh masuk ke himpunan prediksi bukti:

1. String persis berformat `ART-` diikuti enam digit.
2. ID ada dalam evidence P4 yang dikunci.
3. Untuk B/C, ID benar-benar diberikan kepada kondisi tersebut dan tercatat dalam retrieval trace task yang sama. A tidak diberi evidence.

Untuk C, prediction field adalah `relevant_evidence`. Mention dalam narasi tidak digunakan untuk mengganti isi field yang rusak. Untuk A/B, kandidat ID dibaca dari respons teks. Pemeriksaan sintaks tidak membuktikan bahwa isi claim didukung evidence.

ID kurang digit tidak ditambah nol otomatis. Kutipan tidak dipetakan ke ID berdasarkan kemiripan atau pencocokan teks. ID valid tetapi di luar retrieval juga dikarantina. Referensi asli dan alasan penolakan tetap disimpan dalam audit.

## Hasil actual v6

| Kondisi | Kemunculan referensi | Valid | Dikarantina | Validitas identifier |
|---|---:|---:|---:|---:|
| A | 0 | 0 | 0 | N/A |
| B | 10 | 10 | 0 | 100% |
| C | 24 | 12 | 12 | 50% |

Enam output C terdampak: T01, T02, T03, T04, T07, T08. C tidak memiliki citation terverifikasi pada T03/T07. B tidak memiliki citation pada T01/T05/T06/T07/T09; ini memerlukan pemeriksaan apakah jawaban abstain atau membuat claim tanpa dukungan. Jangan menyamakan tidak adanya citation invalid dengan groundedness sempurna.

## Pengaruh terhadap metrik

Referensi rusak tidak dimasukkan sebagai evidence baru dan tidak dapat memperoleh kredit TP. Karantina **tidak mengecilkan universe ground truth**: evidence positif yang tidak ditemukan tetap dihitung sebagai FN. Karena unitnya message-level, string rusak bukan message tambahan untuk matriks kebingungan; kegagalannya dilaporkan terpisah melalui jumlah referensi rusak, validitas identifier, dan task terdampak.

Precision/recall/F1 message-level harus selalu disajikan bersama tabel karantina. Jangan menampilkan metrik hasil penyaringan sebagai kualitas end-to-end tanpa disclosure. Tidak ada jaminan bahwa kesalahan model tidak memengaruhi kesimpulan ilmiah. Yang dijamin oleh validasi adalah referensi rusak tidak diperlakukan sebagai evidence sah atau mengubah label/universe evaluasi.

Jika scoring selesai tetapi ada error citation, status yang benar adalah `P9_FINAL_EVALUATION_COMPLETE_WITH_CITATION_ERRORS`; status precheck aslinya tetap tercatat. Keberhasilan komputasi berbeda dari kualitas jawaban.

## Integritas dan blind evaluation

- Seluruh 14 file pada P8 lock diverifikasi sebelum membuka GT, termasuk config, indeks, log, dan snapshot kode.
- P5 dan P8 tetap tidak berubah.
- GT harus dianotasi evaluator secara independen dengan kolom `message_id,is_key_evidence`; tidak diturunkan dari respons model.
- GT dan lock GT disimpan privat. File label yang berubah setelah dikunci ditolak; duplikasi/ID kosong juga ditolak.
- Pipeline final tidak memanggil P6/P7/P8 atau LLM.
- Output evaluasi tidak boleh menimpa file yang dikunci.
- Rubrik factual correctness dan groundedness tetap memerlukan penilaian claim oleh evaluator; identifier validity bukan penggantinya.

## Paket dan perintah

P8 source lock: `runtime/working/P8_final_v6_20260925/p8_lock_manifest.json`.

Paket review: `runtime/working/P9_review_20260925/`:

- `evaluation_precheck.json`: audit raw dan hasil karantina per task/kondisi.
- `citation_review.csv`: referensi yang boleh digunakan untuk join evidence dan referensi yang ditolak; tidak berisi label ground truth.
- `run_report.md`: laporan P10 dengan status aktual dan tabel karantina.
- `review_manifest.json`: hash paket review, kebijakan, evaluator, dan source lock.

Setelah path GT independen tersedia, jalankan dari root repository:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_p9_final.ps1 `
  -GroundTruthPath "D:\PRIVATE\ground_truth_final.csv" `
  -LockManifest "runtime/working/P8_final_v6_20260925/p8_lock_manifest.json" `
  -OutputDirectory "runtime/working/P9_final_20260925"
```

Path GT di atas hanya contoh; jangan menjalankan dengan label buatan atau file skema kosong. Script mengambil eksperimen, baseline, dan config dari lock yang dipilih, memverifikasi semua hash, mengunci/verifikasi GT, menghitung metrik dengan kebijakan di atas, lalu membangun laporan P10. Folder final harus baru agar hasil terdahulu tidak tertimpa.

Paket review ini tidak menyatakan `P9_COMPLETE`; angka precision/recall/F1 belum tersedia tanpa GT. Tidak ada label penelitian privat yang dibuat oleh agen. Label kecil pada tes otomatis hanyalah fixture pengujian, bukan ground truth penelitian.
