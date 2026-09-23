# Inventaris Perangkat Uji — P3

Diperbarui: 2026-09-23

## Identitas perangkat

- Model: OPPO CPH2819
- Sistem operasi: Android 16
- Build: CPH2819_16.0.5.1201 (EX01B110P02)
- Kernel: 5.15.197
- RAM: 6 GB
- Storage total: **128 GB**
- Storage terpakai: **115 GB**
- Storage tersedia: **±13 GB**

## Versi WhatsApp

- Aplikasi: WhatsApp Messenger
- Versi: **2.26.36.74**

## Waktu dan timezone

- Time zone: **GMT+07:00 / Jakarta**
- Set time automatically: **ON**
- Set time zone automatically: **ON**
- Sinkronisasi jam perangkat vs workstation: **selisih 1 detik (LULUS verifikasi awal)**

## Developer options dan debugging

- Developer options: **ON**
- USB debugging: **ON**
- Catatan: kondisi ini sudah aktif sebelum verifikasi ADB pada sesi P3 ini.

## Status jaringan baseline

- Wi-Fi: **ON**
- Mobile data: **ON**
- Bluetooth: **ON**
- Airplane mode: **OFF**
- Status koneksi Wi-Fi aktif/terhubung: BELUM DICATAT

## Status root

- Magisk: **tidak ada**
- SuperSU: **tidak ada**
- KernelSU: **tidak ada**
- Kesimpulan sementara: **tidak ada indikasi root manager yang terlihat dari daftar aplikasi**.
- Verifikasi teknis via ADB: **BELUM DILAKUKAN**.

## Status akun WhatsApp

- Pengguna memiliki 2 akun WhatsApp aktif.
- Kedua akun masih digunakan untuk kebutuhan nyata/personal.
- Keputusan sementara: **jangan gunakan kedua akun aktif tersebut untuk simulasi LIBERA**.
- Preferensi metodologis: gunakan nomor/akun WhatsApp khusus penelitian pada perangkat uji atau perangkat khusus terpisah.
- Keputusan final akun uji: BELUM DIKUNCI.

## Item yang masih harus diverifikasi

- versi WhatsApp: **WhatsApp Messenger 2.26.36.74**;
- akun/SIM uji final;
- timezone perangkat: **GMT+07:00 / Jakarta; automatic time ON; automatic timezone ON**;
- sinkronisasi jam perangkat vs workstation;
- status root: **tidak ada Magisk/SuperSU/KernelSU; verifikasi ADB belum dilakukan**;
- status jaringan: **Wi-Fi ON; mobile data ON; Bluetooth ON; airplane mode OFF**;
- USB debugging;
- battery/power state awal;
- kapasitas penyimpanan yang akan dikosongkan sebelum simulasi final.

## Catatan risiko storage

Sisa ±13 GB cukup untuk tahap persiapan dan corpus teks, tetapi dinilai terlalu sempit untuk workflow forensik yang mungkin melibatkan media, cache, backup, log, dan akuisisi. Sebelum simulasi final, targetkan ruang kosong yang lebih longgar dan dokumentasikan perubahan storage.
