# Provenance Schema

Every reconstructed/adapted message must preserve lineage.

## Source reconstruction fields
- original_line
- timestamp_original
- sender_original
- recipient_original
- message_original
- conversation_cluster
- source_id
- source_document
- source_page
- source_reference
- reconstruction_status
- confidence
- notes

## Allowed reconstruction_status values
- COURT_VERBATIM
- COURT_PARAPHRASED
- INFERRED_METADATA
- MISSING_FROM_PUBLIC_RECORD

Do not use LLM_GENERATED in the source-reconstruction layer.

## Indonesian adaptation fields
- adapted_message_id
- source_original_line
- source_status
- sender_adapted
- recipient_adapted
- timestamp_adapted
- message_adapted
- transformation_identity
- transformation_geography
- transformation_currency
- transformation_institution
- transformation_language
- transformation_chronology
- provenance

## Allowed adaptation provenance values
- ADAPTED_FROM_REAL_CASE
- SYNTHETIC_BRIDGE
- SYNTHETIC_DISTRACTOR

## Non-negotiable rule
A message synthesized to bridge a gap must never be relabeled as reconstructed or verbatim.
