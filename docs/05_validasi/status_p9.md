# Status P9 — Validasi dan Mitigasi Kesalahan

Status: **IMPLEMENTATION READY — FINAL BLIND EVALUATION MENUNGGU LOCAL P8 LOCK + PRIVATE GT**

Updated: 24 September 2026  
Integration branch: `p3-p10-final-integration`

## Kondisi saat ini

Implementasi evaluator P9, rubrik, protokol blind, lock verification, dan precheck evidence-reference sudah tersedia dan telah melewati jalur integrasi otomatis.

GitHub Actions `Post-P2 Integration Audit` pada HEAD `5b5cc63c56b49ebd32f76e64fe62870360909b0d` (run `36022542952`) selesai dengan **success** pada Python 3.12 dan 3.14. Jalur CI membuktikan P4 -> P5 -> P6 -> P8 dry-run -> P8 lock -> P9 integrity precheck -> P10 report dapat dieksekusi end-to-end.

P9 **final** belum boleh diklaim selesai karena hasil real local P8 (BGE-M3 + Qwen2.5-1.5B) dan ground truth privat evaluator belum tersedia di repo publik dan memang tidak boleh disimpan di sana.

## Yang sudah selesai

- evaluator TP/FP/TN/FN dan precision/recall/F1/specificity;
- validasi ART citation / evidence reference;
- verifikasi lock P8 sebelum ground truth dibuka;
- rubrik evaluasi P9;
- protokol evaluasi blind;
- template evaluasi temuan;
- register error SOLVE-IT;
- checklist gate P9;
- script final terpisah `scripts/run_p9_final.ps1` yang tidak menjalankan ulang P6/P7/P8.

## Status gate saat ini

**READY_FOR_LOCAL_P8_AND_GT_PREPARATION**

Artinya:

1. software P9 siap;
2. dry-run integrity path sudah lulus;
3. final metric run menunggu output P8 real yang telah dikunci;
4. ground truth tetap privat dan baru dibuka sesudah lock P8 diverifikasi.

## Prasyarat sebelum final P9

- jalankan acquisition/extraction track yang dipilih dan stabilkan P4 ART;
- jalankan P5 pada P4 final;
- jalankan BGE-M3 + Qwen2.5-1.5B lokal untuk P6/P7/P8;
- pastikan run log, model tag/version/digest, prompt version, retrieval trace, dan evidence citation tersedia;
- jalankan `tools/lock_p8_outputs.py`;
- siapkan/selesaikan private ground-truth annotation packet;
- lock private GT;
- baru jalankan `scripts/run_p9_final.ps1 -GroundTruthPath <private-path>`.

## Keputusan final

Status **READY_FOR_P9_FINAL** baru boleh dinyatakan tepat sebelum `run_p9_final.ps1` ketika seluruh prerequisite di atas telah diverifikasi.

Status **P9_COMPLETE** baru boleh dinyatakan setelah `runtime/working/P9/evaluation.json` berisi hasil final dari output P8 real yang locked dan private GT yang locked, kemudian P10 dibangun ulang dari hasil tersebut.

## Larangan

- jangan membuat klaim performa final dari hasil dry-run;
- jangan membuka ground truth kepada pipeline AI;
- jangan mengubah atau menjalankan ulang P8 setelah ground truth dibuka;
- jangan memasukkan ground truth privat atau raw acquisition master ke repository publik;
- jangan menyebut ChatSim sebagai WhatsApp atau software dry-run sebagai physical-device acquisition.
