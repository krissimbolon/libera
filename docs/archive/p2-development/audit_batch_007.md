> **Status: Archived** · As of: 2026-09-23 · Original path: `docs/02_case_design/audit_batch_007.md` · Canonical: No  
> Superseded by: [docs/02_case_design/laporan_qa_corpus_10000.md](../../02_case_design/laporan_qa_corpus_10000.md) and `data/adaptasi_indonesia/corpus_freeze_manifest.json`  
> Purpose: historical audit trail / provenance. Working record from P2 corpus construction (batch audits, handoffs, intermediate QA). The corpus was frozen on 2026-09-24; statuses such as "belum final" or "BELUM LULUS" describe intermediate states only. The content below is preserved unchanged from its last working version; relative links inside it may point to pre-archive locations.

# Audit Batch 007 — 2.800 pesan

`python src/libera_corpus_work.py` setelah merge: 2.800 pesan, 256 conversation, komposisi 500/660/1.320/320, 500 anchor exact-match, seluruh source line anchor terpetakan; duplicate ID/row/teks sintetis, collision timestamp per conversation, near-duplicate panjang, serta identitas sumber bocor semuanya 0.

Bridge disandingkan kronologis dengan anchor R063, R065, R066, R068, R069, R071, R075, R090, R091, R092. Dialog Jihan tidak melampaui percakapan keluarga dan jadwal penjemputan. Konflik Kirana dan Tania dibiarkan terbuka. Pengecekan lintas chat menggeser mesin cuci Reza, selimut Rena, dan kiriman Dini sehingga tidak terlalu bertabrakan dengan chat lain.

Risiko gaya tersisa: sebagian dialog context masih penuh jawaban segera dan penutup rapi. Tindak lanjut pada batch berikutnya: variasikan panjang, sisipkan pesan tak terjawab dan jeda alami. Hash manifest anchor lama yang berbeda tetap tercatat tanpa mengubah file anchor. QA final belum selesai.
