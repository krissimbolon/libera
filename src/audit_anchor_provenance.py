"""Read-only comparison of current anchor rows and historical manifest hashes.

Hash mismatch alone cannot establish that an anchor row changed. This auditor
reports byte checks and parsed row identity separately; it never edits sources.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adaptasi_indonesia"
PARTS = DATA / "jangkar_500"


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def variants(original: bytes) -> dict[str, bytes]:
    lf = original.replace(b"\r\n", b"\n")
    values = {
        "current": original,
        "lf": lf,
        "crlf": lf.replace(b"\n", b"\r\n"),
        "lf_no_final_newline": lf.rstrip(b"\n"),
        "crlf_no_final_newline": lf.rstrip(b"\n").replace(b"\n", b"\r\n"),
    }
    candidates = {name: variant for name, variant in values.items() if variant}
    for name, variant in list(candidates.items()):
        if not variant.startswith(b"\xef\xbb\xbf"):
            candidates[f"{name}_with_bom"] = b"\xef\xbb\xbf" + variant
    return candidates


def main() -> None:
    manifest = json.loads((PARTS / "manifest.json").read_text(encoding="utf-8"))
    anchor_path = DATA / "anchor_indonesia_500.csv"
    anchor_rows = rows(anchor_path)
    part_rows = []
    checks = []
    for item in manifest["bagian"]:
        path = PARTS / item["file"]
        content = path.read_bytes()
        parsed = rows(path)
        part_rows.extend(parsed)
        checks.append({
            "file": item["file"],
            "row_count": len(parsed),
            "current_sha256": sha(content),
            "manifest_sha256": item["sha256"],
            "matching_serialization_variants": [
                name for name, variant in variants(content).items()
                if sha(variant) == item["sha256"]
            ],
        })

    content = anchor_path.read_bytes()
    combined_matches = [
        name for name, variant in variants(content).items()
        if sha(variant) == manifest["sha256_file_gabungan"]
    ]
    report = {
        "current_anchor_sha256": sha(content),
        "historical_combined_sha256": manifest["sha256_file_gabungan"],
        "combined_matching_serialization_variants": combined_matches,
        "combined_rows": len(anchor_rows),
        "parts_rows": len(part_rows),
        "rows_equal_in_order": anchor_rows == part_rows,
        "part_checks": checks,
        "historical_byte_provenance_resolved": bool(combined_matches) and all(
            check["matching_serialization_variants"] for check in checks
        ),
        "note": "Row identity is verified separately from historical byte serialization.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
