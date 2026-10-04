> **Status: Archived** · As of: 2026-09-23 · Original path: `docs/02_case_design/audit_batch_005.md` · Canonical: No  
> Superseded by: [docs/02_case_design/laporan_qa_corpus_10000.md](../../02_case_design/laporan_qa_corpus_10000.md) and `data/adaptasi_indonesia/corpus_freeze_manifest.json`  
> Purpose: historical audit trail / provenance. Working record from P2 corpus construction (batch audits, handoffs, intermediate QA). The corpus was frozen on 2026-09-24; statuses such as "belum final" or "BELUM LULUS" describe intermediate states only. The content below is preserved unchanged from its last working version; relative links inside it may point to pre-archive locations.

# Audit Batch 005 — checkpoint 2.000

**Scope:** 432 pesan baru; 188 bridge, 234 context, 10 distractor. Commit checkpoint pada `p2-10k-work`.

- Validator `python src/libera_corpus_work.py`: total 2.000, target checkpoint 500/500/800/200; 194 conversation; 500 anchor exact-match; source line anchor terpetakan.
- Duplicate ID, row, teks sintetis, collision timestamp dalam conversation, near-duplicate panjang, identity leakage: 0.
- Review urutan bridge bersama anchor pada R015–R022, R034/R035/R038/R039, R043–R045, R047–R051, R058–R061, R064. Koreksi R043/R044/R047/R035 dan satu baris R017 untuk suara aktor; R018 tetap satu pasangan anonim tanpa menetapkan identitas.
- Review lintas chat: geser chat Reza tentang kacamata, Rena tentang air, dan makan siang Rena agar tidak menyerempet chat lain pada menit yang sama. Pesan pada chat lain yang berdekatan masih mungkin sebagai multitasking; audit kronologi menyeluruh tetap dibutuhkan saat corpus lengkap.
- Bahasa: percakapan baru berkisar pinjaman benda, makan, hujan, baterai, jadwal, pesanan, serta obrolan sosial. Sebagian thread context masih berirama panjang dan tertib; batch berikut harus mencampur fragmen singkat, jeda, dan pesan yang tidak selalu dibalas.
- Kesenjangan provenance: hash manifest tidak cocok dengan SHA file anchor yang memang sudah ada; jangan mengubah 500 anchor. QA final belum boleh dinyatakan selesai.
