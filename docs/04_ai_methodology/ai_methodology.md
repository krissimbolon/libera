# AI Methodology Notes

Planned comparison:
1. Local LLM only
2. Local LLM + RAG
3. Local LLM + RAG + structured forensic reasoning

Each AI run must log:
- run_id
- model name/version
- Ollama version
- model digest when available
- prompt version
- temperature/seed/context parameters when available
- retrieved evidence IDs
- retrieved domain-source IDs
- output
- timestamps
- reviewer status
- accepted/rejected/partially-supported finding status

Court narrative/source reconstruction used to create the scenario must not be exposed to the case-analysis RAG index, to avoid ground-truth leakage.
