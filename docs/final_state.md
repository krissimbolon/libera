# LIBERA — final state (v1.0.0, 2026-10-05)

**Status: development closed · archived research snapshot · canonical.** This page is the single
English summary of what LIBERA did, what it found, and what it did not establish. Where it cites a
number, the "Source" column names the document that records it. Detailed records remain in Indonesian.

## 1. What the project is

LIBERA is a controlled digital-forensics study. A synthetic Indonesian WhatsApp-style case (P1–P2) is
loaded onto a researcher-controlled Android carrier (LIBERA ChatSim, `DEV-SIM-001`), logically
acquired with SHA-256 preservation (P3), extracted into `ART-*` artifacts (P4) and examined with a
traditional baseline plus human QC (P5). Only after that, local AI assistance is tested (P6–P8) and
its output is locked and validated against the acquired evidence (P9) before reporting (P10).

Research question: *can local AI assistance be inserted after acquisition and traditional examination
while keeping every analytical claim traceable to acquired evidence?* Sub-questions RQ1–RQ5 are in
[01_research_design/research_design.md](01_research_design/research_design.md).

## 2. Canonical facts

| Stage | Final value | Source |
|---|---|---|
| P2 corpus | `data/adaptasi_indonesia/corpus_whatsapp_10000.csv`, 10,000 rows, SHA-256 `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`, `FROZEN_FOR_FORENSIC_SIMULATION` (frozen 2026-09-24, commit `716216f`) | `data/adaptasi_indonesia/corpus_freeze_manifest.json`; CI gate |
| P2 provenance mix | 500 anchors adapted from the Document 547 court record (no verbatim text), 6,500 context, 1,500 bridge, 1,500 distractor messages | freeze manifest; [02_case_design/laporan_qa_corpus_10000.md](02_case_design/laporan_qa_corpus_10000.md) |
| P3 acquisition | `ACQ-SIM-001`, logical copy of ChatSim's app-private SQLite via ADB `run-as` on an Android emulator; master = working SHA-256 `6101c21bf0604566afb1b5af7544eba1140b8ab0165f7a32f481f5c83b2be8cc` | [06_report/BAB_IV_UAS_KSI_KELOMPOK_2.md](06_report/BAB_IV_UAS_KSI_KELOMPOK_2.md) §4.1.1 |
| P4 extraction | 9,997 message artifacts, 25 chats, `integrity_check = ok`, 0 FK errors; `artifacts.csv` SHA-256 `8b3ded048ecc53fede0446e15c372c0cf3783eb4d5271da14e89495e199b624f`. 10,000 − 9,997: the seed builder (`tools/build_demo_seed.py`) excludes 3 anchor messages in which neither endpoint is the device owner (`AKT-RAKA`) and lists them in `source_anomalies.jsonl`; chapter IV reports the gap without attributing a cause. | Bab IV §4.1.1; [04_ai_methodology/P8_REAL_RUN_20260925.md](04_ai_methodology/P8_REAL_RUN_20260925.md); `build-chatsim-final.yml` |
| P5 baseline | 10 tasks, 26 actors, 25 relations; locked before AI; examiner QC of 12 candidates: 6 supported, 4 not supported, 2 uncertain | Bab IV §4.1.2; P8_REAL_RUN |
| P6 retrieval | 645 chunks, BGE-M3 (1,024-dim) via local Ollama; leakage check PASS | P8_REAL_RUN |
| P8 run (v6) | 2026-09-25, `qwen2.5:1.5b`, temperature 0.1, seed 42, context 8,192, top-k 8, output 2,048 tokens, repeat penalty 1.2 / window 256, prompt `v6-forensic-grounded-repeat-control`; 30/30 real responses, 0 transport errors, 30/30 normal stops, 10/10 C outputs schema-valid; output SHA-256 `431bdae950a8df440a6f0d38c1ef0fd3a279ff1bff39cc34cef0a845c98399b9`; lock 14/14 hashes verified | P8_REAL_RUN |
| Earlier P8 attempts | v3, v4, v5 stopped (malformed JSON, `done_reason=length`, repetition). Preserved, not merged, not reported as results. | P8_REAL_RUN §"Percobaan yang dihentikan" |

