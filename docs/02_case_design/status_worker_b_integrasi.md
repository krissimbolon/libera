# Status Worker B — Pemeriksaan Integrasi

Pemeriksaan branch `p2-paralel-b` pada 2026-09-23 menemukan:

- file: `data/adaptasi_indonesia/batch_anchor_b.csv`
- jumlah baris saat diperiksa: **89**
- rentang source line yang sudah ada: **272–360**
- target Worker B: seluruh source line terpetakan pada rentang 272–543
- status: **BELUM SIAP MERGE**

Jangan merge ke `proyek-uas-df` sampai Worker B menyelesaikan seluruh subset input dan QA-nya.

Integrasi final akan memeriksa:
- jumlah total anchor A+B = 500;
- collision message_id;
- collision source_original_line;
- schema drift;
- duplicate / near-duplicate;
- konsistensi actor ID;
- konsistensi timestamp dan conversation ID;
- provenance dan lokalisasi.
