> **Status: Archived** · As of: 2026-09-23 · Original path: `docs/02_case_design/audit_batch_008.md` · Canonical: No  
> Superseded by: [docs/02_case_design/laporan_qa_corpus_10000.md](../../02_case_design/laporan_qa_corpus_10000.md) and `data/adaptasi_indonesia/corpus_freeze_manifest.json`  
> Purpose: historical audit trail / provenance. Working record from P2 corpus construction (batch audits, handoffs, intermediate QA). The corpus was frozen on 2026-09-24; statuses such as "belum final" or "BELUM LULUS" describe intermediate states only. The content below is preserved unchanged from its last working version; relative links inside it may point to pre-archive locations.

# Audit Batch 008 — 3.200 pesan

Total 3.200; komposisi 500/740/1.580/380; 288 conversation. Validator `src/libera_corpus_work.py` lulus: anchor 500 exact-match, ID unik, exact duplicate row/teks sintetis 0, collision timestamp per conversation 0, near-duplicate panjang 0, identity leakage 0.

Bridge R006, R007, R009–R012, R024, R041, R062, R113 ditinjau bersama anchor dan state tanggalnya. ID kontak awalnya salah di R007/R009/R010 dan diperbaiki sebelum gabung. Actor Nara sempat salah dipetakan menjadi Rena dalam draf context, juga diperbaiki. Chat netral Caca/Reza dipisah dari anchor yang mendesak. Context sengaja mencakup pesan tak berbalas dan jeda lebih panjang pada sebagian thread; tinjauan gaya menyeluruh masih harus dilaksanakan menjelang final.

Hash manifest yang berbeda dengan bytes anchor ter-commit tetap dicatat. Tidak ada perubahan file anchor; QA final belum selesai.
