# Data

Status of every data folder in the archived snapshot. Nothing here is acquired evidence: acquisitions and
runtime outputs live outside Git (`demo_evidence/`, `runtime/`), and no private evaluator labels are stored.

| Path | Status | Contents |
|---|---|---|
| `adaptasi_indonesia/corpus_whatsapp_10000.csv` | **Canonical, frozen** | P2 corpus, 10,000 rows, SHA-256 `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6` (see `corpus_freeze_manifest.json`) |
| `adaptasi_indonesia/corpus_freeze_manifest.json` | Canonical | Freeze record: hash, counts, provenance mix, structural checks |
| `adaptasi_indonesia/corpus_whatsapp_working.csv` | Reproducibility | Byte-identical to the frozen corpus; the path read by the P2 audit/construction scripts in `src/` |
| `adaptasi_indonesia/anchor_indonesia_500.csv`, `jangkar_500/` | Reproducibility | The 500 adapted anchors (`anchor_sha256` in the freeze manifest). `jangkar_500/manifest.json` records an earlier byte serialization (combined `63eeaac8…`); the 500 logical rows are identical and the difference is documented in `docs/02_case_design/laporan_qa_corpus_10000.md` |
| `adaptasi_indonesia/*_draft_*.tsv`, `koreksi_*.tsv` | Construction provenance | Hand-authored context/bridge/distractor drafts and manual dialogue/timing corrections used to build the corpus before the freeze |
| `adaptasi_indonesia/qa_*.json`, `review_packets/` | Historical QA snapshots | Outputs of construction-time audits and review dispositions. Re-running `src/audit_*.py` regenerates some style counters differently; the committed files are kept as the record of that time |
| `adaptasi_indonesia/registri_aktor_indonesia.csv` | Canonical | Fictional actor registry (used by the ChatSim seed builder) |
| `adaptasi_indonesia/skema_*.csv` | Canonical (schema only) | Header-only schemas; `skema_ground_truth_privat.csv` contains **no labels** |
| `reconstruction/` | P1 metadata | Line-level reconstruction status for Document 547 (all `message_original` fields empty: verbatim text is kept private), coverage, provenance schema |
| `rekonstruksi/` | P1 metadata | Indonesian-language coverage map and anomaly list for the same reconstruction (kept under its original name to preserve references) |
| `evaluasi/` | Templates | Empty P9 evaluation and SOLVE-IT error-register templates; no results were stored here |
| `toy/` | Test fixture | 15-message toy case for the P6–P8 walkthrough |
