"""
ollama_runner.py - Pemanggil Ollama lokal (P7) dengan logging RUN-ID.

Memakai HTTP API Ollama (http://localhost:11434) lewat urllib standard
library saja - tidak menambah dependency `requests` atau `ollama` pip
package, sesuai arahan "dependency seminimal mungkin".

Setiap run (dry-run maupun sungguhan) dicatat ke run_log dengan field
sesuai PDF Bab 6.1 poin 9 & Bab F:
    run_id, model, ollama_version, model_digest (best-effort),
    prompt_version, temperature, seed, query, retrieved_evidence_ids,
    retrieved_chunk_ids, output, timestamp, error (jika ada)

Mode --dry-run mengembalikan output stub TANPA melakukan koneksi
jaringan apa pun - dipakai untuk praktikum individu / test tanpa Ollama
terpasang.

CLI:
    python -m src.ai_rag.ollama_runner --dry-run --query "..." --prompt-version v1
    python -m src.ai_rag.ollama_runner --model llama3.1 --query "..." --prompt-version v1
"""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from .run_log import append_jsonl, new_run_id, utc_now_iso

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_SEED = 42
DEFAULT_TIMEOUT_SECONDS = 120

STRUCTURED_REASONING_INSTRUCTIONS = """\
Jawab HANYA dalam format JSON dengan field berikut, tanpa teks lain di luar JSON:
{
  "question": "<pertanyaan asli>",
  "relevant_evidence": ["<evidence_id atau chunk_id yang relevan>", ...],
  "observed_facts": "<fakta yang secara eksplisit didukung evidence>",
  "possible_interpretation": "<interpretasi yang wajar dari fakta di atas>",
  "contradicting_evidence": "<evidence yang bertentangan, atau 'tidak ada'>",
  "confidence_uncertainty": "<tinggi/sedang/rendah beserta alasan singkat>",
  "finding": "<ringkasan temuan, satu-dua kalimat>"
}
Jangan menyertakan chain-of-thought atau proses berpikir internal - hanya JSON akhir di atas.
"""


class OllamaError(Exception):
    pass


def _http_post_json(url: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise OllamaError(f"Tidak dapat menghubungi Ollama di {url}: {exc}") from exc


def _http_get_json(url: str, timeout: int) -> Dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise OllamaError(f"Tidak dapat menghubungi Ollama di {url}: {exc}") from exc


def get_ollama_version(host: str, timeout: int = 10) -> Optional[str]:
    try:
        data = _http_get_json(f"{host}/api/version", timeout=timeout)
        return data.get("version")
    except OllamaError:
        return None


def build_prompt(query: str, retrieved_texts: List[str], structured: bool) -> str:
    context_block = ""
    if retrieved_texts:
        joined = "\n---\n".join(retrieved_texts)
        context_block = f"Konteks bukti yang diambil:\n{joined}\n\n"

    instructions = STRUCTURED_REASONING_INSTRUCTIONS if structured else ""
    return f"{instructions}\n{context_block}Pertanyaan: {query}\n"


def call_ollama_generate(
    host: str,
    model: str,
    prompt: str,
    temperature: float,
    seed: int,
    timeout: int,
) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "seed": seed},
    }
    data = _http_post_json(f"{host}/api/generate", payload, timeout=timeout)
    return data.get("response", "")


def run_once(
    query: str,
    model: str = DEFAULT_MODEL,
    prompt_version: str = "v1",
    temperature: float = DEFAULT_TEMPERATURE,
    seed: int = DEFAULT_SEED,
    host: str = DEFAULT_HOST,
    retrieved_chunk_ids: Optional[List[str]] = None,
    retrieved_evidence_ids: Optional[List[str]] = None,
    retrieved_texts: Optional[List[str]] = None,
    structured: bool = False,
    dry_run: bool = False,
    run_log_path: Optional[Path] = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> Dict[str, Any]:
    """Jalankan satu kali pemanggilan LLM (dry-run atau sungguhan) dan
    catat ke run_log. Mengembalikan record lengkap yang juga ditulis ke log.
    """
    retrieved_chunk_ids = retrieved_chunk_ids or []
    retrieved_evidence_ids = retrieved_evidence_ids or []
    retrieved_texts = retrieved_texts or []

    run_id = new_run_id()
    prompt = build_prompt(query, retrieved_texts, structured=structured)

    error_message = None
    if dry_run:
        output = json.dumps(
            {
                "question": query,
                "relevant_evidence": retrieved_evidence_ids,
                "observed_facts": "[DRY-RUN] Tidak ada panggilan model sungguhan.",
                "possible_interpretation": "[DRY-RUN] Stub output untuk testing pipeline.",
                "contradicting_evidence": "tidak ada",
                "confidence_uncertainty": "rendah - ini adalah dry-run, bukan hasil model",
                "finding": "[DRY-RUN] Placeholder finding.",
            },
            ensure_ascii=False,
        ) if structured else "[DRY-RUN] Tidak ada panggilan model sungguhan."
        ollama_version = None
    else:
        ollama_version = get_ollama_version(host, timeout=min(timeout, 10))
        try:
            output = call_ollama_generate(
                host=host, model=model, prompt=prompt, temperature=temperature, seed=seed, timeout=timeout
            )
        except OllamaError as exc:
            output = ""
            error_message = str(exc)

    record = {
        "run_id": run_id,
        "stage": "llm_call",
        "timestamp": utc_now_iso(),
        "model": model,
        "ollama_version": ollama_version,
        "model_digest": None,  # best-effort, diisi jika/ketika tersedia dari /api/show
        "prompt_version": prompt_version,
        "temperature": temperature,
        "seed": seed,
        "dry_run": dry_run,
        "structured": structured,
        "query": query,
        "retrieved_chunk_ids": retrieved_chunk_ids,
        "retrieved_evidence_ids": retrieved_evidence_ids,
        "output": output,
        "error": error_message,
    }

    if run_log_path is not None:
        append_jsonl(Path(run_log_path), record)

    return record


def main() -> None:
    parser = argparse.ArgumentParser(description="Ollama runner dengan RUN-ID logging (P7).")
    parser.add_argument("--query", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--prompt-version", default="v1")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--structured", action="store_true", help="Minta output format structured finding")
    parser.add_argument("--dry-run", action="store_true", help="Jalankan tanpa memanggil Ollama sungguhan")
    parser.add_argument("--run-log", default="configs/run_log.jsonl")
    args = parser.parse_args()

    record = run_once(
        query=args.query,
        model=args.model,
        prompt_version=args.prompt_version,
        temperature=args.temperature,
        seed=args.seed,
        host=args.host,
        structured=args.structured,
        dry_run=args.dry_run,
        run_log_path=Path(args.run_log),
    )

    print(f"[ollama_runner] run_id={record['run_id']} dry_run={record['dry_run']}")
    if record["error"]:
        print(f"[ollama_runner] ERROR: {record['error']}")
    print(f"[ollama_runner] output:\n{record['output']}")


if __name__ == "__main__":
    main()
