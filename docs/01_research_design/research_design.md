# Research Design

## Working title
Local LLM-Assisted Digital Forensic Investigation of Synthetic Human-Trafficking Evidence Using RAG and Structured Reasoning

## Research questions
- RQ1: How effectively can a local LLM identify relevant evidence from synthetic WhatsApp evidence?
- RQ2: Does RAG improve groundedness and evidence attribution compared with a local LLM without RAG?
- RQ3: Does structured reasoning improve understandability and verifiability of the analysis?
- RQ4: What errors arise across acquisition, preprocessing, retrieval, and inference, and how can they be mitigated?
- RQ5: How consistent are AI-assisted findings with ground truth and a traditional forensic baseline?

## Experimental separation
Case-design/source materials and ground truth are not available to the blinded forensic/AI analysis pipeline.

## Evidence logic
Public court record -> source reconstruction -> Indonesian synthetic adaptation -> WhatsApp test-device simulation -> forensic acquisition -> extraction -> baseline/RAG/LLM analysis -> human verification -> reporting.

## Important terminology
- Source reconstruction: what can be recovered from public records, including explicit gaps.
- Adapted synthetic scenario: Indonesian fictionalized data derived structurally from public source material.
- Acquired evidence: artifacts obtained from the test WhatsApp device during the forensic workflow.
- Ground truth: evaluator-only mapping of expected actors, events, relationships, relevant messages, and planted distractors.
