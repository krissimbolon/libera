"""P8 must not report success for transport or malformed-output failures."""
import json

import pytest

from src.ai_rag import ollama_runner, run_experiment


def test_timeout_is_logged(monkeypatch, tmp_path):
    monkeypatch.setattr(ollama_runner, "get_ollama_version", lambda host: "test")
    monkeypatch.setattr(ollama_runner, "get_model_digest", lambda host, model: "test")
    def timeout(*args, **kwargs):
        raise TimeoutError("timed out")
    monkeypatch.setattr(ollama_runner.urllib.request, "urlopen", timeout)
    log = tmp_path / "run.jsonl"
    rec = ollama_runner.run_once("test", run_log_path=log)
    assert "timed out" in rec["error"]
    assert json.loads(log.read_text())["error"] == rec["error"]


def test_transport_retry_preserves_first_success(monkeypatch):
    monkeypatch.setattr(run_experiment.time, "sleep", lambda seconds: None)
    attempts = iter([{"error": "timeout"}, {"error": None, "output": "answer"}])
    assert run_experiment.checked_call("T01 A", lambda: next(attempts))["output"] == "answer"


def test_exhausted_transport_retries_fail(monkeypatch):
    monkeypatch.setattr(run_experiment.time, "sleep", lambda seconds: None)
    with pytest.raises(ValueError, match="exhausted"):
        run_experiment.checked_call("T01 A", lambda: {"error": "timeout"}, retries=1)


@pytest.mark.parametrize("rec", [
    {"output": "", "error": None},
    {"output": "{", "structured": True, "error": None},
    {"output": "{}", "structured": True, "error": None},
    {"output": "partial", "error": None, "generation_metadata": {"done_reason": "length"}},
])
def test_invalid_output_fails_without_quality_retries(rec):
    calls = []
    def call():
        calls.append(1)
        return rec
    with pytest.raises(ValueError):
        run_experiment.checked_call("T01", call)
    assert len(calls) == 1


def test_audit_detects_task_and_retrieval_mismatch(tmp_path):
    from tools.audit_p8_run import audit, CONDITIONS
    obj = {key: "text" for key in ollama_runner.STRUCTURED_OUTPUT_SCHEMA["required"]}
    obj["relevant_evidence"] = []
    record = {"output": json.dumps(obj), "error": None, "dry_run": False,
              "model_digest": "test", "ollama_version": "test",
              "generation_metadata": {"done_reason": "stop"},
              "retrieved_evidence_ids": [], "retrieved_chunk_ids": []}
    row = {"task_id": "T01", "question": "test", **{key: dict(record) for key in CONDITIONS},
           "retrieval_trace": {"retrieved_evidence_ids": [], "retrieved_chunk_ids": []}}
    tasks = tmp_path / "tasks.json"
    tasks.write_text(json.dumps({"tasks": [{"task_id": "T01", "question": "test"}]}))
    output = tmp_path / "output.json"
    output.write_text(json.dumps([row]))
    assert audit(output, tasks)["status"] == "P8_EXECUTION_PASS"
    row["C_llm_rag_structured"]["retrieved_chunk_ids"] = ["different"]
    output.write_text(json.dumps([row]))
    assert audit(output, tasks)["status"] == "P8_EXECUTION_FAIL"
    output.write_text("[]")
    assert audit(output, tasks)["status"] == "P8_EXECUTION_FAIL"


def test_generate_sends_bounded_schema_and_records_stop_reason(monkeypatch):
    captured = {}
    def post(url, payload, timeout):
        captured.update(payload)
        return {"response": "{}", "done": True, "done_reason": "stop", "eval_count": 2}
    monkeypatch.setattr(ollama_runner, "_post", post)
    metadata = {}
    assert ollama_runner.call_generate("http://test", "test", "test", 0.1, 42, 8192,
                                       2048, 600, True, metadata) == "{}"
    assert captured["options"]["repeat_penalty"] == 1.2
    assert captured["options"]["repeat_last_n"] == 256
    assert captured["format"]["properties"]["confidence_uncertainty"]["maxLength"] == 120
    assert metadata["done_reason"] == "stop"
    assert metadata["eval_count"] == 2


def test_precheck_rejects_non_art_structured_references(tmp_path):
    from src.evaluation.evaluate_experiment import integrity_precheck
    obj = {key: "text" for key in ollama_runner.STRUCTURED_OUTPUT_SCHEMA["required"]}
    obj["relevant_evidence"] = ["ART-123", "a quote instead of an ID"]
    path = tmp_path / "output.json"
    path.write_text(json.dumps([{"C_llm_rag_structured": {"output": json.dumps(obj)}}]))
    check = integrity_precheck(path, {"ART-000123"})
    assert check["conditions"]["C_llm_rag_structured"]["invalid_citation_count"] == 2
