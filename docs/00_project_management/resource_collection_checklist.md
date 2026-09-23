# Resource Collection Checklist

Use this while P1 source reconstruction is underway.

## A. Real-case public records
Priority 1:
- Public court opinion/order that quotes Government Exhibit 1A message lines
- Full docket metadata for case 1:17-cr-01235-WJ
- Publicly accessible versions of referenced filings (including Docs. 382, 427, 512, and 547)
- Exhibit list / hearing exhibit references if publicly available
- Any appellate opinion that reproduces or characterizes the same communications

For every file, record:
- exact title
- court/case
- docket/document number
- publication/file date
- source URL or locator
- date accessed
- page count
- whether it contains message-level quotations
- whether victim/minor information appears

Do not paste sensitive victim communications into public GitHub while collecting.

## B. Human-trafficking domain sources for the Indonesian adaptation
Collect authoritative material separately from the case source:
- Indonesian statutory/legal definitions and elements
- official government guidance or reports
- UN/UNODC/IOM or equivalent authoritative trafficking indicators
- peer-reviewed research on recruitment, control, transport/transfer, exploitation, coercion/deception, and online/digital communication patterns

Purpose: these sources define the domain taxonomy used by the RAG knowledge base and ground-truth annotation. They must not be confused with evidence from the case.

## C. Digital-forensics / AI methodology sources
Already provided:
- seizure/acquisition framework
- integrated forensic-analysis framework
- social-media forensic analysis
- ForensicLLM
- SOLVE-IT
- practitioner-driven DFAI framework
- LLMs in digital forensics review
- reasoning-model/CoT assessment

If collecting more, prefer sources on:
- mobile/WhatsApp forensic acquisition
- chain of custody
- forensic hashing and reproducibility
- RAG evaluation
- LLM hallucination/groundedness evaluation
- human-in-the-loop forensic validation

## D. Test environment information
Record but do not publish secrets:
- Android phone/emulator make/model
- Android version
- WhatsApp version
- acquisition workstation OS
- RAM/GPU
- Ollama version
- candidate local models
- storage capacity
- whether the environment can be isolated offline

## E. Collection naming convention
Suggested local filenames:
`SRC_<number>_<case-or-author>_<short-title>_<year>.pdf`

Example:
`SRC_001_Galloway_Doc547_YYYY.pdf`

## F. Handoff rule
When sending a source to the project:
1. provide the original file, not screenshots if a PDF exists;
2. preserve the filename;
3. tell the team where it came from;
4. do not manually rewrite quoted messages before source extraction;
5. flag any sensitive personal/minor information.
