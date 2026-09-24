"""Read-only P8 execution audit; never repairs or regenerates model answers."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CONDITIONS = ("A_llm_only", "B_llm_rag", "C_llm_rag_structured")
FIELDS = {"question", "relevant_evidence", "observed_facts",
          "possible_interpretation", "contradicting_evidence",
          "confidence_uncertainty", "finding"}


def audit(experiment: Path, tasks: Path) -> dict:
    rows = json.loads(experiment.read_text(encoding="utf-8"))
    expected = json.loads(tasks.read_text(encoding="utf-8"))["tasks"]
    errors, citation_findings, summary = [], [], []
    if [r["task_id"] for r in rows] != [t["task_id"] for t in expected]:
        errors.append("Task IDs/order differ from locked task file")
    questions = {t["task_id"]: t["question"] for t in expected}
    for row in rows:
        task = row["task_id"]
        if row["question"] != questions.get(task):
            errors.append(f"{task}: question mismatch")
        info = {"task_id": task}
        for condition in CONDITIONS:
            rec = row.get(condition) or {}
            output = rec.get("output", "")
            if rec.get("error") or not output.strip() or rec.get("dry_run") is not False:
                errors.append(f"{task}/{condition}: missing, failed, or dry-run output")
            if rec.get("generation_metadata", {}).get("done_reason") != "stop":
                errors.append(f"{task}/{condition}: generation did not stop normally")
            if not rec.get("model_digest") or not rec.get("ollama_version"):
                errors.append(f"{task}/{condition}: missing model provenance")
            ids = set(re.findall(r"ART-\d{6}", output))
            if condition == CONDITIONS[2]:
                try:
                    parsed = json.loads(output)
                    if isinstance(parsed, dict) and isinstance(parsed.get("relevant_evidence"), list):
                        ids |= {x for x in parsed["relevant_evidence"] if isinstance(x, str)}
                except ValueError:
                    pass
            supplied = set(rec.get("retrieved_evidence_ids", []))
            if ids - supplied:
                citation_findings.append({"task_id": task, "condition": condition,
                                          "cited_but_not_supplied": sorted(ids - supplied)})
            info[condition] = {"output_chars": len(output), "cited_ids": len(ids)}
            if condition == CONDITIONS[2]:
                try:
                    obj = json.loads(output)
                    valid = isinstance(obj, dict) and set(obj) == FIELDS
                    valid = valid and isinstance(obj["relevant_evidence"], list)
                    valid = valid and len(obj["relevant_evidence"]) <= 8
                    valid = valid and all(isinstance(x, str) for x in obj["relevant_evidence"])
                    valid = valid and all(isinstance(obj[k], str) for k in FIELDS - {"relevant_evidence"})
                    valid = valid and all(len(obj[k]) <= (120 if k == "confidence_uncertainty" else 240)
                                          for k in FIELDS - {"relevant_evidence"})
                except (ValueError, TypeError, KeyError):
                    valid = False
                info[condition]["schema_valid"] = valid
                if not valid:
                    errors.append(f"{task}/C: invalid schema")
        a, b, c = (row.get(k) or {} for k in CONDITIONS)
        if a.get("retrieved_evidence_ids") or a.get("retrieved_chunk_ids"):
            errors.append(f"{task}/A: unexpected supplied evidence")
        for key in ("retrieved_evidence_ids", "retrieved_chunk_ids"):
            if b.get(key) != c.get(key) or b.get(key) != row.get("retrieval_trace", {}).get(key):
                errors.append(f"{task}: B/C retrieval mismatch ({key})")
        summary.append(info)
    return {"status": "P8_EXECUTION_PASS" if not errors else "P8_EXECUTION_FAIL",
            "task_count": len(rows), "response_count": len(rows) * 3,
            "errors": errors, "citation_findings": citation_findings, "tasks": summary,
            "note": "Execution success is not accuracy. Citation findings are retained for evaluation; no answer was repaired."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True, type=Path)
    parser.add_argument("--tasks", default="configs/investigation_tasks.json", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = audit(args.experiment, args.tasks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{result['status']} tasks={result['task_count']} responses={result['response_count']} citation_findings={len(result['citation_findings'])}")
    raise SystemExit(bool(result["errors"]))
