#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

RAKA = "AKT-RAKA"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_actor_names(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as f:
        return {r["actor_id"]: r["nama_adaptasi"] for r in csv.DictReader(f)}

def choose_corpus(root: Path, explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = root / p
        return p
    candidates = [
        root / "data/adaptasi_indonesia/corpus_whatsapp_10000.csv",
        root / "data/adaptasi_indonesia/corpus_whatsapp_working.csv",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("No final/working LIBERA corpus found.")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--out-dir", default="apps/libera-chatsim/app/src/main/assets")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    corpus = choose_corpus(root, args.corpus)
    actors = read_actor_names(root / "data/adaptasi_indonesia/registri_aktor_indonesia.csv")

    out_dir = root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    seed_path = out_dir / "messages_seed.jsonl"
    anomaly_path = out_dir / "source_anomalies.jsonl"
    manifest_path = out_dir / "seed_manifest.json"

    device_rows = 0
    anomaly_rows = 0
    chat_ids: set[str] = set()
    first_ts: str | None = None
    last_ts: str | None = None

    with corpus.open(encoding="utf-8", newline="") as src,          seed_path.open("w", encoding="utf-8", newline="\n") as seed,          anomaly_path.open("w", encoding="utf-8", newline="\n") as anomalies:
        for row in csv.DictReader(src):
            sender = row["sender_id"]
            recipient = row["recipient_id"]
            ts = row["timestamp"]
            first_ts = ts if first_ts is None or ts < first_ts else first_ts
            last_ts = ts if last_ts is None or ts > last_ts else last_ts

            if RAKA not in (sender, recipient):
                anomaly_rows += 1
                anomalies.write(json.dumps({
                    "message_id": row["message_id"],
                    "conversation_id": row["conversation_id"],
                    "timestamp": ts,
                    "sender_id": sender,
                    "recipient_id": recipient,
                    "message_text": row["message_text"],
                    "reason": "Neither sender nor recipient is AKT-RAKA; excluded from DEV-001 direct-chat seed pending provenance review."
                }, ensure_ascii=False) + "\n")
                continue

            peer = recipient if sender == RAKA else sender
            chat_id = f"CHAT-{peer}"
            chat_ids.add(chat_id)
            device_rows += 1

            # Deliberately exclude evaluator-only construction labels:
            # source_provenance, source_original_line, transformation_id.
            seed.write(json.dumps({
                "message_id": row["message_id"],
                "chat_id": chat_id,
                "segment_id": row["conversation_id"],
                "timestamp": ts,
                "sender_id": sender,
                "recipient_id": recipient,
                "sender_name": actors.get(sender, sender.replace("AKT-", "")),
                "recipient_name": actors.get(recipient, recipient.replace("AKT-", "")),
                "peer_id": peer,
                "peer_name": actors.get(peer, peer.replace("AKT-", "")),
                "message_text": row["message_text"],
                "message_type": row.get("message_type") or "text",
                "reply_to_message_id": row.get("reply_to_message_id") or "",
            }, ensure_ascii=False) + "\n")

    manifest = {
        "source_corpus": str(corpus.relative_to(root)).replace("\\", "/"),
        "source_corpus_sha256": sha256(corpus),
        "seed_sha256": sha256(seed_path),
        "anomaly_sha256": sha256(anomaly_path),
        "device_id": "DEV-001",
        "simulated_owner": "Raka Pradana",
        "device_message_count": device_rows,
        "source_anomaly_count": anomaly_rows,
        "chat_count": len(chat_ids),
        "first_timestamp": first_ts,
        "last_timestamp": last_ts,
        "excluded_fields": [
            "source_provenance",
            "source_original_line",
            "transformation_id",
        ],
        "note": "DEV-001 seed contains only Raka-participating direct-message records. Non-Raka source rows remain preserved separately as source-reconstruction anomalies."
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
