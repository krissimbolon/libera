# MULAI DI SINI — Chris / P3–P4

## Tujuan saat Work 10k berjalan
Siapkan seluruh prosedur forensik agar setelah corpus 10.000 LOCKED, perangkat uji dapat langsung disimulasikan, diakuisisi, di-hash, dan diekstrak tanpa mengubah metodologi di tengah jalan.

## Kerjakan berurutan

1. Lengkapi inventaris perangkat uji:
   - OPPO CPH2819;
   - kapasitas storage;
   - versi WhatsApp;
   - akun/SIM uji;
   - timezone;
   - status root;
   - sinkronisasi jam;
   - status jaringan.

2. Lengkapi workstation:
   - edition/build Windows;
   - Python;
   - hashing tool;
   - tool acquisition;
   - tool extraction;
   - versi tool.

3. Buat SOP pra-akuisisi:
   - foto/dokumentasi kondisi perangkat;
   - waktu perangkat;
   - network state;
   - power state;
   - evidence ID;
   - siapa menyerahkan/menerima.

4. Buat template:
   - chain of custody;
   - acquisition log;
   - hash manifest;
   - evidence inventory;
   - master-copy / working-copy register.

5. Dry-run dengan data dummy:
   - jangan gunakan corpus final;
   - uji alur hashing;
   - uji copy master/working;
   - pastikan hash sebelum/sesudah copy identik.

6. Siapkan rencana injeksi/simulasi corpus:
   - jangan jalankan final sebelum 10k LOCKED;
   - dokumentasikan akun pengirim/penerima uji;
   - buat urutan replay chat yang reproducible.

## Jangan dilakukan sekarang
- jangan reset/root perangkat;
- jangan akuisisi final;
- jangan mengubah corpus 10k;
- jangan merge ke main.

## Definition of Done
Semua template dan SOP siap, dry-run berhasil, hashing tervalidasi, dan perangkat siap menerima simulasi setelah P2 selesai.
