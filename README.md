# LIBERA — UAS Digital Forensics Research v2

Research branch for an end-to-end, reproducible digital-forensics UAS project using a local LLM (Ollama), RAG, structured reasoning, and systematic error mitigation.

## Research direction
The project uses a synthetic Indonesian human-trafficking scenario that is structurally adapted from publicly documented communications in a real adjudicated case. Source reconstruction, Indonesian adaptation, forensic acquisition, AI-assisted analysis, and evaluation are kept as distinct layers with explicit provenance.

## Core principles
1. Preserve source provenance and never silently fill missing public-record lines.
2. Keep original/source reconstruction separate from adapted Indonesian synthetic data.
3. Treat acquired WhatsApp artifacts as evidence; do not analyze case-design files as if they were acquired evidence.
4. Keep ground truth hidden from the forensic examiner and AI/RAG pipeline during evaluation.
5. Log hashes, evidence IDs, prompts, model/version, retrieval context, parameters, outputs, and human validation.
6. Use local inference for sensitive forensic evidence.
7. Keep raw/restricted evidence out of the public repository.

## Working branch
`proyek-uas-df`

The legacy prototype on `main` is retained for comparison and migration; it is not the methodological baseline for the v2 study.

## Current phase
P0 Project setup & scope — in progress
P1 Source reconstruction & case design — starting
