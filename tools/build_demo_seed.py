#!/usr/bin/env python3
"""Build the examiner-safe ChatSim seed from the immutable P2 corpus."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

RAKA = "AKT-RAKA"
CANONICAL_SHA256 = "a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6"
CANONICAL_ROWS = 10_000
EXPECTED_DEVICE_ROWS = 9_997
EXPECTED_ANOMALIES = 3


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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--corpus",
        default="data/adaptasi_indonesia/corpus_whatsapp_10000.csv",
    )
    ap.add_argument(
        "--out-dir",
        default="apps/libera-chatsim/app/src/main/assets",
    )
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    corpus = Path(args.corpus)
    if not corpus.is_absolute():
        corpus = root / corpus
    if not corpus.exists():
        raise SystemExit(f"Frozen corpus not found: {corpus}")

    actual_hash = sha256(corpus)
    if actual_hash != CANONICAL_SHA256:
        raise SystemExit(
            "Refusing seed generation: frozen P2 hash mismatch. "
            f"expected={CANONICAL_SHA256} actual={actual_hash}"
        )

    actors = read_actor_names(root / "data/adaptasi_indonesia/registri_aktor_indonesia.csv")
    out_dir = root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    seed_path = out_dir / "messages_seed.jsonl"
    anomaly_path = out_dir / "source_anomalies.jsonl"
    manifest_path = out_dir / "seed_manifest.json"

    device_rows = 0
    anomaly_rows = 0
    source_rows = 0
    chat_ids: set[str] = set()
    first_ts = None
    last_ts = None

    with (
        corpus.open(encoding="utf-8", newline="") as src,
        seed_path.open("w", encoding="utf-8", newline="\n") as seed,
        anomaly_path.open("w", encoding="utf-8", newline="\n") as anomalies,
    ):
        for row in csv.DictReader(src):
            source_rows += 1
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
                    "reason": (
                        "Neither endpoint is AKT-RAKA; not silently placed on "
                        "Raka's simulated device."
                    ),
                }, ensure_ascii=False) + "\n")
                continue

            peer = recipient if sender == RAKA else sender
            chat_id = f"CHAT-{peer}"
            chat_ids.add(chat_id)
            device_rows += 1
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

    if source_rows != CANONICAL_ROWS:
        raise SystemExit(f"Expected {CANONICAL_ROWS} source rows, got {source_rows}")
    if device_rows != EXPECTED_DEVICE_ROWS or anomaly_rows != EXPECTED_ANOMALIES:
        raise SystemExit(
            f"Unexpected device/anomaly split: {device_rows}/{anomaly_rows}; "
            f"expected {EXPECTED_DEVICE_ROWS}/{EXPECTED_ANOMALIES}"
        )

    manifest = {
        "source_corpus": str(corpus.relative_to(root)).replace("\\", "/"),
        "source_corpus_sha256": actual_hash,
        "source_row_count": source_rows,
        "seed_sha256": sha256(seed_path),
        "anomaly_sha256": sha256(anomaly_path),
        "device_id": "DEV-SIM-001",
        "environment": "LIBERA ChatSim Android emulator",
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
            "ground_truth",
        ],
        "disclosure": (
            "ChatSim is a researcher-controlled Android messaging simulator. "
            "It is not WhatsApp and must not be described as WhatsApp acquisition."
        ),
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
