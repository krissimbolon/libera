# Audit draf 001 — corpus WhatsApp LIBERA

Status: **belum final**. Branch: `p2-10k-work`. Audit ini mencatat draf 001; kelanjutan draf 002 dicatat pada log progres dan `qa_corpus_working.json`.

## Cakupan

Corpus kerja berisi 572 pesan: 500 anchor immutable dan 72 bridge yang ditulis serta ditinjau pada 12 conversation. Belum ada context atau distractor. Draf ini tidak memenuhi target 10.000 dan tidak boleh dipakai sebagai dataset final.

Pembangun `src/libera_corpus_work.py` hanya menyusun CSV dari pesan yang telah ditulis dalam `bridge_draft_001.tsv`. Ia tidak membuat teks otomatis dan berhenti bila hash jangkar berubah, sender keluar dari pasangan conversation, atau ada duplikat dan benturan timestamp. Hasil terukur disimpan pada `data/adaptasi_indonesia/qa_corpus_working.json`.

## Hasil cek

| Pemeriksaan | Hasil |
|---|---:|
| Anchor identik terhadap file branch | 500/500 |
| Anchor dari source line unresolved | 0 |
| ID ganda | 0 |
| Teks sintetis identik | 0 |
| Timestamp ganda dalam conversation | 0 |
| Kandidat near-duplicate panjang (rasio ≥0,86) | 0 |
| Nama utama sumber di pesan baru | 0 |
| Conversation campuran baru | 0 |

Review manual dilakukan dengan mengurutkan bridge dan anchor pada masing-masing conversation. Pesan yang mendahului izin perjalanan, mengulang pertanyaan identitas sebelum anchor, atau menyela jawaban konflik dihapus/diubah. QA semantik seluruh 10.000 pesan belum bisa dinyatakan lolos.

## Temuan baseline yang harus diselesaikan

1. Manifest jangkar menyebut SHA-256 `63eeaac83bfd3b9145bbc1d99f3b7bfcce447face3f9cf7e20aa5231d55b0d24`, sedangkan byte `anchor_indonesia_500.csv` pada commit branch menghasilkan `12859745a88aecca306b9f149661361ec2b8da8cd1f7c41c70ead1329b3e5e50`. Hash bagian-bagian dalam manifest juga berbeda dari byte file yang ter-commit. Belum dapat disimpulkan apakah ini perbedaan serialisasi atau manifest lama. Jangan mengubah anchor untuk memaksa cocok.
2. Empat conversation anchor memiliki dua pasangan aktor berbeda: `KONV-GAL-P22-C`, `KONV-GAL-R013`, `KONV-GAL-R080`, `KONV-GAL-R088`. Draf menghindari keempatnya. Perlu keputusan eksplisit tentang pembacaan thread ini sebelum memperluasnya; anchor sendiri tetap immutable.
3. Tidak ada dasar untuk menyatakan actor-state dan chronological consistency di seluruh 10.000 sebelum 9.428 pesan tersisa ditulis dan ditinjau. `qa_corpus_10000.json`, `laporan_qa_corpus_10000.md`, dan `corpus_whatsapp_10000.csv` sengaja belum dibuat.

## Pekerjaan berikutnya

Lanjutkan bridge dengan replay anchor per conversation, lalu context dan distractor pada fase waktu yang sesuai. Jalankan QA setiap 500–1.000 pesan, catat state aktor yang menyeberang conversation, dan hanya publikasikan file final setelah mencapai komposisi 500/1.500/6.500/1.500 serta review manual final.
