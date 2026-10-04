# Security policy

LIBERA is an **archived research project** (final snapshot `v1.0.0`). It is not a forensic product, is not
maintained for production use, and receives no security updates.

## Reporting

If you find a problem that could expose sensitive material — for example a credential, a device identifier,
private evaluator labels, raw acquisition data or restricted source excerpts in the repository or its history —
please contact the repository owner privately through GitHub (do not open a public issue with the sensitive
details). Include the file path and commit SHA.

## What must never be in this repository

- raw acquisition masters, forensic images or ChatSim SQLite acquisitions (`runtime/`, `demo_evidence/`);
- private ground truth / evaluator labels and their lock files;
- restricted source excerpts (court-record originals are kept in restricted local storage);
- credentials, `.env` files, real phone numbers, IMEI/serial numbers.

`.gitignore` excludes the corresponding paths. During the archival cleanup (2026-10-05) every blob reachable
from any branch was screened for common secret signatures (cloud keys, private keys, GitHub/Slack/OpenAI/
Hugging Face tokens, hard-coded passwords) with no hits. This screen is not an exhaustive audit.

## Security-relevant design (summary)

- Local model transport is restricted to loopback and refuses redirects and proxies (`src/ai_rag/local_transport.py`).
- Extraction refuses a working copy whose SHA-256 differs from the acquisition record
  (`src/forensics/extract_artifacts.py --expected-sha256`, `tools/extract_acquired_chatsim.py`).
- Experiment outputs are hash-locked before any evaluator label is read; locks refuse dry-run or
  incomplete executions (`tools/lock_p8_outputs.py`, `src/evaluation/evaluate_experiment.py`).

See [docs/final_state.md](docs/final_state.md) for the security findings and their residual limits.
