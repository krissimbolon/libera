# Legacy v0 synthesizer (archived — not the Libera pipeline)

> **Status: Archived** · As of: 2026-06-03 (commit `4885648`, "rilis awal") · Canonical: **No**
> Superseded by: the P1 → P2 frozen corpus (`data/adaptasi_indonesia/corpus_whatsapp_10000.csv`) and the
> ChatSim → acquisition → ART → examination → AI/evaluation pipeline described in the root [README](../../README.md).
> Purpose: historical provenance of the project's first prototype. **Nothing here is used by the current pipeline,
> the frozen P2 corpus, the tests, or CI.**

This folder preserves the first prototype committed on 2026-06-03, before the research design was rebuilt around a
court-record-anchored synthetic case (P1/P2) and a controlled Android acquisition carrier (ChatSim). The files were
moved here unchanged (`git mv`) during the final archival cleanup (2026-10-05) so that they are not mistaken for the
current workflow.

| File | Original path | What it was |
|---|---|---|
| `data_synthesizer.py` | `/data_synthesizer.py` | v0 generator: mixed an anonymized WhatsApp-structure dataset with CTDC trafficking patterns into 200 CSV "evidence" files plus a hidden ground-truth folder. |
| `libera_evidence/` (200 CSV) | `/libera_evidence/` | v0 generator output ("blind evidence" without label columns). The matching `libera_ground_truth/` was never committed (see `.gitignore`). |
| `ctdc-synthetic.csv` | `/ctdc-synthetic.csv` | Third-party input: Counter-Trafficking Data Collaborative (CTDC) global synthetic dataset. |
| `test_llm.py` | `/test_llm.py` | Manual Ollama connectivity check against `gemma:2b` (pre-research smoke script; not a pytest test). |
| `_inspect.py` | `/_inspect.py` | One-off PDF text probe for a dialogue-inspiration source considered in v0. The PDF was never committed. |

## Historical prototype datasets — retained for provenance

| Input | Identified source | Licence / redistribution status |
|---|---|---|
| `ctdc-synthetic.csv` | CTDC (IOM / partners) global synthetic dataset, <https://www.ctdatacollaborative.org/> | **Not verified** during archival. Check CTDC terms of use before reusing or redistributing. |
| WhatsApp structure source (zip, **not committed**) | Likely "WhatsApp Anonymized Privacy-focused Interactions Dataset (WAPI dataset)", Mendeley Data, DOI [10.17632/zsr5dvx6bk.1](https://doi.org/10.17632/zsr5dvx6bk.1) | **Not verified.** `libera_evidence/` is derived from it. |
| Dialogue inspiration (PDF, **not committed**) | A published Indonesian novel named in the v0 script docstring | Copyrighted work; no text from it is stored in this repository. |

These files are intentionally retained in the default branch as historical prototype provenance. Their inclusion does not make them part of the final experimental dataset, and no unverified redistribution right is claimed. They carry no evidentiary role in Libera's final results.


### Relationship to the final Libera dataset

These legacy files are intentionally retained, but they are **not the evidentiary basis of the final Libera study**. The canonical P1/P2 synthetic case was later reconstructed independently from the open U.S. federal court record **United States v. Matthew Woods, No. 17-CR-1235-WJ, Document 547**, then fictionalized/localized for the Indonesian research scenario. See `data/README.md` and `references/source_registry.csv`. The CTDC/WAPI materials remain labelled as third-party historical prototype material rather than being misrepresented as researcher-created data.
