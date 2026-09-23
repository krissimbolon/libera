# MULAI DI SINI — Meldiro / P6–P7

## Tujuan saat Work 10k berjalan
Bangun pipeline AI yang siap menerima hasil ekstraksi forensik nanti, tanpa melihat ground truth dan tanpa memakai court record sebagai evidence RAG.

## Kerjakan berurutan

1. Rekam environment:
   - OS;
   - CPU/RAM/GPU;
   - Python;
   - Ollama;
   - package versions.

2. Pilih kandidat model lokal:
   - minimal 2 kandidat;
   - catat model tag/digest, quantization, context window.

3. Pilih embedding model dan vector store.

4. Definisikan schema chunk:
   - chunk_id;
   - evidence_id;
   - conversation_id;
   - start/end timestamp;
   - message IDs;
   - source/provenance.

5. Buat chunking berbasis:
   - conversation;
   - time window;
   - target 30–60 pesan;
   - bukan fixed 500-row.

6. Buat retrieval harness:
   - top-k;
   - score;
   - retrieved chunk IDs;
   - evidence citations.

7. Buat runner eksperimen:
   - A: LLM-only;
   - B: LLM + RAG;
   - C: LLM + RAG + structured reasoning.

8. Log tiap run:
   - RUN-ID;
   - model;
   - prompt;
   - retrieved context;
   - parameters;
   - output;
   - timestamp.

9. Uji dengan toy/sanitized sample saja.

## Jangan dilakukan sekarang
- jangan pakai ground truth;
- jangan masukkan Document 547 ke evidence RAG;
- jangan eksperimen final sebelum P4 selesai.

## Definition of Done
Pipeline berjalan end-to-end pada sample, semua run reproducible, retrieval dapat ditelusuri ke evidence ID.
