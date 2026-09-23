#!/usr/bin/env python3
"""Validate the Exhibit 1A source-reconstruction table.

This validator is intentionally conservative. It checks structure and provenance
rules only; it does not infer or fill missing messages.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

EXPECTED_LINES = 543
ALLOWED_STATUSES = {
    "COURT_VERBATIM",
    "COURT_PARAPHRASED",
    "INFERRED_METADATA",
    "MISSING_FROM_PUBLIC_RECORD",
}

REQUIRED_COLUMNS = [
    "original_line",
    "timestamp_original",
    "sender_original",
    "recipient_original",
    "message_original",
    "conversation_cluster",
    "source_id",
    "source_document",
    "source_page",
    "source_reference",
    "reconstruction_status",
    "confidence",
    "notes",
]


def validate(path: Path) -> list[str]:
    errors: list[str] = []

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != REQUIRED_COLUMNS:
            errors.append(
                "Schema mismatch. Expected columns:\n"
                + ",".join(REQUIRED_COLUMNS)
                + "\nFound:\n"
                + ",".join(reader.fieldnames or [])
            )
            return errors
        rows = list(reader)

    if len(rows) != EXPECTED_LINES:
        errors.append(f"Expected {EXPECTED_LINES} rows, found {len(rows)}.")

    seen: list[int] = []
    for i, row in enumerate(rows, start=1):
        try:
            line_no = int(row["original_line"])
        except (TypeError, ValueError):
            errors.append(f"Row {i}: invalid original_line={row['original_line']!r}.")
            continue

        seen.append(line_no)
        status = row["reconstruction_status"].strip()

        if status not in ALLOWED_STATUSES:
            errors.append(f"Line {line_no}: invalid reconstruction_status={status!r}.")

        if status == "MISSING_FROM_PUBLIC_RECORD":
            forbidden = [
                "timestamp_original",
                "sender_original",
                "recipient_original",
                "message_original",
                "conversation_cluster",
                "source_id",
                "source_document",
                "source_page",
                "source_reference",
            ]
            populated = [c for c in forbidden if row[c].strip()]
            if populated:
                errors.append(
                    f"Line {line_no}: missing-public-record row contains "
                    f"source-derived fields: {', '.join(populated)}."
                )

        if status in {"COURT_VERBATIM", "COURT_PARAPHRASED"}:
            for col in ("source_id", "source_document", "source_reference"):
                if not row[col].strip():
                    errors.append(f"Line {line_no}: {status} requires {col}.")
            if not row["message_original"].strip():
                errors.append(f"Line {line_no}: {status} requires message_original.")

        if status == "INFERRED_METADATA":
            if not row["source_id"].strip() or not row["source_reference"].strip():
                errors.append(
                    f"Line {line_no}: INFERRED_METADATA requires source_id "
                    "and source_reference."
                )

    expected = list(range(1, EXPECTED_LINES + 1))
    if sorted(seen) != expected:
        counts = Counter(seen)
        dupes = sorted(k for k, v in counts.items() if v > 1)
        missing = sorted(set(expected) - set(seen))
        if dupes:
            errors.append(f"Duplicate original_line values: {dupes}")
        if missing:
            errors.append(f"Missing original_line values: {missing}")

    return errors


def main() -> int:
    default = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "reconstruction"
        / "galloway_exhibit1a_reconstructed.csv"
    )
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default

    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    errors = validate(path)
    if errors:
        print("RECONSTRUCTION VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("RECONSTRUCTION VALIDATION: PASS")
    print(f"- rows: {EXPECTED_LINES}")
    print(f"- original_line coverage: 1..{EXPECTED_LINES}")
    print(f"- allowed statuses: {', '.join(sorted(ALLOWED_STATUSES))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
