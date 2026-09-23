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
