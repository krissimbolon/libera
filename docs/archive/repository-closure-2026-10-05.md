# Repository closure record — 2026-10-05

> **Status: Archived** · As of: 2026-10-05 · Canonical: No (record of the closure itself)
> Purpose: preserve, inside the repository, what the final cleanup changed and the commit SHAs of every
> development branch before those branches are deleted. Branch pointers are not archival documents; the
> commits below stay reachable from `main`.

## Baseline

| | |
|---|---|
| Original `main` | `3114190dc4d3776921d58e8a08d8bc70c77ffdd2` (merge of PR #22, 2026-10-03) |
| Frozen P2 SHA-256 before | `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6` (10,000 rows) |
| Frozen P2 SHA-256 after | `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6` (10,000 rows) — **unchanged**; `.gitattributes` unchanged |
| CI on original `main` | "Post-P2 Integration Audit" run #115 (`37121835819`) **failed** in the CLI step: the P8 lock (correctly) refused the hashing/dry-run smoke output |

## Branch dispositions

| Branch | Tip SHA | Unique commits vs original `main` | Disposition | Integrated |
|---|---|---:|---|---|
| `libera-presentasi` (PR #16) | `a9cfe3c44865c79b0d33eb47f230dcfae6f63604` | 12 | UNIQUE_AND_USEFUL — actual v6 run docs, citation quarantine, forensic-first workbench, tests, ChatSim UI ID strings | merge `7b45ac3` (semantic conflict resolution, see commit message) |
| `Bab4` | `0e7a92d519b587887911ed6ddc61d61f026fbaef` | 2 (incl. shared `6eae65b`) | UNIQUE_AND_USEFUL — chapter IV results, sandbox evidence, fail-closed ChatSim extractor | merge `4e82520`; Word lock files then removed (`b113ec0`) |
| `p5-finalize-daffa` | `3ccadd065a532a1ed0d8dff5b6190a95637bf699` | 0 | FULLY_CONTAINED (PR #15) | already in `main` |
| `uas-ksi-final` | `c0d9a1c1b1d8f33776a9754a7fac705b77b98a83` | 0 | FULLY_CONTAINED (PR #22) | already in `main` |
| `uas-ksi-w1-forensics` | `db3607f4f1e8f2c62b00ce4f3aa919abfe33d4f7` | 0 | FULLY_CONTAINED (PR #17) | already in `main` |
| `uas-ksi-w2-security` | `bac453e8c7e20c807226233bd6bb768a7c090ab4` | 0 | FULLY_CONTAINED (PR #20) | already in `main` |
| `uas-ksi-w3-llm-evaluation` | `6bfe1afb121aa0fc8ec3de9d23e1b53490d14a85` | 0 | FULLY_CONTAINED (PR #21) | already in `main` |
| `uas-ksi-w4-governance` | `9b5c93da30039eccd2cd1a329090cfaca13c2b76` | 0 | FULLY_CONTAINED (PR #19) | already in `main` |
| `uas-ksi-w5-report` | `48a3676156ec862a89385393b61f3d4c2d3b1c31` | 0 | FULLY_CONTAINED (PR #18) | already in `main` |

After closure every tip above is an ancestor of `main` (`git merge-base --is-ancestor <tip> main`), so
deleting the branch pointers loses no commit. Pull-request heads remain available as `refs/pull/<n>/head`.

## Pull requests and issues

| Item | State before | Final disposition |
|---|---|---|
| PR #1–#12, #14, #15, #17–#22 | merged (heads reachable from original `main`) | none needed |
| PR #16 `libera-presentasi` (draft) | open | integrated by merge `7b45ac3`; GitHub marks it merged once `main` containing `a9cfe3c` is pushed, otherwise close with a link to that merge |
| Issue #13 "final completion tracker" | open, gates unchecked | close with final disposition: gates 1–2 completed on 2026-09-25 with `qwen2.5:1.5b` (not the 7B listed); gates 3–4 not completed as planned (private GT lost; provenance-proxy P9 instead); gate 5 superseded by the archived README/final state |

## File dispositions (development residue)

| Path (original) | Disposition | Result |
|---|---|---|
| `_inspect.py`, `test_llm.py`, `data_synthesizer.py`, `ctdc-synthetic.csv`, `libera_evidence/` (200 CSV) | ARCHIVE_HISTORICAL (v0 prototype, 2026-06-03) | `archive/legacy-v0-synthesizer/` |
| `app.py` | KEEP_CANONICAL (3-line compatibility entry that runs `workbench/libera_workbench.py`) | unchanged |
| `docs/06_report/~$*.docx` (2) | DELETE_DISPOSABLE (editor lock files) | removed |
| `docs/00_project_management/*` | ARCHIVE_HISTORICAL; naming convention KEEP_CANONICAL | `docs/archive/project-management/`, `docs/konvensi_bahasa_dan_penamaan.md` |
| `docs/00_project_management/LIVE_CHECKLIST_PRESENTASI_20260925.md`, `docs/07_demo/*`, `scripts/check_presentation_progress.ps1` | ARCHIVE_HISTORICAL | `docs/archive/presentation-2026-09-25/` |
| 30 P2 working records in `docs/02_case_design/` (batch audits, handoffs, "belum lulus" QA, plans) | ARCHIVE_HISTORICAL | `docs/archive/p2-development/` |
| `final_report_draft.md`, `P6_P7_P8_IMPLEMENTATION_PLAN.md`, `status_p9.md`, `checklist_gate_p9.md` | ARCHIVE_HISTORICAL (superseded) | `docs/archive/superseded/` |
| `docs/03_forensik_persiapan/` | KEEP (consolidated) | `docs/03_forensic_protocol/persiapan_p3_p4/` |
| `docs/08_uas/` | ARCHIVE_HISTORICAL, kept in place (hash-pinned facts, tool output paths) | README added, files unchanged |
| `data/adaptasi_indonesia/*_draft_*.tsv`, `koreksi_*.tsv`, `qa_*.json`, `corpus_whatsapp_working.csv` | KEEP_REPRODUCIBILITY (P2 construction provenance; audit scripts read the working copy) | unchanged, described in `data/README.md` |
| `runtime/`, `demo_evidence/`, ChatSim seed assets, APK | GENERATED_NOT_COMMITTED | `.gitignore` |
| private GT, acquisition masters, Document 547 originals | PRIVATE_NOT_COMMITTED | never in history (all blobs screened) |

## Verification performed for the closure

- `python -m pytest`: 74 passed (Python 3.12, 3.13, 3.14).
- Local emulation of every `LIBERA CI` step on Python 3.12 and 3.14 from clean worktrees: all PASS,
  including the assertion that the P8 lock refuses the smoke output.
- `python tools/check_doc_links.py --paths --include-archive`: 0 broken references.
- Secret-signature screen of all 1,088 blobs reachable from every branch: 0 hits.
- No reachable blob of the reconstruction CSV ever contained verbatim source messages.
