"""P5 traditional forensic baseline: keyword search, timeline, entities, relations.

No LLM, embeddings, source reconstruction, or ground truth is used here.
The output is intentionally transparent and reproducible so it can serve as
the locked comparator required before P8/P9.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


class BaselineError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def load_artifacts(path: Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise BaselineError("Artifact CSV kosong.")
    required = {"evidence_id","message_id","conversation_id","sender","receiver",
                "timestamp_normalized","message_text"}
    missing = required - set(rows[0])
    if missing:
        raise BaselineError(f"Kolom artifact hilang: {sorted(missing)}")
    return rows


def load_tasks(path: Path) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["tasks"]


def keyword_score(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    low = text.casefold()
    hits = sorted({k for k in keywords if k.casefold() in low})
    return len(hits), hits


def run(artifact_csv: Path, tasks_json: Path, output_dir: Path, top_n: int = 20) -> dict:
    rows = load_artifacts(artifact_csv)
    tasks = load_tasks(tasks_json)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Timeline: examiner-visible, deterministic.
    timeline = sorted(rows, key=lambda r: (r["timestamp_normalized"], r["message_id"]))
    with (out / "timeline.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["timestamp_normalized","evidence_id","message_id","conversation_id",
                  "sender","receiver","message_text"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k:r[k] for k in fields} for r in timeline)

    # Actor frequency.
    actor_counts = Counter()
    for r in rows:
        actor_counts[r["sender"]] += 1
        actor_counts[r["receiver"]] += 1
    with (out / "entities.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["entity_id","message_participation_count"])
        w.writerows(actor_counts.most_common())

    # Pair relationships.
    relation_counts = Counter()
    for r in rows:
        relation_counts[tuple(sorted((r["sender"], r["receiver"])))] += 1
    with (out / "relationships.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["actor_a","actor_b","message_count"])
        for (a,b), n in relation_counts.most_common():
            w.writerow([a,b,n])

    findings = []
    for task in tasks:
        ranked = []
        for r in rows:
            score, hits = keyword_score(r["message_text"], task["keywords"])
            if score:
                ranked.append((score, r["timestamp_normalized"], r, hits))
        ranked.sort(key=lambda x: (-x[0], x[1], x[2]["message_id"]))
        selected = ranked[:top_n]
        findings.append({
            "finding_id": f"FND-P5-{task['task_id']}",
            "task_id": task["task_id"],
            "question": task["question"],
            "method": "deterministic_keyword_search",
            "keywords": task["keywords"],
            "candidate_count": len(ranked),
            "evidence": [
                {
                    "evidence_id": r["evidence_id"],
                    "message_id": r["message_id"],
                    "timestamp": r["timestamp_normalized"],
                    "sender": r["sender"],
                    "receiver": r["receiver"],
                    "matched_keywords": hits,
                    "score": score,
                    "text": r["message_text"],
                }
                for score, _, r, hits in selected
            ],
        })
    (out / "baseline_findings.json").write_text(
        json.dumps(findings, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "status": "P5_BASELINE_PASS",
        "artifact_input": str(artifact_csv),
        "artifact_sha256": sha256_file(artifact_csv),
        "task_file": str(tasks_json),
        "task_count": len(tasks),
        "message_count": len(rows),
        "actor_count": len(actor_counts),
        "relationship_count": len(relation_counts),
        "top_n_per_task": top_n,
        "method": "keyword+timeline+actor-frequency+pair-frequency",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (out / "baseline_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    p = argparse.ArgumentParser(description="Run P5 traditional baseline.")
    p.add_argument("--artifacts", default="runtime/working/P4/artifacts.csv")
    p.add_argument("--tasks", default="configs/investigation_tasks.json")
    p.add_argument("--output-dir", default="runtime/working/P5")
    p.add_argument("--top-n", type=int, default=20)
    args = p.parse_args()
    try:
        m = run(Path(args.artifacts), Path(args.tasks), Path(args.output_dir), args.top_n)
    except (BaselineError, FileNotFoundError) as exc:
        print(f"[P5] ERROR: {exc}")
        raise SystemExit(1)
    print("[P5] PASS")
    print(f"  messages={m['message_count']} tasks={m['task_count']} actors={m['actor_count']}")


if __name__ == "__main__":
    main()
