# P5 Traditional Forensic Baseline Protocol — LIBERA

Tujuan: menghasilkan baseline investigator tanpa LLM yang dapat dibandingkan secara fair terhadap kondisi AI.

## Blinding

Investigator baseline hanya melihat acquired/extracted artifacts. Jangan buka:
- P2 ground truth;
- source reconstruction;
- hidden relevant/distractor labels;
- hasil model A/B/C.

Baseline dikunci sebelum evaluasi P9.

## Investigative workflow

### 1. Inventory
Catat:
- artifact yang tersedia;
- coverage waktu;
- jumlah conversation/message;
- attachment availability;
- parser/extraction limitation.

### 2. Keyword/search ledger
Jangan hanya menyimpan kata kunci; simpan query dan hit count.

Kategori awal yang diperbolehkan karena berasal dari research scope, bukan ground truth tersembunyi:
- transport/perjalanan;
- hotel/penginapan/lokasi;
- uang/harga/bayar;
- pulang/pergi/jemput;
- akun/platform/iklan;
- keluarga;
- tekanan/ancaman/kontrol;
- waktu/jadwal.

Setiap hit kandidat diverifikasi konteks manual.

### 3. Actor/entity analysis
Buat daftar actor/entity berdasarkan evidence:
- identifier;
- first/last observed;
- counterparties;
- evidence locators;
- role interpretation;
- uncertainty.

Jangan mengisi role dari case-design bila evidence tidak mendukung.

### 4. Timeline
Susun event hanya bila ada ART/message support.
Simpan:
- event_id;
- start/end;
- actor;
- event statement;
- evidence;
- uncertainty/alternative explanation.

### 5. Link/relationship analysis
Relationship harus memiliki evidence locator dan direction bila relevan.
Pisahkan:
- communication frequency;
- inferred relationship;
- substantive coordination.

### 6. Findings
Setiap finding:
- satu claim yang dapat diuji;
- evidence locator;
- reasoning singkat;
- uncertainty;
- alternative explanation bila ada.

Gunakan `FND-BASE-####`.

## Baseline lock

Setelah selesai:
1. hash/export baseline finding table;
2. catat investigator dan reviewer;
3. jangan mengedit setelah melihat AI output atau ground truth;
4. koreksi pasca-lock harus menjadi versioned amendment.

## P9 comparison

Evaluator kemudian membandingkan baseline dengan ground truth dan kondisi A/B/C menggunakan definisi metric yang sama pada finding level.
