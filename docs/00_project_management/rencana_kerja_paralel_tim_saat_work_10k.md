# Rencana Kerja Paralel Tim Saat Work Membangun Corpus 10.000

Tanggal: 2026-09-23

Tujuan: memanfaatkan waktu empat anggota tanpa mengganggu branch `p2-10k-work`.

## Aturan umum

- Branch canonical proyek tetap `proyek-uas-df`.
- Branch Work 10k tetap `p2-10k-work`.
- Tidak ada anggota yang mengedit corpus 10k selama Work sedang berjalan.
- Jangan merge ke `main`.
- Hasil tiap anggota direview lalu diintegrasikan ke `proyek-uas-df`.
- Ground truth privat tidak boleh masuk ke repo publik atau dibagikan ke Meldiro/AI pipeline.
- Court narrative/Document 547 tidak boleh dimasukkan ke RAG investigator.

## Chris — Lead Forensik Digital
Branch: `p3-p4-persiapan-forensik-chris`

Fokus: persiapan P3/P4 tanpa menunggu corpus final.

Luaran:
1. SOP penyitaan & akuisisi perangkat uji.
2. inventaris perangkat dan workstation yang masih TBD;
3. template evidence ID, chain of custody, acquisition log, hash manifest;
4. pilihan dan versi tool hashing/acquisition/extraction;
5. dry-run akuisisi pada data dummy/non-case;
6. SOP working copy vs master evidence;
7. rencana memasukkan corpus final ke akun/perangkat uji tanpa mengubah evidence setelah simulasi dimulai.

Definition of Done:
- semua template siap dipakai;
- hash workflow diuji;
- evidence ID convention konsisten;
- tidak ada akuisisi final sebelum corpus 10k LOCKED.

## Bela — Lead Kasus & Data
Branch: `p1-penutupan-sumber-bela`

Fokus: menutup sisa P1 dan menyiapkan ground truth P2 secara privat.

Luaran publik/aman:
1. QA silang mapping 500/543 line;
2. daftar 43 unresolved dan prioritas corroboration;
3. hasil pencarian/corroboration Doc. 382, 427, 512, exhibit list, atau Exhibit 1A bila ditemukan;
4. taksonomi aktor, event, relasi, timeline;
5. schema mapping source → adapted;
6. daftar aturan apa yang boleh/tidak boleh ditambahkan ke synthetic corpus.

Luaran privat:
- ground truth actor/event/timeline;
- source line ↔ adapted message ↔ expected finding.

Definition of Done:
- tidak ada gap diisi dengan tebakan;
- setiap keputusan P1 punya provenance;
- ground truth tidak bocor ke branch AI.

## Meldiro — Lead AI/RAG
Branch: `p6-p7-rag-ollama-meldiro`

Fokus: membangun infrastruktur P6/P7 tanpa melihat ground truth.

Luaran:
1. environment Ollama reproducible;
2. kandidat model lokal + konfigurasi benchmark;
3. embedding model dan vector-store choice;
4. chunking berbasis conversation/time window;
5. schema chunk dengan evidence ID/provenance;
6. retrieval harness dan metrik Recall@k/Precision@k/hit rate;
7. runner LLM dengan RUN-ID, prompt, parameter, context, output log;
8. tiga mode eksperimen siap: LLM-only, RAG, RAG + structured reasoning.

Definition of Done:
- pipeline jalan pada toy/sanitized sample;
- tidak memakai ground truth;
- tidak memakai court narrative sebagai RAG evidence;
- semua run reproducible dan terlacak.

## Daffa — Lead Validasi & Dokumentasi
Branch: `p9-p10-validasi-dokumentasi-daffa`

Fokus: menyiapkan validasi independen, QA, dan struktur laporan.

Luaran:
1. rubrik evaluasi factual correctness, evidence attribution, groundedness, hallucination, citation accuracy, contradiction detection;
2. error register berbasis SOLVE-IT;
3. protokol blinded evaluation;
4. template evaluator findings;
5. QA checklist P1/P2/P3/P4/P6/P7;
6. kerangka laporan akhir dan daftar bukti/lampiran yang nanti harus diisi;
7. review independen 500 anchor dan monitoring continuity corpus 10k pada checkpoint.

Definition of Done:
- evaluator bisa menilai output tanpa melihat internal pipeline AI;
- metrik dan kriteria lulus/gagal eksplisit;
- laporan tidak mengklaim hasil yang belum diuji.

## Dependency

Pekerjaan yang BOLEH berjalan sekarang:
- P1 closure;
- P3/P4 preparation;
- P6/P7 infrastructure;
- P9/P10 evaluation/report scaffolding.

Pekerjaan yang HARUS menunggu:
- akuisisi final P3 → tunggu corpus 10k dan simulasi WhatsApp selesai;
- ekstraksi final P4 → tunggu akuisisi;
- baseline final P5 → tunggu artefak hasil ekstraksi;
- eksperimen final P8 → tunggu P4 + pipeline P6/P7;
- validasi hasil final P9 → tunggu P5/P8.

## Ritme integrasi

Setiap anggota:
1. commit hanya ke branch masing-masing;
2. buat ringkasan pekerjaan + QA;
3. jangan merge sendiri;
4. integrasi ke `proyek-uas-df` dilakukan setelah review lintas anggota.
