"""Comprehensive read-only QA gate for the 10k LIBERA working corpus.

This script does not edit the corpus and does not declare semantic QA passed.
It complements audit_repetisi_corpus.py with provenance/source-line checks,
reply integrity, timestamp/window checks, participant consistency, leakage
signals, cadence signals, and long-message near-duplicate candidates.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adaptasi_indonesia"
WORK = DATA / "corpus_whatsapp_working.csv"
ANCHOR = DATA / "anchor_indonesia_500.csv"
OUT = DATA / "qa_final_gate_working.json"

EXPECTED_PROVENANCE = {
    "ADAPTED_FROM_GALLOWAY": 500,
    "SYNTHETIC_BRIDGE": 1500,
    "SYNTHETIC_CONTEXT": 6500,
    "SYNTHETIC_DISTRACTOR": 1500,
}
SCENARIO_START = datetime.fromisoformat("2026-07-01T00:00:00+07:00")
SCENARIO_END = datetime.fromisoformat("2026-07-21T23:59:59+07:00")
EXPECTED_OFFSET = timedelta(hours=7)

# These four mixed-pair conversations are inherited from the immutable anchor baseline.
ALLOWED_BASELINE_MIXED_CONVERSATIONS = {
    "KONV-GAL-P22-C",
    "KONV-GAL-R013",
    "KONV-GAL-R080",
    "KONV-GAL-R088",
}

# Original-source identity terms that must not leak into the localized investigator corpus.
SOURCE_LEAKAGE_TERMS = {
    "galloway",
    "cornelius galloway",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def parse_ts(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def normalize_text(text: str) -> str:
    tokens = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    return " ".join(tokens)


def simhash64(text: str) -> int:
    tokens = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    if not tokens:
        return 0
    shingles = [" ".join(tokens[i:i + 3]) for i in range(max(1, len(tokens) - 2))]
    vector = [0] * 64
    for shingle in shingles:
        digest = hashlib.blake2b(shingle.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        for bit in range(64):
            vector[bit] += 1 if (value >> bit) & 1 else -1
    out = 0
    for bit, score in enumerate(vector):
        if score >= 0:
            out |= 1 << bit
    return out


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def near_duplicate_candidates(rows: list[dict[str, str]], limit: int = 100) -> list[dict[str, object]]:
    candidates: list[tuple[int, str, str, int, int]] = []
    buckets: dict[tuple[int, int], list[tuple[str, int, int]]] = defaultdict(list)
    emitted_pairs: set[tuple[str, str]] = set()

    for row in rows:
        norm = normalize_text(row["message_text"])
        token_count = len(norm.split())
        if token_count < 8:
            continue
        sig = simhash64(norm)
        for band in range(4):
            key = (band, (sig >> (band * 16)) & 0xFFFF)
            for other_id, other_sig, other_len in buckets[key]:
                if abs(token_count - other_len) > 3:
                    continue
                pair = tuple(sorted((row["message_id"], other_id)))
                if pair in emitted_pairs:
                    continue
                dist = hamming(sig, other_sig)
                if dist <= 5:
                    emitted_pairs.add(pair)
                    candidates.append((dist, pair[0], pair[1], token_count, other_len))
            buckets[key].append((row["message_id"], sig, token_count))

    return [
        {
            "message_id_a": a,
            "message_id_b": b,
            "hamming_distance": dist,
            "token_count_a": len_a,
            "token_count_b": len_b,
        }
        for dist, a, b, len_a, len_b in sorted(candidates, key=lambda x: (x[0], x[1], x[2]))[:limit]
    ]

def main() -> None:
    messages = read_rows(WORK)
    anchors = read_rows(ANCHOR)
    anchor_by_id = {row["message_id"]: row for row in anchors}
    by_id = {row["message_id"]: row for row in messages}

    synthetic = [r for r in messages if r["source_provenance"] != "ADAPTED_FROM_GALLOWAY"]
    adapted = [r for r in messages if r["source_provenance"] == "ADAPTED_FROM_GALLOWAY"]

    provenance = Counter(r["source_provenance"] for r in messages)
    ids = Counter(r["message_id"] for r in messages)
    full_rows = Counter(tuple(r.items()) for r in messages)
    synthetic_texts = Counter(r["message_text"] for r in synthetic)
    conv_stamps = Counter((r["conversation_id"], r["timestamp"]) for r in messages)

    parsed: dict[str, datetime | None] = {r["message_id"]: parse_ts(r["timestamp"]) for r in messages}
    invalid_timestamp_ids = [mid for mid, dt in parsed.items() if dt is None]
    wrong_timezone_ids = [
        mid for mid, dt in parsed.items()
        if dt is not None and dt.utcoffset() != EXPECTED_OFFSET
    ]
    outside_window_ids = [
        mid for mid, dt in parsed.items()
        if dt is not None and not (SCENARIO_START <= dt <= SCENARIO_END)
    ]

    synthetic_source_line_nonempty = [
        r["message_id"] for r in synthetic if (r.get("source_original_line") or "").strip()
    ]

    anchor_exact = sum(anchor_by_id.get(r["message_id"]) == r for r in adapted)
    missing_anchor_ids = sorted(set(anchor_by_id) - {r["message_id"] for r in adapted})
    unexpected_adapted_ids = sorted({r["message_id"] for r in adapted} - set(anchor_by_id))

    reply_missing: list[str] = []
    reply_future: list[str] = []
    reply_cross_conversation: list[str] = []
    for row in messages:
        reply_id = (row.get("reply_to_message_id") or "").strip()
        if not reply_id:
            continue
        target = by_id.get(reply_id)
        if target is None:
            reply_missing.append(row["message_id"])
            continue
        if target["conversation_id"] != row["conversation_id"]:
            reply_cross_conversation.append(row["message_id"])
        cur_dt = parsed[row["message_id"]]
        target_dt = parsed[reply_id]
        if cur_dt is not None and target_dt is not None and target_dt > cur_dt:
            reply_future.append(row["message_id"])

    participants: dict[str, set[str]] = defaultdict(set)
    provenance_by_conversation: dict[str, set[str]] = defaultdict(set)
    for row in messages:
        participants[row["conversation_id"]].update((row["sender_id"], row["recipient_id"]))
        provenance_by_conversation[row["conversation_id"]].add(row["source_provenance"])

    mixed_conversation_flags = []
    for conv, actors in participants.items():
        if len(actors) <= 2 or conv in ALLOWED_BASELINE_MIXED_CONVERSATIONS:
            continue
        mixed_conversation_flags.append({
            "conversation_id": conv,
            "participant_count": len(actors),
            "participants": sorted(actors),
            "provenance": sorted(provenance_by_conversation[conv]),
        })

    leakage_hits = []
    for row in synthetic:
        lowered = row["message_text"].lower()
        hits = sorted(term for term in SOURCE_LEAKAGE_TERMS if term in lowered)
        if hits:
            leakage_hits.append({"message_id": row["message_id"], "terms": hits})

    by_context_conversation: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in synthetic:
        if row["conversation_id"].startswith("KONV-CTX-"):
            by_context_conversation[row["conversation_id"]].append(row)

    cadence_247 = 0
    cadence_examples = []
    for conv, thread in by_context_conversation.items():
        thread.sort(key=lambda r: ((parsed[r["message_id"]] or datetime.max.replace(tzinfo=timezone.utc)), r["message_id"]))
        for first, second in zip(thread, thread[1:]):
            a = parsed[first["message_id"]]
            b = parsed[second["message_id"]]
            if a is None or b is None:
                continue
            if (b - a).total_seconds() == 247:
                cadence_247 += 1
                if len(cadence_examples) < 25:
                    cadence_examples.append({
                        "conversation_id": conv,
                        "first_message_id": first["message_id"],
                        "second_message_id": second["message_id"],
                    })

    style = {}
    for label, prefix in (
        ("context_A", "ID-CTX-A-"),
        ("context_B", "ID-CTX-B-"),
        ("bridge", "ID-BRG-"),
        ("distractor", "ID-DST-"),
    ):
        subset = [r for r in synthetic if r["message_id"].startswith(prefix)]
        style[label] = {
            "messages": len(subset),
            "comma_phrase_ya_ending": sum(
                bool(re.search(r", [^,?.!]{1,25} ya[.!?]?$", r["message_text"], re.I))
                for r in subset
            ),
            "barusan_ending": sum(
                bool(re.search(r"\bbarusan[.!?]?$", r["message_text"], re.I))
                for r in subset
            ),
            "short_1_to_3_words": sum(len(re.findall(r"\w+", r["message_text"])) <= 3 for r in subset),
        }

    near_dups = near_duplicate_candidates(synthetic)

    automated_failures = {
        "total_is_10000": len(messages) == 10000,
        "provenance_matches_target": dict(provenance) == EXPECTED_PROVENANCE,
        "message_ids_unique": len(ids) == len(messages),
        "exact_duplicate_rows_zero": all(n == 1 for n in full_rows.values()),
        "synthetic_exact_duplicate_text_zero": all(n == 1 for n in synthetic_texts.values()),
        "synthetic_source_original_line_blank": len(synthetic_source_line_nonempty) == 0,
        "anchor_exact_500": anchor_exact == 500 and len(missing_anchor_ids) == 0 and len(unexpected_adapted_ids) == 0,
        "timestamps_parse": len(invalid_timestamp_ids) == 0,
        "timezone_plus_07": len(wrong_timezone_ids) == 0,
        "timestamps_in_scenario_window": len(outside_window_ids) == 0,
        "conversation_timestamp_collisions_zero": all(n == 1 for n in conv_stamps.values()),
        "reply_targets_exist": len(reply_missing) == 0,
        "reply_not_future": len(reply_future) == 0,
        "reply_same_conversation": len(reply_cross_conversation) == 0,
        "no_new_mixed_participant_conversations": len(mixed_conversation_flags) == 0,
        "source_identity_leakage_zero": len(leakage_hits) == 0,
    }

    report = {
        "automated_gate_passed": all(automated_failures.values()),
        "automated_checks": automated_failures,
        "total": len(messages),
        "provenance_counts": dict(provenance),
        "conversation_count": len(participants),
        "synthetic_source_original_line_nonempty_count": len(synthetic_source_line_nonempty),
        "synthetic_source_original_line_nonempty_examples": synthetic_source_line_nonempty[:25],
        "anchor_exact_match_count": anchor_exact,
        "missing_anchor_ids": missing_anchor_ids[:25],
        "unexpected_adapted_ids": unexpected_adapted_ids[:25],
        "invalid_timestamp_ids": invalid_timestamp_ids[:25],
        "wrong_timezone_ids": wrong_timezone_ids[:25],
        "outside_window_ids": outside_window_ids[:25],
        "reply_missing_target_ids": reply_missing[:25],
        "reply_future_ids": reply_future[:25],
        "reply_cross_conversation_ids": reply_cross_conversation[:25],
        "mixed_conversation_flags": mixed_conversation_flags[:25],
        "source_identity_leakage_hits": leakage_hits[:25],
        "context_gaps_exactly_247_seconds": cadence_247,
        "context_gap_247_examples": cadence_examples,
        "namespace_style_signals": style,
        "near_duplicate_long_candidates_count": len(near_dups),
        "near_duplicate_long_candidates": near_dups,
        "anchor_sha256": hashlib.sha256(ANCHOR.read_bytes()).hexdigest(),
        "working_sha256": hashlib.sha256(WORK.read_bytes()).hexdigest(),
        "manual_semantic_checks_required": [
            "review near-duplicate candidates in context",
            "full chronology/causality audit across anchor and synthetic messages",
            "full actor-state/location/knowledge audit across conversations",
            "language-naturalness review after context-B template repair",
            "reconcile historical combined-anchor manifest hash without modifying anchors",
        ],
        "final_signoff_allowed": False,
        "note": "Automated PASS is necessary but not sufficient. Final signoff requires manual semantic QA and explicit final artifact generation.",
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "automated_gate_passed": report["automated_gate_passed"],
        "total": report["total"],
        "synthetic_source_original_line_nonempty_count": report["synthetic_source_original_line_nonempty_count"],
        "context_gaps_exactly_247_seconds": report["context_gaps_exactly_247_seconds"],
        "near_duplicate_long_candidates_count": report["near_duplicate_long_candidates_count"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
