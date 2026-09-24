"""
chunker.py - Evidence-aware chunking untuk pipeline P6.

Mengelompokkan pesan berdasarkan conversation_id + time window (BUKAN
fixed row count), sesuai PDF Bab 6.1 poin 5: "Chunk berdasarkan
conversation + time window, bukan fixed 500 row. Target awal 30-60
pesan/chunk."

Setiap chunk menyimpan message_ids, evidence_ids, time_range,
participants, dan content_hash (SHA-256) untuk provenance - lihat PDF
Bab 6.3 (traceability CHK -> ART/ID-MSG).

CLI:
    python -m src.ai_rag.chunker --input data/toy/toy_case_evidence.csv \
        --output configs/toy_chunks.jsonl \
        [--min-size 30] [--max-size 60] [--time-window-minutes 120]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .run_log import new_chunk_id, utc_now_iso

REQUIRED_FIELDS = [
    "message_id",
    "conversation_id",
    "sender",
    "receiver",
    "timestamp_normalized",
    "message_text",
]


class ChunkingError(Exception):
    pass


def load_messages(csv_path: Path) -> List[Dict[str, str]]:
    """Baca CSV evidence dan validasi field wajib (error handling dasar)."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise ChunkingError(f"File input tidak ditemukan: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ChunkingError(f"File input kosong: {csv_path}")

    missing = [c for c in REQUIRED_FIELDS if c not in reader.fieldnames]
    if missing:
        raise ChunkingError(
            f"Kolom wajib hilang di {csv_path}: {missing}. "
            f"Kolom yang ditemukan: {reader.fieldnames}"
        )

    return rows


def _parse_ts(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ChunkingError(f"Timestamp tidak valid: {value!r}") from exc


def group_by_conversation_and_window(
    messages: List[Dict[str, str]],
    min_size: int,
    max_size: int,
    time_window_minutes: int,
) -> List[List[Dict[str, str]]]:
    """Kelompokkan pesan per conversation_id, lalu pecah lagi per time
    window dan batas max_size. Jika grup lebih kecil dari min_size (mis.
    pada toy dataset), tetap dijadikan satu chunk dan ditandai
    'below_target_size' oleh caller.
    """
    by_conv: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for m in messages:
        by_conv[m["conversation_id"]].append(m)

    groups: List[List[Dict[str, str]]] = []
    for conv_id, conv_messages in by_conv.items():
        conv_messages.sort(key=lambda m: _parse_ts(m["timestamp_normalized"]))

        current_group: List[Dict[str, str]] = []
        window_start = None

        for msg in conv_messages:
            ts = _parse_ts(msg["timestamp_normalized"])
            if not current_group:
                current_group = [msg]
                window_start = ts
                continue

            elapsed_minutes = (ts - window_start).total_seconds() / 60.0
            if len(current_group) >= max_size or elapsed_minutes > time_window_minutes:
                groups.append(current_group)
                current_group = [msg]
                window_start = ts
            else:
                current_group.append(msg)

        if current_group:
            groups.append(current_group)

    return groups


def build_chunk_record(group: List[Dict[str, str]], min_size: int) -> Dict[str, Any]:
    message_ids = [m["message_id"] for m in group]
    evidence_ids = [m.get("evidence_id", "") for m in group]
    participants = sorted({m["sender"] for m in group} | {m["receiver"] for m in group})
    timestamps = [_parse_ts(m["timestamp_normalized"]) for m in group]

    concat_text = "\n".join(m["message_text"] for m in group)
    content_hash = hashlib.sha256(concat_text.encode("utf-8")).hexdigest()

    return {
        "chunk_id": new_chunk_id(),
        "conversation_id": group[0]["conversation_id"],
        "message_ids": message_ids,
        "evidence_ids": evidence_ids,
        "participants": participants,
        "time_range": {
            "start": min(timestamps).isoformat(),
            "end": max(timestamps).isoformat(),
        },
        "message_count": len(group),
        "below_target_size": len(group) < min_size,
        "content_hash_sha256": content_hash,
        "text": concat_text,
        "created_at": utc_now_iso(),
    }


def run(
    input_csv: Path,
    output_jsonl: Path,
    min_size: int = 30,
    max_size: int = 60,
    time_window_minutes: int = 120,
) -> List[Dict[str, Any]]:
    messages = load_messages(input_csv)
    groups = group_by_conversation_and_window(
        messages, min_size=min_size, max_size=max_size, time_window_minutes=time_window_minutes
    )
    chunks = [build_chunk_record(g, min_size=min_size) for g in groups]

    output_jsonl = Path(output_jsonl)
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with output_jsonl.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Evidence-aware chunker (P6).")
    parser.add_argument("--input", required=True, help="Path CSV evidence (mis. data/toy/toy_case_evidence.csv)")
    parser.add_argument("--output", required=True, help="Path output JSONL chunk")
    parser.add_argument("--min-size", type=int, default=30)
    parser.add_argument("--max-size", type=int, default=60)
    parser.add_argument("--time-window-minutes", type=int, default=120)
    args = parser.parse_args()

    try:
        chunks = run(
            input_csv=Path(args.input),
            output_jsonl=Path(args.output),
            min_size=args.min_size,
            max_size=args.max_size,
            time_window_minutes=args.time_window_minutes,
        )
    except ChunkingError as exc:
        print(f"[chunker] ERROR: {exc}")
        raise SystemExit(1)

    below_target = sum(1 for c in chunks if c["below_target_size"])
    print(f"[chunker] {len(chunks)} chunk dibuat -> {args.output}")
    if below_target:
        print(
            f"[chunker] Catatan: {below_target} chunk di bawah target "
            f"min_size={args.min_size} (wajar untuk toy dataset kecil)."
        )


if __name__ == "__main__":
    main()
