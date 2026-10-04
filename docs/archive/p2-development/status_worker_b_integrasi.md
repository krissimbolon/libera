> **Status: Archived** · As of: 2026-09-23 · Original path: `docs/02_case_design/status_worker_b_integrasi.md` · Canonical: No  
> Superseded by: [docs/02_case_design/laporan_qa_corpus_10000.md](../../02_case_design/laporan_qa_corpus_10000.md) and `data/adaptasi_indonesia/corpus_freeze_manifest.json`  
> Purpose: historical audit trail / provenance. Working record from P2 corpus construction (batch audits, handoffs, intermediate QA). The corpus was frozen on 2026-09-24; statuses such as "belum final" or "BELUM LULUS" describe intermediate states only. The content below is preserved unchanged from its last working version; relative links inside it may point to pre-archive locations.

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
