# Research Design

## Working title
Offline-First Digital Forensic Examination of Synthetic Conversational Evidence with Local AI Assistance, RAG, and Evidence Validation

## Research objective
LIBERA studies how local AI assistance can be inserted **after** acquisition and traditional forensic examination while keeping analytical claims traceable to acquired artifacts. The project is forensic-first: AI is an optional examiner aid, not the evidence source and not a replacement for examiner judgment.

## Research questions
- **RQ1 — Forensic workflow:** Can a controlled Android conversational evidence source be acquired, preserved, extracted, and examined in a reproducible local workflow with traceable artifact identifiers?
- **RQ2 — Evidence assistance:** When AI is introduced after acquisition, how does evidence retrieval change the relationship between model answers and the acquired artifacts compared with an LLM-only control?
- **RQ3 — Structured output:** Does forcing a structured forensic-oriented output improve auditability, and does syntactic validity guarantee valid evidence references?
- **RQ4 — Failure modes:** What failures occur across acquisition, extraction, retrieval, model inference, citation, and reporting, and how are those failures detected rather than silently corrected?
- **RQ5 — Examiner role:** How can a traditional examiner baseline, human QC, cryptographic output locks, and post-run citation validation constrain the use of probabilistic local LLM outputs?

Independent human semantic ground truth was planned but was not completed. Therefore the current study does **not** claim final semantic precision/recall/F1 for key forensic evidence. Provenance-proxy evaluation is reported only as an auxiliary design-reference analysis.

## Forensic workflow
1. **Case design (P1–P2)** — public source reconstruction is adapted into a frozen Indonesian synthetic WhatsApp-style scenario.
2. **Identification** — `DEV-SIM-001` identifies the controlled ChatSim Android evidence carrier used for the research simulation.
3. **Preservation** — acquisition creates master and working copies; SHA-256 values are verified before examination.
4. **Collection** — `ACQ-SIM-001` performs controlled logical acquisition of the ChatSim app-private SQLite database.
5. **Examination** — P4 extracts normalized `ART-*` artifacts; P5 performs deterministic search/timeline/actor analysis and time-boxed human examiner QC; P6 performs local evidence retrieval.
6. **Analysis** — P7/P8 use local Qwen2.5 with three experimental conditions: A without case evidence, B with retrieved evidence, and C with the same retrieval plus structured output.
7. **Validation overlay** — P5 and P8 outputs are locked; P9 validates evidence identifiers and traceability. Invalid model references are quarantined and remain part of the reported result.
8. **Presentation** — P10/Workbench present evidence, examiner findings, AI-assisted outputs, validation status, and limitations.

## A/B/C interpretation
- **A — LLM without case evidence:** negative control. It measures what the model produces when asked an investigation question without access to acquired case artifacts.
- **B — LLM + RAG:** local BGE-M3 retrieval supplies evidence context from the acquired artifact set.
- **C — same retrieval as B + structured output:** tests whether a constrained machine-readable answer is easier to inspect and verify.

The final run showed why these conditions must not be interpreted as a simple ranking. Condition C produced 10/10 schema-valid structured outputs, yet only 12 of 24 submitted evidence references were valid. Structured format therefore improved regularity but did not guarantee evidentiary correctness.

## Evidence separation
- Frozen P2 case-design data is immutable downstream.
- Source reconstruction and design provenance are not examiner evidence.
- P4 acquired artifacts are the downstream evidence input.
- P5 traditional examination and human QC occur before AI-assisted analysis.
- P8 outputs are locked before post-run validation.
- Ground-truth-like design metadata is not exposed to P5/P6/P7/P8.
- Invalid citations are preserved as errors; they are never rewritten into valid evidence IDs after the result is known.

## Important terminology
- **Source reconstruction:** information recoverable from public source records, including documented gaps.
- **Synthetic case:** fictionalized Indonesian WhatsApp-style conversation data derived structurally from public material.
- **ChatSim evidence carrier:** researcher-controlled Android application/emulator used to demonstrate repeatable logical acquisition. It is not WhatsApp.
- **Acquired evidence:** artifacts extracted from the acquired ChatSim SQLite working copy and assigned `ART-*` identifiers.
- **Traditional baseline:** deterministic keyword, timeline, entity, and relationship examination plus time-boxed human QC.
- **AI assistance:** optional post-acquisition retrieval and LLM analysis performed locally.
- **Citation validation:** verification that an AI-provided evidence identifier exists in P4 and, for evidence-assisted conditions, was actually provided to that condition.
- **Provenance proxy:** design-derived anchor/distractor reference used only for auxiliary evaluation; not independent semantic ground truth.

## Scope limitations
- Controlled synthetic case, not a real criminal investigation.
- Controlled logical acquisition, not physical imaging or full-filesystem acquisition.
- Single local LLM/embedding configuration in the final experiment.
- No independent full-corpus semantic ground truth.
- No claim of legal admissibility or validation as a commercial forensic tool.
