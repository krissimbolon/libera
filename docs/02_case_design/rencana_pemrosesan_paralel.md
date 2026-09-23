# Rencana Pemrosesan Paralel P2

Mulai P2, pekerjaan yang dapat dipisahkan akan dikerjakan secara paralel untuk mempercepat produksi tanpa mengorbankan provenance dan QA.

## Struktur kerja

- Branch integrasi/canonical: `proyek-uas-df`
- Worker A: `p2-paralel-a`
- Worker B: `p2-paralel-b`

Branch worker tidak boleh mengubah file canonical yang sama secara bersamaan. Hasil worker digabung setelah lolos pemeriksaan skema, duplicate audit, dan consistency review.

## Pembagian Batch A — 500 anchor

### Worker A — ChatGPT utama
Lingkup:
- `source_original_line` 1–271
- hanya line yang sudah berstatus terpetakan
- transformasi ke Bahasa Indonesia
- lokalisasi aktor/lokasi sesuai peta yang sudah dikunci
- pertahankan substansi event
- simpan provenance

Output:
`data/adaptasi_indonesia/batch_anchor_a.csv`

### Worker B — ChatGPT kedua
Lingkup:
- `source_original_line` 272–543
- hanya line yang sudah berstatus terpetakan
- aturan transformasi sama dengan Worker A
- tidak mengisi unresolved lines
- tidak membuat bridge/context/distractor pada tahap ini

Output:
`data/adaptasi_indonesia/batch_anchor_b.csv`

## Identifier deterministik

Untuk mencegah collision antarworker:

- `message_id = ID-GAL-<source_original_line 4 digit>`
- contoh line 94 → `ID-GAL-0094`
- `transformation_id = TR-GAL-ID-<source_original_line 4 digit>`

Satu source line menghasilkan tepat satu anchor.

## Aturan transformasi anchor

1. Bahasa Indonesia harus natural, bukan terjemahan kata-per-kata.
2. Makna forensik dari pesan sumber tidak boleh berubah.
3. Nama, nomor, lokasi, mata uang, hotel, dan platform dilokalisasi sesuai dokumen peta lokalisasi.
4. Jika pesan sumber sangat pendek, pesan adaptasi juga boleh pendek.
5. Jangan menambah fakta baru.
6. Jangan memperhalus pesan sehingga signal evidentiary hilang.
7. Untuk aktor di bawah umur, hindari konten seksual eksplisit; pertahankan signal forensik melalui wording yang aman.
8. `source_provenance` untuk anchor selalu `ADAPTED_FROM_GALLOWAY`.
9. `source_original_line` wajib terisi.
10. Unresolved source lines tetap kosong dan tidak boleh ditebak.

## Kontrak skema

Kolom wajib:
`message_id,conversation_id,timestamp,sender_id,recipient_id,message_text,message_type,reply_to_message_id,attachment_id,source_provenance,source_original_line,transformation_id`

Kolom tambahan worker tidak boleh dibuat tanpa kesepakatan terlebih dahulu.

## QA setelah merge

Setelah kedua batch tersedia:
- gabungkan A + B;
- assert 500 baris;
- assert `message_id` unik;
- assert `source_original_line` unik;
- assert tidak ada unresolved line yang masuk;
- exact duplicate check;
- near-duplicate check;
- actor mapping check;
- location mapping check;
- manual spot-check minimal 10% dari masing-masing worker;
- hash dataset hasil merge.

## Pembagian tahap berikutnya

Setelah 500 anchor terkunci:
- Worker A: bridge + continuity;
- Worker B: context + distractor;
- integrator: duplicate audit, chronology, leakage, dan final 10.000-row merge.

Dengan pola ini, dua akun dapat bekerja sekaligus tanpa menulis bagian data yang sama.
