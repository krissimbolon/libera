#!/usr/bin/env python3
"""Cryptographically lock P8 outputs before evaluator ground truth is opened."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def item(path: Path, required: bool = True):
    if not path.exists():
        if required:
            raise SystemExit(f"Required lock input not found: {path}")
        return None
    return {"path": str(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}


def validate_real_experiment(path: Path, tasks_path: Path | None = None, config_path: Path | None = None) -> None:
    """Refuse smoke/error/incomplete runs before a real-evaluation lock."""
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("P8 experiment must contain tasks")
    expected = None
    config = None
    if tasks_path is not None:
        tasks = json.loads(tasks_path.read_text(encoding="utf-8"))["tasks"]
        expected = {t["task_id"]: t["question"] for t in tasks}
        if len(expected) != len(tasks):
            raise ValueError("Duplicate registered task IDs")
    if config_path is not None:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    seen = set()
    provenance = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Task row must be an object")
        task = row.get("task_id")
        if not task or task in seen:
            raise ValueError("Missing or duplicate task_id")
        seen.add(task)
        if expected is not None and (task not in expected or row.get("question") != expected[task]):
            raise ValueError("Task question differs from registration")
        if config is not None:
            trace = row.get("retrieval_trace") or {}
            if trace.get("k") != config["retrieval"]["top_k"]:
                raise ValueError("Retrieval top-k differs from registered config")
            if trace.get("embedding_method") != config["embedding"]["final_method"] or trace.get("embedding_model") != config["embedding"]["final_model"]:
                raise ValueError("Embedding differs from registered config")
        for condition in ("A_llm_only", "B_llm_rag", "C_llm_rag_structured"):
            rec = row.get(condition)
            if not isinstance(rec, dict) or rec.get("dry_run") is not False:
                raise ValueError(f"{task}/{condition}: real execution required")
            if rec.get("error") or not str(rec.get("output", "")).strip():
                raise ValueError(f"{task}/{condition}: failed or empty execution")
            if config is not None:
                for field in ("model", "temperature", "seed", "num_ctx"):
                    if rec.get(field) != config["ollama"][field]:
                        raise ValueError(f"Model parameter {field} differs from config")
                if rec.get("prompt_version") != config["prompt"]["prompt_version"] or rec.get("query") != row["question"]:
                    raise ValueError("Prompt/query differs from registration")
            provenance.add((rec.get("model"), rec.get("model_digest"), rec.get("ollama_version")))
            if condition == "C_llm_rag_structured":
                from src.evaluation.evaluate_experiment import _parse_structured_output
                _, valid = _parse_structured_output(rec["output"])
                if not valid:
                    raise ValueError("C structured JSON invalid")
            if not rec.get("model_digest") or not rec.get("ollama_version") :
                raise ValueError(f"{task}/{condition}: model/runtime provenance required")

    if expected is not None and seen != set(expected):
        raise ValueError("Experiment task set incomplete")
    if len(provenance) != 1:
        raise ValueError("Model/runtime provenance differs across conditions")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", default="runtime/working/P4/artifacts.csv")
    ap.add_argument("--baseline", default="runtime/working/P5/baseline_findings.json")
    ap.add_argument("--config", default="configs/p6_p7_config.json")
    ap.add_argument("--tasks", default="configs/investigation_tasks.json")
    ap.add_argument("--experiment", default="runtime/working/P8/experiment_output.json")
    ap.add_argument("--run-log", default="runtime/working/P8/run_log.jsonl")
    ap.add_argument("--output", default="runtime/working/P8/p8_lock_manifest.json")
    args = ap.parse_args()

    out = Path(args.output)
    if out.exists():
        raise SystemExit("Refuse to overwrite an existing P8 lock; register a separate study.")
    try:
        validate_real_experiment(Path(args.experiment), Path(args.tasks), Path(args.config))
    except (ValueError, TypeError) as exc:
        raise SystemExit(f"Refuse P8 lock: {exc}") from exc
    files = {
        "p4_artifacts": item(Path(args.artifacts)),
        "p5_baseline": item(Path(args.baseline)),
        "p6_p7_config": item(Path(args.config)),
        "investigation_tasks": item(Path(args.tasks)),
        "p8_experiment_output": item(Path(args.experiment)),
        "p8_run_log": item(Path(args.run_log)),
    }
    manifest = {
        "status": "P8_OUTPUTS_LOCKED_BEFORE_GROUND_TRUTH",
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "rule": (
            "Do not overwrite these outputs after evaluator ground truth is opened. "
            "A rerun must receive a new RUN/lock manifest and be reported separately."
        ),
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
