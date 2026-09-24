"""Local retrieval harness for LIBERA P6.

Two embedding modes are supported:
- hashing: deterministic stdlib-only fallback for CI/dry-run;
- ollama: final local mode, default model bge-m3.

The index contains examiner-visible ART evidence only. No court narrative,
source reconstruction or evaluator ground truth is accepted by design.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from .run_log import append_jsonl, new_run_id, utc_now_iso

HASH_DIMENSIONS = 256
DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_EMBED_MODEL = "bge-m3"
_TOKEN_RE = re.compile(r"[\w]+", re.UNICODE)


class RetrieverError(Exception):
    pass


def hashing_embed(text: str, dimensions: int = HASH_DIMENSIONS) -> List[float]:
    vector = [0.0] * dimensions
    tokens = _TOKEN_RE.findall(text.casefold())
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:8], "big") % dimensions
        sign = 1.0 if digest[8] % 2 == 0 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(v * v for v in vector))
    return [v / norm for v in vector] if norm else vector


def _post_json(url: str, payload: dict, timeout: int = 120) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RetrieverError(f"Ollama embed endpoint gagal {url}: {exc}") from exc


def ollama_embed_batch(
    texts: List[str],
    host: str = DEFAULT_OLLAMA_HOST,
    model: str = DEFAULT_EMBED_MODEL,
    timeout: int = 120,
) -> List[List[float]]:
    data = _post_json(
        f"{host.rstrip('/')}/api/embed",
        {"model": model, "input": texts},
        timeout,
    )
    embeddings = data.get("embeddings")
    if not embeddings or len(embeddings) != len(texts):
        raise RetrieverError("Respons /api/embed tidak memiliki embeddings yang valid.")
    return embeddings


def embed_batch(
    texts: List[str],
    method: str,
    model: Optional[str] = None,
    host: str = DEFAULT_OLLAMA_HOST,
    timeout: int = 120,
) -> List[List[float]]:
    if method == "hashing":
        return [hashing_embed(t) for t in texts]
    if method == "ollama":
        return ollama_embed_batch(texts, host, model or DEFAULT_EMBED_MODEL, timeout)
    raise RetrieverError(f"Embedding method tidak didukung: {method}")


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise RetrieverError(f"Dimensi vector berbeda: {len(a)} != {len(b)}")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def load_chunks(path: Path) -> List[Dict[str, Any]]:
    if not Path(path).exists():
        raise RetrieverError(f"File chunk tidak ditemukan: {path}")
    rows = [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not rows:
        raise RetrieverError(f"File chunk kosong: {path}")
    return rows


def build_index(
    chunks_path: Path,
    namespace: str,
    index_path: Path,
    embedding_method: str = "hashing",
    embedding_model: Optional[str] = None,
    ollama_host: str = DEFAULT_OLLAMA_HOST,
    batch_size: int = 24,
) -> Dict[str, Any]:
    chunks = load_chunks(chunks_path)
    vectors: List[List[float]] = []
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        vectors.extend(
            embed_batch(
                [c["text"] for c in batch],
                method=embedding_method,
                model=embedding_model,
                host=ollama_host,
            )
        )
    entries = []
    for c, vector in zip(chunks, vectors):
        entries.append({
            "chunk_id": c["chunk_id"],
            "conversation_id": c.get("conversation_id"),
            "message_ids": c.get("message_ids", []),
            "evidence_ids": c.get("evidence_ids", []),
            "content_hash_sha256": c.get("content_hash_sha256"),
            "vector": vector,
            "text": c["text"],
            "text_preview": c["text"][:240],
        })
    index = {
        "namespace": namespace,
        "embedding_method": embedding_method,
        "embedding_model": (
            embedding_model or DEFAULT_EMBED_MODEL
            if embedding_method == "ollama" else "sha256_hashing_v1"
        ),
        "embedding_dimensions": len(vectors[0]) if vectors else 0,
        "ollama_host": ollama_host if embedding_method == "ollama" else None,
        "built_at": utc_now_iso(),
        "source_chunks_file": str(chunks_path),
        "entries": entries,
    }
    Path(index_path).parent.mkdir(parents=True, exist_ok=True)
    Path(index_path).write_text(
        json.dumps(index, ensure_ascii=False),
        encoding="utf-8",
    )
    return index


def load_index(index_path: Path) -> Dict[str, Any]:
    if not Path(index_path).exists():
        raise RetrieverError(f"File index tidak ditemukan: {index_path}")
    return json.loads(Path(index_path).read_text(encoding="utf-8"))


def query_index(
    index: Dict[str, Any],
    query_text: str,
    k: int = 5,
    run_log_path: Optional[Path] = None,
) -> Dict[str, Any]:
    start = time.perf_counter()
    method = index.get("embedding_method", "hashing")
    # Backward compatibility with the old prototype name.
    if method == "placeholder_hashing_vector":
        method = "hashing"
    model = index.get("embedding_model")
    host = index.get("ollama_host") or DEFAULT_OLLAMA_HOST
    qv = embed_batch([query_text], method, model, host)[0]

    scored = [
        (cosine_similarity(qv, e["vector"]), e)
        for e in index["entries"]
    ]
    scored.sort(key=lambda p: p[0], reverse=True)
    results = [{
        "chunk_id": e["chunk_id"],
        "evidence_ids": e.get("evidence_ids", []),
        "score": round(score, 6),
        "text": e.get("text", e.get("text_preview", "")),
        "text_preview": e.get("text_preview", "")[:240],
    } for score, e in scored[:k]]
    record = {
        "run_id": new_run_id(),
        "stage": "retrieval",
        "timestamp": utc_now_iso(),
        "namespace": index.get("namespace"),
        "embedding_method": method,
        "embedding_model": model,
        "query": query_text,
        "k": k,
        "latency_seconds": round(time.perf_counter() - start, 6),
        "retrieved_chunk_ids": [r["chunk_id"] for r in results],
        "retrieved_evidence_ids": sorted({
            eid for r in results for eid in r["evidence_ids"] if eid
        }),
        "scores": [r["score"] for r in results],
    }
    if run_log_path:
        append_jsonl(Path(run_log_path), record)
    return {"query_log": record, "results": results}


def main() -> None:
    p = argparse.ArgumentParser(description="P6 vector index and retrieval.")
    sub = p.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build")
    b.add_argument("--chunks", required=True)
    b.add_argument("--namespace", default="case_evidence",
                   choices=["domain_knowledge", "case_evidence"])
    b.add_argument("--index", required=True)
    b.add_argument("--embedding-method", choices=["hashing","ollama"], default="hashing")
    b.add_argument("--embedding-model", default=DEFAULT_EMBED_MODEL)
    b.add_argument("--ollama-host", default=DEFAULT_OLLAMA_HOST)
    q = sub.add_parser("query")
    q.add_argument("--index", required=True)
    q.add_argument("--query", required=True)
    q.add_argument("--k", type=int, default=5)
    q.add_argument("--run-log", default="runtime/working/P8/run_log.jsonl")
    args = p.parse_args()
    try:
        if args.command == "build":
            idx = build_index(
                Path(args.chunks), args.namespace, Path(args.index),
                args.embedding_method, args.embedding_model, args.ollama_host,
            )
            print(
                f"[P6] PASS entries={len(idx['entries'])} "
                f"embedding={idx['embedding_method']}:{idx['embedding_model']}"
            )
        else:
            idx = load_index(Path(args.index))
            out = query_index(idx, args.query, args.k, Path(args.run_log))
            for r in out["results"]:
                print(f"{r['score']:.4f} {r['chunk_id']} {r['text_preview']}")
    except RetrieverError as exc:
        print(f"[P6] ERROR: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
