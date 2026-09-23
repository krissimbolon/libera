# MULAI DI SINI — Bela / Penutupan P1

## Tujuan saat Work 10k berjalan
Tutup P1 secara defensible tanpa menebak 43 line yang belum terpetakan, dan siapkan ground truth privat untuk evaluasi.

## Kerjakan berurutan

1. QA silang 500/543 line yang sudah terpetakan.
2. Kelompokkan 43 unresolved:
   - 16–27;
   - 116–117;
   - 168–175;
   - 208–217;
   - 531–541.
3. Cari corroboration independen:
   - Doc. 382;
   - Doc. 427;
   - Doc. 512;
   - exhibit list;
   - Exhibit 1A bila tersedia.
4. Untuk setiap unresolved:
   - status;
   - sumber pendukung;
   - confidence;
   - keputusan: resolved / tetap unresolved.
5. Buat taksonomi:
   - actor;
   - event;
   - relation;
   - timeline.
6. Buat mapping privat:
   - source line;
   - adapted message;
   - expected entity/event/relation;
   - expected finding.
7. Pisahkan file publik dan privat.

## Jangan dilakukan sekarang
- jangan mengisi gap dengan LLM;
- jangan mengunggah ground truth privat ke repo publik;
- jangan memberi ground truth ke Meldiro;
- jangan mengubah 500 anchor.

## Definition of Done
P1 punya QA silang, unresolved transparan, provenance lengkap, dan ground truth privat siap untuk evaluator.
