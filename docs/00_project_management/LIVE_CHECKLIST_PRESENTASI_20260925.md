# LIBERA — Live Checklist Persiapan Pengumpulan & Presentasi

**Tanggal:** 25 September 2026  
**Deadline PPT:** **10.00 WIB**  
**Presentasi:** **13.00 WIB**  
**Durasi presentasi:** **10 menit**  
**Canonical branch:** `main`  
**Canonical HEAD saat checklist dibuat:** `acb52e4509ab493b849341903daa9d034bc990d2`

> Dokumen ini adalah **single source of truth operasional** untuk seluruh anggota tim sampai PPT terkumpul dan presentasi selesai.  
> Semua anggota boleh melihat status di sini. Update status hanya berdasarkan output nyata dari laptop; jangan menandai PASS kalau belum benar-benar dijalankan.

---

## 0. Status repo yang SUDAH terverifikasi

Bagian ini tidak perlu dikerjakan ulang kecuali ada commit baru.

- [x] P1 selesai.
- [x] P2 selesai dan frozen.
- [x] Corpus final 10.000 pesan tidak boleh diubah downstream.
- [x] PR #15 `p5-finalize-daffa` sudah merge ke `main`.
- [x] P5 whole-word keyword matching sudah masuk `main`.
- [x] P5 examiner <=5 menit sudah tersedia.
- [x] P5 cryptographic lock sudah tersedia.
- [x] Runner menerima `-P5LockManifestPath`.
- [x] ChatSim SQLite seeding fix sudah masuk `main`.
- [x] Model final presentasi: `qwen2.5:1.5b`.
- [x] Embedding final: `bge-m3`.
- [x] Post-P2 Integration Audit pada merge PR #15: **SUCCESS**.
- [x] Build Final ChatSim pada merge PR #15: **SUCCESS**.
- [x] APK final ChatSim sudah dapat dibangun dari `main`.

**Artinya:** jangan menambah fitur baru kecuali ada bug yang benar-benar menghentikan final run.

---

# 1. Pembagian dua laptop

## Laptop A — Forensik / Demo

Tugas utama:

- Android Emulator + ChatSim.
- P3 acquisition.
- P4 extraction.
- P5 traditional baseline + examiner QC + lock.
- Screenshot acquisition, hash, artifact, examiner, P5 lock.
- Menjadi laptop utama untuk demo pukul 13.00 WIB.

Status:

- [ ] Repo sudah di `main` terbaru.
- [ ] Android emulator siap.
- [ ] `adb devices` mendeteksi emulator.
- [ ] APK ChatSim final terpasang.
- [ ] ChatSim terbuka dan chat terlihat.
- [ ] P3 final run selesai.
- [ ] P4 final extraction selesai.
- [ ] P5 examiner final selesai.
- [ ] P5 lock verify PASS.

## Laptop B — AI / Hasil / PPT

Tugas utama:

- Ollama.
- `bge-m3`.
- `qwen2.5:1.5b`.
- P6 retrieval.
- P7 LLM.
- P8 A/B/C + lock.
- P9 precheck/final evaluation bila GT sudah benar-benar siap.
- P10 report.
- Menyimpan hasil untuk PPT.

Status:

- [ ] Repo sudah di `main` terbaru.
- [ ] Ollama tersedia.
- [ ] `bge-m3` sudah tersedia lokal.
- [ ] `qwen2.5:1.5b` sudah tersedia lokal.
- [ ] P4 evidence + P5 hasil final sudah diterima dari Laptop A.
- [ ] Hash evidence Laptop A = Laptop B.
- [ ] P5 lock verify PASS di Laptop B.
- [ ] P6 final run selesai.
- [ ] P7 final run selesai.
- [ ] P8 A/B/C final run selesai.
- [ ] P8 lock selesai.
- [ ] P9 status sudah dicatat dengan benar.
- [ ] P10 report sudah terbentuk.

---

# 2. Sinkronisasi repo — wajib di kedua laptop

Jalankan di Laptop A dan Laptop B:

```powershell
cd libera
git switch main
git pull --ff-only origin main
git rev-parse HEAD
git status --short
```

Expected HEAD:

```text
acb52e4509ab493b849341903daa9d034bc990d2
```

Isi hasil aktual:

| Pemeriksaan | Laptop A | Laptop B |
|---|---|---|
| HEAD | _belum dilaporkan_ | _belum dilaporkan_ |
| Working tree bersih | _belum_ | _belum_ |
| Python tersedia | _belum_ | _belum_ |

