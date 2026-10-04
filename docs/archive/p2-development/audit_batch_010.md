> **Status: Archived** · As of: 2026-09-23 · Original path: `docs/02_case_design/audit_batch_010.md` · Canonical: No  
> Superseded by: [docs/02_case_design/laporan_qa_corpus_10000.md](../../02_case_design/laporan_qa_corpus_10000.md) and `data/adaptasi_indonesia/corpus_freeze_manifest.json`  
> Purpose: historical audit trail / provenance. Working record from P2 corpus construction (batch audits, handoffs, intermediate QA). The corpus was frozen on 2026-09-24; statuses such as "belum final" or "BELUM LULUS" describe intermediate states only. The content below is preserved unchanged from its last working version; relative links inside it may point to pre-archive locations.

# Audit Batch 010 — checkpoint 4.000

**Kumulatif:** 4.000 pesan, 353 conversation; tepat 500 ADAPTED_FROM_GALLOWAY, 900 SYNTHETIC_BRIDGE, 2.100 SYNTHETIC_CONTEXT, 500 SYNTHETIC_DISTRACTOR. Validator `python src/libera_corpus_work.py` lulus dengan ID unik 4.000/4.000, exact duplicate row 0, duplikat teks sintetis 0, collision waktu dalam conversation 0, near-duplicate panjang 0, identity leakage 0, anchor exact-match 500/500.

Bridge diperiksa bersama anchor R048–R051, R058/R060/R061, R070, R093, R095. Jihan tetap pada state rumah ibunya sampai akhir potongan yang ditinjau; tidak ada klaim penjemputan selesai. Percakapan Rena mengisi perbedaan waktu dan lokasi tanpa mengganti anchor. Review lintas conversation memindahkan context Rena yang berbenturan dengan instruksi anchor R045, memisahkan lima overlap Dini, dan menjauhkan chat netral Raka dari pesan Bagas. Potongan setelah koreksi tidak menunjukkan konflik state/kronologi baru; audit semua pesan lintas aktor tetap tugas final.

**Batasan terbuka:** empat conversation anchor dengan pasangan campur tetap baseline yang tidak diubah; SHA manifest anchor lama berbeda dari bytes file anchor committed; sejumlah dialog netral tetap terdengar lebih rapi dibanding WhatsApp asli. Batch menuju 6.000 perlu memperbaiki variasi ritme. Berkas kerja belum corpus final.
