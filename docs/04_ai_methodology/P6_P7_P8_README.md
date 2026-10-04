# P6/P7/P8 — Cara Pakai (AI/RAG Prototype)

Lihat `P6_P7_P8_IMPLEMENTATION_PLAN.md` untuk penjelasan arsitektur.
File ini fokus ke perintah yang dijalankan.

## 0. Prasyarat

- Python 3.10+ (cek: `python --version`)
- (Opsional, untuk P7 sungguhan) [Ollama](https://ollama.com) berjalan lokal
  di `http://localhost:11434`. Tanpa Ollama, semua skrip tetap bisa
  dijalankan dengan flag `--dry-run`.

## 1. Setup environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r src/ai_rag/requirements.txt
```

`requirements.txt` sengaja minimal (lihat isi filenya) — prototype ini
hanya memakai standard library Python.

## 2. Jalankan chunking pada toy data

```bash
python -m src.ai_rag.chunker --input data/toy/toy_case_evidence.csv --output configs/toy_chunks.jsonl
```

Menghasilkan `configs/toy_chunks.jsonl` — satu baris JSON per chunk,
berisi `chunk_id`, `conversation_id`, `message_ids`, `time_range`,
`participants`, `content_hash`.

## 3. Cek kebocoran sebelum indexing

```bash
python -m src.ai_rag.leakage_check --input configs/toy_chunks.jsonl
```

Keluar dengan exit code bukan-0 dan pesan jelas jika menemukan penanda
Ground Truth atau court narrative.

## 4. Bangun index & coba retrieval

```bash
python -m src.ai_rag.retriever build --chunks configs/toy_chunks.jsonl --namespace case_evidence --index configs/toy_index.json
python -m src.ai_rag.retriever query --index configs/toy_index.json --query "siapa yang terlibat dalam insiden ini" --k 3
```

## 5. Jalankan Ollama runner

Tanpa Ollama (aman, tidak butuh koneksi apa pun):

```bash
python -m src.ai_rag.ollama_runner --dry-run --query "Ringkas insiden yang terjadi" --prompt-version v1
```

Dengan Ollama (pastikan `ollama serve` sudah jalan dan model sudah di-pull,
mis. `ollama pull qwen2.5`):

```bash
python -m src.ai_rag.ollama_runner --model qwen2.5 --query "Ringkas insiden yang terjadi" --prompt-version v1
```

Semua run (dry-run maupun asli) dicatat ke file JSONL `--run-log` (default `runtime/working/P8/run_log.jsonl`; generated at runtime, tidak di-track Git).

## 6. Jalankan eksperimen A/B/C

```bash
python -m src.ai_rag.run_experiment --dry-run --index configs/toy_index.json --questions configs/investigation_tasks.json --output runtime/working/toy/experiment_output.json --run-log runtime/working/toy/run_log.jsonl
```

Ganti `--dry-run` dengan `--model <nama_model>` untuk run sungguhan.
*Koreksi arsip (2026-10-05):* versi awal dokumen ini menyebut `configs/toy_questions.json`
akan dibuat otomatis; `run_experiment.py` tidak melakukannya. Gunakan
`configs/investigation_tasks.json` atau file JSON pertanyaan sendiri
(`{"questions": ["..."]}`). `run_experiment.py` menolak menimpa output yang sudah ada.

## 7. Jalankan test

```bash
python -m pytest tests/test_p6_p7_pipeline.py -v
```

Semua test berjalan tanpa Ollama (memakai mode dry-run / data toy).

## 8. Struktur output yang dihasilkan pipeline (runtime, JANGAN di-commit)

File di bawah ini *generated at runtime* oleh langkah 2–6 dan sengaja tidak di-track Git.

```
configs/toy_chunks.jsonl      # hasil chunking (boleh commit sebagai contoh)
configs/toy_index.json        # index vektor toy (boleh commit sebagai contoh)
configs/run_log.jsonl         # log tiap run Ollama (LOCAL ONLY jika berisi
                               # query/eksperimen sungguhan; contoh toy boleh)
```

Tambahkan ke `.gitignore` proyek (baris baru, jangan timpa file yang ada):

```
configs/run_log.jsonl
configs/*_index.json
!configs/toy_index.json
```
