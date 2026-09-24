"""Export an evaluator packet; never edits model answers or guesses evidence IDs."""
import argparse
import csv
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluation", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Review packet already exists; choose a new output path.")
    evaluation = json.loads(args.evaluation.read_text(encoding="utf-8"))
    validation = evaluation["citation_validation"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["task_id", "condition", "run_id", "reference_status", "raw_reference",
              "verified_evidence_id", "rejection_reason", "claim_review_status"]
    with args.output.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for record in validation["records"]:
            base = {key: record[key] for key in ("task_id", "condition", "run_id")}
            for eid in record["verified_evidence_ids"]:
                writer.writerow({**base, "reference_status": "VERIFIED_ID_ONLY",
                                 "raw_reference": eid, "verified_evidence_id": eid,
                                 "claim_review_status": "NOT_SEMANTICALLY_REVIEWED"})
            for rejected in record["quarantined_references"]:
                raw = rejected["raw_reference"]
                writer.writerow({**base, "reference_status": "QUARANTINED",
                                 "raw_reference": raw if isinstance(raw, str) else json.dumps(raw),
                                 "rejection_reason": rejected["reason"],
                                 "claim_review_status": "NOT_ELIGIBLE_AS_EVIDENCE"})
            if not record["verified_evidence_ids"] and not record["quarantined_references"]:
                writer.writerow({**base, "reference_status": "NO_CITATION",
                                 "claim_review_status": "ABSTENTION_OR_UNSUPPORTED_CLAIM_REVIEW_REQUIRED"})
    print(f"[P9] review packet: {args.output}")
    print(f"SHA-256: {hashlib.sha256(args.output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
