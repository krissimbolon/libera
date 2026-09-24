"""Evidence-aware chunking for LIBERA P6.

Chunks are built per merged participant chat + time window and preserve
traceability to ART evidence IDs. The text sent to retrieval/LLM includes
explicit evidence IDs, timestamps and sender/receiver labels so downstream
claims can cite acquired evidence instead of hidden source identifiers.
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
    "message_id", "conversation_id", "sender", "receiver",
    "timestamp_normalized", "message_text",
]


class ChunkingError(Exception):
    pass


def load_messages(csv_path: Path) -> List[Dict[str, str]]:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise ChunkingError(f"File input tidak ditemukan: {csv_path}")
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if not rows:
        raise ChunkingError(f"File input kosong: {csv_path}")
    missing = [c for c in REQUIRED_FIELDS if c not in fieldnames]
    if missing:
        raise ChunkingError(
            f"Kolom wajib hilang di {csv_path}: {missing}. "
            f"Kolom yang ditemukan: {fieldnames}"
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
    by_conv: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for m in messages:
        by_conv[m["conversation_id"]].append(m)

    groups: List[List[Dict[str, str]]] = []
    for _, conv_messages in sorted(by_conv.items()):
        conv_messages.sort(
            key=lambda m: (_parse_ts(m["timestamp_normalized"]), m["message_id"])
        )
        current: List[Dict[str, str]] = []
        window_start = None
        for msg in conv_messages:
            ts = _parse_ts(msg["timestamp_normalized"])
            if not current:
                current = [msg]
                window_start = ts
                continue
            elapsed = (ts - window_start).total_seconds() / 60.0
            if len(current) >= max_size or elapsed > time_window_minutes:
                groups.append(current)
                current = [msg]
                window_start = ts
            else:
                current.append(msg)
        if current:
            groups.append(current)
    return groups


def _render_evidence_line(m: Dict[str, str]) -> str:
    evidence_id = m.get("evidence_id") or m["message_id"]
    return (
        f"[{evidence_id}] {m['timestamp_normalized']} "
        f"{m['sender']} -> {m['receiver']}: {m['message_text']}"
    )


def build_chunk_record(group: List[Dict[str, str]], min_size: int) -> Dict[str, Any]:
    message_ids = [m["message_id"] for m in group]
    evidence_ids = [m.get("evidence_id", "") for m in group if m.get("evidence_id")]
    participants = sorted({m["sender"] for m in group} | {m["receiver"] for m in group})
    timestamps = [_parse_ts(m["timestamp_normalized"]) for m in group]
    concat_text = "\n".join(_render_evidence_line(m) for m in group)
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
    if min_size < 1 or max_size < min_size:
        raise ChunkingError("Ukuran chunk tidak valid.")
    messages = load_messages(input_csv)
    groups = group_by_conversation_and_window(
        messages, min_size, max_size, time_window_minutes
    )
    chunks = [build_chunk_record(g, min_size) for g in groups]
    output_jsonl = Path(output_jsonl)
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with output_jsonl.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return chunks


def main() -> None:
    p = argparse.ArgumentParser(description="Evidence-aware P6 chunker.")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--min-size", type=int, default=30)
    p.add_argument("--max-size", type=int, default=60)
    p.add_argument("--time-window-minutes", type=int, default=120)
    args = p.parse_args()
    try:
        chunks = run(
            Path(args.input), Path(args.output),
            args.min_size, args.max_size, args.time_window_minutes,
        )
    except ChunkingError as exc:
        print(f"[chunker] ERROR: {exc}")
        raise SystemExit(1)
    print(f"[chunker] PASS chunks={len(chunks)} output={args.output}")


if __name__ == "__main__":
    main()
