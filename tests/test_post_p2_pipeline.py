"""Regression tests for the post-P2 integration path."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from src.forensics import acquisition_simulator, extract_artifacts
from src.baseline import traditional_baseline
from src.ai_rag import chunker, retriever, run_experiment, ollama_runner
from src.evaluation import evaluate_experiment


ROOT = Path(__file__).resolve().parents[1]


def test_frozen_corpus_sha256_is_immutable():
    corpus = ROOT / "data/adaptasi_indonesia/corpus_whatsapp_10000.csv"
    assert acquisition_simulator.sha256_file(corpus) == acquisition_simulator.CANONICAL_SHA256


def test_end_to_end_post_p2_dry_run(tmp_path):
    corpus = ROOT / "data/adaptasi_indonesia/corpus_whatsapp_10000.csv"
    db = tmp_path / "ACQ-DRY-001.sqlite"
    acq_manifest = tmp_path / "acquisition_manifest.json"
    p3 = acquisition_simulator.run(corpus, db, acq_manifest)
    assert p3["source_row_count"] == 10000
    assert p3["is_real_device_acquisition"] is False

    artifacts = tmp_path / "artifacts.csv"
    art_manifest = tmp_path / "artifact_manifest.json"
    p4 = extract_artifacts.run(db, artifacts, art_manifest)
    assert p4["artifact_count"] == 10000
    assert p4["chat_count"] == 26

    with artifacts.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = set(reader.fieldnames or [])
    assert len(rows) == 10000
    assert "source_provenance" not in fields
    assert "source_original_line" not in fields
    assert "is_key_evidence" not in fields
    assert len({r["artifact_id"] for r in rows}) == 10000

    p5_dir = tmp_path / "P5"
    p5 = traditional_baseline.run(
        artifacts,
        ROOT / "configs/investigation_tasks.json",
        p5_dir,
        top_n=20,
    )
    assert p5["status"] == "P5_BASELINE_PASS"
    assert p5["task_count"] == 10

    chunks_path = tmp_path / "chunks.jsonl"
    chunks = chunker.run(
        artifacts, chunks_path, min_size=30, max_size=60, time_window_minutes=120
    )
    assert chunks
    assert all(c["evidence_ids"] for c in chunks)

    index_path = tmp_path / "index.json"
    index = retriever.build_index(
        chunks_path, "case_evidence", index_path, embedding_method="hashing"
    )
    assert index["entries"]
    assert index["embedding_method"] == "hashing"

    args = argparse.Namespace(
        model=ollama_runner.DEFAULT_MODEL,
        prompt_version="v2-forensic-grounded",
        temperature=0.1,
        seed=42,
        host=ollama_runner.DEFAULT_HOST,
        dry_run=True,
        run_log=str(tmp_path / "run_log.jsonl"),
        num_ctx=8192,
        top_k=8,
    )
    questions = run_experiment.load_questions(ROOT / "configs/investigation_tasks.json")
    output = run_experiment.run_all_conditions(questions, index_path, args)
    assert len(output) == 10
    experiment_path = tmp_path / "experiment_output.json"
    experiment_path.write_text(json.dumps(output, ensure_ascii=False), encoding="utf-8")

    p9 = evaluate_experiment.run(
        artifacts,
        experiment_path,
        tmp_path / "evaluation.json",
        p5_dir / "baseline_findings.json",
    )
    assert p9["status"] == "P9_PRECHECK_PASS"
    assert p9["integrity"]["retrieval_invalid_evidence_ids"] == []
    assert p9["integrity"]["conditions"]["C_llm_rag_structured"]["structured_json_valid"] == 10


def test_confusion_metrics():
    labeled = {"ART-000001", "ART-000002", "ART-000003", "ART-000004"}
    positive = {"ART-000001", "ART-000002"}
    predicted = {"ART-000001", "ART-000003"}
    m = evaluate_experiment._confusion(predicted, labeled, positive)
    assert (m["TP"], m["FP"], m["FN"], m["TN"]) == (1, 1, 1, 1)
    assert m["precision"] == 0.5
    assert m["recall"] == 0.5
