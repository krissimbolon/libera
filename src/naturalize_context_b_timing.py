"""Constrained conversational retiming proposal for synthetic Context B.

The model redistributes time *inside a contiguous run of a single scenario
segment in a merged WhatsApp chat*. Run endpoints, chat order, and the side of
every shared-actor anchor stay fixed. Gaps are weighted by sender turn-taking,
message length, and explicit search/interruption cues; no random jitter or
seed is used. The CSV corpus is changed only with --apply.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adaptasi_indonesia"
CORPUS = DATA / "corpus_whatsapp_working.csv"
LEDGER = DATA / "koreksi_waktu_berbasis_thread_001.tsv"
REPORT = DATA / "qa_cadence_proposal_working.json"
VERSION = "thread-weights-v1"


def pair(row: dict[str, str]) -> tuple[str, str]:
    return tuple(sorted((row["sender_id"], row["recipient_id"])))


def is_b(row: dict[str, str]) -> bool:
    return row["message_id"].startswith("ID-CTX-B-")


def stamp(row: dict[str, str]) -> datetime:
    return datetime.fromisoformat(row["timestamp"])


def gap_weight(first: dict[str, str], second: dict[str, str]) -> tuple[int, str]:
    """Use conversational actions, never the previous gap or a random number."""
    previous = first["message_text"].lower()
    current = second["message_text"].lower()
    words = len(re.findall(r"\w+", current))
    typing = min(len(current), 140)
    if first["sender_id"] == second["sender_id"]:
        value, cue = 12 + min(words, 25) * 2 + typing // 3, "double_text"
    else:
        value, cue = 43 + min(words, 25) * 7 + typing // 2, "reply"
    if first["message_text"].rstrip().endswith("?"):
        value = max(20, value - 18)
        cue += "+question"
    if re.search(r"\b(cek|cari|ambil|angkat|pindah|pasang|buka|bilas|lihat)\b", previous):
        value += 110
        cue += "+physical_check"
    if re.search(r"\b(tunggu|bentar|sebentar|nanti|balas dulu|pergi|jalan|sinyal)\b", previous):
        value += 170
        cue += "+interruption"
    if re.search(r"\b(ketemu|sudah|udah|oke|iya|sip)\b", current) and words <= 7:
        value = max(14, value - 26)
        cue += "+short_acknowledgment"
    if len(current) > 110:
        value += 75
        cue += "+long_text"
    return value, cue


def profile(rows: list[dict[str, str]]) -> dict[str, object]:
    by_conv: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if is_b(row):
            by_conv[row["conversation_id"]].append(row)
    gaps = Counter()
    for thread in by_conv.values():
        thread.sort(key=lambda r: r["timestamp"])
        for first, second in zip(thread, thread[1:]):
            gaps[int((stamp(second) - stamp(first)).total_seconds())] += 1
    total = sum(gaps.values())
    return {
        "gaps": total,
        "remainder_7": sum(v for seconds, v in gaps.items() if seconds % 60 == 7),
        "exact_247": gaps[247],
        "remainder_distribution": dict(sorted(Counter({
            rem: sum(count for sec, count in gaps.items() if sec % 60 == rem)
            for rem in range(60)
        }).items())),
        "top_exact_gaps": gaps.most_common(12),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    with CORPUS.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    before = profile(rows)
    original = {row["message_id"]: dict(row) for row in rows}
    anchor = [row for row in rows if row["source_provenance"] == "ADAPTED_FROM_GALLOWAY"]
    anchor_by_actor: dict[str, list[datetime]] = defaultdict(list)
    for row in anchor:
        for actor in {row["sender_id"], row["recipient_id"]}:
            anchor_by_actor[actor].append(stamp(row))
    for times in anchor_by_actor.values():
        times.sort()

    manual_conversations: set[str] = set()
    for path in DATA.glob("koreksi_waktu_manual_*.tsv"):
        with path.open(encoding="utf-8", newline="") as stream:
            manual_ids = {r["message_id"] for r in csv.DictReader(stream, delimiter="\t")}
        manual_conversations.update(
            r["conversation_id"] for r in rows if r["message_id"] in manual_ids and is_b(r)
        )

    by_pair: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_pair[pair(row)].append(row)
    changes = []
    blocks = 0
    for chat_pair, timeline in by_pair.items():
        timeline.sort(key=lambda row: (row["timestamp"], row["message_id"]))
        run: list[dict[str, str]] = []

        def close_run(reserve_end: bool) -> None:
            nonlocal blocks
            if len(run) < 2:
                return
            blocks += 1
            start = stamp(run[0]); end = stamp(run[-1])
            available = int((end - start).total_seconds())
            weighted = [gap_weight(a, b) for a, b in zip(run, run[1:])]
            total_weight = sum(value for value, _ in weighted)
            if available <= len(weighted) or total_weight == 0:
                return
            # Shorten the run to its conversational duration when there is
            # unused space before the next chat/anchor event. If the original
            # window is too tight, fit the weighted turns inside that window.
            # A different segment or an anchor immediately after this run can
            # depend on the original end of the exchange. Preserve that end
            # to avoid inventing an unexplained pause before the next topic.
            target_span = available if reserve_end else min(available, total_weight)
            elapsed_weight = 0
            for idx, row in enumerate(run[1:], 1):
                elapsed_weight += weighted[idx - 1][0]
                seconds = round(target_span * elapsed_weight / total_weight)
                proposed = start.timestamp() + seconds
                proposed_ts = datetime.fromtimestamp(proposed, tz=start.tzinfo).isoformat()
                if proposed_ts != row["timestamp"]:
                    changes.append({
                        "message_id": row["message_id"],
                        "conversation_id": row["conversation_id"],
                        "old_timestamp": row["timestamp"],
                        "new_timestamp": proposed_ts,
                        "before_gap_cue": weighted[idx - 1][1],
                        "model_version": VERSION,
                    })
                    row["timestamp"] = proposed_ts

        previous: dict[str, str] | None = None
        for row in timeline:
            allowed = is_b(row) and row["conversation_id"] not in manual_conversations
            same_segment = previous is not None and previous["conversation_id"] == row["conversation_id"]
            crossed_anchor = False
            if same_segment:
                lo, hi = sorted((stamp(previous), stamp(row)))
                crossed_anchor = any(
                    lo < moment <= hi
                    for actor in chat_pair
                    for moment in anchor_by_actor[actor]
                )
            crossed_day = same_segment and stamp(previous).date() != stamp(row).date()
            if not allowed or not same_segment or crossed_anchor or crossed_day:
                close_run(reserve_end=bool(run) and previous is not None)
                run = []
            if allowed:
                run.append(row)
            previous = row
        close_run(reserve_end=False)

    by_id = {row["message_id"]: row for row in rows}
    assert len(by_id) == len(rows) == 10000
    assert all(original[r["message_id"]] == r for r in anchor)
    for change in changes:
        old = original[change["message_id"]]
        old_time = stamp(old); new_time = stamp(by_id[change["message_id"]])
        assert old_time.date() == new_time.date()
        assert not any(
            min(old_time, new_time) < moment < max(old_time, new_time)
            for actor in {old["sender_id"], old["recipient_id"]}
            for moment in anchor_by_actor[actor]
        ), change["message_id"]
    for p, timeline in by_pair.items():
        old_ids = [r["message_id"] for r in sorted(timeline, key=lambda r: (original[r["message_id"]]["timestamp"], r["message_id"]))]
        new_ids = [r["message_id"] for r in sorted(timeline, key=lambda r: (r["timestamp"], r["message_id"]))]
        assert old_ids == new_ids, (p, "merged-chat order changed")
        assert len({r["timestamp"] for r in timeline}) == len(timeline), (p, "chat collision")
    for row in rows:
        reply = row["reply_to_message_id"]
        if reply:
            assert stamp(by_id[reply]) < stamp(row)

    after = profile(rows)
    report = {
        "version": VERSION,
        "mode": "applied" if args.apply else "dry_run",
        "thread_blocks_considered": blocks,
        "messages_changed": len(changes),
        "manual_thread_conversations_preserved": len(manual_conversations),
        "constraints": "merged-chat order, run endpoints, actor-anchor side, reply order, dates, chat uniqueness checked",
        "before": before,
        "after": after,
        "human_semantic_review_complete": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.apply:
        with CORPUS.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
        with LEDGER.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=changes[0], delimiter="\t", lineterminator="\n")
            writer.writeheader(); writer.writerows(changes)
    print(json.dumps({k: report[k] for k in ("mode", "thread_blocks_considered", "messages_changed", "before", "after")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
