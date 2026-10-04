# Streamlit Workbench terintegrasi langsung dengan ChatSim

Status: demo lokal selesai dan diverifikasi pada 25 September 2026. Workbench kini disusun **forensic-first**: AI berada setelah acquisition, integrity check, dan pemeriksaan tradisional.

## Menjalankan

Jalankan emulator yang sudah terpasang ChatSim, lalu dari root repo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_workbench.ps1
```

Buka `http://127.0.0.1:8501`. Workbench berjalan lokal. Setelah seluruh dependency tersedia, pemeriksaan evidence dan tampilan hasil historis tidak memerlukan pengiriman case data ke layanan cloud.

## Alur data

```text
ChatSim Android (DEV-SIM-001)
  → ADB force-stop + run-as
  → logical SQLite acquisition
  → master copy + working copy
  → SHA-256 verification
  → read-only SQLite examination
  → traditional examiner view
  → optional local AI assistance
  → citation validation
  → report
```

ChatSim adalah controlled Android evidence carrier untuk simulasi penelitian. Ia bukan WhatsApp dan bukan perangkat sitaan nyata.

Dashboard tidak membaca CSV sebagai sumber percakapan. Pesan yang diperiksa berasal dari SQLite hasil acquisition ChatSim. Historical P8/P9/P10 hanya ditampilkan jika lock dan hash yang diperlukan lolos verifikasi.

## Delapan tab Workbench

| Tab | Fungsi |
| --- | --- |
| **Kasus & Integritas** | Menunjukkan acquisition ID, device ID, jumlah artifact/chat, SHA-256, dan status master/working copy. |
| **Percakapan** | Membaca chat kronologis dari working copy. |
| **Pencarian** | Literal search dan filter pengirim tanpa AI. |
| **Timeline** | Meninjau artifact berdasarkan tanggal. |
| **Jejak Bukti** | Menelusuri `ART-*` atau `message_id` kembali ke acquisition snapshot. |
| **Pemeriksaan Tradisional** | Menampilkan actor/pair activity serta P5 human examiner QC bila packet tersedia. |
| **Asisten AI** | Menampilkan locked A/B/C experiment sebagai copilot setelah evidence tersedia. |
| **Validasi & Laporan** | Memprioritaskan citation integrity dan quarantined references; provenance proxy ditempatkan sebagai analisis tambahan. |

## Makna A/B/C

A/B/C bukan tiga tahap forensic workflow.

- **A — tanpa case evidence:** negative control.
- **B — + retrieved evidence:** BGE-M3 mengambil artifact lokal untuk menjawab investigation question.
- **C — + structured output:** retrieval sama dengan B, tetapi jawaban dipaksa ke schema terstruktur agar lebih mudah diaudit.

Final run menyelesaikan 30/30 respons. Semua 10 output C valid secara schema, tetapi hanya 12 dari 24 evidence references C yang valid. Dua belas reference lainnya dikarantina dan tetap dipertahankan sebagai error model.

## Integritas snapshot

Setiap acquisition membuat folder baru. Master sebelumnya tidak ditimpa. ChatSim dihentikan sementara agar SQLite konsisten. Workbench menolak snapshot jika:

- hash perangkat dan file hasil capture berbeda;
- hash master/working/manifest tidak cocok;
- SQLite `integrity_check` gagal;
- `foreign_key_check` menemukan masalah;
- WAL aktif dan tidak kosong.

`ART-xxxxxx` mengikuti urutan deterministik `timestamp,message_id` pada satu snapshot. Jika hash snapshot berbeda dari sumber eksperimen P8, evidence link historis dinonaktifkan agar hasil lama tidak dipetakan ke snapshot baru secara keliru.

## Actual local results

- Acquisition ChatSim: **9.997 pesan, 25 chat**.
- P5 examiner review: **6 SUPPORTED, 4 NOT_SUPPORTED, 2 UNCERTAIN** dari 12 candidate artifacts.
- P6: **645 BGE-M3 index entries**, dimensi 1.024, leakage check PASS.
- P8: **30/30 real responses**, 10/10 C schema valid, **14/14 P8 lock hashes PASS**.
- Citation validation: B tidak menghasilkan invalid reference pada final run; C menghasilkan **12 invalid references dari 24 submitted references**.

## Batas interpretasi

Provenance reconstruction yang tersedia bukan independent semantic ground truth. Proxy metrics hanya mengukur subset anchor-versus-distractor dan tidak boleh disebut semantic accuracy key evidence.

Independent human semantic annotation belum tersedia. Karena itu LIBERA tidak membuat klaim final precision/recall/F1 terhadap key forensic evidence.

## Peran Workbench dalam presentasi

Untuk demo 10 menit, urutan yang disarankan:

1. buka ChatSim;
2. tunjukkan acquisition snapshot dan SHA-256;
3. buka conversation/search/timeline;
4. telusuri satu `ART-*`;
5. buka pemeriksaan tradisional/P5;
6. baru buka satu investigation question pada tab Asisten AI;
7. tunjukkan bahwa structured output dapat tetap memiliki citation error;
8. tutup dengan tab Validasi & Laporan.

Jangan menjalankan full embedding atau 30 inference call saat presentasi. Gunakan hasil P8 yang sudah dikunci.
