# Dry Run

Dry-run menggunakan data dummy/non-case untuk menguji:
- Evidence ID;
- hashing SHA-256;
- pembuatan master copy;
- pembuatan working copy;
- verifikasi hash;
- pencatatan chain of custody;
- acquisition log;
- deteksi controlled mismatch.

Jangan gunakan corpus LIBERA final pada dry-run.


## Dry-run 001 — hash awal dummy.txt

File dummy dibuat pada private evidence storage:
`D:\KSI\Libera Private Evidence\07_P3_forensik\07_dry_run\dummy.txt`

Isi yang ditulis:
`LIBERA forensic dry run`

Hash baseline:
- Algorithm: **SHA-256**
- Hash: `8A02C5FEDFB2862475407B729C8E51C5BF2920ED6FC3352CA50F5CC028AB8375`
- Tool: PowerShell `Get-FileHash`

Status: **baseline hash berhasil dibuat**.

Catatan:
- File ini hanya dummy untuk dry-run, bukan evidence asli.
- Langkah berikutnya adalah membuat copy dan membuktikan hash copy identik sebelum menjalankan uji mismatch terkontrol.
