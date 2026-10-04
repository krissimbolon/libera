"""Regression tests for the ChatSim extractor fix integrated from Bab4 (findings F-01/F-02).

Synthetic temporary SQLite only; no acquired evidence is used.
"""
import hashlib
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR = ROOT / "tools/extract_acquired_chatsim.py"


def _acquisition(tmp_path: Path, with_manifest: bool = True) -> Path:
    acq = tmp_path / "ACQ-SIM-TEST_20260101_000000"
    db = acq / "working" / "libera_messages.db"
    db.parent.mkdir(parents=True)
    with sqlite3.connect(db) as conn:
        conn.executescript("""
            CREATE TABLE messages (message_id TEXT PRIMARY KEY, chat_id TEXT, segment_id TEXT,
                timestamp TEXT, sender_id TEXT, recipient_id TEXT, sender_name TEXT,
                recipient_name TEXT, message_text TEXT, message_type TEXT, reply_to_message_id TEXT);
            CREATE TABLE chats (chat_id TEXT PRIMARY KEY, peer_id TEXT, peer_name TEXT,
                last_timestamp TEXT, last_text TEXT, message_count INTEGER);
            CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT);
            INSERT INTO messages VALUES ('M1','C1','S1','2026-07-01T09:00:00+07:00','A','B','A','B','synthetic','text',NULL);
            INSERT INTO chats VALUES ('C1','B','B','2026-07-01T09:00:00+07:00','synthetic',1);
            INSERT INTO metadata VALUES ('device_id','DEV-SIM-TEST');
        """)
    if with_manifest:
        digest = hashlib.sha256(db.read_bytes()).hexdigest()
        (acq / "acquisition_manifest.json").write_text(json.dumps({
            "acquisition_id": "ACQ-SIM-TEST", "device_id": "DEV-SIM-TEST",
            "master_sha256": digest, "working_sha256": digest}))
    return db


def _run(db: Path, out: Path):
    return subprocess.run([sys.executable, str(EXTRACTOR), str(db), "--out", str(out)],
                          capture_output=True, text=True)


def test_intact_working_copy_is_extracted(tmp_path):
    db = _acquisition(tmp_path)
    result = _run(db, tmp_path / "artifacts")
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "artifacts" / "artifacts.csv").exists()


def test_structurally_valid_tampering_is_refused(tmp_path):
    db = _acquisition(tmp_path)
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE messages SET message_text='tampered' WHERE message_id='M1'")
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    result = _run(db, tmp_path / "artifacts")
    assert result.returncode != 0
    assert "SHA-256 mismatch" in (result.stderr + result.stdout)
    assert not (tmp_path / "artifacts" / "artifacts.csv").exists()


def test_missing_acquisition_manifest_is_refused(tmp_path):
    db = _acquisition(tmp_path, with_manifest=False)
    result = _run(db, tmp_path / "artifacts")
    assert result.returncode != 0
    assert "manifest not found" in (result.stderr + result.stdout)
    assert not (tmp_path / "artifacts" / "artifacts.csv").exists()
