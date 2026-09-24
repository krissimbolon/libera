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

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("Ground truth is empty.")
    required = {"message_id", "is_key_evidence"}
    if not required.issubset(rows[0]):
        raise SystemExit("Ground truth requires message_id and is_key_evidence columns.")

    seen = set()
    duplicates = []
    positive = negative = unlabeled = 0
    for row in rows:
        msg = row["message_id"].strip()
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
        "privacy": "Keep this CSV and lock manifest outside the public repository.",
    }
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
