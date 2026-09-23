# Handoff P2 — Worker Konteks dan Distraktor

Branch kerja: `p2-konteks-distraktor`

Baca sebelum mulai:
- `docs/02_case_design/kontrak_ekspansi_9500_pesan.md`
- `docs/02_case_design/peta_kronologi_generasi.md`
- `docs/02_case_design/peta_lokalisasi_kasus_indonesia.md`
- `data/adaptasi_indonesia/anchor_indonesia_500.csv`
- `data/adaptasi_indonesia/registri_aktor_indonesia.csv`

## Tugas worker ini

### Context B
Buat **3.250** pesan:
- ID: `ID-CTX-B-0001` s.d. `ID-CTX-B-3250`
- provenance: `SYNTHETIC_CONTEXT`

### Distractor
Buat **1.500** pesan:
- ID: `ID-DST-0001` s.d. `ID-DST-1500`
- provenance: `SYNTHETIC_DISTRACTOR`

Total worker: **4.750 pesan**.

Kerjakan dalam file batch maksimum 500 baris agar mudah diaudit. Jangan merge ke `main` atau `proyek-uas-df`; commit hanya ke branch ini.

Aturan wajib:
- source_original_line kosong;
- jangan mengubah 500 anchor;
- exact duplicate message_text pada pesan baru = 0;
- jangan membuat korban utama/tindak pidana utama/outcome baru;
- tetap di semesta Bandung Raya fiktif;
- actor-state dan kronologi mengikuti peta generasi;
- konten aktor di bawah umur tidak seksual eksplisit;
- hindari template copy-paste;
- buat QA per batch: jumlah, uniqueness ID/text, chronology, actor consistency, leakage, near-duplicate.

Setelah selesai, laporkan semua nama file, jumlah baris per file, total 4.750, dan hasil QA.
