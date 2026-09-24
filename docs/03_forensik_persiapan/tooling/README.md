# Tooling

Catat di sini:
- nama tool;
- versi;
- sumber resmi;
- fungsi;
- command/parameter yang digunakan;
- keputusan pemilihan;
- limitation.

Tool final belum dikunci sampai inventaris workstation dan perangkat uji selesai.


## Status awal ADB pada workstation

Percobaan awal:
`adb devices`

Hasil:
PowerShell mengembalikan `CommandNotFoundException` / `adb is not recognized`.

Interpretasi sementara:
- ADB belum terpasang, atau
- Android Platform Tools sudah ada tetapi foldernya belum masuk `PATH`.

Tindakan berikut:
- verifikasi apakah `adb.exe` sudah ada di workstation;
- jika belum, gunakan Android SDK Platform Tools dari sumber resmi;
- dokumentasikan versi ADB sebelum dipakai untuk verifikasi perangkat.


## Verifikasi keberadaan ADB

Pencarian `adb.exe` pada drive C: tidak menghasilkan temuan.

Kesimpulan:
- Android SDK Platform Tools belum tersedia pada workstation ini.
- Tahap berikut adalah memasang paket resmi Android SDK Platform Tools untuk Windows dan mencatat versi `adb` setelah instalasi.


## Android Debug Bridge (ADB)

- Tool: Android Debug Bridge
- Version protocol: **1.0.41**
- Platform Tools build: **37.0.1-15733141**
- Executable: `C:\platform-tools\platform-tools\adb.exe`
- Runtime OS string: **Windows 10.0.26200**
- Sumber: Android SDK Platform Tools resmi
- Status: **terpasang dan berhasil dijalankan**
- Verifikasi: `.\adb.exe version` berhasil tanpa error


## Verifikasi koneksi ADB ke perangkat

Percobaan awal `.\adb.exe devices`:
- daemon ADB berhasil berjalan pada tcp:5037;
- perangkat terdeteksi;
- status koneksi: **unauthorized**.

Interpretasi:
- koneksi USB dan deteksi ADB sudah berfungsi;
- workstation belum diotorisasi oleh perangkat Android untuk sesi debugging;
- identitas/serial perangkat tidak dicatat di repositori publik.

Tindakan berikut:
- otorisasi RSA debugging dari layar perangkat;
- ulangi `.\adb.exe devices` hingga status menjadi `device`.


### Otorisasi ADB
- Status setelah otorisasi RSA pada perangkat: **device**
- Koneksi ADB workstation ↔ perangkat: **berhasil**
- Serial/identifier perangkat: **tidak dicatat di repositori publik**


### Pemeriksaan privilege ADB
- Command: `.\adb.exe shell id`
- Hasil utama: `uid=2000(shell) gid=2000(shell)`
- SELinux context: `u:r:shell:s0`
- Interpretasi: shell ADB tidak berjalan sebagai root.
- Pemeriksaan `su` tetap diperlukan untuk memastikan tidak ada binary/root manager tersembunyi yang dapat memberi privilege root.


### Verifikasi `su`
- Command: `.\adb.exe shell su -c id`
- Hasil: `/system/bin/sh: su: inaccessible or not found`
- Kesimpulan operasional: tidak ditemukan akses `su` dari ADB shell; bersama hasil `uid=2000(shell)` dan ketiadaan Magisk/SuperSU/KernelSU, baseline perangkat dicatat sebagai **tidak ada indikasi root**.


## PowerShell Get-FileHash

- Tool: `Get-FileHash`
- Module: `Microsoft.PowerShell.Utility`
- Module version: **3.1.0.0**
- Command type: **Function**
- Planned algorithm: **SHA-256**
- Status: **tersedia dan siap diuji**
- Peran: hashing baseline untuk evidence, working copy, dan dry-run dummy.


## Kandidat acquisition tool untuk Android/WhatsApp

### Rekomendasi utama (belum dikunci)
**Oxygen Forensic® Detective — Device Extractor / Android Agent**

Alasan:
- perangkat uji LIBERA adalah Android 16 non-root;
- kebutuhan P3 adalah logical acquisition yang terdokumentasi dan reproducible;
- Android Agent saat ini mendukung Android OS 5–16;
- dokumentasi vendor menyatakan dukungan app extraction untuk WhatsApp/WhatsApp Business via USB/Wi-Fi;
- workflow acquisition terstruktur dan cocok untuk perangkat unlocked.

Status:
- **RECOMMENDED CANDIDATE — belum dipasang/dikunci**
- versi exact dan lisensi/trial harus dicatat saat instalasi.

### Mengapa tool dari paper tidak langsung dipilih
Paper Suvarna et al. (2024) menyebut FTK Imager, Autopsy, The Sleuth Kit, dd, CAINE, Memoryze, LiME, dan EnCase. LiME secara eksplisit disebut untuk Full Android Memory acquisition, tetapi untuk perangkat LIBERA saat ini tidak dipilih karena baseline harus non-root/non-invasive dan Android 16 modern tidak cocok untuk workflow LiME tanpa perubahan low-level pada perangkat.

FTK Imager / Autopsy / The Sleuth Kit akan diperlakukan terutama sebagai tool imaging/analysis atas artefak hasil acquisition, bukan sebagai primary direct acquisition tool untuk WhatsApp internal pada Android 16.

### Fallback bila Oxygen tidak tersedia
Gunakan ADB untuk logical collection yang memang dapat diakses, ditambah artefak ekspor WhatsApp sebagai validation artefact, dengan limitation yang dinyatakan eksplisit. Jangan mengklaim full-file-system atau protected WhatsApp database acquisition dari ADB biasa.


## Tool acquisition dipilih

**Primary acquisition tool: Oxygen Forensic® Detective → Device Extractor → Android Agent**

Status keputusan: **DIPILIH untuk workflow P3 LIBERA**.

Rationale:
- perangkat uji adalah Android 16, unlocked, non-root;
- target acquisition adalah logical/selective collection yang terdokumentasi;
- Android Agent berjalan sebagai aplikasi user-level/unprivileged;
- mendukung logical extraction via USB/Wi-Fi;
- mendukung WhatsApp sebagai supported app extraction pada workflow Android Agent;
- tidak diklaim sebagai full-file-system extraction;
- hasil acquisition tetap akan dipreservasi sebagai master evidence, di-hash SHA-256, lalu diperiksa dari working copy.

Batasan yang wajib dicantumkan:
- Android Agent memasang aplikasi pada perangkat sehingga terjadi perubahan state terkontrol;
- Android Agent tidak memberi akses penuh ke internal memory / seluruh protected application files;
- full file system/physical extraction adalah metode berbeda dan tidak akan diklaim bila tidak dilakukan.

Versi exact Oxygen Forensic Detective dan Android Agent: **BELUM DICATAT — isi setelah trial/install berhasil**.
