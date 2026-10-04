"""Operational case lifecycle for Libera.

This module is intentionally separate from the controlled research benchmark.
It reuses the forensic-first extraction/RAG components while keeping software
installation/model caches persistent and case data isolated under a case root.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.resources as resources
import json
import os
import platform
import re
import shutil
import sqlite3
import stat
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.ai_rag import chunker, retriever
from src.ai_rag.ollama_runner import get_model_digest, get_ollama_version, run_once
from src.ai_rag.validate_output import validate_structured_finding, ValidationError
from src.baseline import examiner_packet, p5_lock, traditional_baseline
from src.forensics.extract_artifacts import run as extract_artifacts

CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$")
VERSION = "1.0.0"


class PlatformError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def libera_home() -> Path:
    return Path(os.environ.get("LIBERA_HOME", Path.home() / ".libera")).expanduser().resolve()


def cases_root(explicit: str | None = None) -> Path:
    return Path(explicit).expanduser().resolve() if explicit else libera_home() / "cases"


def case_path(case_id: str, root: str | None = None) -> Path:
    if not CASE_ID_RE.fullmatch(case_id):
        raise PlatformError("Case ID must match [A-Za-z0-9][A-Za-z0-9._-]{1,63}.")
    return cases_root(root) / case_id


def _resource_text(name: str) -> str:
    return resources.files("libera_platform.resources").joinpath(name).read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_case(case_id: str, title: str = "", root: str | None = None, tasks: Path | None = None) -> Path:
    case = case_path(case_id, root)
    if case.exists():
        raise PlatformError(f"Case already exists: {case}")
    for rel in (
        "evidence/master", "evidence/working", "runtime/working/P4",
        "runtime/working/P5", "runtime/working/P6", "runtime/working/AI",
        "logs", "configs", "exports"
    ):
        (case / rel).mkdir(parents=True, exist_ok=True)
    task_text = tasks.read_text(encoding="utf-8") if tasks else _resource_text("investigation_tasks.json")
    (case / "configs/investigation_tasks.json").write_text(task_text, encoding="utf-8")
    (case / "configs/operational_config.json").write_text(_resource_text("operational_config.json"), encoding="utf-8")
    manifest = {
        "schema_version": "libera-operational-case-v1",
        "case_id": case_id,
        "title": title,
        "created_at_utc": utc_now(),
        "libera_version": VERSION,
        "host": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "evidence": None,
        "stages": {},
        "policy": {
            "case_isolated": True,
            "local_ai_only": True,
            "ai_output_is_investigative_aid_not_evidence": True,
        },
    }
    _write_json(case / "case.json", manifest)
    return case


def set_tasks(case_id: str, source: Path, root: str | None = None) -> Path:
    case = require_case(case_id, root)
    data = json.loads(source.read_text(encoding="utf-8"))
    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise PlatformError("Task file must contain a non-empty 'tasks' list.")
    target = case / "configs/investigation_tasks.json"
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def require_case(case_id: str, root: str | None = None) -> Path:
    case = case_path(case_id, root)
    if not (case / "case.json").is_file():
        raise PlatformError(f"Case not found: {case}")
    return case


def _validate_sqlite_schema(path: Path) -> None:
    conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(messages)")}
    finally:
        conn.close()
    required = {
        "message_id", "conversation_id", "timestamp", "sender_id",
        "recipient_id", "message_text", "message_type",
        "reply_to_message_id", "attachment_id",
    }
    missing = required - cols
    if missing:
        raise PlatformError(f"Unsupported SQLite messages schema; missing {sorted(missing)}")


def import_sqlite(
    case_id: str,
    source: Path,
    trusted_sha256: str,
    root: str | None = None,
    device_id: str = "DEV-IMPORTED",
) -> dict:
    case = require_case(case_id, root)
    source = Path(source).expanduser().resolve()
    if not source.is_file():
        raise PlatformError(f"Evidence file not found: {source}")
    trusted_sha256 = trusted_sha256.lower()
    if not re.fullmatch(r"[0-9a-f]{64}", trusted_sha256):
        raise PlatformError("A trusted SHA-256 (64 hex characters) is required.")
    observed = sha256(source)
    if observed != trusted_sha256:
        raise PlatformError(f"Source SHA-256 mismatch: trusted={trusted_sha256} observed={observed}")
    _validate_sqlite_schema(source)

    evidence = case / "evidence"
    master = evidence / "master" / "messages.sqlite"
    working = evidence / "working" / "messages.sqlite"
    if master.exists() or working.exists():
        raise PlatformError("Case already contains imported evidence; create a new case for a new acquisition.")
    shutil.copy2(source, master)
    shutil.copy2(master, working)
    if sha256(master) != trusted_sha256 or sha256(working) != trusted_sha256:
        raise PlatformError("Master/working copy verification failed.")
    try:
        master.chmod(stat.S_IREAD)
    except OSError:
        pass

    acquisition = {
        "status": "IMPORTED_NORMALIZED_SQLITE",
        "acquisition_id": f"ACQ-{case_id}",
        "device_id": device_id,
        "source_filename": source.name,
        "trusted_sha256": trusted_sha256,
        "master_sha256": sha256(master),
        "working_sha256": sha256(working),
        "imported_at_utc": utc_now(),
        "adapter": "normalized_messages_sqlite_v1",
        "disclosure": "Import adapter only; Libera does not claim it performed the upstream device acquisition.",
    }
    _write_json(evidence / "acquisition_manifest.json", acquisition)
    manifest = _json(case / "case.json")
    manifest["evidence"] = acquisition
    manifest["stages"]["import"] = {"status": "PASS", "at_utc": utc_now()}
    _write_json(case / "case.json", manifest)
    return acquisition


def extract(case_id: str, root: str | None = None) -> dict:
    case = require_case(case_id, root)
    acq = _json(case / "evidence/acquisition_manifest.json")
    working = case / "evidence/working/messages.sqlite"
    out = case / "runtime/working/P4/artifacts.csv"
    manifest_path = case / "runtime/working/P4/artifact_manifest.json"
    result = extract_artifacts(working, out, manifest_path, acq["trusted_sha256"])
    # Generic normalized exports may not carry Libera's optional acquisition_metadata
    # table. Preserve evidence bytes and attach case custody identity only to the
    # derived P4 artifact layer.
    if result.get("acquisition_id") == "ACQ-UNKNOWN" or result.get("device_id") == "DEV-UNKNOWN":
        with out.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader); fields = reader.fieldnames or []
        for row in rows:
            row["acquisition_id"] = acq["acquisition_id"]
            row["device_id"] = acq["device_id"]
        with out.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        result["acquisition_id"] = acq["acquisition_id"]
        result["device_id"] = acq["device_id"]
        result["output_sha256"] = sha256(out)
        result["custody_identity_source"] = "case acquisition sidecar; evidence bytes unchanged"
        _write_json(manifest_path, result)
    _stage(case, "P4", result["status"])
    return result


def baseline(case_id: str, root: str | None = None, top_n: int = 20) -> dict:
    case = require_case(case_id, root)
    result = traditional_baseline.run(
        case / "runtime/working/P4/artifacts.csv",
        case / "configs/investigation_tasks.json",
        case / "runtime/working/P5",
        top_n,
    )
    _stage(case, "P5_BASELINE", result["status"])
    return result


def review_p5(case_id: str, root: str | None = None, max_items: int = 12) -> dict:
    case = require_case(case_id, root)
    p5 = case / "runtime/working/P5"
    packet = p5 / "p5_examiner_packet.csv"
    examiner_packet.build_packet(
        p5 / "baseline_findings.json", packet, p5 / "p5_examiner_packet_manifest.json", max_items
    )
    with packet.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = f.fieldnames or []
    start = time.perf_counter()
    for i, row in enumerate(rows, 1):
        print("-" * 80)
        print(f"[{i}/{len(rows)}] {row['evidence_id']} task(s)={row['linked_task_ids']}")
        print(f"{row['timestamp']} {row['sender']} -> {row['receiver']}")
        print(row["text"][:700])
        while True:
            answer = input("Decision [S=supported/N=not supported/U=uncertain]: ").strip().upper()
            if answer in {"S", "N", "U"}:
                break
        row["examiner_decision"] = {"S":"SUPPORTED","N":"NOT_SUPPORTED","U":"UNCERTAIN"}[answer]
        if answer in {"N","U"}:
            note = ""
            while not note:
                note = input("Short reason: ").strip()
            row["examiner_note"] = note
    elapsed = round(time.perf_counter() - start, 3)
    with packet.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    _write_json(p5 / "p5_examiner_timing.json", {
        "schema_version":"libera-p5-human-qc-timing-v1",
        "completed_at_utc":utc_now(), "reviewed_rows":len(rows), "elapsed_seconds":elapsed
    })
    lock = p5_lock.lock(
        case / "runtime/working/P4/artifacts.csv",
        case / "configs/investigation_tasks.json",
        p5, packet, p5 / "p5_lock_manifest.json",
    )
    _stage(case, "P5_REVIEW", lock["status"])
    return lock


def _run_checked(args: list[str], cwd: Path) -> None:
    proc = subprocess.run(args, cwd=cwd)
    if proc.returncode != 0:
        raise PlatformError(f"Command failed ({proc.returncode}): {' '.join(args)}")


def setup_models() -> dict:
    if shutil.which("ollama") is None:
        raise PlatformError("Ollama is not installed/in PATH.")
    host = "http://127.0.0.1:11434"
    if not get_ollama_version(host):
        raise PlatformError("Ollama is installed but not reachable on local loopback.")
    result = {}
    for model in ("bge-m3", "qwen2.5:1.5b"):
        digest = get_model_digest(host, model)
        if not digest:
            _run_checked(["ollama", "pull", model], Path.cwd())
            digest = get_model_digest(host, model)
        if not digest:
            raise PlatformError(f"Model unavailable after pull: {model}")
        result[model] = digest
    return result


def assist(case_id: str, root: str | None = None, top_k: int | None = None) -> dict:
    case = require_case(case_id, root)
    p5_lock.verify(case / "runtime/working/P5/p5_lock_manifest.json")
    cfg = _json(case / "configs/operational_config.json")
    top_k = top_k or int(cfg["retrieval"]["top_k"])
    models = setup_models()

    p4 = case / "runtime/working/P4/artifacts.csv"
    p6 = case / "runtime/working/P6"
    ai = case / "runtime/working/AI"
    p6.mkdir(parents=True, exist_ok=True); ai.mkdir(parents=True, exist_ok=True)
    chunks_path = p6 / "chunks.jsonl"
    chunks = chunker.run(
        p4, chunks_path,
        cfg["chunking"]["min_messages_per_chunk"],
        cfg["chunking"]["max_messages_per_chunk"],
        cfg["chunking"]["time_window_minutes"],
    )
    index_path = p6 / "index.json"
    index = retriever.build_index(
        chunks_path, "case_evidence", index_path,
        embedding_method="ollama", embedding_model=cfg["embedding"]["model"],
        ollama_host=cfg["ollama"]["host"],
    )
    tasks = _json(case / "configs/investigation_tasks.json")["tasks"]
    run_log = ai / "run_log.jsonl"
    outputs = []
    for task in tasks:
        retrieval = retriever.query_index(index, task["question"], k=top_k, run_log_path=run_log)
        results = retrieval["results"]
        rec = run_once(
            query=task["question"], model=cfg["ollama"]["model"],
            prompt_version="operational-v1-structured-grounded",
            temperature=cfg["ollama"]["temperature"], seed=cfg["ollama"]["seed"],
            host=cfg["ollama"]["host"],
            retrieved_chunk_ids=[r["chunk_id"] for r in results],
            retrieved_evidence_ids=sorted({eid for r in results for eid in r["evidence_ids"] if eid}),
            retrieved_texts=[r["text"] for r in results],
            structured=True, dry_run=False, run_log_path=run_log,
            timeout=cfg["ollama"]["request_timeout_seconds"],
            num_ctx=cfg["ollama"]["num_ctx"], num_predict=cfg["ollama"]["num_predict"],
        )
        if rec.get("error") or not rec.get("output"):
            raise PlatformError(f"AI assistance failed for {task['task_id']}: {rec.get('error')}")
        try:
            structured = json.loads(rec["output"])
            validate_structured_finding(structured)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise PlatformError(f"Structured AI output invalid for {task['task_id']}: {exc}") from exc
        supplied = set(rec.get("retrieved_evidence_ids") or [])
        cited = structured.get("relevant_evidence") or []
        invalid = [
            ref for ref in cited
            if not isinstance(ref, str)
            or not re.fullmatch(r"ART-[0-9]{6}", ref)
            or ref not in supplied
        ]
        if invalid:
            raise PlatformError(
                f"AI assistance cited evidence not supplied to {task['task_id']}: {invalid}"
            )
        outputs.append({
            "task_id":task["task_id"], "question":task["question"],
            "retrieval_trace":retrieval["query_log"], "assistance":rec,
            "verified_citations":cited,
        })
    output_path = ai / "assistance.json"
    output_path.write_text(json.dumps(outputs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lock_files = {
        "artifacts": p4,
        "p5_lock": case / "runtime/working/P5/p5_lock_manifest.json",
        "tasks": case / "configs/investigation_tasks.json",
        "config": case / "configs/operational_config.json",
        "chunks": chunks_path,
        "index": index_path,
        "assistance": output_path,
        "run_log": run_log,
    }
    lock = {
        "status":"OPERATIONAL_AI_OUTPUTS_LOCKED",
        "locked_at_utc":utc_now(),
        "model_digests":models,
        "files":{k:{"path":str(v.relative_to(case)), "sha256":sha256(v), "size_bytes":v.stat().st_size}
                 for k,v in lock_files.items()},
        "rule":"AI output is an investigative aid. Verify cited ART evidence before reporting conclusions.",
    }
    _write_json(ai / "assistance_lock.json", lock)
    report = build_report(case_id, root)
    _stage(case, "AI_ASSIST", lock["status"])
    return {"task_count":len(outputs), "chunk_count":len(chunks), "lock":lock, "report":str(report)}


def build_report(case_id: str, root: str | None = None) -> Path:
    case = require_case(case_id, root)
    manifest = _json(case / "case.json")
    p4_path = case / "runtime/working/P4/artifact_manifest.json"
    ai_lock_path = case / "runtime/working/AI/assistance_lock.json"
    p4 = _json(p4_path) if p4_path.exists() else {}
    ai_lock = _json(ai_lock_path) if ai_lock_path.exists() else {}
    report = case / "exports/operational_report.md"
    lines = [
        f"# Libera Operational Case Report — {case_id}", "",
        f"- Title: {manifest.get('title') or '(not set)'}",
        f"- Libera version: {manifest.get('libera_version')}",
        f"- Created: {manifest.get('created_at_utc')}",
        f"- Evidence adapter: {(manifest.get('evidence') or {}).get('adapter','NOT_IMPORTED')}",
        f"- Trusted source SHA-256: {(manifest.get('evidence') or {}).get('trusted_sha256','NOT_IMPORTED')}",
        f"- P4 artifacts: {p4.get('artifact_count','NOT_RUN')}",
        f"- AI lock: {ai_lock.get('status','NOT_RUN')}", "",
        "## Evidentiary boundary", "",
        "Libera AI output is an investigative aid, not evidence and not an admissibility determination.",
        "Every case-specific claim must be checked against the cited ART artifact and upstream acquisition record.",
        "The normalized SQLite adapter does not claim to perform or validate the upstream device acquisition.",
        "",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    return report


def verify(case_id: str, root: str | None = None) -> dict:
    case = require_case(case_id, root)
    problems = []
    acq_path = case / "evidence/acquisition_manifest.json"
    if acq_path.exists():
        acq = _json(acq_path)
        for rel, expected in (
            ("evidence/master/messages.sqlite", acq["master_sha256"]),
            ("evidence/working/messages.sqlite", acq["working_sha256"]),
        ):
            p = case / rel
            if not p.is_file() or sha256(p) != expected:
                problems.append(rel)
    p4_manifest = case / "runtime/working/P4/artifact_manifest.json"
    if p4_manifest.exists():
        p4 = _json(p4_manifest)
        artifacts = case / "runtime/working/P4/artifacts.csv"
        if not artifacts.is_file() or sha256(artifacts) != p4.get("output_sha256"):
            problems.append("P4 artifact hash mismatch")
    p5 = case / "runtime/working/P5/p5_lock_manifest.json"
    if p5.exists():
        try: p5_lock.verify(p5)
        except Exception as exc: problems.append(f"P5 lock: {exc}")
    ai_lock_path = case / "runtime/working/AI/assistance_lock.json"
    if ai_lock_path.exists():
        lock = _json(ai_lock_path)
        for label, rec in lock.get("files", {}).items():
            p = case / rec["path"]
            if not p.is_file() or sha256(p) != rec["sha256"]:
                problems.append(f"AI lock:{label}")
    return {"status":"PASS" if not problems else "FAIL", "problems":problems}


def status(case_id: str, root: str | None = None) -> dict:
    case = require_case(case_id, root)
    checks = {
        "case": case / "case.json",
        "evidence_imported": case / "evidence/acquisition_manifest.json",
        "P4_extracted": case / "runtime/working/P4/artifact_manifest.json",
        "P5_baseline": case / "runtime/working/P5/baseline_manifest.json",
        "P5_review_locked": case / "runtime/working/P5/p5_lock_manifest.json",
        "AI_assistance_locked": case / "runtime/working/AI/assistance_lock.json",
        "report": case / "exports/operational_report.md",
    }
    return {"case_id":case_id, "path":str(case), "stages":{k:v.exists() for k,v in checks.items()}, "verification":verify(case_id, root)}


def archive(case_id: str, output: Path | None = None, root: str | None = None, include_evidence: bool = False) -> Path:
    case = require_case(case_id, root)
    result = verify(case_id, root)
    if result["status"] != "PASS":
        raise PlatformError(f"Refuse archive: case verification failed: {result['problems']}")
    output = Path(output) if output else case / "exports" / f"{case_id}-archive.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    exclude_prefixes = () if include_evidence else ("evidence/master/", "evidence/working/")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in case.rglob("*"):
            if not p.is_file() or p.resolve() == output.resolve():
                continue
            rel = p.relative_to(case).as_posix()
            if any(rel.startswith(prefix) for prefix in exclude_prefixes):
                continue
            zf.write(p, rel)
    return output


def doctor(check_models: bool = True) -> dict:
    home = libera_home()
    home.mkdir(parents=True, exist_ok=True)
    usage = shutil.disk_usage(home)
    result = {
        "libera_version":VERSION,
        "host":{"system":platform.system(),"release":platform.release(),"machine":platform.machine()},
        "python":platform.python_version(),
        "libera_home":str(home),
        "disk_free_gb":round(usage.free/(1024**3),2),
        "ollama":{"installed":shutil.which("ollama") is not None},
    }
    if check_models and result["ollama"]["installed"]:
        host = "http://127.0.0.1:11434"
        result["ollama"].update({
            "version":get_ollama_version(host),
            "bge_m3_digest":get_model_digest(host,"bge-m3"),
            "qwen_digest":get_model_digest(host,"qwen2.5:1.5b"),
        })
    result["ready_for_casework"] = (
        tuple(map(int, platform.python_version_tuple()[:2])) >= (3,12)
        and result["disk_free_gb"] >= 5
    )
    return result


def _stage(case: Path, name: str, status_value: str) -> None:
    manifest = _json(case / "case.json")
    manifest.setdefault("stages", {})[name] = {"status":status_value, "at_utc":utc_now()}
    _write_json(case / "case.json", manifest)
