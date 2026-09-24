"""Build a presentation-ready P10 runtime report.

Acquisition modes are deliberately distinguished:
- ACQ-DRY-001: software-only integration dry-run;
- ACQ-SIM-001: controlled Android-emulator logical acquisition using ChatSim;
- ACQ-001: reserved for a separately documented real-device acquisition.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def val(obj, key, default="NOT_RUN"):
    return obj.get(key, default) if obj else default


def first_value(obj, *keys, default="NOT_RUN"):
    if not obj:
        return default
    for key in keys:
        value = obj.get(key)
        if value not in (None, ""):
            return value
    return default


def load_acquisition_manifest():
    candidates = [
        Path("runtime/working/current_acquisition_manifest.json"),
        Path("runtime/private/ACQ-SIM-001/acquisition_manifest.json"),
        Path("runtime/private/ACQ-001/acquisition_manifest.json"),
        Path("runtime/private/ACQ-DRY-001/acquisition_manifest.json"),
    ]
    for path in candidates:
        obj = load_json(path)
        if obj:
            return obj, path
    return None, None


def classify_acquisition(p3):
    if not p3:
        return "NOT_RUN", "No acquisition manifest available."
    if p3.get("is_real_device_acquisition") is True:
        return "REAL PHYSICAL DEVICE", (
            "A separately documented real-device acquisition. Report the exact "
            "tool/method actually used; do not infer full-file-system capability."
        )
    if p3.get("is_android_emulator_acquisition") is True or str(
        p3.get("acquisition_id", "")
    ).startswith("ACQ-SIM"):
        return "CONTROLLED ANDROID EMULATOR", (
            "Researcher-controlled LIBERA ChatSim logical app-private acquisition. "
            "ChatSim is not WhatsApp and this does not validate WhatsApp extraction."
        )
    return "CONTROLLED SOFTWARE DRY-RUN", (
        "Software integration dry-run only; not an Android or physical-device acquisition."
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Build P10 runtime report.")
    p.add_argument("--output", default="runtime/working/P10/run_report.md")
    p.add_argument("--acquisition-manifest")
    p.add_argument("--artifact-manifest", default="runtime/working/P4/artifact_manifest.json")
    p.add_argument("--evaluation", default="runtime/working/P9/evaluation.json")
    p.add_argument("--p8-lock", default="runtime/working/P8/p8_lock_manifest.json")
    p.add_argument("--config", default="configs/p6_p7_config.json")
    args = p.parse_args()

    if args.acquisition_manifest:
        p3_path = Path(args.acquisition_manifest)
        p3 = load_json(p3_path)
    else:
        p3, p3_path = load_acquisition_manifest()
    p4 = load_json(Path(args.artifact_manifest))
    p5 = load_json(Path("runtime/working/P5/baseline_manifest.json"))
    p9 = load_json(Path(args.evaluation))
    p8_lock = load_json(Path(args.p8_lock))
    config = load_json(Path(args.config)) or {}
    ai = config.get("ollama", {})
    prompt = config.get("prompt", {})

    acquisition_label, acquisition_disclosure = classify_acquisition(p3)
    acquisition_hash = first_value(
        p3, "acquisition_sha256", "master_sha256", default="NOT_RUN"
    )
    artifact_count = first_value(
        p4, "artifact_count", "normalized_artifact_count", "message_count"
    )
    artifact_hash = first_value(
        p4, "output_sha256", "normalized_artifacts_sha256"
    )
    segment_count = first_value(p4, "segment_count", default="N/A")

    lines = [
        "# LIBERA — P3–P10 Runtime Report",
        "",
        "Generated from local runtime artifacts. Frozen P2 is never modified.",
        "",
        "## P2 canonical input",
        "",
        "- Corpus: data/adaptasi_indonesia/corpus_whatsapp_10000.csv",
        "- SHA-256: a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6",
        "- Status: FROZEN_FOR_FORENSIC_SIMULATION",
        "",
        "## P3 acquisition",
        "",
        f"- Mode: **{acquisition_label}**",
        f"- Acquisition ID: {val(p3, 'acquisition_id')}",
        f"- Device ID: {val(p3, 'device_id')}",
        f"- Acquisition class: {first_value(p3, 'acquisition_class', 'acquisition_type')}",
        f"- Acquisition/master SHA-256: {acquisition_hash}",
        f"- Manifest: {p3_path if p3_path else 'NOT_RUN'}",
        f"- Disclosure: {acquisition_disclosure}",
        "",
        "## P4 extraction",
        "",
        f"- Status: {val(p4, 'status')}",
        f"- Artifacts: **{artifact_count}**",
        f"- Chats: **{val(p4, 'chat_count')}**",
        f"- Source segments retained: **{segment_count}**",
        f"- Artifact CSV SHA-256: {artifact_hash}",
        "",
        "## P5 traditional baseline",
        "",
        f"- Status: {val(p5, 'status')}",
        f"- Tasks: **{val(p5, 'task_count')}**",
        f"- Actors: **{val(p5, 'actor_count')}**",
        f"- Relationships: **{val(p5, 'relationship_count')}**",
        "",
        "## P6–P8 AI/RAG",
        "",
        "- Final embedding: bge-m3 via local Ollama",
        f"- Local LLM: {ai.get('model', 'NOT_RUN')}",
        f"- Seed: {ai.get('seed')}; temperature: {ai.get('temperature')}; prompt: {prompt.get('prompt_version')}",
        f"- Context: {ai.get('num_ctx')}; max output tokens: {ai.get('num_predict', 'unspecified')}",
        f"- Repeat penalty: {ai.get('repeat_penalty', 'default')}; repeat window: {ai.get('repeat_last_n', 'default')}",
        "- Conditions: A LLM-only; B LLM+RAG; C LLM+RAG+structured forensic output",
        "- AI case input: P4 ART evidence only; source reconstruction and ground truth prohibited",
        f"- P8 lock: {val(p8_lock, 'status')}",
        "",
        "## P9 evaluation",
        "",
        f"- Status: {val(p9, 'status')}",
    ]

    if p9 and p9.get("integrity"):
        lines += ["", "### Execution / citation precheck", "",
                  "| Condition | Outputs | Errors | Invalid ART citations | Valid structured JSON |",
                  "|---|---:|---:|---:|---:|"]
        for condition, metrics in p9["integrity"]["conditions"].items():
            lines.append(
                f"| {condition} | {metrics['outputs']} | {metrics['errors']} | "
                f"{metrics['invalid_citation_count']} | {metrics['structured_json_valid']} |"
            )
        lines += ["", "These checks do not establish factual correctness or final accuracy.", ""]

    if p9 and p9.get("citation_validation"):
        validation = p9["citation_validation"]
        lines += ["", "### Citation quarantine (original answers preserved)", "",
                  f"- Policy: {validation['policy_version']}",
                  f"- Status: {validation['status']}",
                  "- Only exact P4 IDs supplied to the condition can enter evidence scoring.",
                  "- Invalid references remain errors; they are never repaired, padded, or treated as evidence.",
                  "- Missing positive evidence remains eligible for FN; quarantine does not shrink the labeled universe.",
                  "", "| Condition | Reference occurrences | Accepted | Quarantined | Identifier validity |",
                  "|---|---:|---:|---:|---:|"]
        for condition, summary in validation["conditions"].items():
            rate = summary["reference_validity_rate"]
            rate_text = f"{rate:.2%}" if rate is not None else "N/A (no citations)"
            lines.append(f"| {condition} | {summary['attempted_reference_occurrences']} | "
                         f"{summary['accepted_reference_occurrences']} | "
                         f"{summary['quarantined_reference_occurrences']} | {rate_text} |")
        lines += ["", "Identifier validity is not semantic citation accuracy. Report these errors alongside any ground-truth metrics.", ""]

    if p9 and p9.get("ground_truth_evaluation"):
        gt = p9["ground_truth_evaluation"]
        lines += ["", "### Message-level metrics for the stated reference target", "",
                  "| Set | TP | FP | FN | TN | Precision | Recall | F1 | Predictions outside labeled universe |",
                  "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for name, metric in gt["metrics"].items():
            lines.append(f"| {name} | {metric['TP']} | {metric['FP']} | {metric['FN']} | {metric['TN']} | "
                         f"{metric['precision']} | {metric['recall']} | {metric['f1']} | "
                         f"{metric.get('predictions_outside_labeled_universe', 0)} |")
        lines += ["", "Zero-denominator metrics use the documented 0.0 convention; absent predictions do not establish accuracy.", ""]
        lines += [
            f"- Evaluation protocol: **{gt['protocol']}**",
            f"- Reference target: {gt.get('reference_target', 'message_level_key_evidence')}",
            f"- Labeled acquired messages: **{gt['labeled_rows']}**",
            f"- Reference positives: **{gt['key_evidence_rows']}**",
            f"- Unlabeled rows excluded: **{gt.get('ground_truth_rows_unlabeled', 0)}**",
            f"- Ground-truth rows not acquired: **{gt.get('ground_truth_rows_unacquired', 0)}**",
            "",
            "JSON metrics:",
            "",
            json.dumps(gt["metrics"], indent=2),
        ]
        if gt.get("independent_ground_truth") is False:
            lines[2:2] = ["**POST-HOC PROVENANCE PROXY REPORT — original human ground truth was lost. This is not a restored blind evaluation or semantic key-evidence accuracy report.**", ""]
            lines += ["", "**Reconstructed proxy evaluation only. Original human labels were lost. These metrics measure source-anchor versus designed-distractor discrimination on a partial universe, not forensic key-evidence accuracy. Independent semantic ground truth remains unavailable.**", ""]
    else:
        lines += [
            "- Final TP/FP/TN/FN requires evaluator-only private ground truth after P8 is cryptographically locked.",
        ]

    lines += [
        "",
        "## Acquisition disclosure for presentation",
        "",
        f"> {acquisition_disclosure}",
    ]

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[P10] report written -> {out}")


if __name__ == "__main__":
    main()
