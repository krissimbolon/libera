# P1 — Source Reconstruction Protocol

Goal: build a transparent 1–543 skeleton of the referenced message exhibit before adapting anything to Indonesia.

## Step order
1. Register every public source document in `references/source_registry.csv`.
2. Create rows 1 through 543 in the reconstruction table.
3. Extract only message-level content explicitly present in public records.
4. Preserve original line numbers.
5. Preserve original wording where legally/ethically appropriate for restricted local research.
6. Mark unavailable rows `MISSING_FROM_PUBLIC_RECORD`.
7. Mark metadata inferred from surrounding text separately as `INFERRED_METADATA`.
8. Never fill missing rows with an LLM during P1.
9. Record source page/document reference for every recovered message.
10. Compute coverage statistics only after extraction is complete.

## Expected deliverables
- `data/reconstruction/galloway_exhibit1a_reconstructed.csv`
- `data/reconstruction/reconstruction_coverage.csv`
- source registry entries
- extraction notes
- QA review log

## Publication rule
The public repository should contain only sanitized/derived material. Raw sensitive court excerpts belong in restricted local storage.