- [ ] Kedua laptop menggunakan HEAD yang sama.
- [ ] Tidak ada perubahan lokal penting yang belum disimpan.

---

# 3. Laptop A — P3 acquisition + P4 extraction

## 3.1 Precheck

```powershell
adb devices
py -3 --version
```

Catat:

- ADB/emulator: _belum dilaporkan_
- Python: _belum dilaporkan_
- ChatSim dapat dibuka: **BELUM**
- Isi chat terlihat: **BELUM**

## 3.2 Jalankan P3–P4 actual

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -StopAfterP4
```

**Ini sudah masuk demo/praktikum sebenarnya**, bukan setup biasa.

Isi setelah selesai:

- P3: **BELUM / PROSES / PASS / FAIL**
- Folder ACQ-SIM: _belum_
- Device ID: _belum_
- Acquisition ID: _belum_
- Acquisition type: _belum_
- MASTER SHA-256: _belum_
- WORKING SHA-256: _belum_
- MASTER = WORKING: **BELUM**
- P4 extraction: **BELUM / PROSES / PASS / FAIL**
- Path `artifacts.csv`: _belum_
- Jumlah ART messages: _belum_
- Jumlah chat: _belum_
- SQLite integrity: _belum_

Expected controlled ChatSim state: sekitar **9.997 message artifacts**. Jangan mengubah angka hanya agar sama dengan 10.000; 10.000 adalah P2 source corpus, sedangkan ChatSim device state final memiliki 9.997 pesan.

### Bukti/screenshot lokal yang disimpan

- [ ] `01_chatsim.png`
- [ ] `02_acquisition.png`
- [ ] `03_sha256.png`
- [ ] `04_p4_artifacts.png`

**Wording presentasi:** ChatSim adalah *researcher-controlled Android evidence carrier* untuk simulasi logical acquisition. Jangan menyebut ChatSim sebagai WhatsApp atau menyatakan `run-as` mereplikasi protected WhatsApp acquisition.

---

# 4. Laptop A — P5 final

## 4.1 Cek apakah actual P5 hasil Daffa sudah ada

```powershell
Get-ChildItem runtime\working\P5
```

Checklist:

- [ ] `timeline.csv`
- [ ] `entities.csv`
- [ ] `relationships.csv`
- [ ] `baseline_findings.json`
- [ ] `baseline_manifest.json`
- [ ] `p5_examiner_packet.csv`
- [ ] `p5_examiner_packet_manifest.json`
- [ ] `p5_lock_manifest.json`

## 4.2 Kalau P5 lock sudah ada, VERIFIKASI — jangan rerun P5

```powershell
py -3 -m src.baseline.p5_lock --verify --manifest runtime\working\P5\p5_lock_manifest.json
```

Hasil:

- P5 lock verification: **BELUM / PASS / FAIL**
- Jumlah evidence direview: _belum_
- Waktu human QC: _belum_
- SUPPORTED: _belum_
- NOT_SUPPORTED: _belum_
- UNCERTAIN: _belum_

Kalau hasilnya:

```text
[P5-LOCK] VERIFY PASS
```

maka **P5 selesai. Jangan dijalankan ulang.**

## 4.3 Kalau P5 lock belum ada

Jalankan sekali:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_p5_examiner_review.ps1 -ArtifactsPath "demo_evidence\ACQ-SIM-001_...\artifacts\artifacts.csv"
```

Target human examiner: **<=300 detik** untuk maksimal 12 candidate evidence.

### Bukti/screenshot lokal

- [ ] `05_p5_examiner.png`
- [ ] `06_p5_lock.png`

---

# 5. Transfer Laptop A → Laptop B

Copy **utuh**:

```text
demo_evidence\ACQ-SIM-001_...\
runtime\working\P5\
```

Jangan hanya mengirim `artifacts.csv` atau `baseline_findings.json`.

## 5.1 Verifikasi hash evidence di dua laptop

Laptop A:

```powershell
Get-FileHash "demo_evidence\ACQ-SIM-001_...\artifacts\artifacts.csv" -Algorithm SHA256
```

Laptop B: jalankan command yang sama setelah transfer.

Isi:

- SHA Laptop A: _belum_
- SHA Laptop B: _belum_
- Hash sama: **BELUM / YA / TIDAK**

## 5.2 Verifikasi P5 lock di Laptop B

```powershell
py -3 -m src.baseline.p5_lock --verify --manifest runtime\working\P5\p5_lock_manifest.json
```

- P5 lock verify Laptop B: **BELUM / PASS / FAIL**

