# Independent P2 QA Snapshot — 2026-09-24

Branch kerja audit: `p2-independent-qa`  
Snapshot corpus yang dijadikan dasar: `p2-10k-work@c2c5cbf76bd10fcf072f058505a0badbf65706e7`

Dokumen ini adalah catatan QA independen. Ia tidak menggantikan QA Work dan tidak mengubah corpus. Tujuannya adalah menyediakan second-review yang dapat ditelusuri untuk P2 sebelum dataset dipakai pada tahap forensik P3–P10.

## Keterkaitan dengan desain riset

Desain riset memisahkan case-design/ground truth dari pipeline examiner. Corpus P2 adalah bahan simulasi yang nantinya ditempatkan pada lingkungan uji, diakuisisi, diekstrak, lalu dianalisis sebagai evidence. Karena itu kualitas P2 harus diperiksa sebelum acquisition agar artefak generator tidak menjadi confounder bagi evaluasi LLM/RAG.

ForensicLLM (Sharma et al., 2025; SRC-002) menjadi acuan untuk local inference, evaluasi correctness/relevance, dan source attribution. SOLVE-IT (Hargreaves et al., 2025; SRC-003) menjadi acuan untuk error-focused QA dan pencatatan mitigasi. NIST SP 800-101 Rev. 1 (SRC-004) dan SP 800-86 (SRC-005) digunakan untuk menjaga pemisahan preservation/acquisition/examination/analysis/reporting.

## Structural gate yang diverifikasi independen

Pada snapshot sebelum repair cadence:
- total pesan: 10.000;
- provenance: 500 anchor + 1.500 bridge + 6.500 context + 1.500 distractor;
- anchor exact match: 500/500;
- duplicate message ID: 0;
- duplicate synthetic message_text: 0;
- synthetic `source_original_line` non-empty: 0;
- invalid timestamp: 0;
- timestamp selain +07:00: 0;
- timestamp di luar 1–21 Juli 2026: 0;
- collision timestamp dalam conversation: 0;
- missing reply target: 0;
- reply ke pesan masa depan: 0;
- reply lintas conversation: 0;
- source-identity leakage yang terdeteksi: 0;
- mixed-participant conversation baru: 0.

Structural gate ini diperlukan tetapi tidak cukup untuk final sign-off.

## Language/cadence generator fingerprint

Auditor awal hanya menandai 731 adjacent context gaps tepat 247 detik. Audit independen menunjukkan bahwa itu bagian dari fingerprint yang jauh lebih luas.

Context B:
- 3.250 pesan;
- 2.954 adjacent gaps;
- 2.818 gap (95,40%) memiliki `seconds % 60 == 7`;
- spike utama: 127 detik = 660, 187 = 660, 247 = 731, 307 = 593, 367 = 91.

Context A sebagai sanity comparator:
- 2.957 adjacent gaps;
- hanya 75 gap (2,54%) memiliki remainder 7 detik.

Kesimpulan QA: memperbaiki hanya gap 247 detik tidak cukup. Seluruh cadence family `60n+7` pada Context B harus direview/naturalisasi tanpa menggeser pesan melewati anchor atau merusak causal order.

## Near-duplicate panjang

Audit word-trigram pada synthetic messages dengan >=8 token menemukan dua pasangan yang sangat mirip (Jaccard trigram 0,857):

1. `ID-BRG-1053` vs `ID-BRG-1002`
   - “aku masih di sini, yang tadi masih kuingat ya.”
   - “aku masih di sini, yang tadi masih kuingat.”

2. `ID-BRG-1065` vs `ID-BRG-1014`
   - “habis ini aku balas, yang tadi masih kuingat ya.”
   - “habis ini aku balas, yang tadi masih kuingat.”

Manual context review menunjukkan keempat pesan berada pada conversation berbeda dan berfungsi sebagai filler antara anchor. Redaksinya sangat generik serta nyaris identik, sehingga perlu review Work sebagai kandidat template leakage. Jangan hapus otomatis; perbaikan harus mempertimbangkan anchor sebelum/sesudah masing-masing thread.

## Provenance/hash forensics anchor

Manifest historis menyatakan:
- combined anchor SHA-256: `63eeaac83bfd3b9145bbc1d99f3b7bfcce447face3f9cf7e20aa5231d55b0d24`.

Byte/string snapshot branch saat ini menghasilkan:
- `anchor_indonesia_500.csv`: `12859745a88aecca306b9f149661361ec2b8da8cd1f7c41c70ead1329b3e5e50`.

Row-level verification tetap 500/500 exact-match terhadap reference set yang dipakai corpus.

Investigasi line-ending:
- `bagian_01.csv`: hash manifest dapat direproduksi ketika LF dikonversi ke CRLF;
- `bagian_02.csv` s.d. `bagian_05.csv`: hash manifest **tidak** dapat direproduksi hanya dengan empat varian sederhana yang diuji (LF/CRLF, dengan/tanpa final newline);
- combined hash `63ee…` juga tidak direproduksi oleh varian line-ending sederhana pada file gabungan saat ini.

Git history menunjukkan file combined/parts dan manifest ditambahkan berurutan pada 23 September 2026 dan masing-masing part tidak memiliki commit perubahan lain pada jalur ini. Dengan bukti saat ini, penjelasan “semua hash part hanya berbeda karena CRLF” belum cukup terbukti.

Keputusan forensik:
- jangan mengubah 500 anchor untuk mengejar hash lama;
- pertahankan hash byte file saat ini sebagai hash snapshot yang dapat direproduksi;
- dokumentasikan `63ee…` sebagai historical manifest hash yang provenance serialization-nya belum terkonfirmasi;
- bila file lokal/original integration artifact tersedia, hash ulang byte asli untuk mencoba mereproduksi `63ee…`.

## Release gate P2

P2 belum boleh ditandai final bila salah satu kondisi berikut masih terbuka:
- language-template Context B belum selesai;
- cadence generator fingerprint belum ditangani;
- candidate near-duplicate belum direview;
- chronology + actor-state audit belum selesai;
- provenance hash discrepancy belum didokumentasikan;
- human spot-check belum lulus.

Final artifact hanya boleh diterbitkan setelah working corpus yang sama lulus structural, language, chronology, actor-state, provenance, dan manual review.
