import csv
import hashlib
import json
import sys

from src.evaluation import runtime_metrics, score_postlock_review
from src.evaluation.postlock_review import ensure_locked_extra


def test_locked_extra_requires_matching_hash(tmp_path):
    index = tmp_path / "index.json"
    index.write_text('{"entries":[]}', encoding="utf-8")
    lock = tmp_path / "lock.json"
    lock.write_text(json.dumps({
        "files": {
            "extra_01": {
                "path": str(index),
                "sha256": hashlib.sha256(index.read_bytes()).hexdigest(),
            }
        }
    }), encoding="utf-8")
    ensure_locked_extra(lock, index)
    index.write_text('{"entries":[1]}', encoding="utf-8")
    try:
        ensure_locked_extra(lock, index)
    except SystemExit:
        pass
    else:
        raise AssertionError("changed post-lock source must be refused")


def test_runtime_metrics_reads_powershell_bom_timing(tmp_path, monkeypatch):
    run_log = tmp_path / "run.jsonl"
    rows = [
        {"stage": "retrieval", "latency_seconds": 0.5},
        {
            "stage": "llm_call", "dry_run": False, "structured": False,
            "retrieved_evidence_ids": [],
            "generation_metadata": {
                "total_duration": 2_000_000_000,
                "prompt_eval_count": 10, "eval_count": 5,
            },
        },
        {
            "stage": "llm_call", "dry_run": False, "structured": True,
            "retrieved_evidence_ids": ["ART-000001"],
            "generation_metadata": {
                "total_duration": 3_000_000_000,
                "prompt_eval_count": 20, "eval_count": 7,
            },
        },
    ]
    run_log.write_text("\n".join(json.dumps(x) for x in rows), encoding="utf-8")
    timing = tmp_path / "timing.json"
    timing.write_text(json.dumps({"elapsed_seconds": 12.5}), encoding="utf-8-sig")
    output = tmp_path / "metrics.json"
    monkeypatch.setattr(sys, "argv", [
        "runtime_metrics", "--run-log", str(run_log),
        "--p5-timing", str(timing), "--output", str(output),
    ])
    runtime_metrics.main()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["retrieval"]["total_latency_seconds"] == 0.5
    assert data["local_llm"]["ollama_total_duration_seconds"] == 5.0
    assert data["p5_human_qc"]["elapsed_seconds"] == 12.5


def test_score_postlock_review_separates_retrieval_and_claim_metrics(tmp_path, monkeypatch):
    root = tmp_path / "review"
    root.mkdir()
    retrieval = root / "retrieval_relevance_review.csv"
    with retrieval.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "task_id", "question", "rank", "chunk_id", "similarity_score",
            "chunk_text", "relevance_grade_0_2", "reviewer_note",
        ])
        w.writeheader()
        w.writerow({"task_id":"T01","question":"q","rank":"1","chunk_id":"C1",
                    "similarity_score":"0.9","chunk_text":"x","relevance_grade_0_2":"2","reviewer_note":""})
        w.writerow({"task_id":"T01","question":"q","rank":"2","chunk_id":"C2",
                    "similarity_score":"0.8","chunk_text":"y","relevance_grade_0_2":"0","reviewer_note":""})

    claims = root / "claim_supportedness_review.csv"
    fields = [
        "task_id", "condition", "question", "model_output", "verified_evidence_ids",
        "cited_evidence_text", "support_label", "task_completion_0_2",
        "factual_consistency_0_2", "evidentiary_support_0_2",
        "uncertainty_handling_0_2", "reviewer_note",
    ]
    with claims.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for condition, label in [("B_llm_rag","SUPPORTED"),("C_llm_rag_structured","PARTIAL")]:
            w.writerow({
                "task_id":"T01","condition":condition,"question":"q","model_output":"a",
                "verified_evidence_ids":"ART-000001","cited_evidence_text":"e",
                "support_label":label,"task_completion_0_2":"2",
                "factual_consistency_0_2":"2","evidentiary_support_0_2":"2",
                "uncertainty_handling_0_2":"1","reviewer_note":"",
            })

    output = tmp_path / "review_metrics.json"
    monkeypatch.setattr(sys, "argv", [
        "score_postlock_review", "--review-dir", str(root), "--output", str(output),
    ])
    score_postlock_review.main()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["retrieval"]["mean_P@8"] == 0.5
    assert data["retrieval"]["Recall@8"] is None
    assert data["claim_supportedness"]["supported_or_partial_rate"] == 1.0
