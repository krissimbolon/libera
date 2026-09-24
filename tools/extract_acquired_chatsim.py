#!/usr/bin/env python3
"""Read-only extraction of a LIBERA ChatSim working-copy SQLite.

Produces both container-level forensic artifacts and a normalized message-level
ART CSV compatible with the P5-P10 pipeline.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

NORMALIZED_FIELDS = [
    "evidence_id", "artifact_id", "acquisition_id", "device_id",
    "message_id", "conversation_id", "segment_id", "sender", "receiver",
    "timestamp_normalized", "message_text", "message_type",
    "reply_to_message_id", "attachment_id",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def export_query(conn: sqlite3.Connection, query: str, path: Path) -> int:
    cur = conn.execute(query)
    headers = [d[0] for d in cur.description]
    rows = cur.fetchall()
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    return len(rows)


def load_acquisition_metadata(db_path: Path) -> dict:
    manifest = db_path.parent.parent / "acquisition_manifest.json"
    if not manifest.exists():
        return {
            "acquisition_id": "ACQ-SIM-UNKNOWN",
            "device_id": "DEV-SIM-UNKNOWN",
        }
    return json.loads(manifest.read_text(encoding="utf-8-sig"))


def write_normalized(conn: sqlite3.Connection, path: Path, acq: dict) -> int:
    cur = conn.execute("""
        SELECT message_id, chat_id, segment_id, timestamp, sender_id,
               recipient_id, message_text, message_type, reply_to_message_id
        FROM messages
        ORDER BY timestamp, message_id
    """)
    rows = cur.fetchall()
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=NORMALIZED_FIELDS)
        w.writeheader()
        for i, r in enumerate(rows, start=1):
            art = f"ART-{i:06d}"
            w.writerow({
                "evidence_id": art,
                "artifact_id": art,
                "acquisition_id": acq.get("acquisition_id", "ACQ-SIM-UNKNOWN"),
                "device_id": acq.get("device_id", "DEV-SIM-UNKNOWN"),
                "message_id": r[0],
                "conversation_id": r[1],
                "segment_id": r[2],
                "sender": r[4],
                "receiver": r[5],
                "timestamp_normalized": r[3],
                "message_text": r[6],
                "message_type": r[7] or "",
                "reply_to_message_id": r[8] or "",
                "attachment_id": "",
            })
    return len(rows)


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

    acq = load_acquisition_metadata(db_path)
    uri = db_path.as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise SystemExit(f"SQLite integrity_check failed: {integrity}")

        messages_path = out / "ARTFILE-00001_messages.csv"
        chats_path = out / "ARTFILE-00002_chats.csv"
        metadata_path = out / "ARTFILE-00003_device_metadata.csv"
        normalized_path = out / "artifacts.csv"

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
        metadata_count = export_query(
            conn, "SELECT key, value FROM metadata ORDER BY key", metadata_path
        )
        normalized_count = write_normalized(conn, normalized_path, acq)
        fk_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
    finally:
        conn.close()

    if normalized_count != message_count:
        raise SystemExit("Normalized artifact count differs from source message count.")

    manifest = {
        "status": "P4_CHATSIM_EXTRACTION_PASS",
        "extraction_time_utc": datetime.now(timezone.utc).isoformat(),
        "source_database": str(db_path),
        "source_database_sha256": sha256(db_path),
        "acquisition_id": acq.get("acquisition_id"),
        "device_id": acq.get("device_id"),
        "evidence_carrier": "LIBERA ChatSim Android emulator",
        "whatsapp_acquisition": False,
        "sqlite_integrity_check": "ok",
        "foreign_key_error_count": len(fk_errors),
        "message_count": message_count,
        "chat_count": chat_count,
        "normalized_artifact_count": normalized_count,
        "normalized_artifacts_csv": normalized_path.name,
        "normalized_artifacts_sha256": sha256(normalized_path),
        "container_artifacts": [
            {
                "artifact_id": "ARTFILE-00001",
                "type": "messages_export",
                "path": messages_path.name,
                "row_count": message_count,
                "sha256": sha256(messages_path),
            },
            {
                "artifact_id": "ARTFILE-00002",
                "type": "chats_export",
                "path": chats_path.name,
                "row_count": chat_count,
                "sha256": sha256(chats_path),
            },
            {
                "artifact_id": "ARTFILE-00003",
                "type": "device_metadata_export",
                "path": metadata_path.name,
                "row_count": metadata_count,
                "sha256": sha256(metadata_path),
            },
        ],
        "note": (
            "Read-only examination of the ChatSim working copy. "
            "The acquired app contains no evaluator ground-truth fields."
        ),
    }
    manifest_path = out / "artifact_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": manifest["status"],
        "source_sha256": manifest["source_database_sha256"],
        "messages": message_count,
        "chats": chat_count,
        "normalized_artifacts": str(normalized_path),
        "artifact_manifest": str(manifest_path),
    }, indent=2))


if __name__ == "__main__":
    main()
