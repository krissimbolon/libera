"""Rebuild a provenance proxy, NOT lost human key-evidence judgments.

Inputs are frozen P2 and its design specification only. No model output, P5
prediction, retrieval result, or experimental metric is read by this tool.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

CANONICAL_SHA256 = "a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6"
ORIGIN = "RECONSTRUCTED_PROVENANCE_PROXY_V1"
TARGET = "source_anchor_vs_designed_distractor_not_semantic_key_evidence"
RULES = {"ADAPTED_FROM_GALLOWAY": "1", "SYNTHETIC_DISTRACTOR": "0",
         "SYNTHETIC_CONTEXT": "", "SYNTHETIC_BRIDGE": ""}


def label_for(provenance):
    if provenance not in RULES:
        raise ValueError(f"Unknown provenance: {provenance}")
    return RULES[provenance]


def reconstruct(corpus: Path, design: Path, output_dir: Path):
    if hashlib.sha256(corpus.read_bytes()).hexdigest() != CANONICAL_SHA256:
        raise ValueError("Frozen corpus hash mismatch")
    output = output_dir / "reconstructed_reference.csv"
    manifest_path = output_dir / "reconstruction_manifest.json"
    if output.exists() or manifest_path.exists():
        raise ValueError("Refuse to overwrite reconstructed reference; choose a new directory")
    with corpus.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 10000 or len({r["message_id"] for r in rows}) != 10000:
        raise ValueError("Expected 10,000 unique frozen messages")
    # Validate all provenance values before writing.
    labels = [label_for(r["source_provenance"]) for r in rows]
    output_dir.mkdir(parents=True, exist_ok=True)
    fields = ["message_id", "is_key_evidence", "proxy_label", "label_origin",
              "reference_target", "source_provenance", "review_status",
              "evidence_strength", "event_id", "expected_entity_ids",
              "expected_relation_ids", "annotation_notes"]
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row, label in zip(rows, labels):
            writer.writerow({"message_id": row["message_id"], "is_key_evidence": label,
                             "proxy_label": label, "label_origin": ORIGIN,
                             "reference_target": TARGET, "source_provenance": row["source_provenance"],
                             "review_status": "UNREVIEWED_RECONSTRUCTED_PROXY",
                             "annotation_notes": "Compatibility field is_key_evidence encodes provenance proxy only; human semantic labels are NOT recovered."})
    counts = Counter(labels)
    manifest = {
        "status": "RECONSTRUCTED_PROXY_NOT_INDEPENDENT_GROUND_TRUTH",
        "label_origin": ORIGIN, "reference_target": TARGET,
        "rules": RULES, "row_count": len(rows), "positive_rows": counts["1"],
        "negative_rows": counts["0"], "unlabeled_rows": counts[""],
        "human_review_complete": False, "original_lost_labels_recovered": False,
        "source_corpus_sha256": CANONICAL_SHA256,
        "source_design_sha256": hashlib.sha256(design.read_bytes()).hexdigest(),
        "reference_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "limitation": "Post-hoc provenance benchmark only. Anchors are not automatically key evidence; distractor provenance does not establish semantic irrelevance. Context/bridge remain unlabeled. No claim of restored original or blind human ground truth.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default="data/adaptasi_indonesia/corpus_whatsapp_10000.csv")
    parser.add_argument("--design", type=Path, default="docs/02_case_design/desain_dataset_10000_pesan_indonesia.md")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(reconstruct(args.corpus, args.design, args.output_dir), indent=2))
