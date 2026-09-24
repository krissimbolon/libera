"""
run_experiment.py - Orkestrasi tiga kondisi eksperimen (P8).

Kondisi (PDF Bab 6.1 poin 11, Bab F):
    A_llm_only         - LLM tanpa retrieval
    B_llm_rag          - LLM + RAG (retrieval biasa)
    C_llm_rag_structured - LLM + RAG + structured reasoning format

Pertanyaan, evidence input, dan protokol harus konsisten di ketiga
kondisi (prompt_version/model/seed dikunci sebelum run). Modul ini
TIDAK menilai/membandingkan hasil - itu wewenang evaluator (Daffa)
setelah membuka Ground Truth, sesuai larangan PDF: "Jangan membuat
klaim bahwa salah satu kondisi lebih baik sebelum eksperimen dilakukan."

CLI:
    python -m src.ai_rag.run_experiment --dry-run \
        --index configs/toy_index.json \
        --questions configs/toy_questions.json \
        --output configs/toy_experiment_output.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import ollama_runner
from .retriever import RetrieverError, load_index, query_index
from .run_log import utc_now_iso

DEFAULT_QUESTIONS = [
    "Siapa saja yang berada di ruang C3 pada sore hari kejadian?",
    "Apa urutan kejadian yang bisa direkonstruksi dari percakapan yang ada?",
]


def ensure_questions_file(path: Path) -> List[str]:
    path = Path(path)
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data["questions"] if isinstance(data, dict) else data

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump({"questions": DEFAULT_QUESTIONS}, f, ensure_ascii=False, indent=2)
    return DEFAULT_QUESTIONS


def run_condition_a(question: str, args: argparse.Namespace) -> Dict[str, Any]:
    """A: LLM only - tanpa retrieval sama sekali."""
    return ollama_runner.run_once(
        query=question,
        model=args.model,
        prompt_version=args.prompt_version,
        temperature=args.temperature,
        seed=args.seed,
        host=args.host,
        structured=False,
        dry_run=args.dry_run,
        run_log_path=Path(args.run_log),
    )


def run_condition_b(question: str, index: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    """B: LLM + RAG - retrieval biasa, jawaban bebas + evidence IDs."""
    retrieval = query_index(index, question, k=args.top_k, run_log_path=Path(args.run_log))
    retrieved_texts = [r["text_preview"] for r in retrieval["results"]]
    chunk_ids = [r["chunk_id"] for r in retrieval["results"]]
    evidence_ids = sorted({eid for r in retrieval["results"] for eid in r["evidence_ids"]})

    return ollama_runner.run_once(
        query=question,
        model=args.model,
        prompt_version=args.prompt_version,
        temperature=args.temperature,
        seed=args.seed,
        host=args.host,
        retrieved_chunk_ids=chunk_ids,
        retrieved_evidence_ids=evidence_ids,
        retrieved_texts=retrieved_texts,
        structured=False,
        dry_run=args.dry_run,
        run_log_path=Path(args.run_log),
    )


def run_condition_c(question: str, index: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    """C: LLM + RAG + structured reasoning format."""
    retrieval = query_index(index, question, k=args.top_k, run_log_path=Path(args.run_log))
    retrieved_texts = [r["text_preview"] for r in retrieval["results"]]
    chunk_ids = [r["chunk_id"] for r in retrieval["results"]]
    evidence_ids = sorted({eid for r in retrieval["results"] for eid in r["evidence_ids"]})

    return ollama_runner.run_once(
        query=question,
        model=args.model,
        prompt_version=args.prompt_version,
        temperature=args.temperature,
        seed=args.seed,
        host=args.host,
        retrieved_chunk_ids=chunk_ids,
        retrieved_evidence_ids=evidence_ids,
        retrieved_texts=retrieved_texts,
        structured=True,
        dry_run=args.dry_run,
        run_log_path=Path(args.run_log),
    )


def run_all_conditions(questions: List[str], index_path: Optional[Path], args: argparse.Namespace) -> List[Dict[str, Any]]:
    index = None
    if index_path is not None:
        try:
            index = load_index(Path(index_path))
        except RetrieverError as exc:
            print(f"[run_experiment] WARNING: index tidak dapat dimuat ({exc}); kondisi B/C dilewati.")

    results = []
    for question in questions:
        entry: Dict[str, Any] = {"question": question, "timestamp": utc_now_iso()}
        entry["A_llm_only"] = run_condition_a(question, args)
        if index is not None:
            entry["B_llm_rag"] = run_condition_b(question, index, args)
            entry["C_llm_rag_structured"] = run_condition_c(question, index, args)
        else:
            entry["B_llm_rag"] = None
            entry["C_llm_rag_structured"] = None
        results.append(entry)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Orkestrasi eksperimen A/B/C (P8).")
    parser.add_argument("--index", default=None, help="Path index (configs/toy_index.json). Kosongkan untuk hanya kondisi A.")
    parser.add_argument("--questions", default="configs/toy_questions.json")
    parser.add_argument("--output", default="configs/toy_experiment_output.json")
    parser.add_argument("--model", default=ollama_runner.DEFAULT_MODEL)
    parser.add_argument("--prompt-version", default="v1")
    parser.add_argument("--temperature", type=float, default=ollama_runner.DEFAULT_TEMPERATURE)
    parser.add_argument("--seed", type=int, default=ollama_runner.DEFAULT_SEED)
    parser.add_argument("--host", default=ollama_runner.DEFAULT_HOST)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-log", default="configs/run_log.jsonl")
    args = parser.parse_args()

    questions = ensure_questions_file(Path(args.questions))
    index_path = Path(args.index) if args.index else None
    results = run_all_conditions(questions, index_path, args)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[run_experiment] {len(questions)} pertanyaan dijalankan -> {output_path}")
    print(f"[run_experiment] dry_run={args.dry_run}, model={args.model}, index={args.index}")


if __name__ == "__main__":
    main()
