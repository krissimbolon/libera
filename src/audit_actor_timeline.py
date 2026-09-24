"""Candidate report for a human chronology and actor-state review.

Time proximity is only a review signal: several brief chats in a minute can be
plausible. This report never declares chronology or actor-state to have passed.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adaptasi_indonesia"
CORPUS = DATA / "corpus_whatsapp_working.csv"
OUTPUT = DATA / "qa_actor_timeline_working.json"
GLOBAL_SIGNOFF = ROOT / "docs" / "02_case_design" / "qa_global_actor_state_final.md"
ACTORS = (
    "AKT-RAKA", "AKT-KIRANA", "AKT-TANIA", "AKT-MAYA", "AKT-RENA",
    "AKT-NARA", "AKT-JIHAN", "AKT-DINI", "AKT-REZA", "AKT-BAGAS",
    "AKT-CACA",
)
CACA_BLOCK = datetime.fromisoformat("2026-07-19T15:06:00+07:00")


def main() -> None:
    with CORPUS.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    messages_by_actor: dict[str, list[dict[str, str]]] = defaultdict(list)
    minute_by_actor: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in rows:
        sender = row["sender_id"]
        if sender in ACTORS:
            messages_by_actor[sender].append(row)
            minute_by_actor[sender][row["timestamp"][:16]].append(row)

    rapid_conversation_candidates = []
    for actor in ACTORS:
        for minute, same_minute in minute_by_actor[actor].items():
            conversations = {row["conversation_id"] for row in same_minute}
            if len(conversations) >= 3:
                rapid_conversation_candidates.append({
                    "actor": actor,
                    "minute": minute,
                    "conversation_count": len(conversations),
                    "message_ids": [row["message_id"] for row in same_minute],
                    "conversations": sorted(conversations),
                })

    post_block = [
        row["message_id"] for row in rows
        if "AKT-CACA" in (row["sender_id"], row["recipient_id"])
        and datetime.fromisoformat(row["timestamp"]) > CACA_BLOCK
    ]
    by_id = {row["message_id"]: row for row in rows}
    anchor = [row for row in rows if row["source_provenance"] == "ADAPTED_FROM_GALLOWAY"]
    exact_across_chats: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for actor in ACTORS:
        for row in messages_by_actor[actor]:
            exact_across_chats[(actor, row["timestamp"])].append(row)
    exact_cross_conversation_candidates = [
        {"actor": actor, "timestamp": stamp,
         "message_ids": [row["message_id"] for row in same_instant]}
        for (actor, stamp), same_instant in sorted(exact_across_chats.items())
        if len({row["conversation_id"] for row in same_instant}) > 1
    ]

    moved_across_actor_anchor = []
    for corrections in sorted(DATA.glob("koreksi_waktu_manual_*.tsv")):
        with corrections.open(encoding="utf-8", newline="") as stream:
            for change in csv.DictReader(stream, delimiter="\t"):
                row = by_id[change["message_id"]]
                old = datetime.fromisoformat(change["old_timestamp"])
                new = datetime.fromisoformat(change["new_timestamp"])
                people = {row["sender_id"], row["recipient_id"]}
                for fixed in anchor:
                    if people.intersection((fixed["sender_id"], fixed["recipient_id"])):
                        when = datetime.fromisoformat(fixed["timestamp"])
                        if min(old, new) < when < max(old, new):
                            moved_across_actor_anchor.append({
                                "message_id": change["message_id"],
                                "anchor_id": fixed["message_id"],
                            })

    human_signoff = (
        GLOBAL_SIGNOFF.exists()
        and "GLOBAL_ACTOR_STATE_PASS = true" in GLOBAL_SIGNOFF.read_text(encoding="utf-8")
    )
    report = {
        "scope": "candidate signals plus documented human global actor-state sign-off",
        "chronology_state_passed": human_signoff,
        "actor_message_counts": {
            actor: len(messages_by_actor[actor]) for actor in ACTORS
        },
        "rapid_three_plus_conversations_same_minute": sorted(
            rapid_conversation_candidates,
            key=lambda candidate: (candidate["minute"], candidate["actor"]),
        ),
        "rapid_conversation_counts_by_actor": dict(Counter(
            candidate["actor"] for candidate in rapid_conversation_candidates
        )),
        "caca_messages_after_block": post_block,
        "exact_same_actor_cross_conversation_timestamp": exact_cross_conversation_candidates,
        "timestamp_corrections_crossing_shared_actor_anchor": moved_across_actor_anchor,
        "human_signoff_document": str(GLOBAL_SIGNOFF.relative_to(ROOT)) if human_signoff else None,
        "human_checks_pending": [] if human_signoff else [
            "all actors: mutually exclusive locations, sleep, travel and pickup",
            "knowledge and outcomes relative to anchors across conversations",
            "Raka multitasking and physical activities in nearby conversations",
            "Jihan language sanitation and scene chronology",
            "synthetic bridge causal ordering and representative thread spot-check",
        ],
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "chronology_state_passed": human_signoff,
        "rapid_candidates": len(rapid_conversation_candidates),
        "by_actor": report["rapid_conversation_counts_by_actor"],
        "post_caca_block": len(post_block),
        "exact_cross_chat_actor_collisions": len(exact_cross_conversation_candidates),
        "corrections_crossing_actor_anchor": len(moved_across_actor_anchor),
    }))


if __name__ == "__main__":
    main()
