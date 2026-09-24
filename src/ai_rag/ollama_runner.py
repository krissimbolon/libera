"""P7 local Ollama runner with reproducibility and forensic guardrails."""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from .run_log import append_jsonl, new_run_id, utc_now_iso

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:7b"
DEFAULT_TEMPERATURE = 0.1
DEFAULT_SEED = 42
DEFAULT_NUM_CTX = 8192
DEFAULT_TIMEOUT_SECONDS = 180

FORENSIC_INSTRUCTIONS = """You are assisting a digital-forensic examination.
Use ONLY the case evidence explicitly supplied in this prompt.
Never use hidden source reconstruction, evaluator ground truth, or outside facts.
For case-specific factual claims, cite examiner evidence IDs such as [ART-000001].
If evidence is absent or insufficient, say so. Distinguish observation from
interpretation. Do not invent actors, events, dates, locations, payments, or
relationships. Return only the requested answer, not private chain-of-thought.
"""

STRUCTURED_REASONING_INSTRUCTIONS = """Return ONLY valid JSON with these fields:
{
  "question": "<original question>",
  "relevant_evidence": ["ART-...", "..."],
  "observed_facts": "<facts explicitly supported by supplied evidence>",
  "possible_interpretation": "<bounded interpretation>",
  "contradicting_evidence": "<contradiction or 'tidak ada yang ditemukan'>",
  "confidence_uncertainty": "<tinggi/sedang/rendah + short reason>",
  "finding": "<one or two sentence finding>"
}
"""


class OllamaError(Exception):
    pass


def _post(url: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise OllamaError(f"Ollama tidak dapat dihubungi di {url}: {exc}") from exc


def _get(url: str, timeout: int) -> Dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise OllamaError(f"Ollama tidak dapat dihubungi di {url}: {exc}") from exc


def get_ollama_version(host: str) -> Optional[str]:
    try:
        return _get(f"{host.rstrip('/')}/api/version", 10).get("version")
    except OllamaError:
        return None


def get_model_digest(host: str, model: str) -> Optional[str]:
    try:
        data = _get(f"{host.rstrip('/')}/api/tags", 15)
    except OllamaError:
        return None
    wanted = model.casefold()
    for item in data.get("models", []):
        name = str(item.get("name", "")).casefold()
        if name == wanted or name.split(":")[0] == wanted.split(":")[0]:
            return item.get("digest")
    return None


def build_prompt(query: str, retrieved_texts: List[str], structured: bool) -> str:
    evidence = (
        "\n\n--- RETRIEVED EVIDENCE ---\n"
        + "\n---\n".join(retrieved_texts)
        + "\n--- END EVIDENCE ---\n"
        if retrieved_texts else
        "\n\nNO CASE EVIDENCE WAS SUPPLIED FOR THIS CONDITION.\n"
    )
    format_instruction = STRUCTURED_REASONING_INSTRUCTIONS if structured else (
        "Answer concisely. Cite ART evidence IDs for every case-specific factual claim."
    )
    return (
        FORENSIC_INSTRUCTIONS + "\n" + format_instruction +
        evidence + f"\nQuestion: {query}\n"
    )


def call_generate(
    host: str, model: str, prompt: str, temperature: float, seed: int,
    num_ctx: int, timeout: int,
) -> str:
    data = _post(
        f"{host.rstrip('/')}/api/generate",
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "seed": seed,
                "num_ctx": num_ctx,
            },
        },
        timeout,
    )
    return data.get("response", "")


def run_once(
    query: str,
    model: str = DEFAULT_MODEL,
    prompt_version: str = "v2-forensic-grounded",
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
    num_ctx: int = DEFAULT_NUM_CTX,
) -> Dict[str, Any]:
    retrieved_chunk_ids = retrieved_chunk_ids or []
    retrieved_evidence_ids = retrieved_evidence_ids or []
    retrieved_texts = retrieved_texts or []
    run_id = new_run_id()
    prompt = build_prompt(query, retrieved_texts, structured)
    error = None
    version = None
    digest = None
    if dry_run:
        output = (
            json.dumps({
                "question": query,
                "relevant_evidence": retrieved_evidence_ids,
                "observed_facts": "[DRY-RUN] no model call",
                "possible_interpretation": "[DRY-RUN]",
                "contradicting_evidence": "tidak dievaluasi",
                "confidence_uncertainty": "rendah - dry-run",
                "finding": "[DRY-RUN] pipeline-only output",
            }, ensure_ascii=False)
            if structured else
            "[DRY-RUN] pipeline-only output; no model call."
        )
    else:
        version = get_ollama_version(host)
        digest = get_model_digest(host, model)
        try:
            output = call_generate(
                host, model, prompt, temperature, seed, num_ctx, timeout
            )
        except OllamaError as exc:
            output = ""
            error = str(exc)

    record = {
        "run_id": run_id,
        "stage": "llm_call",
        "timestamp": utc_now_iso(),
        "model": model,
        "ollama_version": version,
        "model_digest": digest,
        "prompt_version": prompt_version,
        "temperature": temperature,
        "seed": seed,
        "num_ctx": num_ctx,
        "dry_run": dry_run,
        "structured": structured,
        "query": query,
        "retrieved_chunk_ids": retrieved_chunk_ids,
        "retrieved_evidence_ids": retrieved_evidence_ids,
        "output": output,
        "error": error,
    }
    if run_log_path:
        append_jsonl(Path(run_log_path), record)
    return record


def main() -> None:
    p = argparse.ArgumentParser(description="P7 local Ollama runner.")
    p.add_argument("--query", required=True)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--prompt-version", default="v2-forensic-grounded")
    p.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument("--num-ctx", type=int, default=DEFAULT_NUM_CTX)
    p.add_argument("--host", default=DEFAULT_HOST)
    p.add_argument("--structured", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--run-log", default="runtime/working/P8/run_log.jsonl")
    args = p.parse_args()
    rec = run_once(
        args.query, args.model, args.prompt_version, args.temperature,
        args.seed, args.host, structured=args.structured,
        dry_run=args.dry_run, run_log_path=Path(args.run_log),
        num_ctx=args.num_ctx,
    )
    print(f"[P7] run_id={rec['run_id']} model={rec['model']} digest={rec['model_digest']}")
    if rec["error"]:
        print(f"[P7] ERROR: {rec['error']}")
        raise SystemExit(1)
    print(rec["output"])


if __name__ == "__main__":
    main()
