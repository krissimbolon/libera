# QA chat gabungan P2 — belum lulus

Snapshot kerja sesudah repair Kirana 10 Juli. Dokumen ini sengaja tidak memberi sign-off atau membuat artefak final.

## Model evidence simulator

`conversation_id` menandai segment skenario; chat fisik harus dibaca berdasarkan pasangan aktor. Auditor `src/audit_chat_level_coherence.py` (diambil sebagai skrip dari branch review independen tanpa merge branch) menghitung 846 segment, 26 pasangan, 9.997 pesan yang melibatkan Raka, 1.500 bridge pada segment anchor, dan 49 pasangan segment yang rentang waktunya overlap dalam chat yang sama.

## Review overlap

Seluruh **49 overlap** teridentifikasi dan contoh pesan pada rentang irisannya dibaca sebagai triase. Ini **belum** merupakan pembacaan lengkap merged chat per pasangan dan tidak dapat dihitung sebagai 49 PASS. Overlap Kirana 10 Juli (`KONV-CTX-KIRANA-B15-031` / `KONV-CTX-KIRANA-B13-003`) direpair sebagai dua segment dalam satu alur kipas dan wadah (30 pesan, `_021.tsv`), tetap perlu verifikasi final setelah cadence global.

Kandidat semantik konkret yang masih terbuka dari triase:

- Dini 7 Juli, segment termos/handuk/kertas dan bolpoin: balasan lintas topik tersisip, termasuk perintah mengeringkan meja di sela pertanyaan minuman.
- Kirana 7 Juli: pembicaraan sepatu, handuk, dan sisir berulang dan saling terputus.
- Tania 12 Juli: instruksi payung berselang dengan anchor `R066` yang menyuruh pergi ke halte bus; memerlukan pemeriksaan causal merged chat.
- Jihan 18 Juli malam: beberapa segment toples, map, kipas, dan teh berjalan sekaligus; sejumlah balasan pendek masih berupa filler dan belum koheren saat dibaca sebagai satu chat.
- Jihan 20 Juli: filler synthetic menyela anchor permintaan bantuan (`R100`), sehingga neighborhood anchor harus dibaca menyeluruh.

Status review 49 overlap: **1 overlap direpair; 48 belum mendapat full merged-chat disposition**. Penghitungan interval overlap tidak otomatis membuktikan kontradiksi fisik; setiap kasus memerlukan pembacaan semantik sebelum PASS.

## Aktor dan anchor

`src/audit_actor_timeline.py` menghasilkan kandidat 15 menit pengirim aktif pada sedikitnya tiga segment (Raka 13, Jihan 2). Tiga timestamp identik lintas segment untuk Raka diperbaiki tanpa menggeser anchor, sehingga collision lintas chat sekarang 0; simultan chat singkat tetap dapat natural. Tidak ada pesan Caca sesudah anchor pemblokiran `R096`; 74 perbaikan waktu manual tidak melintasi anchor yang melibatkan aktor terkait. Ini **belum** memeriksa secara lengkap lokasi, tidur, perjalanan, knowledge, dan outcome untuk setiap aktor. Neighborhood seluruh 500 anchor **belum** mendapat sign-off individual.

Anomali sumber yang harus tetap immutable diberi label `SOURCE_RECONSTRUCTION_ANOMALY`: pesan `ID-GAL-0258`, `ID-GAL-0263`, `ID-GAL-0268` adalah Rena → kontak tidak diketahui tanpa Raka; empat segment multi-participant anchor ialah `KONV-GAL-P22-C`, `KONV-GAL-R013`, `KONV-GAL-R080`, `KONV-GAL-R088`. Semua berasal dari reconstruction anchor, bukan relasi sintetis baru.

## Gate terbuka

- Dari 190 sinyal awal akhiran koma/frasa/`ya`: 8 diperbaiki, 2 dibaca dan dipertahankan natural, **180 masih butuh pembacaan thread lengkap**. Angka auditor saat ini 182 karena dua yang dipertahankan tetap terdeteksi.
- Akhiran `barusan` Context B: 74 → **47**, sisanya perlu review kontekstual.
- Cadence Context B `seconds % 60 == 7`: **2.818/2.954 (95,40%) → 2.757/2.954 (93,33%)**; exact 247: 731 → **718**. Context A 75/2.957 (2,54%). Fingerprint Context B tetap dominan.
- Audit structural otomatis lulus (10.000; provenance 500/1.500/6.500/1.500; anchor 500/500; duplikat synthetic 0; repeated suffix 0; reply dan timestamp valid), tetapi semantic gate gagal.
- Row identity 500 anchor tervalidasi; current byte SHA `12859745a88aecca306b9f149661361ec2b8da8cd1f7c41c70ead1329b3e5e50`. Hash gabungan historis `63eeaac83bfd3b9145bbc1d99f3b7bfcce447face3f9cf7e20aa5231d55b0d24` belum dapat direproduksi; hanya hash bagian 01 cocok pada CRLF. Anchor tidak diubah.

**QA akhir: FAILED_LANGUAGE_CONTINUITY_QA / human semantic sign-off belum sah. Corpus belum di-freeze.**

## Lanjutan dari packet reviewer independen

`build_final_semantic_review_packets.py` dari commit independen `20aca6a` disalin dan dijalankan pada corpus terbaru. Manifest packet sesudah repair: 228 kandidat bahasa (regex packet berbeda dari auditor), 49 overlap, 500 anchor, dan 1.511 jendela actor concurrency 15 menit. Paket tersebut **belum** diberi disposisi PASS secara massal.

Perbaikan baru pada merged chat: Dini dan Kirana 7 Juli, Tania 12 Juli menjelang anchor halte `R066`, Jihan 20 Juli di sekitar anchor `R100`, dan multi-topik Jihan 18 Juli malam. Ini memperbaiki kandidat spesifik tetapi bukan klaim bahwa semua overlap chat tersebut maupun 500 anchor neighborhood sudah dibaca lengkap. Kandidat bahasa awal yang masih memerlukan full disposition = **175/190** (13 diperbaiki, 2 natural); auditor Context B kini 177 pola koma/`ya` dan 47 `barusan`.

Model cadence `thread-weights-v1` mengurangi fingerprint dari 2.757 menjadi 383 gap remainder tujuh; 247 detik dari 718 ke 105. Tiga collision lintas chat akibat retiming langsung diperbaiki di synthetic rows, tanpa perubahan anchor. Pemeriksaan struktur lulus, tetapi validasi aktor global, 49 overlap, dan semua neighborhood anchor belum memiliki human sign-off. **Status tetap FAILED_LANGUAGE_CONTINUITY_QA; tidak boleh ada manifest freeze.**
