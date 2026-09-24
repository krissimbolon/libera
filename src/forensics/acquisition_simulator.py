"""Create a controlled *simulation* acquisition package from the frozen corpus.

This is NOT a substitute for physical-device acquisition. It exists to:
1) exercise the complete P3->P10 software path before the presentation;
2) validate hashing, master/working-copy and extraction contracts;
3) provide CI with a reproducible input that contains no private evidence.

Real P3 remains: replay frozen corpus to the research WhatsApp account on
DEV-001, acquire with the selected mobile-forensics method, hash the master,
then run P4 from a working copy.

The canonical P2 file is read-only and SHA-256 pinned.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

CANONICAL_CORPUS = Path("data/adaptasi_indonesia/corpus_whatsapp_10000.csv")
CANONICAL_SHA256 = "a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6"
CANONICAL_ROWS = 10_000
EXPECTED_COLUMNS = [
    "message_id", "conversation_id", "timestamp", "sender_id", "recipient_id",
    "message_text", "message_type", "reply_to_message_id", "attachment_id",
    "source_provenance", "source_original_line", "transformation_id",
]


class AcquisitionSimulationError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_and_validate_corpus(path: Path) -> list[dict[str, str]]:
    path = Path(path)
    if not path.exists():
        raise AcquisitionSimulationError(f"Corpus tidak ditemukan: {path}")

    actual_hash = sha256_file(path)
    if actual_hash.lower() != CANONICAL_SHA256:
        raise AcquisitionSimulationError(
            "REFUSE: hash corpus berbeda dari frozen P2. "
            f"expected={CANONICAL_SHA256} actual={actual_hash}"
        )

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_COLUMNS:
            raise AcquisitionSimulationError(
                f"Schema corpus berubah. expected={EXPECTED_COLUMNS} actual={reader.fieldnames}"
            )
        rows = list(reader)

    if len(rows) != CANONICAL_ROWS:
        raise AcquisitionSimulationError(
            f"Row count bukan {CANONICAL_ROWS}: {len(rows)}"
        )
    ids = [r["message_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise AcquisitionSimulationError("Duplicate message_id terdeteksi.")
    return rows


def create_sqlite(rows: Iterable[dict[str, str]], output_db: Path) -> None:
    output_db = Path(output_db)
    output_db.parent.mkdir(parents=True, exist_ok=True)
    if output_db.exists():
        output_db.unlink()

    conn = sqlite3.connect(output_db)
    try:
        conn.execute("PRAGMA journal_mode=DELETE")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute("""
            CREATE TABLE messages (
                message_id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                sender_id TEXT NOT NULL,
                recipient_id TEXT NOT NULL,
                message_text TEXT NOT NULL,
                message_type TEXT,
                reply_to_message_id TEXT,
                attachment_id TEXT,
                source_provenance TEXT,
                source_original_line TEXT,
                transformation_id TEXT
            )
        """)
        conn.executemany(
            """INSERT INTO messages VALUES (
                :message_id,:conversation_id,:timestamp,:sender_id,:recipient_id,
                :message_text,:message_type,:reply_to_message_id,:attachment_id,
                :source_provenance,:source_original_line,:transformation_id
            )""",
            rows,
        )
        conn.execute("""
            CREATE TABLE acquisition_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        metadata = {
            "device_id": "DEV-DRY-001",
            "acquisition_id": "ACQ-DRY-001",
            "acquisition_type": "CONTROLLED_SOFTWARE_SIMULATION",
            "source_corpus_sha256": CANONICAL_SHA256,
            "source_row_count": str(CANONICAL_ROWS),
            "notice": "NOT A PHYSICAL-DEVICE FORENSIC ACQUISITION",
        }
        conn.executemany(
            "INSERT INTO acquisition_metadata(key,value) VALUES (?,?)",
            metadata.items(),
        )
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        if count != CANONICAL_ROWS:
            raise AcquisitionSimulationError(
                f"SQLite verification failed: {count} rows"
            )
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise AcquisitionSimulationError(
                f"SQLite integrity_check failed: {integrity}"
            )
    finally:
        conn.close()


def run(input_csv: Path, output_db: Path, manifest_path: Path) -> dict:
    rows = read_and_validate_corpus(input_csv)
    create_sqlite(rows, output_db)
    db_hash = sha256_file(output_db)
    manifest = {
        "status": "SIMULATED_ACQUISITION_FOR_PIPELINE_DRY_RUN",
        "is_real_device_acquisition": False,
        "device_id": "DEV-DRY-001",
        "acquisition_id": "ACQ-DRY-001",
        "source_corpus": str(input_csv),
        "source_corpus_sha256": CANONICAL_SHA256,
        "source_row_count": CANONICAL_ROWS,
        "acquisition_file": str(output_db),
        "acquisition_sha256": db_hash,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "warning": (
            "Do not report this as Oxygen/physical acquisition. "
            "Replace with ACQ-001 after the real local-device workflow."
        ),
    }
    manifest_path = Path(manifest_path)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    p = argparse.ArgumentParser(description="Build controlled P3 dry-run acquisition.")
    p.add_argument("--input", default=str(CANONICAL_CORPUS))
    p.add_argument(
        "--output",
        default="runtime/private/ACQ-DRY-001/libera_simulated_acquisition.sqlite",
    )
    p.add_argument(
        "--manifest",
        default="runtime/private/ACQ-DRY-001/acquisition_manifest.json",
    )
    args = p.parse_args()

    try:
        manifest = run(Path(args.input), Path(args.output), Path(args.manifest))
    except AcquisitionSimulationError as exc:
        print(f"[P3 dry-run] ERROR: {exc}")
        raise SystemExit(1)

    print("[P3 dry-run] PASS")
    print(f"  acquisition_id={manifest['acquisition_id']}")
    print(f"  rows={manifest['source_row_count']}")
    print(f"  sqlite_sha256={manifest['acquisition_sha256']}")
    print("  IMPORTANT: simulated acquisition; NOT physical-device evidence.")


if __name__ == "__main__":
    main()
