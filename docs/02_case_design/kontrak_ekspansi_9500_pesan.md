# Kontrak Ekspansi 9.500 Pesan Sintetis

Tanggal dikunci: 2026-09-23

Dokumen ini mengatur ekspansi dari 500 pesan jangkar menjadi corpus 10.000 pesan. Set jangkar bersifat immutable.

## Komposisi final

- 500 pesan `ADAPTED_FROM_GALLOWAY` — sudah LOCKED.
- 1.500 pesan `SYNTHETIC_BRIDGE`.
- 6.500 pesan `SYNTHETIC_CONTEXT`.
- 1.500 pesan `SYNTHETIC_DISTRACTOR`.

Total: **10.000 pesan**.

## Namespace ID

- Bridge: `ID-BRG-0001` s.d. `ID-BRG-1500`.
- Context Worker A: `ID-CTX-A-0001` s.d. `ID-CTX-A-3250`.
- Context Worker B: `ID-CTX-B-0001` s.d. `ID-CTX-B-3250`.
- Distractor: `ID-DST-0001` s.d. `ID-DST-1500`.

`source_original_line` wajib kosong untuk semua 9.500 pesan sintetis tambahan.

## Aturan substantif

1. Semua pesan tetap berada dalam semesta kasus adaptasi Galloway.
2. Tidak boleh memperkenalkan korban utama baru, tindak pidana utama baru, kematian baru, atau outcome baru.
3. Pesan bridge hanya menghubungkan keadaan yang sudah terlihat pada jangkar.
4. Pesan context menambah realisme kehidupan sehari-hari, perjalanan, keluarga, makanan, baterai, jadwal, percakapan sosial, dan logistik umum.
5. Pesan distractor dibuat relevan secara sosial terhadap aktor/periode, tetapi tidak menjadi bukti kunci.
6. Konten untuk aktor di bawah umur tidak boleh dibuat seksual eksplisit.
7. Nama tempat usaha/alamat tetap fiktif.
8. Tidak boleh menyalin teks court record sebagai pesan sintetis baru.

## Aturan anti-pengulangan

- Exact duplicate row pada 10.000 pesan final: 0.
- Untuk 9.500 pesan sintetis baru, exact duplicate `message_text`: 0.
- Pesan jangkar dikecualikan dari aturan unique-text karena pengulangan respons pendek berasal dari struktur sumber.
- Near-duplicate panjang wajib ditandai untuk review.
- Tidak boleh memperbanyak volume dengan template yang hanya mengganti nama, nominal, atau satu kata.

## Aturan waktu

500 jangkar memakai timestamp skenario sintetis +07:00 pada 2026-07-01 s.d. 2026-07-21.

Pesan bridge:
- ditempatkan di antara atau dekat pesan jangkar pada conversation/event yang sama;
- tidak boleh mengubah urutan sebab-akibat jangkar.

Pesan context/distractor:
- berada di jendela skenario yang sama;
- tidak boleh membuat aktor muncul di dua lokasi yang saling bertentangan pada waktu yang sama;
- timestamp harus unik setidaknya dalam conversation yang sama.

## Aturan conversation

- Reuse `conversation_id` jangkar bila pesan melanjutkan thread yang sudah ada.
- Conversation netral baru boleh dibuat untuk aktor existing dan kontak fiktif non-kunci.
- Kontak baru netral tidak boleh berubah menjadi aktor kriminal utama atau korban baru.

## QA wajib per batch

1. skema;
2. jumlah baris;
3. uniqueness ID;
4. uniqueness synthetic message_text;
5. chronology;
6. actor-state consistency;
7. provenance;
8. leakage;
9. near-duplicate;
10. human spot-check.

## Merge policy

Worker branch tidak merge ke `main`.

Semua hasil hanya diintegrasikan ke:
`proyek-uas-df`

setelah QA.
