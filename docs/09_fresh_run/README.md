# Libera final fresh-run evaluation gate

This directory documents the final fresh local experiment used as the primary empirical source for the report.

The canonical experiment must preserve the frozen P2 corpus and the forensic-first ordering:

```text
P2 frozen corpus
→ P3 controlled acquisition
→ P4 artifact extraction
→ P5 traditional baseline + human QC
→ P6 retrieval
→ P7 local LLM
→ P8 cryptographic output lock
→ post-lock evaluation packets
→ P9 evaluation
→ P10 deterministic report
```

Post-lock evaluation is deliberately separated into:

1. retrieval relevance;
2. citation-reference validity;
3. semantic claim–evidence supportedness;
4. task-component correctness;
5. runtime/reproducibility metadata.

A syntactically valid structured answer is not treated as evidence of semantic correctness, and an existing evidence ID is not treated as proof that the cited artifact supports the associated claim.
