"""
run_log.py - Utilitas ID generation dan logging JSONL append-only.

Dipakai oleh chunker.py, retriever.py, ollama_runner.py, run_experiment.py
supaya format ID dan format log konsisten di seluruh pipeline P6/P7/P8.

ID prefix mengikuti konvensi yang disebut di dokumen proyek (RUN-, CHK-,
FND-, ART-, ACQ-, DEV-, ERR-). Modul ini hanya bertanggung jawab atas
RUN-/CHK-/FND- karena ART-/ACQ-/DEV- adalah tanggung jawab jalur P3/P4.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def utc_now_iso() -> str:
    """Timestamp ISO-8601 UTC, dipakai konsisten di seluruh log."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def new_run_id() -> str:
    return _new_id("RUN")


def new_chunk_id() -> str:
    return _new_id("CHK")


def new_finding_id() -> str:
    return _new_id("FND")


def append_jsonl(path: Path, record: Dict[str, Any]) -> None:
    """Tambahkan satu baris JSON ke file log (append-only).

    Membuat parent directory jika belum ada. Aman dipanggil berulang kali
    dari proses berbeda (tidak melakukan locking khusus - cukup untuk
    prototype single-user).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path: Path):
    """Generator baris JSON dari file JSONL. Mengembalikan list kosong
    jika file belum ada (bukan error) - berguna untuk test/dry-run awal.
    """
    path = Path(path)
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
