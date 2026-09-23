# Audit draf 002 — corpus WhatsApp LIBERA

Status: **belum final**. Branch: `p2-10k-work`.

## Cakupan

Corpus kerja berisi **768 pesan**: 500 anchor, 168 bridge, 70 context, dan 30 distractor. Ada 111 conversation: 101 conversation jangkar serta 10 conversation netral baru dengan pasangan Raka dan aktor yang sudah dikenal. Tidak ada baris sintetis yang diklaim sebagai pesan kasus asli.

Bridge 002 ditulis pada celah jangkar di fase 2–5. Pesan yang membuat instruksi, izin, atau respons anchor tampak mendahului sebabnya telah dihapus atau ditulis ulang setelah replay bersama anchor. Context 001 dan distractor 001 berisi percakapan beberapa giliran dengan benda/topik yang dipertahankan sampai akhir thread; isi tetap berupa kehidupan sehari-hari dan tidak menambah outcome perkara.

## QA terukur

| Pemeriksaan | Hasil |
|---|---:|
| Anchor identik terhadap file branch | 500/500 |
| Source line anchor yang unresolved | 0 |
| ID ganda | 0 |
| Teks sintetis identik | 0 |
| Benturan timestamp dalam conversation | 0 |
| Kandidat near-duplicate panjang | 0 |
| Kebocoran nama utama sumber pada pesan baru | 0 |
| Conversation baru yang mencampur pasangan | 0 |

Validator juga menolak actor ID baru, timestamp di luar 1–21 Juli 2026 atau tanpa offset +07:00, bridge pada empat conversation jangkar campuran, provenance yang melewati kuota, dan perubahan byte jangkar. Hasil lengkap serta hash corpus kerja ada di `qa_corpus_working.json`.

## Batas verifikasi

Pemeriksaan panjang teks yang mirip menggunakan shortlist token tiga kata, sehingga angka nol berarti tidak ada kandidat pada aturan deteksi itu, bukan bukti universal bahwa semua parafrasa berbeda. State fisik aktor lintas semua conversation masih perlu review manusia lebih luas. Ledger aktor membantu melacak perubahan yang diketahui dan area yang belum pasti.

Manifest jangkar masih mencatat hash yang tidak cocok dengan byte file ter-commit. Empat conversation jangkar campuran tetap utuh sebagai anomali baseline. Corpus saat ini kurang **9.232 pesan** dari target. `corpus_whatsapp_10000.csv`, `qa_corpus_10000.json`, dan laporan QA final belum diterbitkan.
