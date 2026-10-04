# Documentation map

Libera contains an operational beta platform plus a preserved research benchmark. Start with the operational platform guide for casework or the research summaries for reproducibility. Detailed historical records are mostly in Indonesian; anything under **Historical archive** describes an intermediate state and is not instructions.

## Current documentation

| Topic | Document |
|---|---|
| **Operational platform (install-once, case-isolated)** | [10_product_platform/README.md](10_product_platform/README.md) |
| **Final research state, results and limitations** | [final_state.md](final_state.md) |
| **How to reproduce (public / local / private tiers)** | [reproducibility.md](reproducibility.md) |
| Research design and research questions | [01_research_design/research_design.md](01_research_design/research_design.md) |
| Methodology references | [01_research_design/methodology_references.md](01_research_design/methodology_references.md) |
| P1 source reconstruction (Document 547) | [02_case_design/P1_source_reconstruction_protocol.md](02_case_design/P1_source_reconstruction_protocol.md), [P1_reconstruction_QA.md](02_case_design/P1_reconstruction_QA.md), [sumber_kerja_kanonik_document_547.md](02_case_design/sumber_kerja_kanonik_document_547.md), [resolusi_anomali_document_547.md](02_case_design/resolusi_anomali_document_547.md) |
| P2 synthetic case design | [02_case_design/desain_dataset_10000_pesan_indonesia.md](02_case_design/desain_dataset_10000_pesan_indonesia.md), [peta_lokalisasi_kasus_indonesia.md](02_case_design/peta_lokalisasi_kasus_indonesia.md), [peta_kronologi_generasi.md](02_case_design/peta_kronologi_generasi.md), [kontrak_gaya_percakapan.md](02_case_design/kontrak_gaya_percakapan.md) |
| P2 final QA and freeze | [02_case_design/laporan_qa_corpus_10000.md](02_case_design/laporan_qa_corpus_10000.md), [qa_global_actor_state_final.md](02_case_design/qa_global_actor_state_final.md), [qa_integrasi_500_jangkar.md](02_case_design/qa_integrasi_500_jangkar.md) |
| Evidence IDs and examiner protocol (P3–P5) | [03_forensic_protocol/evidence_id_convention.md](03_forensic_protocol/evidence_id_convention.md), [P5_EXAMINER_PROTOCOL.md](03_forensic_protocol/P5_EXAMINER_PROTOCOL.md) |
| Acquisition preparation, tooling, custody templates | [03_forensic_protocol/persiapan_p3_p4/](03_forensic_protocol/persiapan_p3_p4/README.md), [FINAL_ACQUISITION_CHECKLIST.md](03_forensic_protocol/persiapan_p3_p4/FINAL_ACQUISITION_CHECKLIST.md) |
| ChatSim evidence carrier | [../apps/libera-chatsim/README.md](../apps/libera-chatsim/README.md) |
| AI methodology (P6–P8) | [04_ai_methodology/ai_methodology.md](04_ai_methodology/ai_methodology.md), [P6_P7_P8_README.md](04_ai_methodology/P6_P7_P8_README.md) |
| Reported P8 run (v6, 2026-09-25) | [04_ai_methodology/P8_REAL_RUN_20260925.md](04_ai_methodology/P8_REAL_RUN_20260925.md) |
| P9 citation policy and proxy evaluation | [05_validasi/P9_CITATION_POLICY_20260925.md](05_validasi/P9_CITATION_POLICY_20260925.md), [GT_RECONSTRUCTION_P9_P10_20260925.md](05_validasi/GT_RECONSTRUCTION_P9_P10_20260925.md) |
| Planned human evaluation instruments (not executed) | [05_validasi/README.md](05_validasi/README.md), [protokol_evaluasi_blind.md](05_validasi/protokol_evaluasi_blind.md), [rubrik_evaluasi_p9.md](05_validasi/rubrik_evaluasi_p9.md), [template_evaluasi_temuan.md](05_validasi/template_evaluasi_temuan.md), [register_error_solve_it.md](05_validasi/register_error_solve_it.md) |
| Results of the local run | [06_report/RESULTS_LOCAL_20260925.md](06_report/RESULTS_LOCAL_20260925.md) |
| UAS chapter IV (security, tamper exercise, evaluation) | [06_report/BAB_IV_UAS_KSI_KELOMPOK_2.md](06_report/BAB_IV_UAS_KSI_KELOMPOK_2.md), [UAS_KSI_STRUKTUR_LAPORAN.md](06_report/UAS_KSI_STRUKTUR_LAPORAN.md), figures in [bab4_run_figures/](06_report/bab4_run_figures/README.md), [uas_figures/](06_report/uas_figures/README.md) |
| Examiner workbench (Streamlit) | [06_report/STREAMLIT_CHATSIM.md](06_report/STREAMLIT_CHATSIM.md) |
| Sources, models, licences | [../references/source_registry.csv](../references/source_registry.csv) |
| Language and naming convention | [konvensi_bahasa_dan_penamaan.md](konvensi_bahasa_dan_penamaan.md) |

## Historical archive

Preserved for provenance and audit trail. Each moved file starts with a status banner (as-of date,
original path, what supersedes it). Content is unchanged apart from repaired relative links.

| Folder | Contents |
|---|---|
| [archive/project-management/](archive/project-management/) | Progress trackers, team/environment intake, resource checklists |
| [archive/p2-development/](archive/p2-development/) | P2 batch audits, handoffs, intermediate QA ("belum lulus") and production plans before the 2026-09-24 freeze |
| [archive/presentation-2026-09-25/](archive/presentation-2026-09-25/) | Live checklist, runbook, outline and 10-minute flow for the 25 Sep presentation |
| [archive/superseded/](archive/superseded/) | Superseded report draft, P6–P8 plan, pre-run P9 status and gate checklist |
| [archive/repository-closure-2026-10-05.md](archive/repository-closure-2026-10-05.md) | Record of the final cleanup: branch tip SHAs, PR/issue and file dispositions, verification |
| [08_uas/](08_uas/README.md) | UAS integration record (2026-10-03): coordinator contract, worker reports, hashed facts and evidence. Kept in place, unchanged. |
| [../archive/legacy-v0-synthesizer/](../archive/legacy-v0-synthesizer/README.md) | 2026-06-03 v0 prototype and its data; not part of the final method |

Git history and closed pull requests are the remaining archival record of development branches; see
[../CHANGELOG.md](../CHANGELOG.md) for milestones.