## 3. Findings

### 3.1 Citation integrity (no ground truth involved)

| | A (no evidence) | B (retrieval) | C (retrieval + JSON schema) |
|---|---:|---:|---:|
| Reference occurrences submitted | 0 | 10 | 24 |
| Valid and supplied to that condition | 0 | 10 | 12 |
| Quarantined (kept visible as model errors) | 0 | 0 | 12 |
| Identifier validity | n/a | 100 % | 50 % |

Source: [05_validasi/P9_CITATION_POLICY_20260925.md](05_validasi/P9_CITATION_POLICY_20260925.md),
[06_report/RESULTS_LOCAL_20260925.md](06_report/RESULTS_LOCAL_20260925.md).
Affected C tasks: T01, T02, T03, T04, T07, T08. **A valid JSON schema did not guarantee valid evidence
references.** Model outputs were not edited; the quarantine policy was added after the P8 audit and
before any label was opened, and is disclosed as a post-experiment change.

### 3.2 Provenance-proxy evaluation (auxiliary; not semantic accuracy)

The original private semantic ground truth was reported lost on the team workstation and was **not**
recreated. A deterministic proxy was built from P2 provenance only: adapted anchors = 1, designed
distractors = 0, context/bridge unlabeled. Labeled universe 1,997 messages (497 acquired anchors +
1,500 distractors). The metric measures *anchor vs. designed distractor selection*, not key-evidence
accuracy, and the policy was chosen after P8 outputs were seen (not preregistered, not blind).

| Prediction set | TP | FP | FN | TN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| P5 baseline | 45 | 24 | 452 | 1,476 | 0.652 | 0.091 | 0.159 |
| A citations | 0 | 0 | 497 | 1,500 | undefined (0 by convention) | 0 | 0 |
| B citations | 0 | 3 | 497 | 1,497 | 0 | 0 | 0 |
| C citations | 1 | 1 | 496 | 1,499 | 0.500 | 0.002 | 0.004 |
| B retrieval | 137 | 107 | 360 | 1,393 | 0.561 | 0.276 | 0.370 |

Source: [05_validasi/GT_RECONSTRUCTION_P9_P10_20260925.md](05_validasi/GT_RECONSTRUCTION_P9_P10_20260925.md),
Bab IV §4.4. Status `P9_RECONSTRUCTED_PROXY_EVALUATION_COMPLETE_WITH_CITATION_ERRORS`.

### 3.3 Evidence-integrity and security findings

| ID | Finding | Fix (on `main`) | Residual limit |
|---|---|---|---|
| F-01 / SEC-001 | A structurally valid but content-modified SQLite working copy passed extraction | Extraction requires the acquisition record's SHA-256 (`extract_artifacts.py --expected-sha256`; ChatSim extractor checks `working_sha256`) | An actor able to replace both file and manifest is not detected; needs protected custody records |
| F-02 | ChatSim extraction ran without an acquisition manifest (`UNKNOWN` identity) | Manifest mandatory; fail closed | Manifest is hashed, not signed |
| F-03 | 12/24 structured-output references invalid | Exact-ID quarantine; no credit, errors reported | Containment only; the model still produces them |
| SEC-002 | Model transport accepted arbitrary hosts | Loopback-only, no redirects/proxies | Does not authenticate the local service |
| SEC-003 | GT-field guard checked only top-level keys | Recursive forbidden-field check | Detects keys, not leaked knowledge in prose |

