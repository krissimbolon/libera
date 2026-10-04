#!/usr/bin/env python3
"""Capture a report-safe local runtime manifest for a Libera study run.

The manifest intentionally avoids usernames, hostnames, and arbitrary environment
variables. It is meant to be hash-locked with P8 so the model/runtime context of
an experiment remains auditable without publishing private case material.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.ai_rag.ollama_runner import get_model_digest, get_ollama_version


FROZEN_CORPUS = Path("data/adaptasi_indonesia/corpus_whatsapp_10000.csv")


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def command_output(*args: str) -> str | None:
    try:
        result = subprocess.run(
            list(args), capture_output=True, text=True, timeout=20, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None
    text = (result.stdout or result.stderr or "").strip()
    return text or None


def git_state() -> dict:
    head = command_output("git", "rev-parse", "HEAD")
    status = command_output("git", "status", "--porcelain")
    return {
        "head": head,
        "working_tree_clean": status == "" if status is not None else None,
    }


def adb_state() -> dict:
    version = command_output("adb", "version")
    raw = command_output("adb", "devices")
    devices = []
    if raw:
        for line in raw.splitlines()[1:]:
            parts = line.split()
            if len(parts) < 2 or parts[1] != "device":
                continue
            serial = parts[0]
            record = {
                "transport": "android-emulator" if serial.startswith("emulator-") else "android-device",
                "serial": serial if serial.startswith("emulator-") else None,
                "serial_sha256": (
                    None if serial.startswith("emulator-")
                    else hashlib.sha256(serial.encode("utf-8")).hexdigest()
                ),
            }
            if serial.startswith("emulator-"):
                for key, prop in {
                    "model": "ro.product.model",
                    "android_release": "ro.build.version.release",
                    "sdk": "ro.build.version.sdk",
                }.items():
                    value = command_output("adb", "-s", serial, "shell", "getprop", prop)
                    record[key] = value
            devices.append(record)
    return {"version": version, "connected_devices": devices}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="runtime/working/P8/run_environment.json")
    p.add_argument("--ollama-host", default="http://localhost:11434")
    p.add_argument("--model", default="qwen2.5:1.5b")
    p.add_argument("--embedding-model", default="bge-m3")
    p.add_argument("--overwrite", action="store_true")
    args = p.parse_args()

    out = Path(args.output)
    if out.exists() and not args.overwrite:
        raise SystemExit(f"Refuse to overwrite runtime manifest: {out}")

    manifest = {
        "schema_version": "libera-run-environment-v1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": git_state(),
        "frozen_corpus": {
            "path": str(FROZEN_CORPUS),
            "sha256": sha256(FROZEN_CORPUS),
        },
        "registered_inputs": {
            "p6_p7_config_sha256": sha256(Path("configs/p6_p7_config.json")),
            "investigation_tasks_sha256": sha256(Path("configs/investigation_tasks.json")),
        },
        "host_runtime": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor() or None,
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_executable_name": Path(sys.executable).name,
        },
        "android": adb_state(),
        "ollama": {
            "host": args.ollama_host,
            "version_api": get_ollama_version(args.ollama_host),
            "cli_version": command_output("ollama", "--version"),
            "generation_model": args.model,
            "generation_model_digest": get_model_digest(args.ollama_host, args.model),
            "embedding_model": args.embedding_model,
            "embedding_model_digest": get_model_digest(args.ollama_host, args.embedding_model),
        },
        "privacy": (
            "No username, hostname, arbitrary environment variables, or private evidence "
            "content is recorded by this manifest."
        ),
    }

    if not manifest["repository"]["head"]:
        raise SystemExit("Unable to resolve repository HEAD.")
    if not manifest["ollama"]["version_api"]:
        raise SystemExit("Ollama version unavailable; runtime is not ready.")
    if not manifest["ollama"]["generation_model_digest"]:
        raise SystemExit(f"Generation model digest unavailable: {args.model}")
    if not manifest["ollama"]["embedding_model_digest"]:
        raise SystemExit(f"Embedding model digest unavailable: {args.embedding_model}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[ENV] PASS -> {out}")


if __name__ == "__main__":
    main()
