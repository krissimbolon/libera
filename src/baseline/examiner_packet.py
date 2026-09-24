"""Build a deterministic, time-boxed P5 examiner review packet.

The packet is a QC/triage instrument, not ground truth. It selects a small,
pre-registered sample from the deterministic P5 baseline so a human examiner
can verify relevance and traceability without reading the full corpus.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ALLOWED_DECISIONS = {"SUPPORTED", "NOT_SUPPORTED", "UNCERTAIN"}
FIELDS = [
    "review_order",
    "evidence_id",
    "primary_task_id",
    "linked_task_ids",
    "best_rank",
    "automated_score",
    "matched_keywords",
    "timestamp",
    "sender",
    "receiver",
    "text",
    "examiner_decision",
    "examiner_note",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_findings(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("P5 baseline_findings.json is empty or invalid.")
    return data


def build_packet(
    baseline_path: Path,
    output_csv: Path,
    output_manifest: Path,
    max_items: int = 12,
) -> dict:
    findings = load_findings(baseline_path)
    if max_items < 10:
        raise ValueError("max_items must be >= 10 to preserve T01-T10 coverage.")

    # Build a stable evidence candidate registry across all pre-registered tasks.
    registry: dict[str, dict] = {}
    task_candidates: dict[str, list[str]] = defaultdict(list)
    task_order: list[str] = []

    for finding in findings:
        task_id = str(finding["task_id"])
        task_order.append(task_id)
        for rank, evidence in enumerate(finding.get("evidence", []), start=1):
            eid = str(evidence["evidence_id"])
            task_candidates[task_id].append(eid)
            entry = registry.setdefault(
                eid,
                {
                    "evidence_id": eid,
                    "task_ids": [],
                    "best_rank": rank,
                    "score": int(evidence.get("score", 0)),
                    "matched_keywords": set(),
                    "timestamp": evidence.get("timestamp", ""),
                    "sender": evidence.get("sender", ""),
                    "receiver": evidence.get("receiver", ""),
                    "text": evidence.get("text", ""),
                },
            )
            if task_id not in entry["task_ids"]:
                entry["task_ids"].append(task_id)
            entry["best_rank"] = min(entry["best_rank"], rank)
            entry["score"] = max(entry["score"], int(evidence.get("score", 0)))
            entry["matched_keywords"].update(evidence.get("matched_keywords", []))

    selected: list[str] = []
    assigned_primary: dict[str, str] = {}
    uncovered_tasks: list[str] = []

    # Coverage pass: select one unique highest-ranked candidate per task where possible.
    for task_id in task_order:
        candidates = task_candidates.get(task_id, [])
        if not candidates:
            uncovered_tasks.append(task_id)
            continue
        choice = next((eid for eid in candidates if eid not in selected), candidates[0])
        if choice not in selected:
            selected.append(choice)
        assigned_primary.setdefault(choice, task_id)

    # Fill remaining slots deterministically with cross-task/high-score candidates.
    remaining = [
        e for eid, e in registry.items() if eid not in selected
    ]
    remaining.sort(
        key=lambda e: (
            -len(e["task_ids"]),
            -e["score"],
            e["best_rank"],
            e["timestamp"],
            e["evidence_id"],
        )
    )
    for entry in remaining:
        if len(selected) >= max_items:
            break
        selected.append(entry["evidence_id"])
        assigned_primary.setdefault(entry["evidence_id"], entry["task_ids"][0])

    selected = selected[:max_items]
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for order, eid in enumerate(selected, start=1):
        e = registry[eid]
        rows.append(
            {
                "review_order": str(order),
                "evidence_id": eid,
                "primary_task_id": assigned_primary.get(eid, e["task_ids"][0]),
                "linked_task_ids": "|".join(e["task_ids"]),
                "best_rank": str(e["best_rank"]),
                "automated_score": str(e["score"]),
                "matched_keywords": "|".join(sorted(e["matched_keywords"])),
                "timestamp": e["timestamp"],
                "sender": e["sender"],
                "receiver": e["receiver"],
                "text": e["text"],
                "examiner_decision": "",
                "examiner_note": "",
            }
        )

    with output_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    covered_tasks = sorted(
        {
            tid
            for row in rows
            for tid in row["linked_task_ids"].split("|")
            if tid
        }
    )
    manifest = {
        "status": "P5_EXAMINER_PACKET_READY",
        "purpose": "time-boxed human QC/triage; not evaluator ground truth",
        "baseline_findings": str(baseline_path),
        "baseline_findings_sha256": sha256_file(baseline_path),
        "packet_csv": str(output_csv),
        "packet_sha256_before_review": sha256_file(output_csv),
        "max_review_items": max_items,
        "selected_unique_evidence": len(rows),
        "covered_task_ids": covered_tasks,
        "uncovered_task_ids": uncovered_tasks,
        "decision_vocabulary": sorted(ALLOWED_DECISIONS),
        "timebox_seconds": 300,
        "selection_rule": (
            "one unique highest-ranked candidate per task where possible, then "
            "fill deterministically by cross-task coverage, score, rank, timestamp, evidence_id"
        ),
    }
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    output_manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    p = argparse.ArgumentParser(description="Build <=5 minute P5 examiner QC packet.")
    p.add_argument(
        "--baseline",
        default="runtime/working/P5/baseline_findings.json",
    )
    p.add_argument(
        "--output",
        default="runtime/working/P5/p5_examiner_packet.csv",
    )
    p.add_argument(
        "--manifest",
        default="runtime/working/P5/p5_examiner_packet_manifest.json",
    )
    p.add_argument("--max-items", type=int, default=12)
    args = p.parse_args()

    try:
        manifest = build_packet(
            Path(args.baseline),
            Path(args.output),
            Path(args.manifest),
            args.max_items,
        )
    except (ValueError, FileNotFoundError, KeyError) as exc:
        print(f"[P5-EXAMINER] ERROR: {exc}")
        raise SystemExit(1)

    print("[P5-EXAMINER] PACKET READY")
    print(f"  review_items={manifest['selected_unique_evidence']}")
    print(f"  task_coverage={len(manifest['covered_task_ids'])}/10")
    print("  timebox=300 seconds; packet is QC/triage, not ground truth")


if __name__ == "__main__":
    main()
