# Desain Dataset Adaptasi Indonesia — 10.000 Pesan

## Keputusan metodologis

Dataset 10.000 baris **bukan** rekonstruksi verbatim kasus Galloway. Istilah yang digunakan adalah:

> Dataset sintetis Indonesia yang diadaptasi secara struktural dari bukti komunikasi publik dalam kasus Galloway.

Rekonstruksi sumber tetap dipisahkan pada P1. P2 menggunakan hasil rekonstruksi yang telah dipetakan sebagai jangkar, kemudian menambahkan pesan sintetis yang konsisten dengan alur kasus tanpa mengklaimnya sebagai fakta pengadilan.

## Target ukuran

Total target: **10.000 pesan WhatsApp sintetis**.

Komposisi awal:
- 500 pesan `ADAPTED_FROM_GALLOWAY`: adaptasi Bahasa Indonesia dari baris sumber yang sudah dipetakan.
- 1.500 pesan `SYNTHETIC_BRIDGE`: penghubung kronologi/percakapan, tidak boleh memperkenalkan fakta kriminal utama baru.
- 6.500 pesan `SYNTHETIC_CONTEXT`: percakapan sehari-hari, logistik umum, keluarga, makanan, perjalanan, waktu, pekerjaan, dan konteks yang membuat corpus realistis.
- 1.500 pesan `SYNTHETIC_DISTRACTOR`: pesan ambigu/tidak relevan yang tetap berada dalam semesta aktor dan periode kasus.

## Aturan "tanpa pengulangan"

Yang dilarang:
- duplikasi baris identik;
- template yang diulang dengan hanya mengganti nama/angka;
- percakapan yang diduplikasi antaraktor;
- blok hasil copy-paste.

Yang **tidak** dilarang:
- kata atau respons alami yang memang dapat berulang seperti “oke”, “iya”, “di mana?”, selama konteks, waktu, dan message_id berbeda.

Memaksa semua teks pesan unik secara literal akan membuat chat tidak natural dan justru merusak validitas simulasi.

## Lokalisasi Indonesia

Lokalisasi dilakukan pada:
- bahasa: Bahasa Indonesia percakapan yang natural;
- mata uang: rupiah;
- lokasi: kota/wilayah Indonesia yang dipilih untuk skenario;
- hotel/penginapan: nama fiktif;
- platform iklan/komunikasi: nama fiktif atau generik;
- nomor telepon: nomor uji/fiktif;
- nama aktor: seluruhnya fiktif;
- slang: disesuaikan ke penggunaan Indonesia tanpa menyalin slang sumber secara literal.

Struktur peristiwa Galloway dipertahankan pada tingkat pola:
- rekrutmen;
- kontrol terhadap pergerakan;
- koordinasi penginapan;
- transportasi;
- pemantauan aktivitas;
- intimidasi/ancaman;
- ketergantungan;
- pencarian orang yang pergi;
- komunikasi dengan calon pelanggan;
- koordinasi antaranggota kelompok.

Detail eksplisit yang tidak diperlukan untuk tujuan forensik dapat disanitasi. Untuk aktor di bawah umur, dataset tidak akan memuat konten seksual eksplisit.

## Ground-truth leakage

Court record, file rekonstruksi sumber, dan tabel ground truth **tidak boleh** dimasukkan ke indeks RAG investigator.

Pipeline eksperimen hanya menerima hasil akuisisi WhatsApp sintetis.

## Empat tingkat evidentiary signal

Setiap pesan diberi label evaluator-only:
- `DIRECT`: bukti langsung yang terkait event ground truth;
- `SUPPORTING`: memperkuat relasi/timeline/event;
- `AMBIGUOUS`: dapat memiliki lebih dari satu interpretasi;
- `NEUTRAL`: konteks normal/distractor.

Label ini disimpan privat dan dihapus dari dataset yang dianalisis model.

## Skema pesan

Kolom inti:
- `message_id`
- `conversation_id`
- `timestamp`
- `sender_id`
- `recipient_id`
- `message_text`
- `message_type`
- `reply_to_message_id`
- `attachment_id`
- `source_provenance`
- `source_original_line`
- `transformation_id`

Kolom ground truth privat:
- `evidence_strength`
- `event_id`
- `expected_entity_ids`
- `expected_relation_ids`
- `is_key_evidence`
- `annotation_notes`

## Aturan generasi

1. 500 pesan anchor dibuat lebih dahulu.
2. Urutan event dibangun dari timeline sumber, bukan dari imajinasi bebas.
3. Pesan bridge hanya mengisi kontinuitas percakapan.
4. Context/distractor tidak boleh menciptakan korban, tindakan kriminal utama, atau outcome baru yang tidak ada pada desain kasus.
5. Semua 10.000 pesan memiliki `message_id` unik.
6. Pemeriksaan exact duplicate dilakukan sebelum dataset dikunci.
7. Pemeriksaan near-duplicate dilakukan untuk mendeteksi template berulang.
8. Distribusi panjang pesan, jam kirim, jeda percakapan, dan respons pendek dibuat heterogen.
9. Corpus tidak pernah dikirim sebagai satu prompt penuh ke Ollama; analisis menggunakan retrieval/chunking.

## Implikasi untuk Ollama

10.000 baris adalah ukuran corpus, bukan ukuran prompt.

Untuk eksperimen:
- chunk berdasarkan conversation + time window, bukan 500 baris arbitrer;
- target awal sekitar 30–60 pesan per chunk;
- overlap hanya pada layer retrieval bila diperlukan, bukan sebagai duplikasi dataset;
- RAG mengambil top-k chunk relevan;
- model menerima evidence ID dan provenance pada setiap chunk.

## Kriteria selesai P2

P2 dianggap selesai bila:
- 10.000 baris lolos duplicate/near-duplicate audit;
- semua aktor dan lokasi fiktif;
- mapping source → adapted tersedia untuk anchor;
- timeline konsisten;
- ground truth privat terpisah;
- tidak ada source court narrative yang bocor ke RAG;
- dataset chat-only siap disimulasikan melalui WhatsApp test account.
