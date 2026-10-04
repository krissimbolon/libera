"""Score manually completed post-lock Libera review packets."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


SUPPORT = {"SUPPORTED", "PARTIAL", "UNSUPPORTED", "CONTRADICTED", "ABSTAINED"}


def dcg(grades: list[int]) -> float:
    return sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(grades))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--review-dir", default="runtime/working/P9/human_review")
    p.add_argument("--output", default="runtime/working/P9/human_review_metrics.json")
    args = p.parse_args()

    root = Path(args.review_dir)
    with (root / "retrieval_relevance_review.csv").open(encoding="utf-8-sig", newline="") as f:
        retrieval = list(csv.DictReader(f))
    with (root / "claim_supportedness_review.csv").open(encoding="utf-8-sig", newline="") as f:
        claims = list(csv.DictReader(f))

    grouped = defaultdict(list)
    for row in retrieval:
        raw = (row.get("relevance_grade_0_2") or "").strip()
        if raw not in {"0", "1", "2"}:
            raise SystemExit(f"Incomplete retrieval review: {row.get('task_id')} rank {row.get('rank')}")
        grouped[row["task_id"]].append((int(row["rank"]), int(raw)))

    per_task = {}
    for task, values in grouped.items():
        grades = [g for _, g in sorted(values)]
        binary = [g > 0 for g in grades]
        first = next((i + 1 for i, ok in enumerate(binary) if ok), None)
        ideal = sorted(grades, reverse=True)
        denom = dcg(ideal)
        per_task[task] = {
            "P@8": round(sum(binary) / len(binary), 6),
            "MRR@8": round(1 / first, 6) if first else 0.0,
            "nDCG@8": round(dcg(grades) / denom, 6) if denom else 0.0,
            "judged_chunks": len(grades),
        }

    retrieval_summary = {
        "per_task": per_task,
        "mean_P@8": round(sum(x["P@8"] for x in per_task.values()) / len(per_task), 6),
        "mean_MRR@8": round(sum(x["MRR@8"] for x in per_task.values()) / len(per_task), 6),
        "mean_nDCG@8": round(sum(x["nDCG@8"] for x in per_task.values()) / len(per_task), 6),
        "Recall@8": None,
        "recall_note": "Not computed: no complete independently judged relevant set.",
    }

    label_counts = Counter()
    components = defaultdict(list)
    for row in claims:
        label = (row.get("support_label") or "").strip().upper()
        if label not in SUPPORT:
            raise SystemExit(f"Incomplete claim review: {row.get('task_id')}/{row.get('condition')}")
        label_counts[label] += 1
        for field in (
            "task_completion_0_2", "factual_consistency_0_2",
            "evidentiary_support_0_2", "uncertainty_handling_0_2",
        ):
            raw = (row.get(field) or "").strip()
            if raw not in {"0", "1", "2"}:
                raise SystemExit(f"Invalid {field}: {row.get('task_id')}/{row.get('condition')}")
            components[field].append(int(raw))

    total = len(claims)
    evaluable = total - label_counts["ABSTAINED"]
    claim_summary = {
        "rows": total,
        "support_label_counts": dict(sorted(label_counts.items())),
        "supported_rate": round(label_counts["SUPPORTED"] / evaluable, 6) if evaluable else None,
        "supported_or_partial_rate": round(
            (label_counts["SUPPORTED"] + label_counts["PARTIAL"]) / evaluable, 6
        ) if evaluable else None,
        "unsupported_or_contradicted_rate": round(
            (label_counts["UNSUPPORTED"] + label_counts["CONTRADICTED"]) / evaluable, 6
        ) if evaluable else None,
        "component_scores_0_1": {
            field: round(sum(values) / (2 * len(values)), 6)
            for field, values in components.items()
        },
        "task_component_score_0_1": round(
            sum(sum(values) for values in components.values()) /
            (2 * sum(len(values) for values in components.values())), 6
        ),
    }

    result = {
        "status": "POSTLOCK_HUMAN_REVIEW_COMPLETE",
        "retrieval": retrieval_summary,
        "claim_supportedness": claim_summary,
        "interpretation": (
            "These human-review metrics are distinct from citation identifier validity and from any "
            "message-level private ground-truth classification."
        ),
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[POSTLOCK-SCORE] PASS -> {out}")


if __name__ == "__main__":
    main()
