# Master Progress Tracker

Updated: 2026-09-23

| ID | Milestone | Primary output | Status | Progress |
|---|---|---|---|---:|
| P0 | Project setup & scope | research design, branch, folder structure, source/provenance rules | IN PROGRESS | 97% |
| P1 | Source reconstruction & case design | 1–543 skeleton, verbatim recoveries, gaps, source registry | IN PROGRESS | 35% |
| P2 | Indonesian synthetic adaptation | adapted actors, events, messages, distractors, ground truth | NOT STARTED | 0% |
| P3 | Seizure & acquisition | seizure record, device documentation, acquisition, hashes | NOT STARTED | 0% |
| P4 | Evidence extraction | structured WhatsApp artifacts, attachments, timestamps, evidence IDs | NOT STARTED | 0% |
| P5 | Traditional forensic baseline | keyword, timeline, entity, relationship analysis | NOT STARTED | 0% |
| P6 | RAG | domain KB, evidence index, provenance-aware retrieval | NOT STARTED | 0% |
| P7 | Local LLM | Ollama model config, prompts, run logs | NOT STARTED | 0% |
| P8 | Experiments | LLM-only vs RAG vs RAG + structured reasoning | NOT STARTED | 0% |
| P9 | Validation & error mitigation | metrics, hallucination audit, SOLVE-IT-inspired error register | NOT STARTED | 0% |
| P10 | Final report | verified findings, limitations, chain of custody, appendices | NOT STARTED | 0% |
| P11 | Presentation/demo | reproducible demo and defense materials | NOT STARTED | 0% |

## P0 completed items
- active research branch: `proyek-uas-df`
- v2 README created
- research questions and evidence flow documented
- provenance rules documented
- public/private evidence boundaries documented
- forensic-safe .gitignore hardened
- resource collection checklist created
- team/environment intake template created
- evidence/artifact ID convention created
- team roles assigned: Chris, Bela, Meldiro, Daffa
- candidate test device recorded: OPPO CPH2819 / Android 16 / Snapdragon 685 / 6 GB RAM

Remaining P0 items:
- confirm acquisition/LLM workstation details;
- confirm private evidence-storage location;
- confirm remaining device metadata before acquisition (storage, WhatsApp version, test account, timezone, root state).

## P1 completed items
- initialized exact 1–543 reconstruction skeleton
- initialized reconstruction coverage table
- initialized QA review log
- initialized resource intake and source-extraction logs
- source registry created
- provenance validator added
- reconstruction schema test added
- Document 547 ingested as SRC-001 and hashed
- initial Exhibit 1A line-reference scan completed
- internal source-reference anomalies identified and documented
- explicit rule: no LLM gap filling during source reconstruction

Next P1 action:
- extract message clusters into a restricted reconstruction workspace;
- map only unambiguous messages to original lines;
- keep contradictory/ambiguous line references unresolved;
- seek corroboration from Docs. 382, 427, 512, exhibit lists, or Exhibit 1A;
- calculate verified (not merely referenced) public-record coverage.

## Parallel team task
Collect additional court records, authoritative human-trafficking domain sources, and workstation metadata using `docs/00_project_management/resource_collection_checklist.md`.

## Team roles
- Chris — Member A — Digital Forensics Lead
- Bela — Member B — Case & Data Lead
- Meldiro — Member C — AI/RAG Lead
- Daffa — Member D — Validation & Documentation Lead
