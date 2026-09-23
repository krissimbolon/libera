# Rencana Produksi 10.000 Pesan

## Tahap produksi

### Batch A — 500 anchor
Terjemahkan dan lokalisasi 500 line Galloway yang sudah dipetakan. Setiap baris wajib mempertahankan:
- `source_original_line`
- `source_provenance=ADAPTED_FROM_GALLOWAY`
- `transformation_id`
- event/aktor yang sama secara substantif.

### Batch B — 1.500 bridge
Tambahkan pesan penghubung antarpesan/event agar kronologi percakapan terasa alami. Bridge tidak boleh memperkenalkan fakta kriminal kunci baru.

### Batch C — 6.500 context
Tambahkan percakapan non-kunci dalam semesta kasus yang sama: jadwal, makanan, baterai, perjalanan, keluarga, cuaca, koordinasi umum, percakapan pribadi, dan aktivitas sehari-hari.

### Batch D — 1.500 distractor
Tambahkan pesan ambigu/tidak relevan yang tetap berasal dari aktor dan periode yang sama sehingga retrieval tidak menjadi terlalu mudah.

## QA
Setiap batch menjalani:
1. exact duplicate check;
2. near-duplicate/template check;
3. chronological consistency check;
4. actor-state consistency check;
5. source-line/provenance validation;
6. leakage check;
7. safety/sanitization review;
8. sample human review oleh anggota kedua.

## Target kualitas
Dataset tidak dibuat hanya untuk menambah jumlah baris. Variasi harus berasal dari konteks percakapan dan state aktor, bukan paraphrase berulang.

## Catatan Ollama
10.000 pesan disimpan sebagai corpus dan tidak dimasukkan sekaligus ke prompt. P6 akan membangun retrieval berbasis conversation/time window dan evidence metadata.
