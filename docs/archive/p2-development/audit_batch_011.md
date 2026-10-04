> **Status: Archived** · As of: 2026-09-23 · Original path: `docs/02_case_design/audit_batch_011.md` · Canonical: No  
> Superseded by: [docs/02_case_design/laporan_qa_corpus_10000.md](../../02_case_design/laporan_qa_corpus_10000.md) and `data/adaptasi_indonesia/corpus_freeze_manifest.json`  
> Purpose: historical audit trail / provenance. Working record from P2 corpus construction (batch audits, handoffs, intermediate QA). The corpus was frozen on 2026-09-24; statuses such as "belum final" or "BELUM LULUS" describe intermediate states only. The content below is preserved unchanged from its last working version; relative links inside it may point to pre-archive locations.

# Audit Batch 011 — 4.650

**Kumulatif:** 4.650 pesan, 393 conversation; 500 ADAPTED_FROM_GALLOWAY, 1.000 SYNTHETIC_BRIDGE, 2.530 SYNTHETIC_CONTEXT, 620 SYNTHETIC_DISTRACTOR.

QA struktural lulus: message_id unik 4.650/4.650, exact duplicate row 0, duplicate synthetic message_text 0, collision timestamp dalam conversation 0, near-duplicate panjang 0, source identity leakage 0, anchor exact-match 500/500. Empat baseline mixed conversation tidak disentuh.

**Continuity spot-check:** bridge direplay bersama anchor pada R029, R030, R031, R036, R043, R044, R045, R047, R048, R049, R050, R051, R058, R060, R061, R063, R064, R066, R068, dan R071. Tambahan hanya mengisi jeda komunikasi, kesiapan, benda sehari-hari, baterai/sinyal, dan respons pendek; tidak mengubah event atau outcome anchor. Context/distractor baru tetap berpasangan dengan Raka dan tidak membuat aktor mengetahui informasi yang belum diterima. Jihan hanya mendapat chat keluarga/Wi-Fi netral; tidak ada konten seksual eksplisit. Caca tidak diperpanjang setelah baseline pemblokiran 19 Juli.

**Perbaikan gaya:** 30 conversation context yang sebelumnya tepat 10 pesan diperpanjang dengan callback pendek sehingga distribusi panjang mulai pecah. Batch baru memuat 92/100 bridge, 336/430 context, dan 89/120 distractor dengan panjang <=3 kata; fragmen, double-text, typo ringan, respons tidak selalu berpasangan, dan akhir thread yang tidak selalu rapi ditulis sebagai bagian continuity, bukan hasil pemotongan massal.

**Batasan terbuka:** audit lintas-aktor penuh tetap dilakukan lagi pada checkpoint 6.000. Discrepancy hash manifest anchor dipertahankan sebagai isu provenance; anchor tidak diubah.
