#!/usr/bin/env python3
"""Cryptographically lock P8 outputs before evaluator ground truth is opened."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def item(path: Path, required: bool = True):
    if not path.exists():
        if required:
            raise SystemExit(f"Required lock input not found: {path}")
        return None
    return {"path": str(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", default="runtime/working/P4/artifacts.csv")
    ap.add_argument("--baseline", default="runtime/working/P5/baseline_findings.json")
    ap.add_argument("--config", default="configs/p6_p7_config.json")
    ap.add_argument("--tasks", default="configs/investigation_tasks.json")
    ap.add_argument("--experiment", default="runtime/working/P8/experiment_output.json")
    ap.add_argument("--run-log", default="runtime/working/P8/run_log.jsonl")
    ap.add_argument("--output", default="runtime/working/P8/p8_lock_manifest.json")
    ap.add_argument("--extra-file", action="append", default=[],
                    help="Additional run-specific code, index or validation file to lock")
    args = ap.parse_args()
    if Path(args.output).exists():
        raise SystemExit("Refuse to overwrite an existing P8 lock; use a new run directory.")

    files = {
        "p4_artifacts": item(Path(args.artifacts)),
        "p5_baseline": item(Path(args.baseline)),
        "p6_p7_config": item(Path(args.config)),
        "investigation_tasks": item(Path(args.tasks)),
        "p8_experiment_output": item(Path(args.experiment)),
        "p8_run_log": item(Path(args.run_log), required=False),
    }
    for number, path in enumerate(args.extra_file, 1):
        files[f"extra_{number:02d}"] = item(Path(path))
    manifest = {
        "status": "P8_OUTPUTS_LOCKED_BEFORE_GROUND_TRUTH",
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "rule": (
            "Do not overwrite these outputs after evaluator ground truth is opened. "
            "A rerun must receive a new RUN/lock manifest and be reported separately."
        ),
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
