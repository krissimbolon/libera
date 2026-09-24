# Protokol Akuisisi Test Device LIBERA

Tujuan: menghasilkan acquisition package yang forensically defensible untuk eksperimen akademik LIBERA tanpa mengklaim kemampuan acquisition yang tidak benar-benar dilakukan.

Acuan metodologis:
- NIST SP 800-101 Rev. 1 (SRC-004): validation, preservation, acquisition, examination, analysis, reporting.
- NIST SP 800-86 (SRC-005): dokumentasi proses forensik dan keterbatasan.
- Konvensi evidence ID LIBERA: DEV / ACQ / ART / CHK / RUN / FND / ERR.

## Scope

Perangkat adalah test device milik tim, bukan perangkat sitaan nyata. Dataset dan akun yang dipakai harus khusus skenario penelitian. Hindari memasukkan data pribadi nyata yang tidak diperlukan.

## 1. Freeze metadata sebelum acquisition

Tetapkan ID: `DEV-001`.

Catat:
- tanggal/waktu lokal dan timezone;
- produsen/model;
- Android version + build;
- WhatsApp/app version;
- kapasitas storage;
- battery level/power state;
- SIM/account test identifier dalam bentuk yang tidak membuka kredensial;
- network state;
- developer options/USB debugging state;
- root state;
- layar locked/unlocked saat mulai;
- perubahan yang sengaja dilakukan sebelum acquisition.

Jangan root, reset, reinstall, atau update perangkat hanya untuk mempermudah acquisition setelah evidence staging dinyatakan selesai, kecuali eksperimen memang mendefinisikan prosedur tersebut dan dampaknya didokumentasikan.

## 2. Evidence staging freeze

Sebelum P3:
1. P2 final corpus harus sudah frozen.
2. Hitung SHA-256 file final.
3. Simpan evaluator-only ground truth terpisah.
4. Catat bagaimana data ditempatkan pada test environment/device.
5. Setelah staging selesai, jangan mengubah corpus desain tanpa version bump.

## 3. Pilih acquisition method dan beri label yang jujur

Gunakan salah satu label:
- `LOGICAL_EXPORT`
- `LOGICAL_FILE_COPY`
- `BACKUP_ACQUISITION`
- `FILESYSTEM_ACQUISITION`
- `PHYSICAL_ACQUISITION`

Label harus mengikuti metode yang benar-benar dilakukan.

Jika hanya menggunakan fitur Export Chat WhatsApp, catat sebagai `LOGICAL_EXPORT`, bukan image perangkat. WhatsApp menyatakan chat export menghasilkan file teks/copy dan tidak dapat diimpor kembali sebagai backup.

Jika acquisition tool komersial/forensik digunakan, catat nama, versi, mode acquisition, dan opsi yang dipilih.

## 4. Buat ACQ package

Tetapkan `ACQ-001`.

Direktori privat yang disarankan:

```text
D:\KSI\Libera Private Evidence\
├── 02_master_evidence\ACQ-001\
├── 03_working_copy\ACQ-001\
└── 05_log_akuisisi\
```

Setiap output acquisition:
- simpan filename asli;
- catat size byte;
- hitung SHA-256 segera setelah acquisition;
- jangan edit master;
- buat working copy;
- hash ulang working copy dan cocokkan dengan master sebelum examination.

Windows PowerShell contoh:
```powershell
Get-FileHash -Algorithm SHA256 "PATH_FILE"
```

Untuk banyak file:
```powershell
Get-ChildItem -File -Recurse "PATH_FOLDER" |
  Get-FileHash -Algorithm SHA256
```

Simpan command/alat yang dipakai di acquisition log.

## 5. Chain of custody

Setiap perpindahan atau copy material evidence harus memiliki:
- evidence/acquisition ID;
- timestamp;
- from;
- to;
- purpose;
- location/path;
- hash verification status;
- person responsible;
- notes.

Untuk proyek tim akademik, chain of custody berfungsi sebagai reproducibility dan integrity log, bukan klaim legal admissibility.

## 6. Validation setelah acquisition

Minimum gate:
- acquisition selesai tanpa error yang tidak terdokumentasi;
- hash tersedia untuk semua master outputs;
- working copy hash cocok;
- master tidak digunakan untuk analisis;
- device state akhir dicatat;
- perubahan yang disebabkan acquisition dicatat;
- limitation statement tersedia.

## 7. Handoff ke P4

Bela menerima **working copy** ACQ-001, bukan master.

Setiap artifact hasil extraction diberi `ART-#####` dan wajib mencatat:
- source ACQ ID;
- source path/object;
- extraction tool/script + version;
- extraction timestamp;
- artifact hash bila berupa file;
- row/object count;
- transformation notes.

## Limitation statement minimum

Laporan harus membedakan dengan tegas:
- synthetic scenario;
- test-device staging;
- acquisition method;
- acquired artifact;
- extraction/transformation;
- AI analysis.

Jangan menyimpulkan bahwa logical export merepresentasikan seluruh state internal WhatsApp/database bila metode tidak memperoleh data tersebut.
