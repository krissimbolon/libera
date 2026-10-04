#!/usr/bin/env python3
"""Check Markdown links and repository path references in documentation.

Usage: python tools/check_doc_links.py [--include-archive] [--paths]

* Markdown links ``[text](target)`` with relative targets must resolve.
* With ``--paths``: back-ticked repository paths (``src/...``, ``docs/...`` ...)
  must exist, unless they are runtime/private locations that are generated
  locally and intentionally untracked (reported separately, never an error).
External URLs are listed but not fetched.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|!\[[^\]]*\]\(([^)\s]+)\)")
TICK = re.compile(r"`((?:docs|src|tools|scripts|tests|configs|data|workbench|apps|references|archive|runtime|demo_evidence|evidence_vault|\.github)/[^`\s*<>{}$]+)`")
CMD_PATH = re.compile(r"(?<![\w/\\.-])((?:scripts|tools|src|workbench)[\\/][\w./\\-]+\.(?:py|ps1))")
MODULE = re.compile(r"-m\s+(src(?:\.\w+)+)")
GENERATED = ("runtime/", "configs/toy_", "configs/run_log.jsonl", "demo_evidence/", "evidence_vault/", "data/private/", "data/source_restricted/",
             "apps/libera-chatsim/app/build/", "apps/libera-chatsim/app/src/main/assets/messages_seed",
             "apps/libera-chatsim/app/src/main/assets/seed_manifest", "apps/libera-chatsim/app/src/main/assets/source_anomalies")


def tracked_markdown(include_archive: bool) -> list[Path]:
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    files = [ROOT / p for p in out]
    if not include_archive:
        files = [p for p in files if not str(p.relative_to(ROOT)).startswith(("docs/archive/", "archive/", "docs/08_uas/"))]
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-archive", action="store_true")
    ap.add_argument("--paths", action="store_true")
    args = ap.parse_args()
    broken, generated, external = [], set(), set()
    for md in tracked_markdown(args.include_archive):
        text = md.read_text(encoding="utf-8-sig")
        # Ignore fenced code blocks for link parsing (commands are checked separately).
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        for m in LINK.finditer(prose):
            target = (m.group(1) or m.group(2)).split("#", 1)[0]
            if not target or target.startswith(("mailto:",)):
                continue
            if re.match(r"^[a-z]+://", target):
                external.add(target)
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{md.relative_to(ROOT)}: link -> {target}")
        # Archived records are historical text: only their Markdown links are checked;
        # path mentions inside them describe the repository as of their date.
        if args.paths and not str(md.relative_to(ROOT)).startswith(("docs/archive/", "archive/", "docs/08_uas/")):
            for m in TICK.finditer(text):
                path = m.group(1).rstrip(".,;:)")
                if path.startswith(GENERATED):
                    generated.add(path)
                    continue
                if any(ch in path for ch in "?[]"):
                    continue
                if not (ROOT / path).exists() and not list(ROOT.glob(path)):
                    broken.append(f"{md.relative_to(ROOT)}: path `{path}`")
            for m in CMD_PATH.finditer(text):
                path = m.group(1).replace("\\", "/")
                if not (ROOT / path).exists():
                    broken.append(f"{md.relative_to(ROOT)}: command path {path}")
            for m in MODULE.finditer(text):
                mod = m.group(1).replace(".", "/")
                if not ((ROOT / (mod + ".py")).exists() or (ROOT / mod / "__init__.py").exists()):
                    broken.append(f"{md.relative_to(ROOT)}: module {m.group(1)}")
    for line in sorted(set(broken)):
        print("BROKEN", line)
    print(f"external URLs (not fetched): {len(external)}")
    print(f"generated/private runtime paths referenced (intentionally untracked): {len(generated)}")
    print(f"broken: {len(set(broken))}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
