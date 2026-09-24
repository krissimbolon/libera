#!/usr/bin/env python3
"""Generate a PRIVATE ground-truth annotation packet without assigning labels.

The output belongs under runtime/private or another non-repository location.
It uses P4 acquired evidence as the evaluation universe and joins frozen-P2
design metadata only as evaluator hints. It NEVER auto-fills is_key_evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

CANONICAL_SHA256 = "a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", required=True)
    ap.add_argument(
        "--corpus",
        default="data/adaptasi_indonesia/corpus_whatsapp_10000.csv",
    )
    ap.add_argument(
        "--output",
        default="runtime/private/P9/ground_truth_annotation_packet.csv",
    )
    ap.add_argument(
        "--manifest",
        default="runtime/private/P9/ground_truth_annotation_manifest.json",
    )
    args = ap.parse_args()

    artifacts_path = Path(args.artifacts)
    corpus_path = Path(args.corpus)
    output_path = Path(args.output)
    manifest_path = Path(args.manifest)

    if sha256(corpus_path) != CANONICAL_SHA256:
        raise SystemExit("Frozen P2 hash mismatch; refusing GT packet generation.")

    with corpus_path.open("r", encoding="utf-8", newline="") as f:
        design = {r["message_id"]: r for r in csv.DictReader(f)}

    with artifacts_path.open("r", encoding="utf-8", newline="") as f:
        artifacts = list(csv.DictReader(f))
    if not artifacts:
        raise SystemExit("P4 artifact input is empty.")

    fields = [
        "message_id",
        "evidence_strength",
        "event_id",
        "expected_entity_ids",
        "expected_relation_ids",
        "is_key_evidence",
        "annotation_notes",
        "review_status",
        "review_hint_source_anchor",
        "evidence_id",
        "timestamp",
        "sender",
        "receiver",
        "message_text",
        "design_segment_id",
        "source_original_line_private_hint",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    anchor_candidates = 0
    missing_design = 0
    with output_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for art in artifacts:
            msg = art["message_id"]
            d = design.get(msg)
            if d is None:
                missing_design += 1
                d = {}
            anchor = d.get("source_provenance") == "ADAPTED_FROM_GALLOWAY"
            anchor_candidates += int(anchor)
            w.writerow({
                "message_id": msg,
                "evidence_strength": "",
                "event_id": "",
                "expected_entity_ids": "",
                "expected_relation_ids": "",
                "is_key_evidence": "",
                "annotation_notes": "",
                "review_status": "UNREVIEWED",
                "review_hint_source_anchor": "1" if anchor else "0",
                "evidence_id": art.get("evidence_id", ""),
                "timestamp": art.get("timestamp_normalized", ""),
                "sender": art.get("sender", ""),
                "receiver": art.get("receiver", ""),
                "message_text": art.get("message_text", ""),
                "design_segment_id": d.get("conversation_id", ""),
                "source_original_line_private_hint": d.get("source_original_line", ""),
            })

    manifest = {
        "status": "PRIVATE_ANNOTATION_PACKET_READY",
        "artifact_input": str(artifacts_path),
        "artifact_input_sha256": sha256(artifacts_path),
        "frozen_corpus_sha256": CANONICAL_SHA256,
        "row_count": len(artifacts),
        "source_anchor_review_hints": anchor_candidates,
        "artifact_rows_missing_design_join": missing_design,
        "labels_auto_assigned": 0,
        "required_human_action": (
            "Evaluator/Case Lead must set review_status and explicitly label "
            "is_key_evidence plus event/entity/relation fields where established."
        ),
        "privacy": (
            "Do not commit this generated CSV. It contains evaluator-only "
            "source-design hints and annotation state."
        ),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
