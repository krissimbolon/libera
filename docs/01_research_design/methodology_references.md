# Methodology References — LIBERA P3–P10

Dokumen ini memetakan keputusan metode LIBERA ke rujukan teknis/ilmiah yang digunakan.

## Mobile forensics and evidence integrity

1. Ayers, R., Brothers, S., & Jansen, W. (2014). *Guidelines on Mobile Device Forensics*. NIST SP 800-101 Rev. 1. DOI: 10.6028/NIST.SP.800-101r1.
   - Dipakai untuk validation, preservation, acquisition, examination, analysis, dan reporting.
2. Scientific Working Group on Digital Evidence (SWGDE). (2025). *Best Practices for Mobile Device Evidence Collection & Preservation, Handling, and Acquisition*, 18-F-003-2.0.
   - Dipakai untuk dokumentasi state perangkat, chain of custody, perubahan state akibat interaksi, validasi tool, dan acquisition logging.
3. Anglano, C. (2014). *Forensic analysis of WhatsApp Messenger on Android smartphones*. Digital Investigation, 11(3), 201–213. DOI: 10.1016/j.diin.2014.04.003.
   - Dipakai sebagai rujukan korelasi artefak WhatsApp, chronology reconstruction, contacts, dan pesan.

## RAG and embeddings

4. Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. arXiv:2005.11401.
   - Dasar pemisahan parametric memory dan evidence retrieval serta kebutuhan provenance.
5. Chen, J. et al. (2024). *BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation*. arXiv:2402.03216.
   - Dasar pemilihan BGE-M3 untuk retrieval multilingual lokal.

## LLM-assisted digital forensics

6. *ForensicLLM: A local large language model for digital forensics*. Forensic Science International: Digital Investigation, 52(Supplement), 2025, 301872. DOI: 10.1016/j.fsidi.2025.301872.
   - Mendukung pendekatan local LLM, source attribution, dan perhatian terhadap hallucination; digunakan sebagai rujukan metodologis, bukan alasan untuk memaksakan model yang sama pada corpus Indonesia.
7. Yang, A. et al. (2024). *Qwen2 Technical Report*. arXiv:2407.10671; Qwen Team (2024), *Qwen2.5 Technical Report*, arXiv:2412.15115.
   - Qwen2 mendokumentasikan dukungan multilingual termasuk Indonesian/Malay; Qwen2.5 meningkatkan instruction following, structured-data understanding, dan structured output. Ini mendukung pemilihan keluarga Qwen2.5 untuk corpus chat Indonesia; profil final menggunakan `qwen2.5:1.5b` agar eksperimen lokal tetap reproducible dan dapat dijalankan pada workstation praktikum yang terbatas.
8. *Towards a standardized methodology and dataset for evaluating LLM-based digital forensic timeline analysis*. Forensic Science International: Digital Investigation, 54(Supplement), 2025, 301982. DOI: 10.1016/j.fsidi.2025.301982.
   - Mendukung locked experimental protocol, ground truth, dan evaluasi kuantitatif.
9. *Digital forensics in law enforcement: A case study of LLM-driven evidence analysis*. Forensic Science International: Digital Investigation, 54, 2025, 301939.
   - Mendukung penggunaan precision, recall, F1, dan hallucination-oriented evaluation pada data messenger.
10. *Large language models in digital forensics: capabilities, challenges and future directions*. Forensic Science International: Digital Investigation, 56, 2026, 302043.
   - Mendukung human-AI collaboration, reproducibility, explainability, dan perlunya validation framework.

## LIBERA operational mapping

- P3: preserve device state, log examiner interaction, chain of custody, hash master/working copy.
- P4: normalized ART schema; no evaluator-only ground truth enters examiner evidence.
- P5: deterministic keyword/timeline/entity/relationship baseline locked before P9.
- P6: examiner-visible ART only -> evidence-aware chunks -> BGE-M3 -> cosine retrieval.
- P7: local `qwen2.5:1.5b`, seed 42, temperature 0.1, model digest logged when available.
- P8: A/B/C use the same task list; B and C share the exact same retrieval trace.
- P9: P8 outputs locked before private ground truth is opened.
- P10: report distinguishes observation, interpretation, limitation, and dry-run vs real acquisition.
