"""Build blinded/manual review packets only after P8 is cryptographically locked.

The packets do not contain evaluator ground truth. They separate:
- ranked retrieval relevance at the chunk level; and
- semantic support of B/C answers by the citations that survived strict validation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from src.evaluation.citation_validation import validate as validate_citations
from src.evaluation.evaluate_experiment import verify_p8_lock


RETRIEVAL_FIELDS = [
    "task_id", "question", "rank", "chunk_id", "similarity_score",
    "chunk_text", "relevance_grade_0_2", "reviewer_note",
]
CLAIM_FIELDS = [
    "task_id", "condition", "question", "model_output",
    "verified_evidence_ids", "cited_evidence_text",
    "support_label", "task_completion_0_2", "factual_consistency_0_2",
    "evidentiary_support_0_2", "uncertainty_handling_0_2", "reviewer_note",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_locked_extra(lock_path: Path, candidate: Path) -> None:
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    target = candidate.resolve()
    for record in lock.get("files", {}).values():
        if not isinstance(record, dict) or not record.get("path"):
            continue
        path = Path(record["path"])
        if path.resolve() == target and path.is_file() and sha256(path) == record.get("sha256"):
            return
    raise SystemExit(f"Required post-lock source is not hash-locked by P8: {candidate}")


def load_artifacts(path: Path) -> dict[str, dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return {row["evidence_id"]: row for row in rows}


def evidence_text(row: dict) -> str:
    return (
        f"[{row.get('evidence_id','')}] {row.get('timestamp','')} "
        f"{row.get('sender','')} -> {row.get('receiver','')}: {row.get('text','')}"
    ).strip()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--artifacts", default="runtime/working/P4/artifacts.csv")
    p.add_argument("--baseline", default="runtime/working/P5/baseline_findings.json")
    p.add_argument("--experiment", default="runtime/working/P8/experiment_output.json")
    p.add_argument("--index", default="runtime/working/P6/index.json")
    p.add_argument("--lock-manifest", default="runtime/working/P8/p8_lock_manifest.json")
    p.add_argument("--output-dir", default="runtime/working/P9/human_review")
    args = p.parse_args()

    artifacts_path = Path(args.artifacts)
    baseline_path = Path(args.baseline)
    experiment_path = Path(args.experiment)
    index_path = Path(args.index)
    lock_path = Path(args.lock_manifest)

    verify_p8_lock(lock_path, artifacts_path, baseline_path, experiment_path)
    ensure_locked_extra(lock_path, index_path)

    out_dir = Path(args.output_dir)
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"Refuse to overwrite existing human-review directory: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    artifacts = load_artifacts(artifacts_path)
    experiment = json.loads(experiment_path.read_text(encoding="utf-8"))
    index = json.loads(index_path.read_text(encoding="utf-8"))
    chunks = {entry["chunk_id"]: entry for entry in index["entries"]}

    retrieval_path = out_dir / "retrieval_relevance_review.csv"
    with retrieval_path.open("x", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=RETRIEVAL_FIELDS)
        w.writeheader()
        for row in experiment:
            trace = row["retrieval_trace"]
            ids = trace.get("retrieved_chunk_ids", [])
            scores = trace.get("scores", [])
            for rank, chunk_id in enumerate(ids, 1):
                chunk = chunks.get(chunk_id)
                if chunk is None:
                    raise SystemExit(f"Retrieved chunk missing from locked index: {chunk_id}")
                w.writerow({
                    "task_id": row["task_id"],
                    "question": row["question"],
                    "rank": rank,
                    "chunk_id": chunk_id,
                    "similarity_score": scores[rank - 1] if rank - 1 < len(scores) else "",
                    "chunk_text": chunk.get("text", ""),
                    "relevance_grade_0_2": "",
                    "reviewer_note": "",
                })

    citation = validate_citations(experiment_path, set(artifacts))
    valid_by_task_condition = {
        (rec["task_id"], rec["condition"]): rec["verified_evidence_ids"]
        for rec in citation["records"]
    }

    claim_path = out_dir / "claim_supportedness_review.csv"
    with claim_path.open("x", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CLAIM_FIELDS)
        w.writeheader()
        for row in experiment:
            for condition in ("B_llm_rag", "C_llm_rag_structured"):
                rec = row[condition]
                ids = valid_by_task_condition.get((row["task_id"], condition), [])
                cited = "\n".join(evidence_text(artifacts[eid]) for eid in ids)
                w.writerow({
                    "task_id": row["task_id"],
                    "condition": condition,
                    "question": row["question"],
                    "model_output": rec.get("output", ""),
                    "verified_evidence_ids": "|".join(ids),
                    "cited_evidence_text": cited,
                    "support_label": "",
                    "task_completion_0_2": "",
                    "factual_consistency_0_2": "",
                    "evidentiary_support_0_2": "",
                    "uncertainty_handling_0_2": "",
                    "reviewer_note": "",
                })

    manifest = {
        "status": "POSTLOCK_HUMAN_REVIEW_PACKETS_READY",
        "source_p8_lock_sha256": sha256(lock_path),
        "source_experiment_sha256": sha256(experiment_path),
        "source_index_sha256": sha256(index_path),
        "retrieval_packet": {
            "path": str(retrieval_path),
            "sha256_before_review": sha256(retrieval_path),
            "rows": sum(1 for _ in retrieval_path.open(encoding="utf-8")) - 1,
            "rubric": "0=irrelevant, 1=partially relevant, 2=directly relevant",
            "metrics_after_review": ["Precision@8", "MRR@8", "nDCG@8"],
            "recall_note": "Recall@8 is not reportable without a complete independently judged relevant set.",
        },
        "claim_packet": {
            "path": str(claim_path),
            "sha256_before_review": sha256(claim_path),
            "rows": sum(1 for _ in claim_path.open(encoding="utf-8")) - 1,
            "support_labels": ["SUPPORTED", "PARTIAL", "UNSUPPORTED", "CONTRADICTED", "ABSTAINED"],
            "component_scale": "0=not satisfied, 1=partial, 2=satisfied",
        },
        "separation_rule": (
            "Identifier validity, retrieval relevance, semantic claim support and task correctness "
            "are evaluated as distinct layers. These packets contain no private evaluator ground truth."
        ),
    }
    manifest_path = out_dir / "review_packet_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[POSTLOCK-REVIEW] PASS -> {out_dir}")


if __name__ == "__main__":
    main()