Kalau FAIL, **jangan mengedit manifest secara manual**. Cari penyebab path/hash terlebih dahulu.

---

# 6. Laptop B — AI environment

Jalankan:

```powershell
ollama --version
ollama list
```

Status:

- Ollama version: _belum_
- [ ] `bge-m3` tersedia.
- [ ] `qwen2.5:1.5b` tersedia.

Kalau belum:

```powershell
ollama pull bge-m3
ollama pull qwen2.5:1.5b
```

**Download model dilakukan sekarang, bukan saat presentasi.**

Locked final config:

```text
embedding   = bge-m3
model       = qwen2.5:1.5b
temperature = 0.1
seed        = 42
num_ctx     = 8192
top_k       = 8
prompt      = v2-forensic-grounded
```

---

# 7. P6 — memang dikerjakan SEKARANG

P6 bukan bagian yang ditunggu live saat presentasi.

P6 flow:

```text
P4 ART evidence
      ↓
evidence-aware chunking
      ↓
leakage guard
      ↓
BGE-M3 embeddings
      ↓
local retrieval index
```

Status:

- P6: **BELUM / PROSES / SELESAI / FAIL**
- Menggunakan P4 artifacts actual: **BELUM / YA / TIDAK**
- P5 lock sudah PASS sebelum final AI run: **BELUM / YA / TIDAK**
- Jumlah chunks: _belum_
- Leakage check: **BELUM / PASS / FAIL**
- Embedding model: _belum_
- Index berhasil dibuat: **BELUM / YA / TIDAK**
- Error/blocker: _tidak ada / isi error_

**Kalau teman sedang menjalankan P6 lokal sekarang, jangan dihentikan.** Yang tidak perlu adalah mengembangkan ulang P6 dari nol.

### Bukti/screenshot

- [ ] `07_p6_retrieval.png`

---

# 8. Dry-run satu kali sebelum final real AI run

Kalau belum pernah diverifikasi pada local actual evidence:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_libera_local.ps1 `
  -ArtifactsPath "demo_evidence\ACQ-SIM-001_...\artifacts\artifacts.csv" `
  -UseLockedP5 `
  -P5LockManifestPath "runtime\working\P5\p5_lock_manifest.json" `
  -DryRun
```

Status:

- Dry-run: **BELUM / PROSES / PASS / FAIL**
- Sampai `=== COMPLETE ===`: **BELUM / YA / TIDAK**
- Error: _tidak ada / isi error_

Kalau PASS, tidak perlu mengulang dry-run berkali-kali.

---

# 9. P7–P8 — kerjakan SEKARANG karena ini bisa lama

Final real run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_libera_local.ps1 `
  -ArtifactsPath "demo_evidence\ACQ-SIM-001_...\artifacts\artifacts.csv" `
  -UseLockedP5 `
  -P5LockManifestPath "runtime\working\P5\p5_lock_manifest.json"
```

Runner ini akan mengerjakan downstream secara otomatis:

```text
verify P5 lock
      ↓
P6 chunking + BGE-M3
      ↓
P7 Qwen2.5-1.5B
      ↓
P8 A/B/C
      ↓
P8 lock
      ↓
P9 precheck
      ↓
