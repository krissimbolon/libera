import hashlib
import json
import sqlite3

import pytest

from workbench import chatsim_data as source


@pytest.fixture
def snapshot(tmp_path):
    master = tmp_path / "master/libera_messages.db"
    working = tmp_path / "working/libera_messages.db"
    master.parent.mkdir()
    working.parent.mkdir()
    conn = sqlite3.connect(master)
    conn.execute("CREATE TABLE chats(chat_id TEXT, peer_name TEXT)")
    conn.execute("INSERT INTO chats VALUES ('chat1','Peer')")
    conn.execute("CREATE TABLE messages(" + ",".join(c + " TEXT" for c in source.MESSAGE_COLUMNS) + ")")
    for identity, stamp in [("m2", "2026-09-25T12:00:00"), ("m1", "2026-09-25T11:00:00")]:
        conn.execute("INSERT INTO messages VALUES (?,?,?,?,?,?,?,?,?,?,?)", (identity, "chat1", "s1", stamp, "a", "b", "Alice", "Bob", "Hello", "text", None))
    conn.commit()
    conn.close()
    working.write_bytes(master.read_bytes())
    digest = source.sha256(master)
    (tmp_path / "acquisition_manifest.json").write_text(json.dumps({"master_sha256": digest, "working_sha256": digest}), encoding="utf-8")
    return tmp_path


def test_read_sqlite_without_csv_and_preserve_bytes(snapshot):
    before = source.sha256(snapshot / "working/libera_messages.db")
    data = source.load_snapshot(snapshot)
    assert [m["message_id"] for m in data["messages"]] == ["m1", "m2"]
    assert [m["evidence_id"] for m in data["messages"]] == ["ART-000001", "ART-000002"]
    assert data["inspection"]["message_count"] == 2
    assert source.sha256(snapshot / "working/libera_messages.db") == before
    assert not list(snapshot.rglob("*.csv"))


def test_tampered_snapshot_rejected(snapshot):
    with (snapshot / "working/libera_messages.db").open("ab") as stream:
        stream.write(b"tampered")
    with pytest.raises(ValueError, match="Hash"):
        source.load_snapshot(snapshot)


def test_adb_capture_creates_verified_sqlite(snapshot, tmp_path, monkeypatch):
    payload = (snapshot / "working/libera_messages.db").read_bytes()
    calls = []

    def adb(_adb, arguments, serial=None, binary=False, timeout=30):
        calls.append(arguments)
        if arguments == ["devices"]:
            return "List of devices attached\nemulator-test\tdevice"
        if "ls" in arguments:
            return "libera_messages.db"
        if "sha256sum" in arguments:
            return hashlib.sha256(payload).hexdigest() + "  databases/libera_messages.db"
        if "cat" in arguments:
            return payload
        return ""

    monkeypatch.setattr(source, "adb_command", adb)
    output = source.capture_snapshot("adb", "emulator-test", tmp_path / "captures")
    data = source.load_snapshot(output)
    assert data["manifest"]["source"] == "CHATSIM_DEVICE_SQLITE"
    assert data["inspection"]["message_count"] == 2
    assert ["shell", "am", "force-stop", source.PACKAGE] in calls


def test_unready_device_cannot_capture(tmp_path, monkeypatch):
    monkeypatch.setattr(source, "devices", lambda _: [{"serial": "emulator-test", "state": "unauthorized"}])
    with pytest.raises(RuntimeError, match="tidak siap"):
        source.capture_snapshot("adb", "emulator-test", tmp_path)


def test_nonempty_wal_cannot_capture(tmp_path, monkeypatch):
    monkeypatch.setattr(source, "devices", lambda _: [{"serial": "e", "state": "device"}])
    def adb(_adb, arguments, *args, **kwargs):
        if "ls" in arguments:
            return "libera_messages.db\nlibera_messages.db-wal"
        return b"pending" if "cat" in arguments else ""
    monkeypatch.setattr(source, "adb_command", adb)
    with pytest.raises(RuntimeError, match="WAL"):
        source.capture_snapshot("adb", "e", tmp_path)
