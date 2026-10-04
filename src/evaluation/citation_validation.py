"""Strict, ground-truth-independent citation quarantine for locked outputs.

Never rewrite a model response, pad an ID, or infer an ID from quoted text.
Only exact P4 identifiers supplied to that condition can enter evidence scoring.
Rejected references remain visible as model errors, not silently discarded.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

POLICY_VERSION = "p9-strict-citation-quarantine-v1"
CONDITIONS = ("A_llm_only", "B_llm_rag", "C_llm_rag_structured")
ART_TOKEN = re.compile(r"(?<![\w-])ART-[\w-]+")
EXACT_ART = re.compile(r"ART-[0-9]{6}")


def candidates(record: dict, structured: bool) -> list:
    if not structured:
        return ART_TOKEN.findall(record.get("output", ""))
    # The contracted prediction field is relevant_evidence. Narrative mentions
    # must not silently replace rejected IDs in that field.
    try:
        obj = json.loads(record.get("output", ""))
    except (ValueError, TypeError):
        return []
    refs = obj.get("relevant_evidence") if isinstance(obj, dict) else None
    return refs if isinstance(refs, list) else []


def validate(experiment: Path, artifact_ids: set[str]) -> dict:
    rows = json.loads(experiment.read_text(encoding="utf-8"))
    details, summaries = [], {}
    for condition in CONDITIONS:
        valid_ids, rejected_values = set(), set()
        attempted = accepted = 0
        affected_tasks, without_citations = [], []
        for row in rows:
            record = row.get(condition) or {}
            supplied = set(record.get("retrieved_evidence_ids", []))
            trace = set(row.get("retrieval_trace", {}).get("retrieved_evidence_ids", []))
            # A has no evidence by design. B/C must agree with their trace.
            allowed = (supplied & trace) if condition != CONDITIONS[0] else set()
            valid, rejected = [], []
            for raw in candidates(record, condition == CONDITIONS[2]):
                attempted += 1
                if not isinstance(raw, str) or not EXACT_ART.fullmatch(raw):
                    reason = "INVALID_IDENTIFIER_FORMAT"
                elif raw not in artifact_ids:
                    reason = "NOT_IN_P4"
                elif raw not in allowed:
                    reason = "NOT_SUPPLIED_TO_CONDITION"
                else:
                    reason = None
                if reason:
                    rejected.append({"raw_reference": raw, "reason": reason})
                    rejected_values.add(json.dumps(raw, ensure_ascii=False, sort_keys=True))
                else:
                    accepted += 1
                    valid.append(raw)
                    valid_ids.add(raw)
            if rejected:
                affected_tasks.append(row["task_id"])
            if not valid:
                without_citations.append(row["task_id"])
            details.append({"task_id": row["task_id"], "condition": condition,
                            "run_id": record.get("run_id"),
                            "verified_evidence_ids": sorted(set(valid)),
                            "quarantined_references": rejected})
        summaries[condition] = {
            "attempted_reference_occurrences": attempted,
            "accepted_reference_occurrences": accepted,
            "quarantined_reference_occurrences": attempted - accepted,
            "quarantined_unique_references": len(rejected_values),
            "reference_validity_rate": round(accepted / attempted, 6) if attempted else None,
            "verified_unique_evidence_ids": sorted(valid_ids),
            "tasks_with_quarantined_references": affected_tasks,
            "tasks_without_verified_citations": without_citations,
        }
    rejected = sum(s["quarantined_reference_occurrences"] for s in summaries.values())
    return {
        "policy_version": POLICY_VERSION,
        "status": "READY_WITH_QUARANTINED_REFERENCES" if rejected else "CITATIONS_VALID",
        "experiment_sha256": hashlib.sha256(experiment.read_bytes()).hexdigest(),
        "policy": "Exact P4 ID and supplied-to-condition membership required; no padding, quote matching, or output rewriting.",
        "interpretation": "Verified citations are not proof of factual correctness. Quarantined references remain model errors and must accompany any message-level metrics.",
        "conditions": summaries, "records": details,
    }


def prediction_sets(validation: dict) -> dict[str, set[str]]:
    return {
        condition[0] + "_citations": set(summary["verified_unique_evidence_ids"])
        for condition, summary in validation["conditions"].items()
    }
