#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "data" / "adaptasi_indonesia" / "corpus_whatsapp_working.csv"
OUT_DIR = ROOT / "data" / "adaptasi_indonesia" / "review_packets"

RAKA = "AKT-RAKA"
STYLE_RE = re.compile(r",\s*[^,]{1,36}\s+ya[.!?…]*$", re.I)
BARUSAN_RE = re.compile(r"\bbarusan[.!?…]*$", re.I)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def dt(s: str) -> datetime:
    return datetime.fromisoformat(s)


def pair(row: dict[str, str]) -> tuple[str, str]:
    return tuple(sorted((row["sender_id"], row["recipient_id"])))


def write_jsonl(path: Path, items: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def compact(row: dict[str, str]) -> dict[str, str]:
    return {
        "message_id": row["message_id"],
        "conversation_id": row["conversation_id"],
        "timestamp": row["timestamp"],
        "sender_id": row["sender_id"],
        "recipient_id": row["recipient_id"],
        "message_text": row["message_text"],
        "source_provenance": row["source_provenance"],
        "reply_to_message_id": row.get("reply_to_message_id", ""),
    }


def context_for_pair(
    rows_by_pair: dict[tuple[str, str], list[dict[str, str]]],
    p: tuple[str, str],
    center: datetime,
    before: timedelta,
    after: timedelta,
) -> list[dict[str, str]]:
    lo, hi = center - before, center + after
    return [
        compact(r)
        for r in rows_by_pair[p]
        if lo <= dt(r["timestamp"]) <= hi
    ]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    args = ap.parse_args()

    corpus = Path(args.corpus)
    rows = read_rows(corpus)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows_sorted = sorted(rows, key=lambda r: (r["timestamp"], r["message_id"]))
    by_pair: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    by_conv: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows_sorted:
        by_pair[pair(r)].append(r)
        by_conv[r["conversation_id"]].append(r)

    # 1. Context-B style candidates with merged-chat context.
    language_packets: list[dict] = []
    for r in rows_sorted:
        if r["source_provenance"] != "SYNTHETIC_CONTEXT":
            continue
        if not r["message_id"].startswith("ID-CTX-B-"):
            continue
        text = r["message_text"].strip()
        reasons = []
        if STYLE_RE.search(text):
            reasons.append("comma_phrase_ya")
        if BARUSAN_RE.search(text):
            reasons.append("barusan_ending")
        if not reasons:
            continue
        center = dt(r["timestamp"])
        language_packets.append({
            "candidate_message_id": r["message_id"],
            "reasons": reasons,
            "chat_pair": "|".join(pair(r)),
            "segment_id": r["conversation_id"],
            "candidate": compact(r),
            "merged_chat_context_pm_15min": context_for_pair(
                by_pair, pair(r), center, timedelta(minutes=15), timedelta(minutes=15)
            ),
            "decision": "REVIEW",
            "repair_notes": "",
        })

    # 2. Overlapping segment intervals within same dyadic chat.
    intervals_by_pair: dict[tuple[str, str], list[tuple[datetime, datetime, str]]] = defaultdict(list)
    participants_by_conv: dict[str, set[str]] = {}
    for cid, items in by_conv.items():
        actors = set()
        times = []
        for r in items:
            actors.update([r["sender_id"], r["recipient_id"]])
            times.append(dt(r["timestamp"]))
        participants_by_conv[cid] = actors
        if len(actors) == 2:
            p = tuple(sorted(actors))
            intervals_by_pair[p].append((min(times), max(times), cid))

    overlap_packets: list[dict] = []
    seen = set()
    for p, intervals in intervals_by_pair.items():
        intervals.sort()
        for i, (sa, ea, ca) in enumerate(intervals):
            for sb, eb, cb in intervals[i + 1:]:
                if sb > ea:
                    break
                key = (p, ca, cb)
                if key in seen:
                    continue
                seen.add(key)
                lo = min(sa, sb) - timedelta(minutes=10)
                hi = max(ea, eb) + timedelta(minutes=10)
                merged = [
                    compact(r) for r in by_pair[p]
                    if lo <= dt(r["timestamp"]) <= hi
                ]
                overlap_packets.append({
                    "chat_pair": "|".join(p),
                    "segment_a": ca,
                    "segment_b": cb,
                    "segment_a_interval": [sa.isoformat(), ea.isoformat()],
                    "segment_b_interval": [sb.isoformat(), eb.isoformat()],
                    "merged_context_pm_10min": merged,
                    "decision": "REVIEW",
                    "repair_notes": "",
                })

    # 3. Every anchor with nearest 6 previous/6 next messages in the same real chat pair.
    anchor_packets: list[dict] = []
    pair_positions: dict[tuple[str, str], dict[str, int]] = {}
    for p, items in by_pair.items():
        pair_positions[p] = {r["message_id"]: i for i, r in enumerate(items)}

    for r in rows_sorted:
        if r["source_provenance"] != "ADAPTED_FROM_GALLOWAY":
            continue
        p = pair(r)
        items = by_pair[p]
        idx = pair_positions[p][r["message_id"]]
        lo, hi = max(0, idx - 6), min(len(items), idx + 7)
        anchor_packets.append({
            "anchor_message_id": r["message_id"],
            "chat_pair": "|".join(p),
            "anchor_segment_id": r["conversation_id"],
            "anchor": compact(r),
            "same_chat_neighbor_messages": [compact(x) for x in items[lo:hi]],
            "decision": "REVIEW",
            "semantic_checks": {
                "cause_effect_preserved": None,
                "knowledge_order_preserved": None,
                "outcome_not_premature": None,
                "actor_state_consistent": None,
            },
            "repair_notes": "",
        })

    # 4. Global actor concurrency: >=3 distinct segment IDs in any 15-min bucket.
    actor_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows_sorted:
        actor_rows[r["sender_id"]].append(r)

    concurrency_packets: list[dict] = []
    for actor, items in actor_rows.items():
        for i, r in enumerate(items):
            start = dt(r["timestamp"])
            end = start + timedelta(minutes=15)
            window = [x for x in items[i:] if dt(x["timestamp"]) <= end]
            segments = sorted({x["conversation_id"] for x in window})
            if len(segments) < 3:
                continue
            key = (actor, start.strftime("%Y-%m-%dT%H:%M"), tuple(segments))
            if any(
                p["actor_id"] == actor
                and p["window_start"] == start.isoformat()
                and p["segments"] == segments
                for p in concurrency_packets
            ):
                continue
            participants = sorted({
                a
                for x in window
                for a in (x["sender_id"], x["recipient_id"])
            })
            concurrency_packets.append({
                "actor_id": actor,
                "window_start": start.isoformat(),
                "window_end": end.isoformat(),
                "segments": segments,
                "participants": participants,
                "messages": [compact(x) for x in window],
                "decision": "REVIEW",
                "physical_state_conflict": None,
                "knowledge_conflict": None,
                "repair_notes": "",
            })

    write_jsonl(OUT_DIR / "language_candidates.jsonl", language_packets)
    write_jsonl(OUT_DIR / "merged_overlap_candidates.jsonl", overlap_packets)
    write_jsonl(OUT_DIR / "anchor_neighborhoods.jsonl", anchor_packets)
    write_jsonl(OUT_DIR / "actor_concurrency_candidates.jsonl", concurrency_packets)

    manifest = {
        "corpus": str(corpus),
        "counts": {
            "language_candidates": len(language_packets),
            "merged_overlap_candidates": len(overlap_packets),
            "anchor_neighborhoods": len(anchor_packets),
            "actor_concurrency_candidates": len(concurrency_packets),
        },
        "review_contract": {
            "language": "Review candidate in merged-chat context; repair only if formulaic or incoherent.",
            "overlap": "Read merged context as one WhatsApp chat; PASS, REPAIR, or SOURCE_ANOMALY.",
            "anchor": "Preserve anchor exactly; repair only synthetic neighbors if cause/state/knowledge/order is wrong.",
            "actor": "Simultaneous texting is allowed; flag only incompatible physical state/location/knowledge.",
        },
    }
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
