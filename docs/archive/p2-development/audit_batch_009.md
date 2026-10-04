> **Status: Archived** · As of: 2026-09-23 · Original path: `docs/02_case_design/audit_batch_009.md` · Canonical: No  
> Superseded by: [docs/02_case_design/laporan_qa_corpus_10000.md](../../02_case_design/laporan_qa_corpus_10000.md) and `data/adaptasi_indonesia/corpus_freeze_manifest.json`  
> Purpose: historical audit trail / provenance. Working record from P2 corpus construction (batch audits, handoffs, intermediate QA). The corpus was frozen on 2026-09-24; statuses such as "belum final" or "BELUM LULUS" describe intermediate states only. The content below is preserved unchanged from its last working version; relative links inside it may point to pre-archive locations.

# Audit Batch 009 — 3.600 pesan

`python src/libera_corpus_work.py`: total 3.600; provenance 500/820/1.840/440; 320 conversation. Seluruh anchor 500 exact-match; duplicate ID/baris/teks sintetis, collision timestamp conversation, near-duplicate panjang, dan kebocoran identitas sumber 0.

Review manual: R001/R002 tidak mengubah informasi Maya yang belum terverifikasi atau menghasilkan penemuan; R032/R037, P34-XX/P34-YY, R105, R100, R113, R041 melanjutkan state tanpa outcome utama. Kalimat bridge identik antarchat direvisi. Dua chat Dini pada jam sama dan kedekatan beberapa chat Raka diperbaiki dengan pergeseran waktu, tanpa menyentuh anchor.

Masih ada risiko ritme dialog netral cenderung teratur. Keputusan selanjutnya: tambah fragmen dan jeda, lakukan audit lintas tanggal saat seluruh corpus lengkap. Hash manifest jangkar yang berbeda tetap terbuka.