P10 report
```

## Status real run

- P7: **BELUM / PROSES / PASS / FAIL**
- P8: **BELUM / PROSES / PASS / FAIL**
- Real run sampai `=== COMPLETE ===`: **BELUM / YA / TIDAK**
- T01–T10 selesai: _belum_
- Condition A lengkap: **BELUM / YA / TIDAK**
- Condition B lengkap: **BELUM / YA / TIDAK**
- Condition C lengkap: **BELUM / YA / TIDAK**
- Model aktual: _belum_
- Prompt version aktual: _belum_
- Top-k aktual: _belum_
- Temperature aktual: _belum_
- Seed aktual: _belum_
- Error/blocker: _tidak ada / isi error_

**Jangan menjalankan P6–P8 full live pada presentasi 10 menit.**

---

# 10. P8 LOCK

Cek:

```powershell
Get-Item runtime\working\P8\p8_lock_manifest.json
```

Status:

- [ ] `experiment_output.json` ada.
- [ ] `run_log.jsonl` ada.
- [ ] `p8_lock_manifest.json` ada.
- P8 lock: **BELUM / PASS / FAIL**

Setelah P8 locked:

> **Jangan rerun P8 setelah private ground truth dibuka.**

### Bukti/screenshot

- [ ] `08_p8_abc.png`
- [ ] `09_p8_lock.png`

Untuk PPT cukup pilih **satu task yang paling mudah dijelaskan** dan tunjukkan perbedaan:

```text
A — LLM only
B — LLM + RAG
C — LLM + RAG + structured forensic output
```

---

# 11. P9 — bedakan PRECHECK vs FINAL METRICS

## Kalau private GT belum selesai

Status yang sah:

- P9 = **PRECHECK**
- P9_PRECHECK_PASS: **BELUM / YA / TIDAK**
- Invalid ART references: _belum_
- Structured JSON C valid: _belum_/10

Boleh masuk PPT sebagai **integrity/pre-evaluation check**, tetapi jangan disebut final accuracy.

## Kalau private GT benar-benar sudah selesai oleh evaluator

Syarat:

- [ ] GT tidak pernah diberikan ke P5/P6/P7/P8.
- [ ] P8 sudah di-lock sebelum GT dibuka.
- [ ] GT final sudah dikunci.
- [ ] Final P9 tidak rerun P8.

Hasil aktual:

- jumlah labeled evidence: _belum_
- positive/key evidence: _belum_
- precision A/B/C: _belum_
- recall A/B/C: _belum_
- F1 A/B/C: _belum_
- unacquired evidence: _belum_

**Dilarang membuat atau mengira-ngira angka P9.**

---

# 12. P10 — report

Cek:

```powershell
Get-Item runtime\working\P10\run_report.md
```

Status:

- P10 report: **BELUM / ADA / FAIL**
- Acquisition mode yang tertulis: _belum_
- P4 artifact count: _belum_
- P5 status: _belum_
- Model: _belum_
- P8 lock tercatat: **BELUM / YA / TIDAK**
- P9 status: _belum_

### Screenshot

- [ ] `10_p10_report.png`

---

# 13. Folder screenshot/bukti presentasi

Buat secara lokal:

```powershell
New-Item -ItemType Directory -Force presentation_evidence
```

Target:

```text
presentation_evidence\
├── 01_chatsim.png
├── 02_acquisition.png
├── 03_sha256.png
├── 04_p4_artifacts.png
├── 05_p5_examiner.png
├── 06_p5_lock.png
├── 07_p6_retrieval.png
├── 08_p8_abc.png
├── 09_p8_lock.png
└── 10_p10_report.png
```

Progress screenshot: **0/10** _(update angka ini sesuai kondisi nyata)_.

Catatan: screenshot adalah bukti presentasi. Jangan memasukkan private ground truth atau informasi sensitif ke repo publik.

---

# 14. PPT — harus terkumpul 10.00 WIB

**Target internal submit: 09.40 WIB. Jangan menunggu 09.59.**

Untuk presentasi hanya 10 menit, target **8–10 slide**:

- [ ] 1. Judul + masalah.
- [ ] 2. P1/P2 — research case design + frozen corpus.
- [ ] 3. Diagram DFRWS / pipeline P3–P10.
- [ ] 4. ChatSim + disclosure controlled simulation.
- [ ] 5. P3/P4 — acquisition, hash, extraction.
- [ ] 6. P5 — traditional baseline + examiner <=5 menit + lock.
- [ ] 7. P6/P7 — RAG + local LLM.
- [ ] 8. P8 — satu contoh A/B/C actual result.
- [ ] 9. P9/P10 — actual status/results + integrity.
- [ ] 10. Kesimpulan + keterbatasan.

PPT progress:

- Total slide selesai: _belum_/10
- PPT final backup di Laptop A: **BELUM**
- PPT final backup di Laptop B: **BELUM**
- Backup Drive/flashdisk: **BELUM**
- Target submit <=09.40: **BELUM**

---

# 15. Presentasi 13.00 WIB — maksimal 10 menit

## Yang dilakukan live

```text
ChatSim
  ↓
P3 acquisition singkat
  ↓
P4 extraction
  ↓
tunjukkan mekanisme P5
  ↓
