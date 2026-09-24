"""P9 evaluation for locked P5/P8 outputs.

Two layers:
1) integrity/groundedness precheck that needs no evaluator ground truth;
2) optional blinded message-level TP/FP/TN/FN evaluation using a PRIVATE
   ground-truth CSV after P8 outputs are locked.

Ground truth is never written back to the repository or AI index.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ART_RE = re.compile(r"ART-\d{6}")


class EvaluationError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_p8_lock(lock_manifest: Path, artifacts: Path, baseline: Path | None, experiment: Path) -> dict:
    data = json.loads(Path(lock_manifest).read_text(encoding="utf-8"))
    if data.get("status") != "P8_OUTPUTS_LOCKED_BEFORE_GROUND_TRUTH":
        raise EvaluationError("P8 lock manifest status is invalid.")
    files = data.get("files", {})
    checks = [
        ("p4_artifacts", artifacts),
        ("p8_experiment_output", experiment),
    ]
    if baseline is not None:
        checks.append(("p5_baseline", baseline))
    for key, path in checks:
        recorded = (files.get(key) or {}).get("sha256")
        actual = _sha256(path)
        if not recorded or recorded != actual:
            raise EvaluationError(
                f"P8 lock mismatch for {key}: recorded={recorded} actual={actual}"
            )
    return {
        "lock_status": data["status"],
        "locked_at_utc": data.get("locked_at_utc"),
        "lock_manifest": str(lock_manifest),
    }


def load_artifacts(path: Path):
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise EvaluationError("Artifact CSV kosong.")
    art_to_msg = {r["evidence_id"]: r["message_id"] for r in rows}
    msg_to_art = {v: k for k, v in art_to_msg.items()}
    return rows, art_to_msg, msg_to_art


def _extract_art_ids(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, (list, dict)):
        text = json.dumps(value, ensure_ascii=False)
    else:
        text = str(value)
    return set(ART_RE.findall(text))


def _parse_structured_output(text: str):
    if not text:
        return None, False
    candidate = text.strip()
    if candidate.startswith("~~~"):
        candidate = re.sub(r"^~~~(?:json)?\s*", "", candidate)
        candidate = re.sub(r"\s*~~~$", "", candidate)
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*", "", candidate)
        candidate = re.sub(r"\s*```$", "", candidate)
    try:
        obj = json.loads(candidate)
    except json.JSONDecodeError:
        return None, False
    required = {
        "question", "relevant_evidence", "observed_facts",
        "possible_interpretation", "contradicting_evidence",
        "confidence_uncertainty", "finding",
    }
    return obj, required.issubset(obj)


def integrity_precheck(experiment_path: Path, artifact_ids: set[str]) -> dict:
    data = json.loads(Path(experiment_path).read_text(encoding="utf-8"))
    summary = {
        "task_count": len(data),
        "conditions": {},
        "retrieval_invalid_evidence_ids": [],
    }
    retrieval_ids = set()
    for row in data:
        retrieval_ids |= set(
            row.get("retrieval_trace", {}).get("retrieved_evidence_ids", [])
        )
    summary["retrieval_invalid_evidence_ids"] = sorted(retrieval_ids - artifact_ids)

    for condition in ["A_llm_only", "B_llm_rag", "C_llm_rag_structured"]:
        cited = set()
        invalid = set()
        errors = 0
        structured_valid = 0
        outputs = 0
        for row in data:
            rec = row.get(condition)
            if not rec:
                continue
            outputs += 1
            if rec.get("error"):
                errors += 1
            output = rec.get("output", "")
            ids = _extract_art_ids(output)
            cited |= ids
            invalid |= (ids - artifact_ids)
            if condition == "C_llm_rag_structured":
                _, ok = _parse_structured_output(output)
                structured_valid += int(ok)
        summary["conditions"][condition] = {
            "outputs": outputs,
            "errors": errors,
            "unique_cited_artifacts": len(cited),
            "invalid_citation_count": len(invalid),
            "invalid_citations": sorted(invalid),
            "structured_json_valid": (
                structured_valid if condition == "C_llm_rag_structured" else None
            ),
        }
    return summary


def _binary_label(value: str):
    token = str(value).strip().casefold()
    if token in {"1", "true", "yes", "y", "ya", "key", "relevant", "positive"}:
        return True
    if token in {"0", "false", "no", "n", "tidak", "non-key", "irrelevant", "negative"}:
        return False
    return None


def load_ground_truth(path: Path, msg_to_art: dict[str, str]):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise EvaluationError("Ground truth privat kosong.")
    required = {"message_id", "is_key_evidence"}
    if not required.issubset(rows[0]):
        raise EvaluationError(
            "Ground truth harus memiliki kolom message_id dan is_key_evidence."
        )
    labeled = set()
    positive = set()
    unknown = []
    unlabeled = []
    for r in rows:
        msg = r["message_id"]
        label = _binary_label(r["is_key_evidence"])
        if label is None:
            unlabeled.append(msg)
            continue
        if msg not in msg_to_art:
            unknown.append(msg)
            continue
        art = msg_to_art[msg]
        labeled.add(art)
        if label:
            positive.add(art)
    # Ground truth may be partially annotated and may describe the complete
    # designed case while one acquired device contains only its own evidence
    # universe. Unlabeled and unacquired rows are reported separately and never
    # silently treated as negatives.
    return labeled, positive, unknown, unlabeled


def _confusion(predicted: set[str], labeled: set[str], positive: set[str]) -> dict:
    predicted = predicted & labeled
    negative = labeled - positive
    tp = len(predicted & positive)
    fp = len(predicted & negative)
    fn = len(positive - predicted)
    tn = len(negative - predicted)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    specificity = tn / (tn + fp) if tn + fp else 0.0
    return {
        "TP": tp, "FP": fp, "FN": fn, "TN": tn,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "specificity": round(specificity, 6),
        "predicted_positive": len(predicted),
        "ground_truth_positive": len(positive),
        "labeled_universe": len(labeled),
    }


def _experiment_sets(experiment_path: Path):
    data = json.loads(Path(experiment_path).read_text(encoding="utf-8"))
    sets = {
        "B_retrieval": set(),
        "B_citations": set(),
        "C_citations": set(),
    }
    for row in data:
        sets["B_retrieval"] |= set(
            row.get("retrieval_trace", {}).get("retrieved_evidence_ids", [])
        )
        sets["B_citations"] |= _extract_art_ids(
            (row.get("B_llm_rag") or {}).get("output", "")
        )
        c = row.get("C_llm_rag_structured") or {}
        obj, ok = _parse_structured_output(c.get("output", ""))
        if ok and isinstance(obj.get("relevant_evidence"), list):
            sets["C_citations"] |= set(obj["relevant_evidence"])
        else:
            sets["C_citations"] |= _extract_art_ids(c.get("output", ""))
    return sets


def _baseline_set(path: Path) -> set[str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {
        e["evidence_id"]
        for finding in data
        for e in finding.get("evidence", [])
        if e.get("evidence_id")
    }


def run(
    artifacts: Path,
    experiment: Path,
    output: Path,
    baseline: Path | None = None,
    ground_truth: Path | None = None,
    outputs_locked: bool = False,
    lock_manifest: Path | None = None,
) -> dict:
    rows, art_to_msg, msg_to_art = load_artifacts(artifacts)
    artifact_ids = set(art_to_msg)
    result = {
        "status": "P9_PRECHECK_PASS",
        "artifact_count": len(rows),
        "outputs_locked": outputs_locked,
        "integrity": integrity_precheck(experiment, artifact_ids),
        "ground_truth_evaluation": None,
        "p8_lock_verification": None,
    }
    if result["integrity"]["retrieval_invalid_evidence_ids"]:
        result["status"] = "P9_PRECHECK_FAIL_INVALID_EVIDENCE_REFERENCE"

    if ground_truth is not None:
        if not outputs_locked:
            raise EvaluationError(
                "Refuse: ground truth hanya boleh dibuka setelah outputs_locked."
            )
        if lock_manifest is None:
            raise EvaluationError(
                "Refuse: private ground truth requires a cryptographic P8 lock manifest."
            )
        result["p8_lock_verification"] = verify_p8_lock(
            lock_manifest, artifacts, baseline, experiment
        )
        labeled, positive, unacquired, unlabeled = load_ground_truth(ground_truth, msg_to_art)
        predictions = _experiment_sets(experiment)
        if baseline is not None:
            predictions["P5_baseline"] = _baseline_set(baseline)
        metrics = {
            name: _confusion(pred, labeled, positive)
            for name, pred in predictions.items()
        }
        result["ground_truth_evaluation"] = {
            "protocol": "blinded message-level key-evidence classification",
            "ground_truth_path_redacted": True,
            "labeled_rows": len(labeled),
            "key_evidence_rows": len(positive),
            "ground_truth_rows_unacquired": len(unacquired),
            "ground_truth_unacquired_examples": unacquired[:10],
            "ground_truth_rows_unlabeled": len(unlabeled),
            "ground_truth_unlabeled_examples": unlabeled[:10],
            "evaluation_universe_note": (
                "Metrics are computed only on ground-truth messages present in "
                "the acquired P4 evidence universe; unacquired rows are reported "
                "separately and are not counted as TN/FN."
            ),
            "metrics": metrics,
        }
        result["status"] = "P9_FINAL_EVALUATION_COMPLETE"

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    p = argparse.ArgumentParser(description="P9 blind evaluation.")
    p.add_argument("--artifacts", default="runtime/working/P4/artifacts.csv")
    p.add_argument("--experiment", default="runtime/working/P8/experiment_output.json")
    p.add_argument("--baseline", default="runtime/working/P5/baseline_findings.json")
    p.add_argument("--ground-truth", default=None)
    p.add_argument("--outputs-locked", action="store_true")
    p.add_argument("--lock-manifest", default=None)
    p.add_argument("--output", default="runtime/working/P9/evaluation.json")
    args = p.parse_args()
    try:
        result = run(
            Path(args.artifacts),
            Path(args.experiment),
            Path(args.output),
            Path(args.baseline) if args.baseline else None,
            Path(args.ground_truth) if args.ground_truth else None,
            args.outputs_locked,
            Path(args.lock_manifest) if args.lock_manifest else None,
        )
    except (EvaluationError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"[P9] ERROR: {exc}")
        raise SystemExit(1)
    print(f"[P9] {result['status']}")


if __name__ == "__main__":
    main()
