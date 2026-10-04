#!/usr/bin/env python3
"""Summarize retrieval and local-LLM runtime from the append-only P8 run log."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def condition_name(row: dict) -> str:
    if row.get("structured"):
        return "C_llm_rag_structured"
    if row.get("retrieved_evidence_ids"):
        return "B_llm_rag"
    return "A_llm_only"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run-log", default="runtime/working/P8/run_log.jsonl")
    p.add_argument("--p5-timing", default="runtime/working/P5/p5_examiner_timing.json")
    p.add_argument("--output", default="runtime/working/P8/runtime_metrics.json")
    args = p.parse_args()

    lines = [
        json.loads(line) for line in Path(args.run_log).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not lines:
        raise SystemExit("P8 run log is empty.")

    retrieval = [r for r in lines if r.get("stage") == "retrieval"]
    llm = [r for r in lines if r.get("stage") == "llm_call" and not r.get("dry_run")]
    if not llm:
        raise SystemExit("No real local LLM calls found.")

    by_condition = defaultdict(lambda: {
        "calls": 0, "ollama_total_duration_seconds": 0.0,
        "prompt_tokens": 0, "generated_tokens": 0,
    })
    for row in llm:
        name = condition_name(row)
        rec = by_condition[name]
        rec["calls"] += 1
        meta = row.get("generation_metadata") or {}
        duration = meta.get("total_duration")
        if isinstance(duration, (int, float)):
            rec["ollama_total_duration_seconds"] += duration / 1_000_000_000
        rec["prompt_tokens"] += int(meta.get("prompt_eval_count") or 0)
        rec["generated_tokens"] += int(meta.get("eval_count") or 0)

    p5 = None
    p5_path = Path(args.p5_timing)
    if p5_path.is_file():
        p5 = json.loads(p5_path.read_text(encoding="utf-8"))

    result = {
        "schema_version": "libera-runtime-metrics-v1",
        "retrieval": {
            "calls": len(retrieval),
            "total_latency_seconds": round(sum(float(r.get("latency_seconds") or 0) for r in retrieval), 6),
            "mean_latency_seconds": round(
                sum(float(r.get("latency_seconds") or 0) for r in retrieval) / len(retrieval), 6
            ) if retrieval else None,
        },
        "local_llm": {
            "calls": len(llm),
            "conditions": {
                key: {
                    **value,
                    "ollama_total_duration_seconds": round(value["ollama_total_duration_seconds"], 6),
                }
                for key, value in sorted(by_condition.items())
            },
            "ollama_total_duration_seconds": round(
                sum(v["ollama_total_duration_seconds"] for v in by_condition.values()), 6
            ),
        },
        "p5_human_qc": p5,
        "interpretation": (
            "Durations describe this machine/run only. They are operational measurements, "
            "not proof that AI is faster than an examiner on complete casework."
        ),
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[RUNTIME] PASS -> {out}")


if __name__ == "__main__":
    main()
