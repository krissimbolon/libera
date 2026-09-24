"""Read-only chat-level coherence audit for LIBERA 10k corpus.

This audit treats the forensic acquisition as one Raka-centric WhatsApp device.
Existing conversation_id values are preserved as scenario/event segments. A
derived dyadic chat_id groups all segments for the same participant pair so
that human reviewers can inspect how the corpus reads as an actual WhatsApp
chat timeline rather than isolated generated threads.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adaptasi_indonesia"
WORK = DATA / "corpus_whatsapp_working.csv"
OUT = DATA / "qa_chat_level_coherence.json"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def pair_key(row: dict[str, str]) -> tuple[str, str]:
    return tuple(sorted((row["sender_id"], row["recipient_id"])))


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def main() -> None:
    rows = read_rows(WORK)
    by_segment: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_pair: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    anchor_segments: set[str] = set()

    for row in rows:
        by_segment[row["conversation_id"]].append(row)
        by_pair[pair_key(row)].append(row)
        if row["source_provenance"] == "ADAPTED_FROM_GALLOWAY":
            anchor_segments.add(row["conversation_id"])

    segment_participants: dict[str, set[str]] = {}
    segment_intervals: dict[str, tuple[datetime, datetime]] = {}
    for segment_id, items in by_segment.items():
        actors: set[str] = set()
        times = [parse_ts(r["timestamp"]) for r in items]
        for row in items:
            actors.update((row["sender_id"], row["recipient_id"]))
        segment_participants[segment_id] = actors
        segment_intervals[segment_id] = (min(times), max(times))

    dyadic_segments = [
        sid for sid, actors in segment_participants.items() if len(actors) == 2
    ]
    multi_segments = [
        {
            "conversation_id": sid,
            "participants": sorted(actors),
            "messages": len(by_segment[sid]),
            "provenance": sorted({r["source_provenance"] for r in by_segment[sid]}),
        }
        for sid, actors in segment_participants.items()
        if len(actors) > 2
    ]

    raka_rows = [
        r for r in rows
        if "AKT-RAKA" in (r["sender_id"], r["recipient_id"])
    ]
    non_raka_rows = [
        r for r in rows
        if "AKT-RAKA" not in (r["sender_id"], r["recipient_id"])
    ]

    # Segment overlap within the same dyadic chat. These are candidates for
    # merged-chat human review, not automatic failures.
    overlaps: list[dict[str, object]] = []
    pair_segment_counts: dict[str, int] = {}

    for pair, items in by_pair.items():
        segments = sorted({r["conversation_id"] for r in items})
        pair_name = "|".join(pair)
        pair_segment_counts[pair_name] = len(segments)

        intervals = []
        for sid in segments:
            actors = segment_participants[sid]
            if len(actors) != 2:
                continue
            start, end = segment_intervals[sid]
            intervals.append((start, end, sid))

        intervals.sort()
        for i, (start_a, end_a, sid_a) in enumerate(intervals):
            for start_b, end_b, sid_b in intervals[i + 1:]:
                if start_b > end_a:
                    break
                overlaps.append({
                    "chat_pair": pair_name,
                    "segment_a": sid_a,
                    "segment_b": sid_b,
                    "start_a": start_a.isoformat(),
                    "end_a": end_a.isoformat(),
                    "start_b": start_b.isoformat(),
                    "end_b": end_b.isoformat(),
                })

    # Every synthetic bridge should live in a segment that also contains at
    # least one immutable anchor.
    bridge_without_anchor: list[str] = []
    for row in rows:
        if row["source_provenance"] != "SYNTHETIC_BRIDGE":
            continue
        if row["conversation_id"] not in anchor_segments:
            bridge_without_anchor.append(row["message_id"])

    # For each Raka dyad, verify the social relation exists in anchor evidence.
    raka_pairs = {
        pair for pair in by_pair
        if "AKT-RAKA" in pair
    }
    anchor_pairs = {
        pair_key(r) for r in rows
        if r["source_provenance"] == "ADAPTED_FROM_GALLOWAY"
    }
    synthetic_only_raka_pairs = sorted(
        "|".join(pair) for pair in raka_pairs if pair not in anchor_pairs
    )

    # Nearest-anchor distance for bridge messages in the same scenario segment.
    anchor_times_by_segment: dict[str, list[datetime]] = defaultdict(list)
    for row in rows:
        if row["source_provenance"] == "ADAPTED_FROM_GALLOWAY":
            anchor_times_by_segment[row["conversation_id"]].append(
                parse_ts(row["timestamp"])
            )

    bridge_distances: list[float] = []
    for row in rows:
        if row["source_provenance"] != "SYNTHETIC_BRIDGE":
            continue
        stamp = parse_ts(row["timestamp"])
        anchors = anchor_times_by_segment[row["conversation_id"]]
        bridge_distances.append(
            min(abs((stamp - anchor).total_seconds()) for anchor in anchors)
        )

    bridge_distances.sort()

    def percentile(p: float) -> float | None:
        if not bridge_distances:
            return None
        idx = int((len(bridge_distances) - 1) * p)
        return bridge_distances[idx]

    daily = Counter(r["timestamp"][:10] for r in rows)

    report = {
        "interpretation": (
            "Model the corpus as one Raka-centric WhatsApp acquisition containing "
            "multiple dyadic chats. Existing conversation_id values are scenario/"
            "event segmentation IDs, not physical WhatsApp chat IDs."
        ),
        "total_messages": len(rows),
        "time_span": {
            "first": min(r["timestamp"] for r in rows),
            "last": max(r["timestamp"] for r in rows),
            "days_with_messages": len(daily),
        },
        "segment_count": len(by_segment),
        "dyadic_segment_count": len(dyadic_segments),
        "multi_participant_segment_count": len(multi_segments),
        "multi_participant_segments": multi_segments,
        "unique_participant_pairs": len(by_pair),
        "raka_participant_pairs": len(raka_pairs),
        "messages_involving_raka": len(raka_rows),
        "messages_not_involving_raka": len(non_raka_rows),
        "non_raka_messages": [
            {
                "message_id": r["message_id"],
                "conversation_id": r["conversation_id"],
                "sender_id": r["sender_id"],
                "recipient_id": r["recipient_id"],
                "source_provenance": r["source_provenance"],
            }
            for r in non_raka_rows
        ],
        "synthetic_only_raka_pairs": synthetic_only_raka_pairs,
        "bridge_messages_without_anchor_segment": bridge_without_anchor,
        "bridge_nearest_anchor_seconds": {
            "median": percentile(0.50),
            "p75": percentile(0.75),
            "p90": percentile(0.90),
            "p95": percentile(0.95),
            "max": bridge_distances[-1] if bridge_distances else None,
            "within_5_minutes": sum(d <= 300 for d in bridge_distances),
            "within_30_minutes": sum(d <= 1800 for d in bridge_distances),
            "within_1_hour": sum(d <= 3600 for d in bridge_distances),
            "total_bridge_messages": len(bridge_distances),
        },
        "same_chat_segment_overlap_count": len(overlaps),
        "same_chat_segment_overlaps": overlaps,
        "segments_per_chat_pair": dict(
            sorted(pair_segment_counts.items(), key=lambda x: (-x[1], x[0]))
        ),
        "manual_review_required": [
            "Read merged timelines per participant pair, not only individual conversation_id segments.",
            "Review all same-chat overlapping segments for topic interleaving and continuity.",
            "Review Raka global chronology for impossible location/action overlap.",
            "Preserve immutable anchor content and ordering.",
            "Derive a stable chat_id per participant pair for forensic-demo/export layer while retaining conversation_id as segment_id.",
        ],
        "final_chat_level_signoff": False,
    }

    OUT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "total_messages": report["total_messages"],
        "unique_participant_pairs": report["unique_participant_pairs"],
        "messages_involving_raka": report["messages_involving_raka"],
        "synthetic_only_raka_pairs": len(synthetic_only_raka_pairs),
        "bridge_without_anchor": len(bridge_without_anchor),
        "same_chat_segment_overlap_count": len(overlaps),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
