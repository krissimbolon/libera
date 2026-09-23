# Instruksi Lanjutan Work — Selesaikan Corpus 10.000

Status awal:
- branch: `p2-10k-work`
- commit acuan: `b22405e19e30a0fa81cb80330422ea37a884c864`
- corpus kerja: 768/10.000
- komposisi: 500 anchor, 168 bridge, 70 context, 30 distractor
- 500 anchor immutable

## Tujuan

Lanjutkan pekerjaan secara mandiri sampai tepat 10.000 pesan dan QA final selesai.

Checkpoint 2.000, 4.000, 6.000, dan 8.000 tetap wajib dicatat dan di-commit, tetapi jangan berhenti untuk meminta konfirmasi pengguna setelah checkpoint. Setelah satu checkpoint lulus QA, lanjutkan langsung ke checkpoint berikutnya.

## Target kumulatif

| Checkpoint | Anchor | Bridge | Context | Distractor | Total |
|---|---:|---:|---:|---:|---:|
| 2.000 | 500 | 500 | 800 | 200 | 2.000 |
| 4.000 | 500 | 900 | 2.100 | 500 | 4.000 |
| 6.000 | 500 | 1.200 | 3.400 | 900 | 6.000 |
| 8.000 | 500 | 1.400 | 4.900 | 1.200 | 8.000 |
| 10.000 | 500 | 1.500 | 6.500 | 1.500 | 10.000 |

## Cara kerja

Kerjakan batch 400–800 pesan:
1. baca state conversation/aktor yang relevan;
2. tulis pesan sebagai rangkaian percakapan, bukan baris independen;
3. gabungkan ke corpus working;
4. jalankan validator otomatis;
5. lakukan spot-check manual;
6. perbaiki masalah;
7. commit;
8. lanjutkan batch berikutnya.

Script boleh dipakai untuk validasi, merge, hash, dan QA, tetapi prose percakapan jangan dibuat dengan template mekanis berulang.

## Continuity

Jaga:
- hubungan pesan sebelum/sesudah;
- pasangan percakapan;
- lokasi/state terakhir aktor;
- waktu dan urutan;
- topik yang belum selesai;
- konsistensi thread.

Jangan membuat pesan baru yang bertentangan dengan anchor berikutnya.

## Bahasa Indonesia

Gunakan gaya WhatsApp Indonesia yang natural dan tidak terlalu formal:
- variasi pesan pendek/panjang;
- bentuk seperti `nggak`, `udah`, `bentar`, `gimana`, `iya`, `oke`, `ntar`, `kasih tahu` bila cocok;
- sesekali singkatan atau typo ringan bila natural;
- jangan semua aktor terdengar sama;
- rewrite kalimat yang terasa seperti laporan atau AI.

## Variasi context

Context harus beragam: rutinitas harian, perjalanan, makanan/minuman, baterai/charger, keluarga, cuaca, kesehatan ringan, jadwal, koneksi, barang tertinggal, kendaraan, belanja kecil, dan percakapan sosial.

Hindari tema yang sama berulang terlalu banyak.

## Distractor

Distractor harus terasa natural dalam semesta aktor yang sama, tetapi tidak menjadi evidence utama dan tidak mengubah event utama yang sudah ditetapkan.

## Guardrail

- jangan menambah event utama baru;
- jangan menambah aktor inti baru;
- jangan mengubah outcome skenario;
- jangan mengubah 500 anchor;
- tetap gunakan konten yang aman dan disanitasi untuk aktor di bawah umur;
- jangan memasukkan detail operasional baru di luar yang dibutuhkan untuk simulasi forensik.

## QA wajib

Setiap checkpoint:
- total row;
- provenance counts;
- uniqueness message_id;
- exact duplicate row;
- exact duplicate synthetic message_text;
- timestamp collision;
- near-duplicate panjang;
- conversation count;
- source identity leakage;
- anchor exact match;
- chronology conflict;
- actor-state conflict;
- catatan continuity/gaya yang diperbaiki.

Jika QA gagal, perbaiki sebelum lanjut.

## Kondisi selesai

Pekerjaan baru selesai jika:
- total tepat 10.000;
- komposisi tepat 500/1.500/6.500/1.500;
- 10.000 message_id unik;
- exact duplicate row = 0;
- exact duplicate synthetic message_text = 0;
- 500 anchor tetap exact-match;
- chronology dan actor-state audit selesai;
- continuity dan language-style review selesai.

## Output final

Buat:
- `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`
- `data/adaptasi_indonesia/qa_corpus_10000.json`
- `docs/02_case_design/laporan_qa_corpus_10000.md`
- update `docs/02_case_design/log_progres_generasi_10000.md`

Commit seluruh hasil final ke `p2-10k-work`.

Jangan merge ke `main` atau `proyek-uas-df`.

Berhenti hanya setelah final 10.000 + QA committed, atau bila ada blocker nyata yang memerlukan keputusan pengguna.
