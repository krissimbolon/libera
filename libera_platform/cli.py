"""Console interface for the Libera operational platform."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .case import (
    PlatformError, archive, assist, baseline, create_case, doctor, extract,
    import_sqlite, review_p5, set_tasks, setup_models, status, verify,
)


def _emit(value, as_json: bool = False) -> None:
    if as_json or isinstance(value, (dict, list)):
        print(json.dumps(value, ensure_ascii=False, indent=2))
    else:
        print(value)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="libera", description="Local forensic case platform.")
    p.add_argument("--version", action="version", version=f"Libera {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("doctor", help="Check local runtime readiness.")
    d.add_argument("--json", action="store_true")
    d.add_argument("--skip-models", action="store_true")

    sub.add_parser("setup-models", help="Ensure persistent local Ollama models are cached.")

    case = sub.add_parser("case", help="Manage isolated forensic cases.")
    cs = case.add_subparsers(dest="case_command", required=True)

    c = cs.add_parser("create")
    c.add_argument("case_id"); c.add_argument("--title", default=""); c.add_argument("--root"); c.add_argument("--tasks", type=Path)

    i = cs.add_parser("import-sqlite")
    i.add_argument("case_id"); i.add_argument("source", type=Path); i.add_argument("--sha256", required=True)
    i.add_argument("--device-id", default="DEV-IMPORTED"); i.add_argument("--root")

    for name in ("extract","baseline","review-p5","assist","verify","status"):
        q = cs.add_parser(name); q.add_argument("case_id"); q.add_argument("--root")
        if name == "baseline": q.add_argument("--top-n", type=int, default=20)
        if name == "review-p5": q.add_argument("--max-items", type=int, default=12)
        if name == "assist": q.add_argument("--top-k", type=int)

    t = cs.add_parser("set-tasks")
    t.add_argument("case_id"); t.add_argument("source", type=Path); t.add_argument("--root")

    a = cs.add_parser("archive")
    a.add_argument("case_id"); a.add_argument("--output", type=Path); a.add_argument("--root")
    a.add_argument("--include-evidence", action="store_true")

    return p


def main() -> None:
    args = parser().parse_args()
    try:
        if args.command == "doctor":
            result = doctor(not args.skip_models); _emit(result, args.json)
        elif args.command == "setup-models":
            _emit(setup_models())
        elif args.command == "case":
            cmd = args.case_command
            if cmd == "create":
                _emit(str(create_case(args.case_id,args.title,args.root,args.tasks)))
            elif cmd == "import-sqlite":
                _emit(import_sqlite(args.case_id,args.source,args.sha256,args.root,args.device_id))
            elif cmd == "extract":
                _emit(extract(args.case_id,args.root))
            elif cmd == "baseline":
                _emit(baseline(args.case_id,args.root,args.top_n))
            elif cmd == "review-p5":
                _emit(review_p5(args.case_id,args.root,args.max_items))
            elif cmd == "assist":
                _emit(assist(args.case_id,args.root,args.top_k))
            elif cmd == "verify":
                _emit(verify(args.case_id,args.root))
            elif cmd == "status":
                _emit(status(args.case_id,args.root))
            elif cmd == "set-tasks":
                _emit(str(set_tasks(args.case_id,args.source,args.root)))
            elif cmd == "archive":
                _emit(str(archive(args.case_id,args.output,args.root,args.include_evidence)))
    except (PlatformError, FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"[Libera] ERROR: {exc}") from exc


if __name__ == "__main__":
    main()
