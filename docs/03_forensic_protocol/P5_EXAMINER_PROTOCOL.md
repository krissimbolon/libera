# P5 Examiner QC Protocol — Presentation Timebox <= 5 Minutes

## Purpose

P5 is a deterministic traditional-forensic baseline. The computer performs the full timeline, actor-frequency, pair-frequency, and pre-registered T01-T10 keyword triage. The human examiner does **not** read all acquired messages.

The human step is a short quality-control (QC) review that verifies whether a small deterministic candidate packet is relevant and traceable to P4 ART evidence. It is **not evaluator ground truth**, and it must not be used to tune P5 keywords after seeing results.

## Forensic position

- P4: read-only extraction / examiner-visible ART evidence.
- P5 automated baseline: examination and deterministic triage.
- P5 human QC: limited examiner verification of candidate relevance.
- P5 lock: freezes P4 input, task definitions, baseline outputs, and completed QC before P6-P8 AI-assisted analysis begins.

## Deterministic packet selection

`src.baseline.examiner_packet` selects at most 12 unique evidence items:

1. one unique highest-ranked candidate per T01-T10 where possible;
2. remaining slots are filled deterministically by cross-task coverage, automated keyword score, best rank, timestamp, then evidence ID.

This avoids ad-hoc cherry-picking during the presentation while keeping the human workload small.

## Decision vocabulary

- `SUPPORTED`: the message is a reasonable candidate for the linked investigative question(s);
- `NOT_SUPPORTED`: the candidate is not relevant enough to support the linked question(s);
- `UNCERTAIN`: relevance cannot be decided from that artifact alone.

`NOT_SUPPORTED` and `UNCERTAIN` require a short note. These labels are QC labels only. They are not P9 key-evidence ground truth.

## Time budget

- 00:00-00:20 — read packet scope and integrity summary;
- 00:20-04:20 — review up to 12 evidence rows (~20 seconds each);
- 04:20-04:40 — save decisions;
- 04:40-05:00 — generate and verify P5 cryptographic lock.

If the actual review exceeds five minutes, keep the result and report the measured elapsed time; never fabricate a shorter duration.

## Command

After P4 has produced `artifacts.csv`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_p5_examiner_review.ps1 -ArtifactsPath "<ACQ-SIM folder>\artifacts\artifacts.csv"
```

Outputs:

- `runtime/working/P5/timeline.csv`
- `runtime/working/P5/entities.csv`
- `runtime/working/P5/relationships.csv`
- `runtime/working/P5/baseline_findings.json`
- `runtime/working/P5/baseline_manifest.json`
- `runtime/working/P5/p5_examiner_packet.csv`
- `runtime/working/P5/p5_examiner_packet_manifest.json`
- `runtime/working/P5/p5_lock_manifest.json`

## Non-negotiable rules

1. P5 input must be P4 ART evidence, not the frozen P2 source corpus.
2. Do not expose source reconstruction or evaluator ground truth to P5.
3. Do not change T01-T10 keywords after looking at P5 output for the final run.
4. Do not interpret `SUPPORTED` as legal/factual ground truth.
5. After `p5_lock_manifest.json` is created, do not overwrite P5 outputs.
6. Any rerun must create a new lock and be reported separately.
