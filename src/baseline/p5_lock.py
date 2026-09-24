"""Cryptographically lock P5 baseline + completed examiner QC before AI."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_DECISIONS = {"SUPPORTED", "NOT_SUPPORTED", "UNCERTAIN"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def file_item(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    return {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def validate_review(packet: Path) -> dict:
    with packet.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("Examiner packet is empty.")
    invalid = []
    for row in rows:
        decision = (row.get("examiner_decision") or "").strip().upper()
        if decision not in ALLOWED_DECISIONS:
            invalid.append(row.get("evidence_id", "UNKNOWN"))
        if decision in {"NOT_SUPPORTED", "UNCERTAIN"} and not (
            row.get("examiner_note") or ""
        ).strip():
            invalid.append(row.get("evidence_id", "UNKNOWN") + ":missing_note")
    if invalid:
        raise ValueError(
            "Examiner review incomplete/invalid: " + ", ".join(invalid[:20])
        )
    return {
        "reviewed_rows": len(rows),
        "supported": sum(
            (r.get("examiner_decision") or "").strip().upper() == "SUPPORTED"
            for r in rows
        ),
        "not_supported": sum(
            (r.get("examiner_decision") or "").strip().upper() == "NOT_SUPPORTED"
            for r in rows
        ),
        "uncertain": sum(
            (r.get("examiner_decision") or "").strip().upper() == "UNCERTAIN"
            for r in rows
        ),
    }


def lock(
    artifacts: Path,
    tasks: Path,
    p5_dir: Path,
    packet: Path,
    output: Path,
) -> dict:
    review = validate_review(packet)
    files = {
        "p4_artifacts": file_item(artifacts),
        "investigation_tasks": file_item(tasks),
        "p5_timeline": file_item(p5_dir / "timeline.csv"),
        "p5_entities": file_item(p5_dir / "entities.csv"),
        "p5_relationships": file_item(p5_dir / "relationships.csv"),
        "p5_baseline_findings": file_item(p5_dir / "baseline_findings.json"),
        "p5_baseline_manifest": file_item(p5_dir / "baseline_manifest.json"),
        "p5_examiner_packet": file_item(packet),
    }
    manifest = {
        "status": "P5_BASELINE_AND_EXAMINER_REVIEW_LOCKED_BEFORE_AI",
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "review_summary": review,
        "files": files,
        "rule": (
            "Do not overwrite P5 outputs or examiner review after this lock. "
            "Any rerun must create a new lock and be reported separately."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify(manifest_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "P5_BASELINE_AND_EXAMINER_REVIEW_LOCKED_BEFORE_AI":
        raise ValueError("P5 lock manifest status is invalid.")
    mismatches = []
    for label, item in manifest.get("files", {}).items():
        path = Path(item["path"])
        if not path.exists() or sha256_file(path) != item["sha256"]:
            mismatches.append(label)
    if mismatches:
        raise ValueError("P5 lock verification failed: " + ", ".join(mismatches))


def main() -> None:
    p = argparse.ArgumentParser(description="Lock or verify reviewed P5 outputs.")
    p.add_argument("--artifacts", default="runtime/working/P4/artifacts.csv")
    p.add_argument("--tasks", default="configs/investigation_tasks.json")
    p.add_argument("--p5-dir", default="runtime/working/P5")
    p.add_argument(
        "--packet",
        default="runtime/working/P5/p5_examiner_packet.csv",
    )
    p.add_argument(
        "--output",
        default="runtime/working/P5/p5_lock_manifest.json",
    )
    p.add_argument("--verify", action="store_true")
    p.add_argument(
        "--manifest",
        default="runtime/working/P5/p5_lock_manifest.json",
    )
    args = p.parse_args()

    try:
        if args.verify:
            verify(Path(args.manifest))
            print("[P5-LOCK] VERIFY PASS")
            return
        manifest = lock(
            Path(args.artifacts),
            Path(args.tasks),
            Path(args.p5_dir),
            Path(args.packet),
            Path(args.output),
        )
    except (ValueError, FileNotFoundError, KeyError) as exc:
        print(f"[P5-LOCK] ERROR: {exc}")
        raise SystemExit(1)

    print("[P5-LOCK] PASS")
    print(f"  reviewed={manifest['review_summary']['reviewed_rows']}")
    print(f"  manifest={args.output}")


if __name__ == "__main__":
    main()
