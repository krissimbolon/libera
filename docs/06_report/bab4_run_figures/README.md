# Gambar dokumentasi run Bab IV

Kelima PNG di folder ini **merender ulang teks keluaran nyata** agar terbaca di halaman A4. Gambar ini bukan tangkapan layar terminal dan tidak mengklaim ada emulator aktif saat dibuat. Angka, status, hash, stdout/stderr, dan exit code berasal dari berkas berikut; teks gambar IV.3 menyingkat path direktori temporer.

| Gambar | Sumber mentah | Isi |
|---|---|---|
| `IV-01_hash_run.png` | `demo_evidence/ACQ-SIM-001_20260925_010848/acquisition_manifest.json`, master dan working SQLite | Hash dihitung ulang dari berkas asli |
| `IV-02_ekstraksi_run.png` | `docs/06_report/bab4_evidence/experiment.json` bagian `clean.remediated.stdout`; `artifact_manifest.json` | Output ekstraktor pada salinan bersih dan hasil manifest historis |
| `IV-03_retest_run.png` | `experiment.json` bagian `clean`, `tamper`, `missing_manifest` | Exit code dan pesan penolakan sebelum/sesudah perbaikan |
| `IV-04_ancaman_run.png` | `experiment.json` bagian `tamper` | Hash, IoC, SQLite integrity, jumlah pesan, exit code |
| `IV-05_evaluasi_run.png` | `runtime/working/P9_reconstructed_20260925/evaluation.json` | Output evaluasi proxy dan validitas referensi A/B/C |

Kode pembuat gambar: `scripts/generate_uas_ch4_run_images.py`. Eksperimen F-01/F-02 dapat diulang dengan `scripts/run_uas_ch4_sandbox.py`; kode ini menulis hanya pada salinan temporer. Naskah Bab IV ada di `docs/06_report/BAB_IV_UAS_KSI_KELOMPOK_2.md`.

Tangkapan layar Workbench **asli** dari run arsip tersedia di `runtime/workbench_overview.png` dan `runtime/workbench_evaluation.png`. Screenshot tersebut berasal dari snapshot `ACQ-SIM-LIVE`, sehingga tidak dipakai sebagai dokumentasi langsung akuisisi `ACQ-SIM-001` dalam Bab IV.
