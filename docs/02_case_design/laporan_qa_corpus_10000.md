# Laporan QA Final Corpus LIBERA 10.000 Pesan

**Status akhir: LULUS — FROZEN_FOR_FORENSIC_SIMULATION**

Corpus P2 telah selesai diproduksi, diperbaiki, direview, dan dibekukan untuk dipakai sebagai bahan simulasi barang bukti pada tahap digital forensics. Setelah freeze ini, corpus tidak boleh diedit lagi kecuali proyek secara eksplisit membuka versi baru dan mengulang QA.

## 1. Artefak canonical

- Corpus final: `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`
- SHA-256 corpus final: `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`
- Git blob: `de6d2d20ac9b35938edaef9df0f88a7d82796366`
- Ukuran: 1.410.686 bytes
- Freeze: 24 September 2026, 21:53:01 WIB
- Rentang skenario: 1–21 Juli 2026 (+07:00)

## 2. Komposisi

| Provenance | Jumlah |
|---|---:|
| ADAPTED_FROM_GALLOWAY | 500 |
| SYNTHETIC_BRIDGE | 1.500 |
| SYNTHETIC_CONTEXT | 6.500 |
| SYNTHETIC_DISTRACTOR | 1.500 |
| **Total** | **10.000** |

Terdapat 26 pasangan partisipan. Sebanyak 9.997 pesan melibatkan Raka; tiga anchor non-Raka tetap dipertahankan sebagai anomali rekonstruksi sumber.

## 3. Automated QA

GitHub Actions `P2 Final Audit` run **36015548551** selesai dengan status **success**.

Hasil utama:

- automated final gate: PASS
- 10.000 message ID unik
- exact duplicate row: 0
- duplicate synthetic text: 0
- repeated four-message suffix window: 0
- long near-duplicate candidate: 0
- timestamp invalid: 0
- collision timestamp dalam conversation: 0
- synthetic `source_original_line` nonblank: 0
- reply target hilang/future/cross-conversation: 0
- source-identity leakage: 0
- new mixed-participant synthetic conversation: 0
- synthetic-only Raka relationship: 0
- bridge tanpa anchor segment: 0
- anchor exact-match: 500/500

## 4. Language QA

Seluruh **228/228 kandidat bahasa** pada review packet mempunyai disposition.

- REPAIR: 222
- PASS_NATURAL: 6
- unresolved: 0

Enam detector hit yang tersisa dibaca dalam merged-chat context dan dipertahankan karena natural. Akhiran Context-B `barusan` yang sebelumnya bermasalah turun menjadi 0.

Selain itu, 25 synthetic messages yang masih memuat istilah internal **bridge** telah direwrite agar examiner tidak melihat istilah konstruksi dataset.

## 5. Cadence QA

Fingerprint awal Context B sangat kuat:

- `seconds % 60 == 7`: 2.757/2.954 = 93,33%
- exact 247 seconds: 718

Setelah deterministic, thread-aware retiming:

- `seconds % 60 == 7`: **383/2.954 = 12,97%**
- exact 247 seconds: **105**

Anchor timestamps tidak diubah. Message order, reply integrity, batas 1–21 Juli, dan struktur tetap valid.

## 6. Merged-chat continuity

Seluruh **49/49** overlap antar-segment pada participant pair yang sama mempunyai disposition:

- PASS: 17
- REPAIR: 32
- unresolved: 0

Review dilakukan dengan membaca segment sebagai satu timeline chat per kontak, bukan sebagai thread generation yang terpisah.

## 7. Global actor-state

Seluruh 16 dense concurrency window telah direview:

- 16/16 = `PASS_CHAT_MULTITASKING`

Audit global tambahan memeriksa pernyataan fisik/lokasi:

- 10 aktor memiliki klaim lokasi/pergerakan kuat
- 59 klaim fisik/lokasi ditinjau
- Raka: 37 klaim
- candidate physical conflict lintas chat dalam ≤30 menit: **0**

Tujuh synthetic rows yang masih menciptakan ambiguitas actor-state pada neighborhood anchor telah diperbaiki tanpa menyentuh anchor.

Dokumen sign-off: `docs/02_case_design/qa_global_actor_state_final.md`.

## 8. Anchor-neighborhood QA

Seluruh **500/500 anchor** mempunyai disposition semantik; unresolved = 0.

Untuk 481 anchor yang sebelumnya masih terbuka, review dilakukan melalui 98 anchor-event segments dalam merged-chat context.

Hasil event-level:
- 88 event PASS langsung
- 3 event REPAIR_THEN_PASS
- 7 event source-reconstruction anomaly

Yang diuji:
1. cause/effect tidak dibalik;
2. knowledge tidak muncul sebelum sumber informasi;
3. outcome tidak muncul prematur;
4. actor-state tetap konsisten.

Anchor tidak pernah diubah.

## 9. Source reconstruction anomalies

Dipertahankan apa adanya:

Non-Raka anchors:
- `ID-GAL-0258`
- `ID-GAL-0263`
- `ID-GAL-0268`

Multi-identity anchor segments:
- `KONV-GAL-P22-C`
- `KONV-GAL-R013`
- `KONV-GAL-R080`
- `KONV-GAL-R088`

Ini bukan synthetic defects dan tidak boleh “dibersihkan” dengan mengubah sumber.

## 10. Anchor provenance

- current anchor SHA-256: `12859745a88aecca306b9f149661361ec2b8da8cd1f7c41c70ead1329b3e5e50`
- historical manifest combined SHA-256: `63eeaac83bfd3b9145bbc1d99f3b7bfcce447face3f9cf7e20aa5231d55b0d24`

500 logical rows identik dan urutannya terverifikasi. Historical combined byte serialization belum berhasil direproduksi. Perbedaan ini didokumentasikan dan **bukan blocker**; anchor tidak dimodifikasi untuk memaksa hash historis.

## 11. Keputusan

Corpus memenuhi structural, language, cadence, merged-chat continuity, anchor-neighborhood, dan global actor-state gates yang telah ditetapkan.

**P2 corpus generation is complete and frozen. Proceed to digital forensics.**

Tahap berikutnya:

`corpus final → DEV-001 → ACQ-001 → hashing → working copy → ART extraction → traditional baseline → local LLM/RAG → evidence-attributed findings → TP/FP/TN/FN and ground-truth validation`.
