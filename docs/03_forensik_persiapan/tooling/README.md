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
