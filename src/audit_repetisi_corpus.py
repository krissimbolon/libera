"""Flag repeated prose in the 10k working corpus before final QA signoff."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adaptasi_indonesia"
WORK = DATA / "corpus_whatsapp_working.csv"
ANCHOR = DATA / "anchor_indonesia_500.csv"
REPORT = DATA / "qa_repetisi_corpus_working.json"
WORK_QA = DATA / "qa_corpus_working.json"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def ending(text: str) -> str:
    return " ".join(re.findall(r"\w+", text.lower())[-2:])


def main() -> None:
    messages = rows(WORK)
    anchor = {row["message_id"]: row for row in rows(ANCHOR)}
    synthetic = [r for r in messages if r["source_provenance"] != "ADAPTED_FROM_GALLOWAY"]
    by_conversation: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in synthetic:
        by_conversation[row["conversation_id"]].append(row)

    windows = []
    for conversation, thread in by_conversation.items():
        thread.sort(key=lambda row: (row["timestamp"], row["message_id"]))
        for start in range(len(thread) - 3):
            group = thread[start : start + 4]
            suffixes = {ending(row["message_text"]) for row in group}
            if len(suffixes) == 1:
                windows.append({
                    "conversation_id": conversation,
                    "first_message_id": group[0]["message_id"],
                    "last_message_id": group[-1]["message_id"],
                    "repeated_suffix": next(iter(suffixes)),
                })

    namespaces = {}
    for label, prefix in (("context_A", "ID-CTX-A-"), ("context_B", "ID-CTX-B-"),
                          ("bridge", "ID-BRG-"), ("distractor", "ID-DST-")):
        subset = [r for r in synthetic if r["message_id"].startswith(prefix)]
        namespaces[label] = {
            "messages": len(subset),
            "comma_phrase_ya_ending": sum(bool(re.search(r", [^,?.!]{1,25} ya[.!?]?$", r["message_text"], re.I)) for r in subset),
            "barusan_ending": sum(bool(re.search(r"\bbarusan[.!?]?$", r["message_text"], re.I)) for r in subset),
        }

    ids = Counter(row["message_id"] for row in messages)
    texts = Counter(row["message_text"] for row in synthetic)
    counts = Counter(row["source_provenance"] for row in messages)
    full_rows = Counter(tuple(row.items()) for row in messages)
    stamps = Counter((row["conversation_id"], row["timestamp"]) for row in messages)
    report = {
        "status": "FAILED_LANGUAGE_CONTINUITY_QA",
        "total": len(messages),
        "provenance_counts": dict(counts),
        "unique_message_ids": len(ids),
        "duplicate_message_ids": len(messages) - len(ids),
        "exact_duplicate_rows": sum(n - 1 for n in full_rows.values() if n > 1),
        "duplicate_synthetic_text": sum(n - 1 for n in texts.values() if n > 1),
        "same_conversation_timestamp_collisions": sum(n - 1 for n in stamps.values() if n > 1),
        "conversation_count": len({row["conversation_id"] for row in messages}),
        "anchor_exact_match_count": sum(row == anchor.get(row["message_id"]) for row in messages if row["message_id"] in anchor),
        "anchor_sha256": hashlib.sha256(ANCHOR.read_bytes()).hexdigest(),
        "working_sha256": hashlib.sha256(WORK.read_bytes()).hexdigest(),
        "repeated_four_message_suffix_windows": len(windows),
        "affected_conversations": len({r["conversation_id"] for r in windows}),
        "examples": windows[:20],
        "namespace_style_signals": namespaces,
        "manual_decision": "Corpus berjumlah tepat 10.000 tetapi pengulangan dalam satu thread merusak dialog natural. Jangan terbitkan sebagai final sebelum diperbaiki dan diaudit ulang.",
        "remaining_checks": ["near-duplicate panjang pada snapshot ini", "chronology dan actor-state menyeluruh", "hash manifest jangkar lama"],
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    WORK_QA.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{report['status']}: {len(messages)} rows, {len(windows)} repeated windows in {report['affected_conversations']} conversations")


if __name__ == "__main__":
    main()
