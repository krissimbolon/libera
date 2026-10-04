# Contributing

Libera's development phase is **closed**. The repository is kept as an archived, reproducible research snapshot,
so new features and methodology changes are not accepted.

Changes that are still welcome:

- corrections to documentation that is factually wrong about the archived state;
- fixes that keep the documented public pipeline and CI runnable on supported Python versions;
- provenance or licensing clarifications.

Rules that every change must respect (CI enforces the first and fourth):

1. The frozen P2 corpus `data/adaptasi_indonesia/corpus_whatsapp_10000.csv` is never modified
   (SHA-256 `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`).
2. Recorded results, failed runs and invalid model citations are not rewritten or "corrected".
3. Private ground truth, raw acquisitions, credentials and device identifiers are never committed.
4. Fail-closed safeguards (lock refusal, hash checks, loopback-only transport) are not weakened to make tests pass.
5. Historical records under `docs/archive/`, `docs/08_uas/` and `archive/` are not edited except for
   archive banners or link repairs.

Workflow: open a pull request against `main`; the `Libera CI` checks must pass. Run locally with:

```bash
python -m pip install -e ".[test]"
python -m pytest
python tools/check_doc_links.py --paths
```
