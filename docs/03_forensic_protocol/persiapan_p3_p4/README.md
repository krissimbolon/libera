# Persiapan P3–P4 Forensik Digital

Folder ini berisi artefak publik/aman untuk persiapan penyitaan, akuisisi, hashing, chain of custody, dry-run, dan tooling sebelum corpus 10.000 pesan LIBERA dikunci.

## Struktur

- `inventaris_perangkat/` — inventaris HP uji dan workstation.
- `sop_akuisisi/` — SOP pra-akuisisi, master evidence, working copy, dan akuisisi.
- `template_chain_of_custody/` — template pencatatan perpindahan evidence, acquisition log, evidence inventory, dan hash manifest.
- `dry_run/` — dokumentasi uji alur dengan data dummy.
- `tooling/` — daftar tool, versi, command, dan keputusan pemilihan tool.

## Batas publik/private

Jangan commit ke repo publik:
- raw acquisition;
- forensic image;
- data WhatsApp nyata;
- nomor telepon pribadi;
- IMEI/serial sensitif;
- akun/SIM pribadi;
- token/kredensial;
- ground truth privat.

Artefak privat disimpan di luar repo pada storage evidence lokal.
