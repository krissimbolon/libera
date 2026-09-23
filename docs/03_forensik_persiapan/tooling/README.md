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
