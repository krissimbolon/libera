# Evidence and Artifact ID Convention

Use stable identifiers so every later AI finding can be traced to its source.

## Physical / acquired evidence
- DEV-### : test device
- ACQ-### : acquisition package/image/export
- ART-### : extracted forensic artifact
- ATT-### : attachment/media artifact

## Case-design and reconstruction artifacts
- SRC-### : external/public source
- REC-##### : reconstructed source-message row, normally matching original line when available
- ID-MSG-##### : Indonesian adapted synthetic message

## AI / analysis artifacts
- CHK-##### : RAG chunk
- RUN-##### : LLM invocation
- FND-##### : investigator finding
- ERR-##### : error/mitigation register item

## Traceability rule
A final finding should be traceable as:

FND -> RUN (if AI-assisted) -> CHK -> ART -> ACQ -> DEV

For non-AI findings:
FND -> ART -> ACQ -> DEV

Ground-truth and source-reconstruction identifiers must never be silently substituted for acquired-evidence identifiers.
