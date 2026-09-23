# Audit Integrasi Paralel P2

Tanggal: 2026-09-23  
Branch kanonik: `proyek-uas-df`

## Ringkasan

Worker A dan Worker B telah selesai untuk tahap anchor.

| Worker | Rentang tanggung jawab | Anchor valid |
|---|---:|---:|
| A | source line 1–271 | 239 |
| B | source line 272–543 | 261 |
| **Total** | source line terpetakan | **500** |

Tidak ada overlap source line. Semua 43 line yang masih unresolved dari P1 tetap tidak dimasukkan.

## Verifikasi Worker B

File yang diunggah ke chat dan file terbaru pada branch `p2-paralel-b` sama setelah normalisasi BOM dan line ending:
- baris: 261
- first ID: `ID-GAL-0272`
- last ID: `ID-GAL-0543`
- FNV-1a32 normalized: `b52287d6`
- Git blob terbaru: `d3c0f4a5dc93b8dfb8422bbbad68e3abcbdc6476`

## Temuan struktur Git

1. `main` saat ini berisi `batch_anchor_b.csv` versi **179 baris (272–450)** karena PR #4 di-merge sebelum Worker B menyelesaikan batch 5/6 dan 6/6.
2. PR #3 berjudul *P2 paralel a* tidak membawa `batch_anchor_a.csv`; file yang berubah hanya:
   - `docs/02_case_design/handoff_chatgpt_paralel_b.md`
   - `docs/02_case_design/rencana_pemrosesan_paralel.md`
3. Branch `p2-paralel-a` memiliki QA Worker A, tetapi CSV A tetap merupakan artefak kerja lokal/chat.
4. Karena itu, `main` tidak boleh digunakan sebagai sumber data eksperimen P2.
5. Branch kanonik tetap `proyek-uas-df`.

## QA gabungan 500 anchor

- jumlah baris: 500
- source line unik: 500
- message ID unik: 500
- transformation ID unik: 500
- conversation ID setelah normalisasi: 101
- exact duplicate row: 0
- unresolved line yang masuk: 0
- mapped line yang hilang: 0
- kebocoran nama utama sumber pada `message_text`: 0
- SHA-256 final: `63eeaac83bfd3b9145bbc1d99f3b7bfcce447face3f9cf7e20aa5231d55b0d24`

Respons pendek seperti `Oke.` dan `Iya.` boleh berulang karena natural dalam chat. Tidak ditemukan blok pesan duplikat.

## Normalisasi lintas-worker

- Actor ID distandardisasi ke format `AKT-*`.
- Conversation ID diturunkan dari cluster sumber Document 547.
- Timestamp yang dipakai adalah timestamp skenario sintetis zona +07:00, bukan timestamp asli Exhibit 1A.
- Nominal uang memakai faktor lokalisasi sintetis 15.000 rupiah per satuan nilai dolar sumber agar kedua worker konsisten; ini bukan klaim kurs historis.
- Alias dan lokasi dibuat fiktif/Indonesia.
- Wording untuk aktor di bawah umur disanitasi tanpa menghilangkan signal koordinasi/kontrol yang relevan bagi analisis forensik.

## Keputusan

Set `ANCHOR-500` dinyatakan **LOCKED**. Tahap berikutnya boleh menambah bridge, context, dan distractor, tetapi tidak boleh mengubah anchor tanpa mencatat change request dan alasan QA.