Sources: Bab IV §4.2–4.3; `docs/08_uas/workers/W2_SECURITY_REPORT.md`; regression tests in `tests/`.
Governance work (DPIA-style analysis, 19 ISO/IEC 27002 control mappings, 5 audit findings) is an
academic exercise recorded in `docs/08_uas/workers/W4_GOVERNANCE.md`; it is not a certification or
an institutional deployment.

### 3.4 Answer to the research question (bounded)

The workflow kept AI downstream of acquisition and examination, and every AI citation could be checked
against acquired `ART-*` identifiers; invalid ones were detected rather than silently accepted. Local
retrieval supplied evidence that B cited validly, but structured output (C) did not by itself produce
valid citations. There is **no basis** in this study to claim that RAG or structured output is more
accurate semantically, because independent semantic ground truth is not available.

## 4. Not established / limitations

- Synthetic case; controlled ChatSim carrier on an emulator — **not** WhatsApp, not a seized device, not
  physical or full-file-system acquisition.
- One local model/embedding configuration; small model (1.5B); single run per condition.
- No independent semantic ground truth; human claim-level supportedness review not performed.
- The public corpus carries `source_provenance` labels, so strict evaluator blindness cannot be claimed
  for anyone with repository access.
- Incident tabletop with real participants, signed ethics/RoE, and the final rendered UAS report are not
  part of this repository.
- Not validated as a forensic tool; no legal-admissibility claim.

## 5. Source-of-truth reconciliation

Two lines of final work diverged from commit `acb52e4` (PR #15):

1. `libera-presentasi` (PR #16, 2026-09-25): the real v6 run, citation quarantine, forensic-first
   workbench and their tests, plus `Bab4` (2026-10-03): chapter IV results and the ChatSim extractor fix.
2. UAS integration (PR #17–#22, 2026-10-03), created from `62f8088` *before* the v6 run was committed.
   Its `docs/08_uas/00_MASTER_STATE.md` records "real P8/P9 BLOCKED" because the coordinator environment
   had no Ollama and no access to the team's local runtime.

Both are merged on the final `main` (merge commits `7b45ac3`, `4e82520`). Where they overlapped:

- **Results:** the 25 September local run (§2–3) is canonical. The UAS "BLOCKED" gates are historical
  statements about what that environment could verify; they are not contradicted findings.
- **Evaluator code:** v6 quarantine + UAS W3 hardening. Private-label scoring when any citation is invalid
  is refused by default and allowed only with `--citation-policy quarantine` (`run_p9_final.ps1
  -CitationPolicy quarantine`), the documented policy used on 2026-09-25.
- **Configuration:** the prompt text in the code had already become v6 on the presentation line, while
  `configs/p6_p7_config.json` and the CLI defaults still carried the v2 label. At archival the registered
  config (v1.1.0) and defaults were aligned with the executed v6 parameters (§2); the v2 baseline is kept in
  the config's `history` block. The v6 run itself was locked against its own run-specific
  `run_config.json` (private runtime).

## 6. What can be verified from the public repository

| Verifiable publicly | Requires the team's private/local artifacts |
|---|---|
| Corpus hash/row count; all code paths with synthetic data; lock refusal of dry-runs; citation-quarantine logic; extractor fail-closed behaviour; Bab IV sandbox hashes of the extractor and harness | `ACQ-SIM-001` SQLite master/working copies, `artifacts.csv`, P5 lock, P6 index, P8 v6 outputs/lock/logs, P9 proxy reference and outputs (`demo_evidence/`, `runtime/` — never committed) |

The v6 lock was produced and verified (14/14) with the 2026-09-25 tooling. The stricter registered-
execution validator added later (UAS W3) has **not** been re-run against those private files in this
archive. Re-verifying with final `main` may refuse it if its run-specific config lacks registered
fields; the exact 2026-09-25 evaluator is preserved in Git (`a9cfe3c`) and, per the run notes, as a code
snapshot next to the private outputs.

Reproduction instructions: [reproducibility.md](reproducibility.md).
