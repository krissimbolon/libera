"""
validate_output.py - Validasi format 'structured finding' (P6/P7/P8).

Format wajib mengikuti PDF Bab 6.1 poin 10:
    Question -> Relevant Evidence -> Observed Facts ->
    Possible Interpretation -> Contradicting Evidence ->
    Confidence/Uncertainty -> Finding

Modul ini TIDAK meminta/menyimpan chain-of-thought internal model,
sesuai larangan PDF di poin yang sama.

Juga melakukan pengecekan dasar agar output tidak mengandung field
Ground Truth (evidence_strength, expected_entity_ids, dst) - lihat
skema_ground_truth_privat.csv yang disebut di snapshot repository.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_FIELDS = [
    "question",
    "relevant_evidence",
    "observed_facts",
    "possible_interpretation",
    "contradicting_evidence",
    "confidence_uncertainty",
    "finding",
]

# Field ini berasal dari skema Ground Truth privat dan TIDAK BOLEH muncul
# di output model manapun (mencegah kebocoran tidak sengaja).
FORBIDDEN_GT_FIELDS = [
    "evidence_strength",
    "expected_entity_ids",
    "expected_relation_ids",
    "is_key_evidence",
    "annotation_notes",
]


class ValidationError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


def validate_structured_finding(finding: Dict[str, Any]) -> None:
    """Raise ValidationError jika finding tidak memenuhi schema wajib.
    Tidak mengembalikan apa pun jika valid.
    """
    errors: List[str] = []

    missing = [f for f in REQUIRED_FIELDS if f not in finding]
    if missing:
        errors.append(f"Field wajib hilang: {missing}")

    leaked = [f for f in FORBIDDEN_GT_FIELDS if f in finding]
    if leaked:
        errors.append(f"Field Ground Truth terdeteksi di output (DILARANG): {leaked}")

    if "relevant_evidence" in finding and not isinstance(finding["relevant_evidence"], list):
        errors.append("'relevant_evidence' harus berupa list evidence/chunk IDs")

    if "finding" in finding and not isinstance(finding["finding"], str):
        errors.append("'finding' harus berupa teks ringkasan (string)")

    if errors:
        raise ValidationError(errors)


def validate_file(path: Path) -> None:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    findings = data if isinstance(data, list) else [data]
    all_errors: List[str] = []
    for idx, finding in enumerate(findings):
        try:
            validate_structured_finding(finding)
        except ValidationError as exc:
            all_errors.append(f"[finding #{idx}] {exc}")

    if all_errors:
        raise ValidationError(all_errors)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Validasi structured finding JSON (P6/P7/P8).")
    parser.add_argument("--input", required=True, help="Path file JSON berisi satu/banyak finding")
    args = parser.parse_args()

    try:
        validate_file(Path(args.input))
    except ValidationError as exc:
        print("[validate_output] GAGAL:")
        for e in exc.errors:
            print(f"  - {e}")
        raise SystemExit(1)
    except FileNotFoundError:
        print(f"[validate_output] ERROR: file tidak ditemukan: {args.input}")
        raise SystemExit(1)

    print(f"[validate_output] OK - {args.input} memenuhi schema structured finding.")


if __name__ == "__main__":
    main()
