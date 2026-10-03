# Shared contract 1.0

Only Coordinator changes this contract. Workers refresh integration before each checkpoint and report contract version in their status. Requests go to requests/Wx_*.md; no unilateral interface changes. Do not inspect evaluator GT or reconstruct labels from case-design assets. Existing public leakage must be reported as a limitation, never hidden by rewriting Git history.

## Terminology
LIBERA: this synthetic-case digital-forensics research project.
digital evidence: acquisition-derived data with traceable provenance and hashes.
acquisition: documented acquisition process, with ACQ-* identifying its package.
device DEV-*: acquisition source; DEV-SIM/DEV-DRY must be disclosed as simulated.
artifact ART-*: normalized P4 examiner evidence, not a synthetic provenance label.
finding FND-*: a claimed inference with cited ART evidence and limitations.
ground truth: evaluator-only reference labels, not examiner evidence.
traditional forensic baseline: P5 deterministic rules independent of LLM.
local LLM: locally executed model; a dry-run stub is not LLM execution.
RAG: retrieval over P4 ART evidence only, supplied to local LLM.
structured forensic output: constrained output schema with claims and evidence references.
supported claim: claim whose content is supported by cited source evidence; ID existence alone is insufficient.
unsupported claim: claim lacking adequate evidence or exceeding its evidence.

## Experiments and pipeline
P5 = traditional deterministic forensic baseline
A = Local LLM only (current implementation receives no case evidence; disclose lower-bound design)
B = Local LLM + RAG
C = Local LLM + RAG + structured forensic output
P2 -> P3 -> P4 -> P5 -> P6 -> P7 -> P8 -> LOCK -> P9 -> P10
B and C share retrieval. No P8 rerun after private GT is opened. An invalidated lock requires a new separately registered study, never silent replacement.

## Existing canonical paths and schema
P2: data/adaptasi_indonesia/corpus_whatsapp_10000.csv (immutable)
P4: runtime/working/P4/artifacts.csv; extraction manifest at same stage; authoritative schema src/forensics/extract_artifacts.py OUTPUT_FIELDS:
evidence_id, artifact_id, acquisition_id, device_id, message_id, conversation_id, segment_id, sender, receiver, timestamp_normalized, message_text, message_type, reply_to_message_id, attachment_id.
P5: src/baseline/traditional_baseline.py; preserve existing output fields pending W1 verified inventory.
P6/P7: src/ai_rag/chunker.py and retriever.py; evidence-only input.
Tasks: configs/investigation_tasks.json; changes require Coordinator approval before benchmark freeze.
P8: runtime/working/P8/experiment_output.json; task_id, question, timestamp, A_llm_only, B_llm_rag, C_llm_rag_structured, retrieval_trace.
LOCK: tools/lock_p8_outputs.py; exact manifest schema to be verified by W3. No gate opens on a stub run.
P9: src/evaluation/evaluate_experiment.py; private GT outside Git and never in handoffs.
P10: src/report/build_report.py; UAS report separate from historical report.
New public executed evidence: docs/08_uas/evidence/Wx/ (synthetic/sanitized only).
Report draft: docs/08_uas/workers/W5_report.md. Governance: docs/08_uas/workers/W4_*.

## Ownership and checkpoints
W1: src/forensics, src/baseline, acquisition/extraction tools, dependency/hygiene/docs foundation. W1 owns workbench; other shared-path changes require request.
W2: security tests, src/security and tools/security*, security documentation. For hardening another owner's source, document exact patch request and obtain Coordinator approval first.
W3: src/ai_rag, src/evaluation, P8/GT locking tools, AI tests/protocol. No GT access before Coordinator gate.
W4: governance/standards/architecture documents and safe protection/tabletop evidence.
W5: literature and report/chapter/formatting assets only. No final result numbers before REPORT_RESULTS_OPEN.
Workers may create uniquely named tests/test_uas_wx_*.py. Historical tests jointly owned; use request.
Workers never write 00_MASTER_STATE.md, 00_SHARED_CONTRACT.md, 01_UAS_COMPLIANCE_MATRIX.md, 07_REPORT_FACT_MATRIX.md, 08_FINAL_QA.md.

## Facts and status
Allowed: CANDIDATE, VERIFIED_BY_WORKER, CANONICAL_VERIFIED, IMPLEMENTED_NOT_EXECUTED, BLOCKED, REJECTED, NOT_APPLICABLE.
Only Coordinator promotes CANONICAL_VERIFIED.
Each handoffs/Wx_FACTS.jsonl line has claim_id, owner, claim, status, source_type, source_path, source_commit, source_sha256, command, observed_value, allowed_report_sections, limitations.
Source commit must exist; commit evidence first, then generate facts in next commit to avoid self-referential hashes. Status records commands, results, changed paths, blockers, source integration SHA, contract version, cross-worker requests and next action.
