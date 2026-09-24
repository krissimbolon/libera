"""Build a presentation-ready P10 run report from runtime manifests.

The report deliberately distinguishes controlled dry-run acquisition from a
real physical-device ACQ-001 so the presentation cannot accidentally overclaim.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def val(obj, key, default="NOT_RUN"):
    return obj.get(key, default) if obj else default


def main() -> None:
    p = argparse.ArgumentParser(description="Build P10 runtime report.")
    p.add_argument("--output", default="runtime/working/P10/run_report.md")
    args = p.parse_args()

    p3 = load_json(Path("runtime/private/ACQ-DRY-001/acquisition_manifest.json"))
    p4 = load_json(Path("runtime/working/P4/artifact_manifest.json"))
    p5 = load_json(Path("runtime/working/P5/baseline_manifest.json"))
    p9 = load_json(Path("runtime/working/P9/evaluation.json"))

    acquisition_label = (
        "REAL DEVICE"
        if val(p3, "is_real_device_acquisition", False)
        else "CONTROLLED DRY-RUN"
    )
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
        f"- Acquisition SHA-256: {val(p3, 'acquisition_sha256')}",
        "",
        "## P4 extraction",
        "",
        f"- Status: {val(p4, 'status')}",
        f"- Artifacts: **{val(p4, 'artifact_count')}**",
        f"- Merged chats: **{val(p4, 'chat_count')}**",
        f"- Source segments retained: **{val(p4, 'segment_count')}**",
        f"- Artifact CSV SHA-256: {val(p4, 'output_sha256')}",
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
        "- Local LLM: llama3.1:8b",
        "- Seed: 42; temperature: 0.1; prompt: v2-forensic-grounded",
        "- Conditions: A LLM-only; B LLM+RAG; C LLM+RAG+structured forensic output",
        "- AI case input: P4 ART evidence only; source reconstruction and ground truth prohibited",
        "",
        "## P9 evaluation",
        "",
        f"- Status: {val(p9, 'status')}",
    ]
    if p9 and p9.get("ground_truth_evaluation"):
        lines += [
            f"- Labeled messages: **{p9['ground_truth_evaluation']['labeled_rows']}**",
            f"- Key evidence messages: **{p9['ground_truth_evaluation']['key_evidence_rows']}**",
            "",
            "JSON metrics:",
            "",
            json.dumps(p9["ground_truth_evaluation"]["metrics"], indent=2),
        ]
    else:
        lines += [
            "- Final TP/FP/TN/FN requires evaluator-only private ground truth after P8 is locked.",
        ]

    if acquisition_label != "REAL DEVICE":
        lines += [
            "",
            "> PRESENTATION DISCLOSURE: P3 in this report is a controlled software dry-run,",
            "> not the final Oxygen/physical-device acquisition. Do not label it ACQ-001.",
        ]

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[P10] report written -> {out}")


if __name__ == "__main__":
    main()
