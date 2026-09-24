# Presentation Outline — LIBERA

## Slide 1 — Problem & contribution
- Digital-forensic chat volume is large; LLMs can help but hallucination/provenance are risks.
- Contribution: end-to-end synthetic WhatsApp forensic workflow with local LLM, RAG, evidence citations, and blind evaluation.

## Slide 2 — Research design
- Public source reconstruction -> Indonesian synthetic scenario -> acquisition -> ART extraction -> baseline/RAG/LLM -> blind evaluation.
- Stress separation between case design, examiner evidence, and evaluator ground truth.

## Slide 3 — P2 frozen corpus
- 10,000 messages; 500/1,500/6,500/1,500 composition.
- QA passed; canonical SHA-256 pinned.
- P2 is immutable.

## Slide 4 — P3/P4 forensic integrity
- DEV -> ACQ -> ART traceability.
- Chain of custody, SHA-256, master vs working copy.
- Explain whether demo uses ACQ-DRY-001 or real ACQ-001.

## Slide 5 — P5 baseline
- Deterministic keyword search, timeline, actors, communication pairs.
- Baseline locked before AI evaluation.

## Slide 6 — P6/P7 local RAG
- BGE-M3 local multilingual embeddings.
- Qwen2.5-7B through Ollama.
- ART evidence IDs included in chunk context and model citations.

## Slide 7 — P8 A/B/C experiment
- A: LLM-only.
- B: LLM + RAG.
- C: B + structured forensic schema.
- Same T01–T10; B/C share same retrieval.

## Slide 8 — P9 evaluation
- Output lock before ground truth.
- Citation validity + TP/FP/TN/FN, precision, recall, F1, specificity.
- Show actual metrics only after local run.

## Slide 9 — Error analysis & limitations
- Retrieval miss vs inference hallucination vs unsupported citation.
- Synthetic-case limitation and acquisition-mode disclosure.

## Slide 10 — Demo & conclusion
- Run one T-task.
- Show retrieval trace -> ART IDs -> model finding.
- Show P10 runtime report.
- Conclude from measured results, not from model reputation.
