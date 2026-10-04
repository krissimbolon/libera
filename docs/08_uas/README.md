# UAS integration record (2026-10-03) — archived

> **Status: Archived** · As of: 2026-10-03 (PR #17–#22, merge `3114190`) · Canonical: **No**
> Superseded by: [docs/final_state.md](../final_state.md) for the project's final state and results.
> Purpose: historical audit trail of the UAS (final-exam) integration: coordinator contract, five worker
> streams (W1 forensics, W2 security, W3 LLM evaluation, W4 governance, W5 report), hashed handoff facts and
> their executed evidence.

This folder is kept **in place and byte-for-byte unchanged** because its handoff facts
(`handoffs/W*_FACTS.jsonl`) pin `source_path` + `source_commit` + `source_sha256`, and two tools
(`tools/security_uas_audit.py`, `tools/security_uas_owner_retest.py`) write to `evidence/W2/` by default. Moving
or editing these files would break those references.

How to read it correctly:

- Gate values such as `BLOCKED`, `CLOSED` and "real P8/P9 BLOCKED" in `00_MASTER_STATE.md` describe what the
  **UAS coordinator environment** could verify on 2026-10-03 (no Ollama, no PowerShell, no access to the team's
  local runtime). They are not a statement that the team never ran P8.
- The UAS integration branch was created from commit `62f8088` and therefore did not contain the
  25 September 2026 local run (`libera-presentasi`, PR #16). Both lines of work were reconciled on the final
  `main`; see [docs/final_state.md](../final_state.md) §"Source-of-truth reconciliation".
- `workers/W5_report.md` is a *candidate* report draft. The later chapter IV text is in
  [docs/06_report/BAB_IV_UAS_KSI_KELOMPOK_2.md](../06_report/BAB_IV_UAS_KSI_KELOMPOK_2.md).
- Every fact can be re-checked with `git show <source_commit>:<source_path> | sha256sum`.
