#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def export_query(conn: sqlite3.Connection, query: str, path: Path) -> int:
    cur = conn.execute(query)
    headers = [d[0] for d in cur.description]
    count = 0
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in cur:
            writer.writerow(row)
            count += 1
    return count


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("database")
    ap.add_argument("--out", default="artifacts")
    args = ap.parse_args()

    db_path = Path(args.database).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    uri = f"file:{db_path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise SystemExit(f"SQLite integrity_check failed: {integrity}")

        messages_path = out / "ART-00001_messages.csv"
        chats_path = out / "ART-00002_chats.csv"
        metadata_path = out / "ART-00003_device_metadata.csv"

        message_count = export_query(conn, """
            SELECT message_id, chat_id, segment_id, timestamp, sender_id,
                   recipient_id, sender_name, recipient_name, message_text,
                   message_type, reply_to_message_id
            FROM messages
            ORDER BY timestamp, message_id
        """, messages_path)

        chat_count = export_query(conn, """
            SELECT chat_id, peer_id, peer_name, last_timestamp, last_text,
                   message_count
            FROM chats
            ORDER BY last_timestamp DESC
        """, chats_path)

        metadata_count = export_query(conn, """
            SELECT key, value FROM metadata ORDER BY key
        """, metadata_path)

        fk_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
    finally:
        conn.close()

    manifest = {
        "extraction_time_utc": datetime.now(timezone.utc).isoformat(),
        "source_database": str(db_path),
        "source_database_sha256": sha256(db_path),
        "sqlite_integrity_check": "ok",
        "foreign_key_error_count": len(fk_errors),
        "artifacts": [
            {
                "artifact_id": "ART-00001",
                "type": "messages",
                "path": messages_path.name,
                "row_count": message_count,
                "sha256": sha256(messages_path),
            },
            {
                "artifact_id": "ART-00002",
                "type": "chats",
                "path": chats_path.name,
                "row_count": chat_count,
                "sha256": sha256(chats_path),
            },
            {
                "artifact_id": "ART-00003",
                "type": "device_metadata",
                "path": metadata_path.name,
                "row_count": metadata_count,
                "sha256": sha256(metadata_path),
            },
        ],
        "note": "Read-only examination of LIBERA ChatSim working-copy SQLite. No evaluator ground-truth fields exist in the acquired database."
    }
    manifest_path = out / "artifact_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "source_sha256": manifest["source_database_sha256"],
        "messages": message_count,
        "chats": chat_count,
        "foreign_key_errors": len(fk_errors),
        "artifact_manifest": str(manifest_path),
    }, indent=2))


if __name__ == "__main__":
    main()
