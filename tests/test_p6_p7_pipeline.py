"""
test_p6_p7_pipeline.py - Test dasar pipeline P6/P7 (LIBERA).

Semua test berjalan TANPA Ollama (memakai mode dry-run / data toy) agar
bisa dijalankan siapa saja di tim tanpa setup tambahan.

Jalankan dengan:
    python -m pytest tests/test_p6_p7_pipeline.py -v
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Tambahkan root repo ke sys.path supaya `from src.ai_rag import ...` bekerja
# baik dijalankan dari root repo maupun langsung sebagai file test.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ai_rag import chunker, leakage_check, ollama_runner, retriever, validate_output  # noqa: E402

TOY_CSV = ROOT / "data" / "toy" / "toy_case_evidence.csv"


@pytest.fixture()
def tmp_paths(tmp_path):
    return {
        "chunks": tmp_path / "chunks.jsonl",
        "index": tmp_path / "index.json",
        "run_log": tmp_path / "run_log.jsonl",
    }


def test_toy_dataset_exists_and_has_required_columns():
    assert TOY_CSV.exists(), "Toy dataset harus ada untuk test ini berjalan"
    rows = chunker.load_messages(TOY_CSV)
    assert len(rows) >= 8, "Toy dataset harus punya minimal 8 pesan (sesuai instruksi praktikum)"
    assert len(rows) <= 20, "Toy dataset sebaiknya tetap kecil untuk testing"


def test_chunker_produces_chunks_with_provenance(tmp_paths):
    chunks = chunker.run(TOY_CSV, tmp_paths["chunks"], min_size=30, max_size=60)
    assert len(chunks) > 0
    for c in chunks:
        assert "chunk_id" in c and c["chunk_id"].startswith("CHK-")
        assert "content_hash_sha256" in c
        assert "message_ids" in c and len(c["message_ids"]) > 0
        # Toy dataset lebih kecil dari target 30-60 -> wajar below_target_size True
        assert c["below_target_size"] is True


def test_leakage_check_flags_banned_terms(tmp_path):
    bad_file = tmp_path / "bad.jsonl"
    bad_file.write_text(
        json.dumps({"text": "Ini mengutip Document 547 secara langsung"}) + "\n",
        encoding="utf-8",
    )
    matches = leakage_check.scan_file(bad_file, leakage_check.DEFAULT_BANNED_TERMS)
    assert "Document 547" in matches


def test_leakage_check_passes_clean_file(tmp_paths):
    chunker.run(TOY_CSV, tmp_paths["chunks"], min_size=30, max_size=60)
    matches = leakage_check.scan_file(tmp_paths["chunks"], leakage_check.DEFAULT_BANNED_TERMS)
    assert matches == [], f"Toy chunks seharusnya bersih dari penanda terlarang, ditemukan: {matches}"


def test_retriever_build_and_query_roundtrip(tmp_paths):
    chunker.run(TOY_CSV, tmp_paths["chunks"], min_size=30, max_size=60)
    index = retriever.build_index(tmp_paths["chunks"], "case_evidence", tmp_paths["index"])
    assert len(index["entries"]) > 0

    loaded = retriever.load_index(tmp_paths["index"])
    out = retriever.query_index(loaded, "ruang C3", k=3, run_log_path=tmp_paths["run_log"])
    assert len(out["results"]) <= 3
    assert tmp_paths["run_log"].exists()

    with tmp_paths["run_log"].open("r", encoding="utf-8") as f:
        logged = [json.loads(line) for line in f]
    assert len(logged) == 1
    assert logged[0]["stage"] == "retrieval"
    assert logged[0]["query"] == "ruang C3"


def test_ollama_runner_dry_run_does_not_need_network(tmp_paths):
    record = ollama_runner.run_once(
        query="Apa yang terjadi di ruang C3?",
        prompt_version="v1",
        dry_run=True,
        structured=True,
        run_log_path=tmp_paths["run_log"],
    )
    assert record["dry_run"] is True
    assert record["error"] is None
    assert record["run_id"].startswith("RUN-")

    parsed_output = json.loads(record["output"])
    validate_output.validate_structured_finding(parsed_output)  # tidak boleh raise


def test_validate_output_rejects_missing_fields():
    incomplete = {"question": "test"}
    with pytest.raises(validate_output.ValidationError):
        validate_output.validate_structured_finding(incomplete)


def test_validate_output_rejects_ground_truth_leakage():
    finding = {
        "question": "test",
        "relevant_evidence": [],
        "observed_facts": "x",
        "possible_interpretation": "x",
        "contradicting_evidence": "x",
        "confidence_uncertainty": "x",
        "finding": "x",
        "evidence_strength": "high",  # field Ground Truth - dilarang
    }
    with pytest.raises(validate_output.ValidationError):
        validate_output.validate_structured_finding(finding)


def test_end_to_end_dry_run_condition_b(tmp_paths):
    """Simulasi ringkas kondisi B (LLM+RAG) tanpa Ollama sungguhan."""
    chunker.run(TOY_CSV, tmp_paths["chunks"], min_size=30, max_size=60)
    index = retriever.build_index(tmp_paths["chunks"], "case_evidence", tmp_paths["index"])

    retrieval = retriever.query_index(index, "siapa yang masuk ruang C3", k=2, run_log_path=tmp_paths["run_log"])
    chunk_ids = [r["chunk_id"] for r in retrieval["results"]]
    evidence_ids = sorted({eid for r in retrieval["results"] for eid in r["evidence_ids"]})

    record = ollama_runner.run_once(
        query="siapa yang masuk ruang C3",
        retrieved_chunk_ids=chunk_ids,
        retrieved_evidence_ids=evidence_ids,
        retrieved_texts=[r["text_preview"] for r in retrieval["results"]],
        structured=False,
        dry_run=True,
        run_log_path=tmp_paths["run_log"],
    )
    assert record["retrieved_chunk_ids"] == chunk_ids
    assert record["dry_run"] is True
