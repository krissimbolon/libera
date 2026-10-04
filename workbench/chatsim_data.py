"""ChatSim ADB -> immutable SQLite snapshot -> read-only dashboard queries.

Chat data is never loaded from CSV. Experiment JSON is a separate historical
record, linked only when the acquired database hash matches its source.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import threading
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "id.libera.chatsim"
SNAPSHOTS = ROOT / "runtime/chatsim_snapshots"
CAPTURE_LOCK = threading.Lock()
MESSAGE_COLUMNS = ("message_id", "chat_id", "segment_id", "timestamp", "sender_id",
                   "recipient_id", "sender_name", "recipient_name", "message_text",
                   "message_type", "reply_to_message_id")


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def find_adb():
    candidates = [os.environ.get("LIBERA_ADB"), shutil.which("adb")]
    for variable in ("ANDROID_HOME", "ANDROID_SDK_ROOT"):
        if os.environ.get(variable):
            candidates.append(str(Path(os.environ[variable]) / "platform-tools/adb.exe"))
    if os.environ.get("LOCALAPPDATA"):
        candidates.append(str(Path(os.environ["LOCALAPPDATA"]) / "Android/Sdk/platform-tools/adb.exe"))
    return next((str(Path(p)) for p in candidates if p and Path(p).is_file()), None)


def adb_command(adb, arguments, serial=None, binary=False, timeout=30):
    cmd = [adb] + (["-s", serial] if serial else []) + list(arguments)
    result = subprocess.run(cmd, capture_output=True, timeout=timeout,
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if result.returncode:
        detail = (result.stderr or result.stdout).decode("utf-8", errors="replace")
        raise RuntimeError(f"ADB gagal: {detail.strip()}")
    return result.stdout if binary else result.stdout.decode("utf-8", errors="replace").strip()


def devices(adb):
    if not adb:
        return []
    lines = adb_command(adb, ["devices"]).splitlines()[1:]
    return [{"serial": parts[0], "state": parts[1]} for line in lines
            if len(parts := line.split()) >= 2]


def inspect_database(path):
    path = Path(path).resolve()
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.execute("PRAGMA query_only=ON")
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("SQLite integrity_check gagal")
        if conn.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Relasi SQLite tidak valid")
        columns = {row[1] for row in conn.execute("PRAGMA table_info(messages)")}
        if not set(MESSAGE_COLUMNS).issubset(columns):
            raise ValueError("Database bukan schema ChatSim yang didukung")
        message_count = conn.execute("SELECT count(*) FROM messages").fetchone()[0]
        chat_count = conn.execute("SELECT count(*) FROM chats").fetchone()[0]
        return {"message_count": message_count, "chat_count": chat_count, "sqlite_integrity": "ok"}


def capture_snapshot(adb, serial, root=SNAPSHOTS):
    """Capture fixed app DB, verifying device hash and local copies. No shell strings."""
    with CAPTURE_LOCK:
        ready = {d["serial"] for d in devices(adb) if d["state"] == "device"}
        if serial not in ready:
            raise RuntimeError("Perangkat tidak siap/unauthorized. Periksa emulator dan USB debugging.")
        adb_command(adb, ["shell", "am", "force-stop", PACKAGE], serial)
        # The supported ChatSim build disables WAL. Refuse nonempty WAL rather
        # than silently producing a snapshot missing committed transactions.
        listing = adb_command(adb, ["shell", "run-as", PACKAGE, "ls", "databases"], serial)
        if "libera_messages.db-wal" in listing.split():
            wal = adb_command(adb, ["exec-out", "run-as", PACKAGE, "cat",
                                    "databases/libera_messages.db-wal"], serial, binary=True)
            if wal:
                raise RuntimeError("WAL aktif; gunakan build ChatSim tanpa WAL sebelum akuisisi.")
        remote_hash = adb_command(adb, ["exec-out", "run-as", PACKAGE, "sha256sum",
                                       "databases/libera_messages.db"], serial).split()[0]
        data = adb_command(adb, ["exec-out", "run-as", PACKAGE, "cat",
                                "databases/libera_messages.db"], serial, binary=True, timeout=90)
        if not data.startswith(b"SQLite format 3\x00") or hashlib.sha256(data).hexdigest() != remote_hash:
            raise ValueError("Snapshot SQLite tidak valid atau hash perangkat berbeda")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
        folder = Path(root) / ("ACQ-SIM-LIVE_" + stamp)
        (folder / "master").mkdir(parents=True, exist_ok=False)
        (folder / "working").mkdir()
        master = folder / "master/libera_messages.db"
        working = folder / "working/libera_messages.db"
        master.write_bytes(data)
        working.write_bytes(data)
        counts = inspect_database(working)
        manifest = {"acquisition_id": folder.name, "device_id": "DEV-SIM-001",
                    "package": PACKAGE, "adb_serial": serial,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "method": "ADB exec-out run-as, app force-stopped, no nonempty WAL",
                    "source": "CHATSIM_DEVICE_SQLITE", "research_simulation": True,
                    "remote_sha256": remote_hash, "master_sha256": sha256(master),
                    "working_sha256": sha256(working), **counts}
        (folder / "acquisition_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return folder


def available_snapshots():
    folders = []
    for root in (SNAPSHOTS, ROOT / "demo_evidence"):
        if root.exists():
            folders.extend(p for p in root.iterdir() if p.is_dir()
                           and (p / "working/libera_messages.db").is_file()
                           and (p / "acquisition_manifest.json").is_file())
    return sorted(folders, key=lambda p: (p / "acquisition_manifest.json").stat().st_mtime, reverse=True)


def load_snapshot(folder):
    folder = Path(folder)
    manifest = read_json(folder / "acquisition_manifest.json")
    working = folder / "working/libera_messages.db"
    master = folder / "master/libera_messages.db"
    digest = sha256(working)
    if not (digest == manifest.get("working_sha256") == manifest.get("master_sha256") == sha256(master)):
        raise ValueError("Hash master/working/manifest berbeda. Snapshot ditolak.")
    inspection = inspect_database(working)
    with closing(sqlite3.connect(working.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
        conn.execute("PRAGMA query_only=ON")
        conn.row_factory = sqlite3.Row
        messages = [dict(row) for row in conn.execute(
            "SELECT " + ",".join(MESSAGE_COLUMNS) + " FROM messages ORDER BY timestamp,message_id")]
        chats = [dict(row) for row in conn.execute("SELECT * FROM chats ORDER BY peer_name,chat_id")]
    # Same deterministic ordering as P4; ordinal IDs are scoped to this snapshot.
    for number, row in enumerate(messages, 1):
        row["evidence_id"] = f"ART-{number:06d}"
    return {"messages": messages, "chats": chats, "manifest": manifest,
            "sha256": digest, "inspection": inspection, "database": str(working)}


def load_research(snapshot_hash, root=ROOT):
    root = Path(root)
    run_dir = root / "runtime/working/P8_final_v6_20260925"
    evaluation_dir = root / "runtime/working/P9_reconstructed_20260925"
    lock_path = run_dir / "p8_lock_manifest.json"
    if not lock_path.is_file():
        return None
    lock = read_json(lock_path)
    errors = []
    # Hash locked inputs, including the historical CSV, but NEVER parse its
    # message contents. The dashboard's only chat-data reader is SQLite.
    for name, item in lock["files"].items():
        if item:
            path = root / item["path"]
            if not path.is_file() or sha256(path) != item["sha256"]:
                errors.append(name)
    if errors:
        raise ValueError("Lock eksperimen gagal: " + ", ".join(errors))
    artifacts_path = root / lock["files"]["p4_artifacts"]["path"]
    source_manifest = read_json(artifacts_path.parent.parent / "acquisition_manifest.json")
    source_hash = source_manifest["working_sha256"]
    evaluation = None
    report = ""
    if (evaluation_dir / "completion_manifest.json").exists():
        completion = read_json(evaluation_dir / "completion_manifest.json")
        # Verify only the displayed results against their completion hashes.
        # Private label CSVs are neither opened nor exposed in the workbench.
        for name in ("evaluation.json", "run_report.md"):
            path = evaluation_dir / name
            relative = str(path.relative_to(root))
            entry = next((v for k, v in completion["files"].items()
                          if Path(k) == Path(relative)), None)
            if entry is None or sha256(path) != entry["sha256"]:
                raise ValueError(f"Hash hasil {name} tidak cocok dengan completion manifest")
        evaluation = read_json(evaluation_dir / "evaluation.json")
        report = (evaluation_dir / "run_report.md").read_text(encoding="utf-8")
    return {"matches_snapshot": snapshot_hash == source_hash, "source_sha256": source_hash,
            "lock": lock, "experiment": read_json(root / lock["files"]["p8_experiment_output"]["path"]),
            "evaluation": evaluation, "report": report, "run_dir": str(run_dir)}
