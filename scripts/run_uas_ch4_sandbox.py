"""Controlled, non-destructive Chapter IV security experiment.

The original acquisition files are read only. All SQLite mutations occur in a
temporary copy, and only text/JSON evidence is retained in the report folder.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ACQ = ROOT / "demo_evidence/ACQ-SIM-001_20260925_010848"
OUT = ROOT / "docs/06_report/bab4_evidence"
EXTRACTOR = ROOT / "tools/extract_acquired_chatsim.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script: Path, db: Path, output: Path) -> dict:
    p = subprocess.run([sys.executable, str(script), str(db), "--out", str(output)],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return {"exit_code": p.returncode, "stdout": p.stdout[:1200], "stderr": p.stderr[:1200]}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    legacy = OUT / "legacy_extractor_before_fix.py"
    if not legacy.exists():
        p = subprocess.run(["git", "show", "HEAD:tools/extract_acquired_chatsim.py"], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8", check=True)
        if "ACQ-SIM-UNKNOWN" not in p.stdout:
            raise SystemExit("HEAD is not the expected pre-remediation extractor; legacy snapshot required")
        legacy.write_text(p.stdout, encoding="utf-8")

    source = ACQ / "working/libera_messages.db"
    manifest_source = ACQ / "acquisition_manifest.json"
    acquisition = json.loads(manifest_source.read_text(encoding="utf-8-sig"))
    assert sha(source) == acquisition["working_sha256"]
    with tempfile.TemporaryDirectory(prefix="libera_uas_ch4_") as temp:
        root = Path(temp) / "case"
        db_dir = root / "working"
        db_dir.mkdir(parents=True)
        db = db_dir / "libera_messages.db"
        shutil.copy2(source, db)
        manifest = root / "acquisition_manifest.json"
        shutil.copy2(manifest_source, manifest)
        clean = {"legacy": run(legacy, db, Path(temp)/"clean_old"),
                 "remediated": run(EXTRACTOR, db, Path(temp)/"clean_new")}
        old_hash = sha(db)
        conn = sqlite3.connect(db)
        row = conn.execute("SELECT message_id, message_text FROM messages ORDER BY message_id LIMIT 1").fetchone()
        if not row:
            raise SystemExit("No messages in test copy")
        marker = "[UAS_CONTROLLED_TAMPER_SAMPLE]"
        conn.execute("UPDATE messages SET message_text=? WHERE message_id=?", (row[1] + " " + marker, row[0]))
        conn.commit()
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        after_text = conn.execute("SELECT message_text FROM messages WHERE message_id=?", (row[0],)).fetchone()[0]
        count = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        conn.close()
        changed_hash = sha(db)
        tamper = {"message_id": row[0], "marker": marker, "before_text_sha256": hashlib.sha256(row[1].encode()).hexdigest(),
                  "after_text_sha256": hashlib.sha256(after_text.encode()).hexdigest(),
                  "before_db_sha256": old_hash, "after_db_sha256": changed_hash,
                  "sqlite_integrity_check": integrity, "message_count_after": count,
                  "legacy": run(legacy, db, Path(temp)/"tamper_old"),
                  "remediated": run(EXTRACTOR, db, Path(temp)/"tamper_new")}
        shutil.copy2(source, db)
        manifest.unlink()
        missing = {"legacy": run(legacy, db, Path(temp)/"missing_old"),
                   "remediated": run(EXTRACTOR, db, Path(temp)/"missing_new")}

    experiment = ROOT / "runtime/working/P8_final_v6_20260925/experiment_output.json"
    p9 = json.loads((ROOT / "runtime/working/P9_reconstructed_20260925/evaluation.json").read_text(encoding="utf-8"))
    citation = p9["integrity"]["conditions"]["C_llm_rag_structured"]
    from src.evaluation.citation_validation import validate
    import csv
    with (ACQ / "artifacts/artifacts.csv").open(encoding="utf-8-sig", newline="") as f:
        ids = {r["evidence_id"] for r in csv.DictReader(f)}
    validation = validate(experiment, ids)
    cval = validation["conditions"]["C_llm_rag_structured"]
    result = {
        "experiment": "UAS_CH4_CONTROLLED_WORKING_COPY_TEST",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "temporary copy of ACQ-SIM-001 working SQLite; no original file modified",
        "legacy_extractor_sha256": sha(legacy), "remediated_extractor_sha256": sha(EXTRACTOR),
        "test_harness_sha256": sha(Path(__file__)),
        "source_working_sha256": sha(source), "source_master_sha256": sha(ACQ / "master/libera_messages.db"),
        "clean": clean, "tamper": tamper, "missing_manifest": missing,
        "citation": {"p8_experiment_sha256": sha(experiment),
                     "reported_invalid_references": citation["invalid_citation_count"],
                     "attempted_occurrences": cval["attempted_reference_occurrences"],
                     "accepted_occurrences": cval["accepted_reference_occurrences"],
                     "quarantined_occurrences": cval["quarantined_reference_occurrences"],
                     "policy": validation["policy_version"]},
    }
    assert clean["legacy"]["exit_code"] == clean["remediated"]["exit_code"] == 0
    assert integrity == "ok" and old_hash != changed_hash
    assert tamper["legacy"]["exit_code"] == 0 and tamper["remediated"]["exit_code"] != 0
    assert missing["legacy"]["exit_code"] == 0 and missing["remediated"]["exit_code"] != 0
    assert cval["quarantined_reference_occurrences"] == 12
    (OUT / "experiment.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"clean": clean["remediated"]["exit_code"],
                      "tamper_before": tamper["legacy"]["exit_code"],
                      "tamper_after": tamper["remediated"]["exit_code"],
                      "missing_before": missing["legacy"]["exit_code"],
                      "missing_after": missing["remediated"]["exit_code"],
                      "citation_quarantined": cval["quarantined_reference_occurrences"]}, indent=2))


if __name__ == "__main__":
    main()
