"""Build and check the in-progress Indonesian LIBERA chat corpus.

The draft is hand-authored; this program does not generate message prose.
It refuses to overwrite the locked anchor or publish an incomplete final corpus.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from difflib import SequenceMatcher
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adaptasi_indonesia"
ANCHOR = DATA / "anchor_indonesia_500.csv"
DRAFT = DATA / "bridge_draft_001.tsv"
WORK = DATA / "corpus_whatsapp_working.csv"
QA = DATA / "qa_corpus_working.json"
# SHA of the actual committed anchor bytes on p2-10k-work. The older manifest
# records a different SHA; keep that provenance discrepancy visible in QA.
EXPECTED_ANCHOR_SHA = "12859745a88aecca306b9f149661361ec2b8da8cd1f7c41c70ead1329b3e5e50"
MANIFEST_ANCHOR_SHA = "63eeaac83bfd3b9145bbc1d99f3b7bfcce447face3f9cf7e20aa5231d55b0d24"
PROVENANCE_TARGET = {
    "ADAPTED_FROM_GALLOWAY": 500,
    "SYNTHETIC_BRIDGE": 1500,
    "SYNTHETIC_CONTEXT": 6500,
    "SYNTHETIC_DISTRACTOR": 1500,
}
LEAK = re.compile(
    r"\b(?:Cornelius|Galloway|Matthew Woods|Marcus Taylor|Danielle Galloway|"
    r"Albuquerque|Backpage|Howard Johnson|Motel 6|Staxx)\b", re.I
)


def read(path: Path, delimiter: str = ",") -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert digest(ANCHOR) == EXPECTED_ANCHOR_SHA, "Anchor byte hash changed"
    anchors = read(ANCHOR)
    coverage = {
        row["baris_exhibit1a"]: row["status_doc547"]
        for row in read(ROOT / "data" / "rekonstruksi" / "cakupan_baris_document_547_aman.csv")
    }
    assert all(coverage.get(row["source_original_line"], "").startswith("TERPETAKAN_") for row in anchors)
    draft = read(DRAFT, "\t")
    assert len(anchors) == 500 and len(draft) > 0
    fields = list(anchors[0])
    pairs: dict[str, set[frozenset[str]]] = defaultdict(set)
    for row in anchors:
        pairs[row["conversation_id"]].add(
            frozenset((row["sender_id"], row["recipient_id"]))
        )
    mixed_baseline = {k: len(v) for k, v in pairs.items() if len(v) > 1}
    messages = anchors.copy()
    for number, item in enumerate(draft, 1):
        conversation = item["conversation_id"]
        sender = item["sender_id"]
        assert conversation in pairs, (number, conversation)
        assert len(pairs[conversation]) == 1, (number, "mixed legacy thread")
        pair = next(iter(pairs[conversation]))
        assert sender in pair, (number, "sender outside conversation")
        recipient = next(x for x in pair if x != sender)
        assert len(item["message_text"].strip()) > 2, number
        datetime.fromisoformat(item["timestamp"])
        messages.append(dict.fromkeys(fields, "") | {
            "message_id": f"ID-BRG-{number:04d}",
            "conversation_id": conversation,
            "timestamp": item["timestamp"],
            "sender_id": sender,
            "recipient_id": recipient,
            "message_text": item["message_text"].strip(),
            "message_type": "text",
            "source_provenance": "SYNTHETIC_BRIDGE",
        })

    messages.sort(key=lambda x: (x["timestamp"], x["message_id"]))
    ids = Counter(x["message_id"] for x in messages)
    duplicate_ids = sum(n - 1 for n in ids.values() if n > 1)
    synthetic = [x for x in messages if x["source_provenance"] != "ADAPTED_FROM_GALLOWAY"]
    texts = Counter(x["message_text"] for x in synthetic)
    duplicate_texts = sum(n - 1 for n in texts.values() if n > 1)
    conversation_times: dict[str, set[str]] = defaultdict(set)
    time_collisions = []
    for row in messages:
        key = row["conversation_id"]
        if row["timestamp"] in conversation_times[key]:
            time_collisions.append((key, row["timestamp"]))
        conversation_times[key].add(row["timestamp"])
    assert not duplicate_ids and not duplicate_texts and not time_collisions
    assert not any(LEAK.search(r["message_text"]) for r in synthetic)
    assert all(not r["source_original_line"] and not r["transformation_id"] for r in synthetic)
    # Compare each full anchor row; sorted working order may differ from source order.
    anchor_by_id = {r["message_id"]: r for r in anchors}
    assert {r["message_id"]: r for r in messages if r["message_id"] in anchor_by_id} == anchor_by_id
    assert all(set(row) == set(fields) for row in messages)
    near_pairs = []
    for i, left in enumerate(synthetic):
        if len(left["message_text"]) < 35:
            continue
        for right in synthetic[i + 1:]:
            if len(right["message_text"]) < 35:
                continue
            score = SequenceMatcher(None, left["message_text"].lower(), right["message_text"].lower()).ratio()
            if score >= 0.86:
                near_pairs.append((left["message_id"], right["message_id"], round(score, 3)))

    with WORK.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(messages)
    counts = Counter(r["source_provenance"] for r in messages)
    qa = {
        "status": "DRAFT_INCOMPLETE",
        "total": len(messages),
        "target": 10000,
        "provenance_counts": {k: counts[k] for k in PROVENANCE_TARGET},
        "provenance_targets": PROVENANCE_TARGET,
        "conversation_count": len({r["conversation_id"] for r in messages}),
        "anchor_sha256": digest(ANCHOR),
        "manifest_anchor_sha256": MANIFEST_ANCHOR_SHA,
        "manifest_hash_matches_committed_anchor": digest(ANCHOR) == MANIFEST_ANCHOR_SHA,
        "working_sha256": digest(WORK),
        "anchor_row_exact_match": True,
        "duplicate_message_ids": duplicate_ids,
        "duplicate_synthetic_text": duplicate_texts,
        "same_conversation_timestamp_collisions": time_collisions,
        "baseline_mixed_anchor_conversations": mixed_baseline,
        "new_mixed_conversations": 0,
        "source_identity_leak_in_new_messages": 0,
        "near_duplicate_long_text_candidates": near_pairs,
        "manual_continuity_review": "Draft 001 replayed with adjacent anchors; later drafts and full actor-state audit pending.",
    }
    QA.write_text(json.dumps(qa, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(qa, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
