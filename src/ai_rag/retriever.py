"""
retriever.py - Vector store lokal + retrieval harness untuk pipeline P6.

Embedding di modul ini adalah PLACEHOLDER stdlib-only (hashing-vector),
bukan model embedding sungguhan - lihat catatan di
docs/04_ai_methodology/P6_P7_P8_IMPLEMENTATION_PLAN.md Bab 3.
Fungsi embed() adalah satu-satunya tempat yang perlu diganti nanti.

Index disimpan sebagai JSON lokal (bukan vector DB berat), dengan dua
namespace terpisah sesuai PDF Bab 6.1 poin 6:
  - "domain_knowledge": materi umum, bukan bukti kasus
  - "case_evidence": hasil ekstraksi P4 (working evidence), tidak boleh
    berisi court narrative / Ground Truth (lihat leakage_check.py)

Retrieval harness mencatat query, top-k, scores, chunk_ids, evidence_ids,
dan latency ke run_log (PDF Bab 6.1 poin 7-8).

CLI:
    python -m src.ai_rag.retriever build --chunks configs/toy_chunks.jsonl \
        --namespace case_evidence --index configs/toy_index.json

    python -m src.ai_rag.retriever query --index configs/toy_index.json \
        --query "pertanyaan investigasi" --k 5 [--namespace case_evidence]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .run_log import append_jsonl, new_run_id, utc_now_iso

EMBEDDING_DIMENSIONS = 256
_TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")


def embed(text: str, dimensions: int = EMBEDDING_DIMENSIONS) -> List[float]:
    """PLACEHOLDER embedding: hashing-trick bag-of-words, dinormalisasi.

    Deterministik (tidak butuh model/network), cukup untuk membuktikan
    arsitektur pipeline pada tahap prototype. GANTI fungsi ini dengan
    model embedding sungguhan setelah dipilih tim (PDF Bab 6.1 poin 3).
    """
    vector = [0.0] * dimensions
    tokens = _TOKEN_RE.findall(text.lower())
    if not tokens:
        return vector

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        index = int(digest, 16) % dimensions
        sign = 1.0 if int(digest, 16) % 2 == 0 else -1.0
        vector[index] += sign

    norm = math.sqrt(sum(v * v for v in vector))
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class RetrieverError(Exception):
    pass


def load_chunks(chunks_path: Path) -> List[Dict[str, Any]]:
    chunks_path = Path(chunks_path)
    if not chunks_path.exists():
        raise RetrieverError(f"File chunk tidak ditemukan: {chunks_path}")
    chunks = []
    with chunks_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    if not chunks:
        raise RetrieverError(f"File chunk kosong: {chunks_path}")
    return chunks


def build_index(chunks_path: Path, namespace: str, index_path: Path) -> Dict[str, Any]:
    chunks = load_chunks(chunks_path)

    entries = []
    for c in chunks:
        entries.append(
            {
                "chunk_id": c["chunk_id"],
                "conversation_id": c.get("conversation_id"),
                "message_ids": c.get("message_ids", []),
                "evidence_ids": c.get("evidence_ids", []),
                "content_hash_sha256": c.get("content_hash_sha256"),
                "vector": embed(c["text"]),
                "text_preview": c["text"][:200],
            }
        )

    index = {
        "namespace": namespace,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "embedding_method": "placeholder_hashing_vector",
        "built_at": utc_now_iso(),
        "source_chunks_file": str(chunks_path),
        "entries": entries,
    }

    index_path = Path(index_path)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return index


def load_index(index_path: Path) -> Dict[str, Any]:
    index_path = Path(index_path)
    if not index_path.exists():
        raise RetrieverError(f"File index tidak ditemukan: {index_path}. Jalankan `retriever build` dulu.")
    with index_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def query_index(
    index: Dict[str, Any],
    query_text: str,
    k: int = 5,
    run_log_path: Optional[Path] = None,
) -> Dict[str, Any]:
    start = time.perf_counter()
    query_vector = embed(query_text)

    scored = []
    for entry in index["entries"]:
        score = cosine_similarity(query_vector, entry["vector"])
        scored.append((score, entry))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    top_k = scored[:k]
    latency_seconds = time.perf_counter() - start

    results = [
        {
            "chunk_id": entry["chunk_id"],
            "evidence_ids": entry["evidence_ids"],
            "score": round(score, 6),
            "text_preview": entry["text_preview"],
        }
        for score, entry in top_k
    ]

    record = {
        "run_id": new_run_id(),
        "stage": "retrieval",
        "timestamp": utc_now_iso(),
        "namespace": index.get("namespace"),
        "query": query_text,
        "k": k,
        "latency_seconds": round(latency_seconds, 6),
        "retrieved_chunk_ids": [r["chunk_id"] for r in results],
        "retrieved_evidence_ids": sorted({eid for r in results for eid in r["evidence_ids"]}),
        "scores": [r["score"] for r in results],
    }

    if run_log_path is not None:
        append_jsonl(Path(run_log_path), record)

    return {"query_log": record, "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Vector store + retrieval harness (P6).")
    sub = parser.add_subparsers(dest="command", required=True)

    build_p = sub.add_parser("build", help="Bangun index dari file chunk JSONL")
    build_p.add_argument("--chunks", required=True)
    build_p.add_argument("--namespace", required=True, choices=["domain_knowledge", "case_evidence"])
    build_p.add_argument("--index", required=True)

    query_p = sub.add_parser("query", help="Query index yang sudah dibangun")
    query_p.add_argument("--index", required=True)
    query_p.add_argument("--query", required=True)
    query_p.add_argument("--k", type=int, default=5)
    query_p.add_argument("--run-log", default="configs/run_log.jsonl")

    args = parser.parse_args()

    try:
        if args.command == "build":
            index = build_index(Path(args.chunks), args.namespace, Path(args.index))
            print(f"[retriever] Index '{args.namespace}' dibangun: {len(index['entries'])} entri -> {args.index}")
        elif args.command == "query":
            index = load_index(Path(args.index))
            out = query_index(index, args.query, k=args.k, run_log_path=Path(args.run_log))
            print(f"[retriever] Top-{args.k} hasil untuk query: {args.query!r}")
            for r in out["results"]:
                print(f"  score={r['score']:.4f} chunk_id={r['chunk_id']} preview={r['text_preview'][:80]!r}")
    except RetrieverError as exc:
        print(f"[retriever] ERROR: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
