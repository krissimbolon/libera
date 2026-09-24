#!/usr/bin/env python3
"""Validate and hash-lock a private LIBERA ground-truth annotation CSV."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


POSITIVE = {"1", "true", "yes", "y", "ya", "key", "relevant", "positive"}
NEGATIVE = {"0", "false", "no", "n", "tidak", "non-key", "irrelevant", "negative"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ground_truth")
    ap.add_argument("--output", default=None)
    ap.add_argument("--require-complete", action="store_true")
    args = ap.parse_args()

    path = Path(args.ground_truth)
    if not path.exists():
        raise SystemExit(f"Ground truth not found: {path}")
    out = Path(args.output) if args.output else path.with_suffix(path.suffix + ".lock.json")
    if out.resolve() == path.resolve():
        raise SystemExit("Ground-truth lock must not overwrite its source CSV.")
    if out.exists():
        existing = json.loads(out.read_text(encoding="utf-8"))
        if (existing.get("status") != "PRIVATE_GROUND_TRUTH_LOCKED" or
                existing.get("ground_truth_sha256") != sha256(path)):
            raise SystemExit("Existing GT lock mismatch; refusing to re-lock changed labels.")
        if args.require_complete and not existing.get("complete_binary_labels"):
            raise SystemExit("Existing GT lock contains incomplete labels.")
        print("[GT-LOCK] Existing lock VERIFY PASS (unchanged)")
        return

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("Ground truth is empty.")
    required = {"message_id", "is_key_evidence"}
    if not required.issubset(rows[0]):
        raise SystemExit("Ground truth requires message_id and is_key_evidence columns.")
    origins = {r.get("label_origin", "independent_evaluator_labels") for r in rows}
    targets = {r.get("reference_target", "message_level_key_evidence") for r in rows}
    if len(origins) != 1 or len(targets) != 1:
        raise SystemExit("Mixed reference origins/targets cannot share one ground-truth lock.")

    seen = set()
    duplicates = []
    positive = negative = unlabeled = 0
    for row in rows:
        msg = row["message_id"].strip()
        if not msg:
            raise SystemExit("Ground truth has an empty message_id.")
        if msg in seen:
            duplicates.append(msg)
        seen.add(msg)
        label = row["is_key_evidence"].strip().casefold()
        if label in POSITIVE:
            positive += 1
        elif label in NEGATIVE:
            negative += 1
        else:
            unlabeled += 1

    if duplicates:
        raise SystemExit(f"Duplicate message_id in ground truth: {duplicates[:10]}")
    if args.require_complete and unlabeled:
        raise SystemExit(f"Ground truth has {unlabeled} unlabeled rows.")

    out = Path(args.output) if args.output else path.with_suffix(path.suffix + ".lock.json")
    manifest = {
        "status": "PRIVATE_GROUND_TRUTH_LOCKED",
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "ground_truth_filename": path.name,
        "ground_truth_sha256": sha256(path),
        "row_count": len(rows),
        "positive_rows": positive,
        "negative_rows": negative,
        "unlabeled_rows": unlabeled,
        "complete_binary_labels": unlabeled == 0,
        "label_origin": next(iter(origins)),
        "reference_target": next(iter(targets)),
        "privacy": "Keep this CSV and lock manifest outside the public repository.",
    }
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
