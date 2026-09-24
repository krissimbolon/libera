"""P8 A/B/C experiment harness.

A: local LLM only, deliberately receives no case evidence. This is a lower
   bound for unsupported-case hallucination/abstention.
B: local LLM + RAG with full retrieved chunk text and evidence IDs.
C: same retrieval as B + locked structured forensic answer schema.

B and C run the same query and retrieval configuration. Outputs are locked
before evaluator ground truth is opened.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import ollama_runner
from .retriever import RetrieverError, load_index, query_index
from .run_log import utc_now_iso


def load_questions(path: Path) -> List[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "tasks" in data:
        return [{"task_id": t["task_id"], "question": t["question"]} for t in data["tasks"]]
    qs = data.get("questions", data)
    if isinstance(qs, list) and qs and isinstance(qs[0], str):
        return [{"task_id": f"T{i:02d}", "question": q} for i, q in enumerate(qs, 1)]
    return qs


def run_condition_a(question: str, args: argparse.Namespace) -> Dict[str, Any]:
    return ollama_runner.run_once(
        query=question, model=args.model, prompt_version=args.prompt_version,
        temperature=args.temperature, seed=args.seed, host=args.host,
        structured=False, dry_run=args.dry_run,
        run_log_path=Path(args.run_log), num_ctx=args.num_ctx,
        num_predict=getattr(args, "num_predict", ollama_runner.DEFAULT_NUM_PREDICT),
        timeout=getattr(args, "timeout", ollama_runner.DEFAULT_TIMEOUT_SECONDS),
    )


def _retrieve(question: str, index: Dict[str, Any], args: argparse.Namespace):
    return query_index(
        index, question, k=args.top_k, run_log_path=Path(args.run_log)
    )


def _rag_call(question: str, retrieval: dict, args: argparse.Namespace, structured: bool):
    results = retrieval["results"]
    return ollama_runner.run_once(
        query=question,
        model=args.model,
        prompt_version=args.prompt_version,
        temperature=args.temperature,
        seed=args.seed,
        host=args.host,
        retrieved_chunk_ids=[r["chunk_id"] for r in results],
        retrieved_evidence_ids=sorted({
            eid for r in results for eid in r["evidence_ids"] if eid
        }),
        retrieved_texts=[r["text"] for r in results],
        structured=structured,
        dry_run=args.dry_run,
        run_log_path=Path(args.run_log),
        num_ctx=args.num_ctx,
        num_predict=getattr(args, "num_predict", ollama_runner.DEFAULT_NUM_PREDICT),
        timeout=getattr(args, "timeout", ollama_runner.DEFAULT_TIMEOUT_SECONDS),
    )


def checked_call(label, call, retries=2):
    """Retry transport errors only; retain every attempt in the append-only log."""
    for attempt in range(retries + 1):
        print(f"[P8] {label} attempt={attempt + 1}", flush=True)
        record = call()
        if not record.get("error"):
            if record.get("generation_metadata", {}).get("done_reason") == "length":
                raise ValueError(f"{label}: output truncated at token limit")
            if not record.get("output", "").strip():
                raise ValueError(f"{label}: empty model output")
            if record.get("structured"):
                obj = json.loads(record["output"])
                schema = ollama_runner.STRUCTURED_OUTPUT_SCHEMA
                if not isinstance(obj, dict) or set(obj) != set(schema["required"]):
                    raise ValueError(f"{label}: invalid structured fields")
                ids = obj["relevant_evidence"]
                if not isinstance(ids, list) or len(ids) > 8 or not all(isinstance(x, str) for x in ids):
                    raise ValueError(f"{label}: invalid relevant_evidence")
                if not all(isinstance(obj[k], str) for k in obj if k != "relevant_evidence"):
                    raise ValueError(f"{label}: invalid structured field types")
                if not record.get("dry_run") and any(
                    len(obj[k]) > schema["properties"][k]["maxLength"]
                    for k in obj if k != "relevant_evidence"
                ):
                    raise ValueError(f"{label}: structured field exceeds maximum length")
            return record
        print(f"[P8] {label} ERROR {record['error']}", flush=True)
        if attempt < retries:
            time.sleep(3)
    raise ValueError(f"{label}: transport retries exhausted; see run log")


def save_checkpoint(results, output):
    path = Path(output).with_suffix(".partial.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run_all_conditions(
    questions: List[dict],
    index_path: Optional[Path],
    args: argparse.Namespace,
) -> List[Dict[str, Any]]:
    index = None
    if index_path:
        index = load_index(index_path)
    results = []
    retries = getattr(args, "retries", 2)
    for item in questions:
        q = item["question"]
        row: Dict[str, Any] = {
            "task_id": item.get("task_id"),
            "question": q,
            "timestamp": utc_now_iso(),
            "A_llm_only": checked_call(f"{item.get('task_id')} A", lambda: run_condition_a(q, args), retries),
        }
        if index is None:
            row["B_llm_rag"] = None
            row["C_llm_rag_structured"] = None
        else:
            # One locked retrieval shared by B and C for a fair comparison.
            retrieval = _retrieve(q, index, args)
            row["retrieval_trace"] = retrieval["query_log"]
            row["B_llm_rag"] = checked_call(f"{item.get('task_id')} B", lambda: _rag_call(q, retrieval, args, False), retries)
            row["C_llm_rag_structured"] = checked_call(f"{item.get('task_id')} C", lambda: _rag_call(q, retrieval, args, True), retries)
        results.append(row)
        if getattr(args, "output", None):
            save_checkpoint(results, args.output)
        print(f"[P8] COMPLETE {item.get('task_id')} ({len(results)}/{len(questions)})", flush=True)
    return results


def main() -> None:
    p = argparse.ArgumentParser(description="P8 locked A/B/C experiment.")
    p.add_argument("--index", default=None)
    p.add_argument("--questions", default="configs/investigation_tasks.json")
    p.add_argument("--output", default="runtime/working/P8/experiment_output.json")
    p.add_argument("--model", default=ollama_runner.DEFAULT_MODEL)
    p.add_argument("--prompt-version", default="v2-forensic-grounded")
    p.add_argument("--temperature", type=float, default=ollama_runner.DEFAULT_TEMPERATURE)
    p.add_argument("--seed", type=int, default=ollama_runner.DEFAULT_SEED)
    p.add_argument("--num-ctx", type=int, default=ollama_runner.DEFAULT_NUM_CTX)
    p.add_argument("--num-predict", type=int, default=ollama_runner.DEFAULT_NUM_PREDICT)
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--retries", type=int, default=2)
    p.add_argument("--host", default=ollama_runner.DEFAULT_HOST)
    p.add_argument("--top-k", type=int, default=8)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--run-log", default="runtime/working/P8/run_log.jsonl")
    args = p.parse_args()
    try:
        if Path(args.output).exists() or Path(args.output).with_name("p8_lock_manifest.json").exists():
            raise ValueError("Refuse to overwrite existing experiment/lock; use a new output directory.")
        questions = load_questions(Path(args.questions))
        index = Path(args.index) if args.index else None
        results = run_all_conditions(questions, index, args)
    except (RetrieverError, OSError, ValueError) as exc:
        print(f"[P8] ERROR: {exc}")
        raise SystemExit(1)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[P8] PASS tasks={len(results)} dry_run={args.dry_run} "
        f"model={args.model} output={out}"
    )


if __name__ == "__main__":
    main()
