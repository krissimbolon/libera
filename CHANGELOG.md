# Changelog

Milestones of the LIBERA research project. Dates are commit dates (UTC+7).

## v1.0.0 — 2026-10-05 · Final archived research snapshot

Repository closure; no new research features.

- Reconciled the two divergent lines of final work into one `main`:
  the 25 September 2026 local v6 run, citation quarantine and forensic-first workbench (PR #16,
  `libera-presentasi`) and the UAS chapter IV results and extractor fix (`Bab4`), on top of the UAS
  integration (PR #17–#22).
- Evaluator merges the v6 citation-quarantine path with the UAS W3 lock hardening; scoring with invalid
  citations now requires the explicit documented policy (`--citation-policy quarantine`).
- CI made green and meaningful: frozen-corpus gate, full test suite, and an assertion that the P8 lock
  **refuses** CI smoke outputs.
- Historical records moved to `docs/archive/` (with status banners) and `archive/legacy-v0-synthesizer/`.
- Added `pyproject.toml`, reproducibility manifest, final-state summary, documentation index, citation and
  community metadata; completed `references/source_registry.csv`.

## 2026-10-03 · UAS integration (PR #17–#22) and chapter IV

- Five worker streams (forensics, security, LLM evaluation, governance, report) with hashed handoff facts
  (`docs/08_uas/`). Trusted-digest P4 extraction, loopback-only transport, recursive GT-field guard,
  fail-closed P8 lock validation.
- Chapter IV (`Bab4`): controlled tamper exercise, ChatSim extractor made fail-closed (F-01/F-02),
  provenance-proxy P9 results reported with limitations.

## 2026-09-25 · Local experiment and presentation

- ChatSim logical acquisition `ACQ-SIM-001` (9,997 artifacts, 25 chats); P5 locked baseline with human QC.
- P8 v6: 30/30 real A/B/C responses (qwen2.5:1.5b, bge-m3), 14/14 lock hashes verified;
  12 of 24 condition-C references invalid and quarantined. Earlier v3–v5 attempts preserved, not merged.
- P9 provenance-proxy evaluation after the original private ground truth was reported lost.

## 2026-09-24 · P2 frozen; P3–P10 pipeline

- `corpus_whatsapp_10000.csv` frozen (`716216f`, SHA-256 `a014a02e…467e6`), status
  `FROZEN_FOR_FORENSIC_SIMULATION`.
- Windows P3–P10 runner, ChatSim Android carrier and CI-built APK.

## 2026-09-23 · P1 source reconstruction

- Document 547 line-level reconstruction metadata (verbatim text kept private) and 500 adapted anchors.

## 2026-06-03 · v0 prototype

- Initial synthesizer prototype (now `archive/legacy-v0-synthesizer/`; not part of the final method).
