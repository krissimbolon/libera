"""
leakage_check.py - Guard dasar sebelum data masuk index RAG (P6).

Menolak ingest jika file input mengandung penanda Ground Truth (nama
kolom schema privat) atau penanda court narrative / Document 547,
sesuai larangan PDF ("Document 547 dan narasi pengadilan tidak
dimasukkan ke RAG investigator", "Jangan memasukkan Ground Truth ke
RAG").

PENTING: ini adalah guard sederhana berbasis pencarian string, BUKAN
jaminan mutlak. Review manusia tetap wajib sebelum data masuk index
produksi (lihat P6_P7_P8_IMPLEMENTATION_PLAN.md Bab 4).

CLI:
    python -m src.ai_rag.leakage_check --input configs/toy_chunks.jsonl
    python -m src.ai_rag.leakage_check --input configs/toy_chunks.jsonl \
        --config configs/p6_p7_config.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

DEFAULT_BANNED_TERMS = [
    "Document 547",
    "ground_truth",
    "skema_ground_truth_privat",
    "expected_entity_ids",
    "expected_relation_ids",
    "is_key_evidence",
    "court transcript",
    "narasi pengadilan",
]


class LeakageDetected(Exception):
    def __init__(self, matches: List[str]):
        self.matches = matches
        super().__init__(f"Ditemukan {len(matches)} penanda terlarang: {matches}")


def load_banned_terms(config_path: Path | None) -> List[str]:
    if config_path is None:
        return DEFAULT_BANNED_TERMS
    config_path = Path(config_path)
    if not config_path.exists():
        return DEFAULT_BANNED_TERMS
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg.get("leakage_check", {}).get("banned_terms", DEFAULT_BANNED_TERMS)


def scan_text(text: str, banned_terms: List[str]) -> List[str]:
    lowered = text.lower()
    return [term for term in banned_terms if term.lower() in lowered]


def scan_file(path: Path, banned_terms: List[str]) -> List[str]:
    """Pindai satu file teks/JSONL baris-per-baris dan kembalikan daftar
    penanda yang ditemukan (kosong berarti aman)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    found = set()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            for term in scan_text(line, banned_terms):
                found.add(term)
    return sorted(found)


def main() -> None:
    parser = argparse.ArgumentParser(description="Leakage guard sebelum ingest RAG (P6).")
    parser.add_argument("--input", required=True, help="File JSONL/teks yang akan dipindai")
    parser.add_argument("--config", default=None, help="Path configs/p6_p7_config.json (opsional)")
    args = parser.parse_args()

    banned_terms = load_banned_terms(Path(args.config) if args.config else None)

    try:
        matches = scan_file(Path(args.input), banned_terms)
    except FileNotFoundError as exc:
        print(f"[leakage_check] ERROR: {exc}")
        raise SystemExit(1)

    if matches:
        print(f"[leakage_check] GAGAL - ditemukan penanda terlarang di {args.input}: {matches}")
        print("[leakage_check] Jangan ingest file ini ke index case_evidence. Review manual diperlukan.")
        raise SystemExit(2)

    print(f"[leakage_check] OK - tidak ditemukan penanda terlarang di {args.input}")


if __name__ == "__main__":
    main()
