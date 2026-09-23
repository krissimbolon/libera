# Handoff Lanjutan dari Checkpoint 4.000 ke 10.000

Branch aktif: `p2-10k-work`

Head saat handoff: `da66ca09a693e333954edac75b88301b901a58a2`

## State sekarang
- Total: 4.000/10.000
- Anchor: 500
- Bridge: 900
- Context: 2.100
- Distractor: 500
- Conversation: 353
- Checkpoint 2.000: LULUS QA
- Checkpoint 4.000: LULUS QA struktural
- Checkpoint 6.000: DALAM PROSES

## QA struktural checkpoint 4.000
- message_id unik: 4.000/4.000
- exact duplicate row: 0
- exact duplicate synthetic message_text: 0
- timestamp collision per conversation: 0
- near-duplicate panjang: 0
- source identity leakage: 0
- anchor exact-match: 500/500

## Isu gaya yang harus diperbaiki sambil lanjut
Audit commit `da66ca0` menunjukkan percakapan sintetis masih terlalu rapi:
- anchor <=3 kata: 163/500
- bridge <=3 kata: 20/900
- context <=3 kata: 89/2.100 setelah koreksi
- distractor <=3 kata: 35/500 setelah koreksi
- 107 context conversation masih tepat 10 pesan
- 44 distractor conversation masih tepat 10 pesan

Arah perbaikan:
- lebih banyak fragmen pendek;
- double text;
- unanswered message;
- jeda;
- typo/singkatan ringan yang natural;
- panjang thread bervariasi;
- jangan semua thread ditutup rapi;
- jangan semua aktor terdengar sama.

## Target selanjutnya
Checkpoint 6.000:
- 500 anchor
- 1.200 bridge
- 3.400 context
- 900 distractor

Checkpoint 8.000:
- 500 anchor
- 1.400 bridge
- 4.900 context
- 1.200 distractor

Final 10.000:
- 500 anchor
- 1.500 bridge
- 6.500 context
- 1.500 distractor

## Dokumen wajib dibaca
- `docs/02_case_design/instruksi_lanjut_sampai_10000.md`
- `docs/02_case_design/handoff_work_10000_pesan.md`
- `docs/02_case_design/kontrak_gaya_percakapan.md`
- `docs/02_case_design/kontrak_ekspansi_9500_pesan.md`
- `docs/02_case_design/peta_kronologi_generasi.md`
- `docs/02_case_design/ledger_kontinuitas_aktor_10k.md`
- `docs/02_case_design/audit_gaya_4000.md`
- `docs/02_case_design/log_progres_generasi_10000.md`

## Larangan penting
- jangan ubah 500 anchor;
- jangan merge ke `main`;
- jangan merge ke `proyek-uas-df`;
- jangan gunakan snapshot di `main` sebagai source of truth;
- jangan berhenti hanya di 6k atau 8k;
- jangan menghasilkan teks dengan template mekanis.

## Catatan Git
PR #11 pernah salah di-merge dari `p2-10k-work` ke `main`. Abaikan snapshot `main` sebagai sumber kebenaran. Lanjutkan hanya dari branch `p2-10k-work`.

## Kondisi selesai
Baru berhenti setelah:
- tepat 10.000 pesan;
- komposisi tepat 500/1500/6500/1500;
- QA final selesai;
- output final dibuat:
  - `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`
  - `data/adaptasi_indonesia/qa_corpus_10000.json`
  - `docs/02_case_design/laporan_qa_corpus_10000.md`
  - log progres final diperbarui.
