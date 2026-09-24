"""Scoring must preserve model errors without joining malformed IDs to evidence."""
import hashlib
import json

import pytest

from src.evaluation import citation_validation as citations
from src.evaluation import evaluate_experiment as evaluator


@pytest.fixture
def packet(tmp_path):
    artifacts = tmp_path / "artifacts.csv"
    artifacts.write_text("evidence_id,message_id\nART-000001,m1\nART-000002,m2\nART-000003,m3\n")
    structured = {key: "test" for key in (
        "question", "observed_facts", "possible_interpretation",
        "contradicting_evidence", "confidence_uncertainty", "finding")}
    structured["relevant_evidence"] = ["ART-000001", "ART-2", "quote", "ART-000003"]
    supplied = ["ART-000001", "ART-000002"]
    row = {"task_id": "T01", "question": "test",
           "retrieval_trace": {"retrieved_evidence_ids": supplied},
           "A_llm_only": {"output": "Insufficient evidence", "retrieved_evidence_ids": []},
           "B_llm_rag": {"output": "[ART-000001]", "retrieved_evidence_ids": supplied},
           "C_llm_rag_structured": {"output": json.dumps(structured), "retrieved_evidence_ids": supplied}}
    experiment = tmp_path / "experiment.json"
    experiment.write_text(json.dumps([row]))
    config = tmp_path / "config.json"
    config.write_text('{}')
    files = {}
    for key, path in [("p4_artifacts", artifacts), ("p8_experiment_output", experiment), ("config", config)]:
        files[key] = {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    lock = tmp_path / "p8_lock.json"
    lock.write_text(json.dumps({"status": "P8_OUTPUTS_LOCKED_BEFORE_GROUND_TRUTH", "files": files}))
    gt = tmp_path / "toy_labels.csv"
    gt.write_text("message_id,is_key_evidence\nm1,1\nm2,1\nm3,0\n")
    gt_lock = tmp_path / "toy_labels.csv.lock.json"
    gt_lock.write_text(json.dumps({"status": "PRIVATE_GROUND_TRUTH_LOCKED",
                                   "ground_truth_sha256": hashlib.sha256(gt.read_bytes()).hexdigest()}))
    return artifacts, experiment, lock, gt, config


def test_no_padding_quote_matching_or_out_of_context_credit(packet):
    artifacts, experiment, _, _, _ = packet
    before = experiment.read_bytes()
    result = citations.validate(experiment, {"ART-000001", "ART-000002", "ART-000003"})
    c = result["conditions"]["C_llm_rag_structured"]
    assert c["verified_unique_evidence_ids"] == ["ART-000001"]
    assert c["quarantined_reference_occurrences"] == 3
    assert c["reference_validity_rate"] == 0.25
    assert experiment.read_bytes() == before


def test_final_preserves_false_negatives_and_discloses_errors(packet, tmp_path):
    artifacts, experiment, lock, gt, _ = packet
    result = evaluator.run(artifacts, experiment, tmp_path / "evaluation.json",
                           ground_truth=gt, outputs_locked=True, lock_manifest=lock)
    assert result["status"] == "P9_FINAL_EVALUATION_COMPLETE_WITH_CITATION_ERRORS"
    assert result["precheck_status"] != "P9_PRECHECK_PASS"
    scores = result["ground_truth_evaluation"]["metrics"]["C_citations"]
    assert scores["labeled_universe"] == 3
    assert (scores["TP"], scores["FP"], scores["TN"], scores["FN"]) == (1, 0, 1, 1)
    assert scores["recall"] == 0.5
    assert "A_citations" in result["ground_truth_evaluation"]["metrics"]


def test_modified_auxiliary_input_blocks_before_gt(packet, tmp_path):
    artifacts, experiment, lock, gt, config = packet
    config.write_text('{"tampered":true}')
    gt.unlink()  # The lock failure must happen before trying to open labels.
    with pytest.raises(evaluator.EvaluationError, match="P8 lock mismatch"):
        evaluator.run(artifacts, experiment, tmp_path / "out.json",
                       ground_truth=gt, outputs_locked=True, lock_manifest=lock)


def test_modified_gt_cannot_be_scored(packet, tmp_path):
    artifacts, experiment, lock, gt, _ = packet
    gt.write_text("message_id,is_key_evidence\nm1,0\n")
    with pytest.raises(evaluator.EvaluationError, match="ground-truth lock mismatch"):
        evaluator.run(artifacts, experiment, tmp_path / "out.json",
                       ground_truth=gt, outputs_locked=True, lock_manifest=lock)


def test_precheck_verifies_all_locked_files_without_gt(packet, tmp_path):
    artifacts, experiment, lock, _, _ = packet
    result = evaluator.run(artifacts, experiment, tmp_path / "precheck.json",
                           outputs_locked=True, lock_manifest=lock)
    assert result["p8_lock_verification"]["verified_file_count"] == 3
    assert result["ground_truth_evaluation"] is None


def test_long_art_id_never_matches_valid_prefix():
    assert evaluator._extract_art_ids("ART-0000019 ART-000001suffix") == set()


def test_duplicate_gt_rejected(tmp_path):
    path = tmp_path / "labels.csv"
    path.write_text("message_id,is_key_evidence\nm1,1\nm1,0\n")
    with pytest.raises(evaluator.EvaluationError, match="duplicate"):
        evaluator.load_ground_truth(path, {"m1": "ART-000001"})


def test_cannot_write_evaluation_over_locked_experiment(packet):
    artifacts, experiment, lock, _, _ = packet
    with pytest.raises(evaluator.EvaluationError, match="overwrite"):
        evaluator.run(artifacts, experiment, experiment, outputs_locked=True, lock_manifest=lock)


def test_reconstructed_proxy_cannot_be_mislabeled_as_blind(packet, tmp_path):
    from tools.reconstruct_private_reference import ORIGIN, TARGET
    artifacts, experiment, lock, gt, _ = packet
    gt.write_text("message_id,is_key_evidence,label_origin,reference_target\n" +
                  "\n".join(f"m{i},{label},{ORIGIN},{TARGET}" for i, label in [(1,1),(2,1),(3,0)]) + "\n")
    gt_lock = gt.with_name(gt.name + ".lock.json")
    data = json.loads(gt_lock.read_text())
    data["ground_truth_sha256"] = hashlib.sha256(gt.read_bytes()).hexdigest()
    gt_lock.write_text(json.dumps(data))
    with pytest.raises(evaluator.EvaluationError, match="origin/target"):
        evaluator.run(artifacts, experiment, tmp_path / "wrong.json", ground_truth=gt,
                       outputs_locked=True, lock_manifest=lock)
    data.update(label_origin=ORIGIN, reference_target=TARGET)
    gt_lock.write_text(json.dumps(data))
    result = evaluator.run(artifacts, experiment, tmp_path / "proxy.json", ground_truth=gt,
                           outputs_locked=True, lock_manifest=lock)
    assert result["status"].startswith("P9_RECONSTRUCTED_PROXY_")
    assert result["ground_truth_evaluation"]["independent_ground_truth"] is False
    assert result["ground_truth_evaluation"]["reference_target"] == TARGET


def test_proxy_leaves_context_and_bridge_unlabeled():
    from tools.reconstruct_private_reference import label_for
    assert label_for("ADAPTED_FROM_GALLOWAY") == "1"
    assert label_for("SYNTHETIC_DISTRACTOR") == "0"
    assert label_for("SYNTHETIC_CONTEXT") == ""
    assert label_for("SYNTHETIC_BRIDGE") == ""
    with pytest.raises(ValueError):
        label_for("unknown")
