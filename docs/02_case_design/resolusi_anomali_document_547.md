# Resolusi Anomali Rekonstruksi Document 547

## Status
Sumber kerja kanonik: `Document 547 Galloway.md`  
Source ID: `SRC-001`  
SHA-256 sumber: `195a880e87f59d882e70c16b4c42a9df23a0eaec547b928f1ad1a9afae4ae889`

Rekonstruksi v2 menghasilkan **500 dari 543 line (92,08%)** yang dapat dipetakan ke pesan dengan tingkat dukungan yang memadai. **43 line (7,92%)** sengaja belum dipetakan.

## Prinsip resolusi
Anomali hanya boleh diselesaikan apabila struktur internal Document 547 memberikan pembatas yang kuat dan dapat diaudit. Tidak ada LLM yang digunakan untuk mengarang pesan yang hilang. Setiap koreksi terhadap nomor line sumber harus tetap mempertahankan teks salah cetak asli dalam catatan provenance.

## A-001 — Konflik 85–96 vs 382–389
Pada halaman 22, satu blok percakapan memuat 12 pesan. Dokumen mencetak `(lines 382-389)` setelah delapan pesan pertama, lalu `(Id, lines 85-96)` setelah empat pesan berikutnya. Narasi setelah blok secara eksplisit menyebut **line 94** sebagai pesan yang salah kirim. Jika seluruh 12 pesan dipetakan berurutan ke 85–96, line 94 tepat berada pada pesan yang dibahas narasi tersebut.

Selain itu, halaman 34–35 kemudian menggunakan 382–386, 387, 388, dan 389–392 secara berurutan untuk blok lain yang berbeda. Karena itu, working reconstruction v2 memperlakukan `382-389` di halaman 22 sebagai anomali referensi dan menggunakan 85–96 untuk 12 pesan tersebut.

Status: **DISELESAIKAN_INTERNAL_QA_PENDING**.

## A-002 — 382–392
Referensi pada halaman 34–35 membentuk urutan koheren: 382–386, 387, 388, lalu 389–392. Mapping ini digunakan sebagai sumber line 382–392.

Status: **DISELESAIKAN_DARI_REFERENSI_LANGSUNG**.

## A-003 — 511–5521
Document 547 mencetak `(Id, lines 511-5521)`. Blok tersebut berisi 11 giliran pesan, sementara blok berikutnya dimulai pada 522–526. Working resolution yang paling terbatas adalah 511–521.

Kesalahan cetak asli **tidak dihapus dari provenance**; rekonstruksi menyimpan bahwa 511–521 adalah resolusi kerja, bukan teks line-range yang benar-benar dicetak sumber.

Status: **DISELESAIKAN_TYPO_QA_PENDING**.

## Anomali yang tetap unresolved
- **16–26:** 11 line tetapi hanya 10 pesan yang dapat ditempatkan dari bagian tersebut.
- **27:** tidak cukup disebut pada Document 547.
- **116–117:** sumber mencetak `117-117` untuk dua pesan. Kandidat 116–117 kuat dari urutan tetangga, tetapi belum dipromosikan menjadi mapping final.
- **168–175:** terdapat penanda `(skip)`, sehingga posisi line per pesan tidak aman ditentukan.
- **208–217:** 10 line tetapi 11 giliran pesan.
- **531–541:** 11 line tetapi hanya 10 pesan direproduksi.

## Batas publik dan privat
Repo publik hanya menyimpan status, rentang, hash, dan keputusan QA. Isi verbatim rekonstruksi disimpan di:

`D:\KSI\Libera Private Evidence\06_rekonstruksi_terbatas\`

Paket privat v2:
`paket_rekonstruksi_privat_doc547_v2.zip`

SHA-256:
`5cf1e2e3f1631942fa98a8a5cc1a5307d8d08aad3419caad215b5e332e54785e`
