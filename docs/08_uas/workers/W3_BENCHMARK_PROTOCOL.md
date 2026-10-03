# W3 benchmark protocol — CANDIDATE, contract 1.0

No private ground truth was accessed. This protocol is not a completed benchmark.
P8/P9 execution is BLOCKED: Ollama binary is absent and localhost port 11434 refused connection. Do not treat synthetic tests, hashing retrieval smoke tests or schema validation as LLM accuracy.

## Registered design to confirm after W1 stable evidence

Use immutable P4 ART evidence only; checksum extraction, P5 outputs, task configuration and P6/P7 configuration. A has no case evidence (lower-bound abstention condition); B and C share one retrieval per task; C requires seven structured forensic fields. Configured model qwen2.5:1.5b, embedding bge-m3, top-k 8, seed 42, temperature 0.1, context 8192. Availability of these models is unverified. Hashing fallback is harness-only and cannot represent this final design. Fixed seed does not guarantee numerical reproducibility across hardware/runtime.

Before real P8: Coordinator confirms evidence/config/task freeze and installs/runs models on authorized local hardware. Record exact runtime/model digest, embedding provenance and index hash, code SHA, hardware, retrieval outputs and all prompts. Inspect context length; no truncation may silently change B/C evidence. Run A/B/C once per task, disclose latency/quality evidence separately. If any call errors or provenance is absent, do not lock or open GT. Keep a new separately registered run for any changed settings.

Lock tool refuses dry-run/missing conditions/errors/empty outputs/missing model provenance and refuses to overwrite an existing manifest. Manifest hashes P4/P5/config/tasks/P8/run-log. Coordinator independently verifies all hashes and model logs; then alone opens GT gate. An asserted model digest in JSON is not proof of execution without trustworthy runtime evidence.

## Evaluation boundaries

P9 message-level metrics evaluate pooled selected ART citations against acquired labeled message IDs. Retrieval selection and citation selection are separate outcomes; they are not semantic claim truth, complete timeline accuracy or legal proof. Partial GT coverage and acquisition scope must be disclosed. A's no-evidence design cannot support an ordinary equal-evidence accuracy comparison.

For semantic supportedness: freeze a separate human review rubric and claim inventory before results. Two independent reviewers label each case-specific claim supported/unsupported/indeterminate against cited evidence, resolve disagreement transparently and document inter-rater agreement. Valid IDs alone never count as supported. Current software precheck does not implement this review; outputs explicitly mark supportedness NOT_EVALUATED. No groundedness performance claim is permitted until reviewed evidence exists.

## Rerun commands

`python -m pytest tests/test_p6_p7_pipeline.py tests/test_uas_w3_lock_integrity.py -q`

After real P4/P5/index are verified, use `python -m src.ai_rag.run_experiment --index <verified-index> --output runtime/working/P8/experiment_output.json` then `python tools/lock_p8_outputs.py`; Coordinator verifies lock before P9 and private GT access. Never replace placeholder index text with an unverified source. CLI default index is absent: explicitly provide final verified index.
