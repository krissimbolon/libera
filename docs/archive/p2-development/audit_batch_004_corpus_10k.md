> **Status: Archived** · As of: 2026-09-23 · Original path: `docs/02_case_design/audit_batch_004_corpus_10k.md` · Canonical: No  
> Superseded by: [docs/02_case_design/laporan_qa_corpus_10000.md](../../02_case_design/laporan_qa_corpus_10000.md) and `data/adaptasi_indonesia/corpus_freeze_manifest.json`  
> Purpose: historical audit trail / provenance. Working record from P2 corpus construction (batch audits, handoffs, intermediate QA). The corpus was frozen on 2026-09-24; statuses such as "belum final" or "BELUM LULUS" describe intermediate states only. The content below is preserved unchanged from its last working version; relative links inside it may point to pre-archive locations.

# Audit batch 004 — corpus kerja 1.568 pesan

Status: **draf berlanjut**, belum memenuhi checkpoint 2.000.

Batch 004 menambah 397 pesan, terdiri atas 69 bridge, 258 context, dan 70 distractor. Corpus kumulatif: 500 `ADAPTED_FROM_GALLOWAY`, 312 `SYNTHETIC_BRIDGE`, 566 `SYNTHETIC_CONTEXT`, 190 `SYNTHETIC_DISTRACTOR`. Ada 169 conversation.

QA otomatis: 1.568 message ID unik; exact duplicate row 0; duplicate synthetic message text 0; timestamp collision per conversation 0; kandidat near-duplicate panjang 0; kebocoran nama utama sumber pada tambahan 0; anchor exact-match 500/500; tidak ada source line unresolved dijadikan anchor. Prose tambahan tidak dihasilkan oleh template skrip.

Review manual memutar ulang bridge 004 bersama seluruh anchor pada thread yang ditambah. Lima baris dihapus karena respons yang menyela sebab, pertanyaan akun yang memperumit urutan, atau pengulangan pembukaan. Sampel lintas thread memeriksa Kirana yang mulai kurang sehat 2 Juli sebelum meminta obat 3–4 Juli, Tania yang belum selesai membahas kepulangan, Nara yang tidak dipindahkan saat meminta selimut, dan Caca yang tidak dikirimi pesan baru setelah nomor terblokir pada 19 Juli.

QA semantik menyeluruh dan laporan final tetap tertunda. Empat conversation anchor campuran dan ketidakcocokan hash manifest masih menjadi temuan baseline yang tidak diubah. Batch berikutnya menuju komposisi checkpoint 2.000: 500/500/800/200.
