import hashlib
import json
import sqlite3
from pathlib import Path

from libera_platform.case import archive, baseline, create_case, extract, import_sqlite, status, verify


def _make_sqlite(path: Path) -> str:
    conn = sqlite3.connect(path)
    conn.execute("""CREATE TABLE messages(
        message_id TEXT PRIMARY KEY,
        conversation_id TEXT,
        timestamp TEXT,
        sender_id TEXT,
        recipient_id TEXT,
        message_text TEXT,
        message_type TEXT,
        reply_to_message_id TEXT,
        attachment_id TEXT
    )""")
    conn.executemany(
        "INSERT INTO messages VALUES(?,?,?,?,?,?,?,?,?)",
        [
            ("m1","c1","2026-01-01T10:00:00","alice","bob","tolong transfer invoice ini","text","",""),
            ("m2","c1","2026-01-01T10:01:00","bob","alice","sudah, cek rekening","text","",""),
            ("m3","c2","2026-01-01T11:00:00","charlie","alice","ketemu di kantor jam 2","text","",""),
        ],
    )
    conn.commit(); conn.close()
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_operational_case_lifecycle_without_models(tmp_path):
    root = tmp_path / "cases"
    case = create_case("CASE-001", "fixture", str(root))
    assert case == root / "CASE-001"

    source = tmp_path / "source.sqlite"
    digest = _make_sqlite(source)
    imported = import_sqlite("CASE-001", source, digest, str(root), "DEV-TEST")
    assert imported["master_sha256"] == digest

    p4 = extract("CASE-001", str(root))
    assert p4["artifact_count"] == 3
    assert p4["acquisition_id"] == "ACQ-CASE-001"
    assert p4["device_id"] == "DEV-TEST"

    p5 = baseline("CASE-001", str(root), top_n=5)
    assert p5["message_count"] == 3
    assert p5["task_count"] == 10

    state = status("CASE-001", str(root))
    assert state["stages"]["evidence_imported"] is True
    assert state["stages"]["P4_extracted"] is True
    assert state["stages"]["P5_baseline"] is True
    assert state["verification"]["status"] == "PASS"

    out = archive("CASE-001", root=str(root))
    assert out.is_file()
    assert verify("CASE-001", str(root))["status"] == "PASS"


def test_case_manifest_separates_operational_platform_from_research(tmp_path):
    case = create_case("CASE-ABC", root=str(tmp_path / "cases"))
    manifest = json.loads((case / "case.json").read_text(encoding="utf-8"))
    assert manifest["policy"]["case_isolated"] is True
    assert manifest["policy"]["ai_output_is_investigative_aid_not_evidence"] is True
    assert "frozen_p2" not in manifest


def test_operational_verify_detects_derived_artifact_tampering(tmp_path):
    root = tmp_path / "cases"
    create_case("CASE-TAMPER", root=str(root))
    source = tmp_path / "source.sqlite"
    digest = _make_sqlite(source)
    import_sqlite("CASE-TAMPER", source, digest, str(root), "DEV-TEST")
    extract("CASE-TAMPER", str(root))
    artifacts = root / "CASE-TAMPER/runtime/working/P4/artifacts.csv"
    artifacts.write_text(artifacts.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    result = verify("CASE-TAMPER", str(root))
    assert result["status"] == "FAIL"
    assert "P4 artifact hash mismatch" in result["problems"]
