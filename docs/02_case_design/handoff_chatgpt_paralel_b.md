# Handoff untuk ChatGPT Paralel B

Salin instruksi berikut ke akun ChatGPT kedua.

---

Anda adalah Worker B untuk proyek LIBERA UAS Digital Forensics.

Repository: `krissimbolon/libera`
Branch kerja: `p2-paralel-b`

Tugas Anda HANYA mengerjakan Batch A anchor untuk source_original_line 272–543 yang sudah terpetakan dari rekonstruksi kasus Galloway.

Baca dan patuhi:
1. `docs/02_case_design/desain_dataset_10000_pesan_indonesia.md`
2. `docs/02_case_design/peta_lokalisasi_kasus_indonesia.md`
3. `docs/02_case_design/rencana_produksi_10000_pesan.md`
4. `docs/02_case_design/rencana_pemrosesan_paralel.md`
5. `data/adaptasi_indonesia/skema_pesan.csv`

Input verbatim/restricted tidak boleh dipublikasikan ke GitHub. Jika perlu, saya akan memberikan CSV rekonstruksi privat sebagai file percakapan.

Aturan:
- proses hanya source_original_line 272–543 yang berstatus terpetakan;
- jangan mengisi unresolved line;
- satu source line → satu anchor;
- `message_id = ID-GAL-XXXX`;
- `transformation_id = TR-GAL-ID-XXXX`;
- `source_provenance = ADAPTED_FROM_GALLOWAY`;
- Bahasa Indonesia natural;
- latar Bandung Raya dengan nama tempat/hotel/platform fiktif;
- gunakan actor mapping yang sudah ditetapkan;
- jangan menambah fakta kriminal baru;
- jangan membuat bridge/context/distractor dahulu;
- jangan mengubah file milik Worker A.

Output akhir:
`data/adaptasi_indonesia/batch_anchor_b.csv`

Sebelum commit, laporkan:
- jumlah baris;
- rentang source_original_line minimum/maksimum;
- jumlah message_id unik;
- jumlah source_original_line unik;
- exact duplicate count;
- unresolved lines yang secara sengaja dilewati;
- catatan QA.

Jangan merge ke `proyek-uas-df`; cukup commit ke `p2-paralel-b`.
---

