"""Forensic provenance audit for the locked 500-anchor reference set.

Read-only. It never rewrites anchor files. The goal is to distinguish:
1) semantic/row identity,
2) current byte hashes, and
3) historical manifest hashes that may reflect another serialization.
"""

from __future__ import annotations

import csv
import hashlib
import json
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adaptasi_indonesia"
ANCHOR = DATA / "anchor_indonesia_500.csv"
PART_DIR = DATA / "jangkar_500"
MANIFEST = PART_DIR / "manifest.json"
OUT = DATA / "qa_anchor_provenance.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows_from_bytes(data: bytes) -> list[dict[str, str]]:
    text = data.decode("utf-8-sig")
    return list(csv.DictReader(StringIO(text, newline="")))


def variants(data: bytes) -> dict[str, bytes]:
    # Work in decoded UTF-8 because these files are text CSV. Include BOM and
    # newline variants explicitly so a historical hash can be explained rather
    # than silently replaced.
    text = data.decode("utf-8-sig")
    lf = text.replace("\r\n", "\n").replace("\r", "\n")
    no_final = lf.rstrip("\n")
    candidates = {
        "current_bytes": data,
        "lf_final_newline": (no_final + "\n").encode("utf-8"),
        "lf_no_final_newline": no_final.encode("utf-8"),
        "crlf_final_newline": (no_final.replace("\n", "\r\n") + "\r\n").encode("utf-8"),
        "crlf_no_final_newline": no_final.replace("\n", "\r\n").encode("utf-8"),
    }
    bom = b"\xef\xbb\xbf"
    for name, blob in list(candidates.items()):
        if name != "current_bytes":
            candidates[name + "_bom"] = bom + blob
    return candidates


def audit_file(path: Path, expected: str | None) -> dict[str, object]:
    data = path.read_bytes()
    hashes = {name: sha(blob) for name, blob in variants(data).items()}
    matches = [name for name, digest in hashes.items() if expected and digest == expected]
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "size_bytes": len(data),
        "current_sha256": sha(data),
        "historical_expected_sha256": expected,
        "historical_hash_reproduced": bool(matches),
        "matching_serializations": matches,
        "tested_serialization_hashes": hashes,
        "row_count": len(rows_from_bytes(data)),
    }


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    combined_bytes = ANCHOR.read_bytes()
    combined_rows = rows_from_bytes(combined_bytes)

    combined = audit_file(ANCHOR, manifest.get("sha256_file_gabungan"))

    part_reports: list[dict[str, object]] = []
    concatenated_rows: list[dict[str, str]] = []
    for item in manifest["bagian"]:
        path = PART_DIR / item["file"]
        report = audit_file(path, item.get("sha256"))
        part_reports.append(report)
        concatenated_rows.extend(rows_from_bytes(path.read_bytes()))

    same_row_count = len(combined_rows) == len(concatenated_rows) == 500
    same_ordered_rows = same_row_count and all(
        a == b for a, b in zip(combined_rows, concatenated_rows)
    )

    combined_ids = [row.get("message_id") for row in combined_rows]
    parts_ids = [row.get("message_id") for row in concatenated_rows]

    report = {
        "status": "PASS_ROW_IDENTITY_WITH_HISTORICAL_HASH_DISCREPANCY"
        if same_ordered_rows
        else "FAIL_ROW_IDENTITY",
        "combined": combined,
        "parts": part_reports,
        "combined_vs_parts": {
            "combined_rows": len(combined_rows),
            "parts_rows": len(concatenated_rows),
            "same_row_count": same_row_count,
            "same_ordered_rows": same_ordered_rows,
            "same_message_id_order": combined_ids == parts_ids,
            "unique_combined_message_ids": len(set(combined_ids)),
            "unique_parts_message_ids": len(set(parts_ids)),
        },
        "forensic_interpretation": (
            "Row-level identity can be accepted independently from the historical "
            "manifest byte hash. Do not modify locked anchors to force an old digest. "
            "If a historical digest is not reproduced by tested serializations, preserve "
            "it as a provenance discrepancy and seek the original integration artifact."
        ),
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "combined_current_sha256": combined["current_sha256"],
        "combined_historical_reproduced": combined["historical_hash_reproduced"],
        "part_historical_reproduced": [
            p["historical_hash_reproduced"] for p in part_reports
        ],
        "same_ordered_rows": same_ordered_rows,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
