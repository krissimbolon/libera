# W3 status

Status: BLOCKED (real P8 and P9); implemented harness fixes VERIFIED_BY_WORKER.
Contract version: 1.0.
Integration source commit: 5b13f4bd2c0d017f3a015a7b7b47657bb411590a.
GT access: CLOSED, no GT files read. Benchmark protocol CANDIDATE until W1 evidence stable and authorized real model execution.

Owned paths: src/ai_rag/ollama_runner.py, src/evaluation/evaluate_experiment.py, tools/lock_p8_outputs.py, tests/test_uas_w3_lock_integrity.py and docs/08_uas W3 files.

Checks: `python -m pytest tests/test_p6_p7_pipeline.py tests/test_uas_w3_lock_integrity.py -q` — 16 passed; synthetic harness only. Unit discovery 7 passed. Legacy unittest discovery 0 because historical suite is pytest; do not count that as a passed suite.

Exact blocker: no ollama binary; HTTP localhost:11434/api/tags refused connection. No model downloads attempted. No actual LLM calls, final performance metrics, private GT evaluation or valid real P8 lock produced.

Fixes: prevent stub/error/incomplete/provenance-free P8 lock and overwrite; verify all manifest inputs before GT; reject integrity failure before GT read; exact model tag digest lookup; structured scalar JSON no longer crashes; clearly disclose semantic supportedness NOT_EVALUATED.

Cross-worker request: Coordinator approved W2 loopback Ollama guard for W3-owned sources; awaiting W2 patch details. No other worker source edits.

Next: Coordinator integrates foundation then independently verifies W3 fixes; prepare authorized local real runtime and freeze design before actual P8. Final blind P9 is blocked until GT gate opens.