buka hasil P6–P10 yang SUDAH JADI
```

## Yang TIDAK dijalankan full live

- `ollama pull`
- BGE-M3 full indexing
- 30 inference A/B/C
- P8 full experiment
- P9 final evaluation

Semua proses yang bisa lama harus sudah selesai **sebelum PPT dikumpulkan**.

## Pembagian waktu presentasi

| Waktu | Isi |
|---:|---|
| 0:00–1:00 | Masalah + tujuan |
| 1:00–2:15 | P1/P2 |
| 2:15–3:30 | DFRWS / arsitektur |
| 3:30–5:30 | Demo ChatSim → P3/P4 |
| 5:30–6:30 | P5 + examiner |
| 6:30–8:15 | P6/P7/P8 + hasil A/B/C yang sudah jadi |
| 8:15–9:15 | P9/P10 |
| 9:15–10:00 | Kesimpulan |

Rehearsal:

- [ ] Emulator sudah terbuka.
- [ ] ChatSim siap.
- [ ] Hasil final P8/P10 tersedia lokal.
- [ ] PPT ada di Laptop A.
- [ ] PPT ada di Laptop B.
- [ ] Backup tersedia.
- [ ] Charger dua laptop siap.
- [ ] Rehearsal <=10 menit.
- Waktu rehearsal aktual: _belum_.

---

# 16. Prioritas waktu dari sekarang

## PRIORITAS 1 — sekarang juga

1. Pastikan P3/P4/P5 actual outputs ada dan P5 lock PASS.
2. Kalau P6 sedang berjalan dengan actual P4 evidence dan P5 sudah locked, **biarkan P6 lanjut**.
3. Pull/download `bge-m3` dan `qwen2.5:1.5b` sekarang.
4. Jalankan P6/P7/P8 sekarang; jangan tunggu mendekati presentasi.
5. Screenshot setiap checkpoint penting ketika berhasil.

## PRIORITAS 2 — sambil Laptop B menghitung

Laptop A / anggota lain langsung menyusun PPT bagian yang tidak menunggu hasil AI:

- masalah;
- desain penelitian;
- DFRWS;
- P1/P2;
- ChatSim;
- P3/P4;
- P5;
- metodologi P6/P7/P8.

Jangan menunggu P8 selesai baru mulai PPT.

## PRIORITAS 3 — begitu AI selesai

1. Masukkan satu contoh A/B/C actual result.
2. Catat P8 lock.
3. Catat P9 yang memang tersedia.
4. Masukkan P10 report.
5. Finalisasi PPT.
6. Rehearsal.
7. Submit sebelum 09.40.

---

# 17. Format update progress tim

Setiap anggota boleh copy blok ini dan update di commit/PR/chat tim:

```text
UPDATE LIBERA

TIME:
NAMA:

A — Sync
Laptop A HEAD:
Laptop B HEAD:

C/D — P3/P4
P3:
P4:
artifacts.csv:
jumlah ART:
SHA MASTER:
SHA WORKING:

E — P5
examiner:
waktu:
P5 lock verify:

F — Transfer
SHA Laptop A:
SHA Laptop B:
P5 verify Laptop B:

H — P6
status:
chunks:
leakage:
index:

J/K — P7/P8
status:
model:
A/B/C:
P8 lock:

L — P9
status:

M — P10
report:

N — Screenshots
__/10

O — PPT
__/10 slide selesai

ERROR/BLOCKER:
(copy-paste error apa adanya)
```

---

# 18. Aturan update dokumen ini

Agar tracking tidak kacau:

1. Selalu `git pull --ff-only origin main` sebelum mengedit tracker.
2. **Satu orang saja** yang mengedit tracker pada satu waktu.
3. Jangan push runtime evidence, private GT, credentials, atau file sensitif ke repo publik.
4. Tracker hanya menyimpan **status, angka ringkas, path relatif, dan hasil PASS/FAIL**.
5. Gunakan commit message sederhana, misalnya:

```text
progress: update P6 final run
progress: record P8 lock
progress: finalize presentation checklist
```

6. Kalau ada conflict pada tracker, jangan overwrite hasil anggota lain; pull dan gabungkan status terbaru.
7. Status `PASS` hanya boleh ditulis kalau ada output nyata yang mendukungnya.

---

# Ringkasan posisi saat checklist dibuat

```text
REPO / IMPLEMENTATION
P1             ✅
P2             ✅ FROZEN
P3 implementation ✅
P4 implementation ✅
P5 implementation ✅ + merged
P6 implementation ✅
P7 implementation ✅
P8 implementation ✅
P9 implementation ✅
P10 implementation ✅
CI             ✅
ChatSim build  ✅

LOCAL FINAL EXECUTION
P3/P4          ⏳ perlu status aktual tim
P5 lock        ⏳ perlu status aktual tim
P6             ⏳ mungkin sedang berjalan lokal
P7/P8          ⏳ jalankan sekarang
P9             ⏳ setelah P8 lock
P10            ⏳ setelah run
PPT            ⏳ harus submit <=09.40 WIB
PRESENTASI     ⏳ 13.00 WIB, 10 menit
```
