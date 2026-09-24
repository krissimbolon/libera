# Theoretical Framework — LIBERA Digital Forensics

## 1. Position of the study

LIBERA is a **digital-forensic investigation study** using a synthetic human-trafficking scenario as the investigative domain.

Human trafficking is not the forensic method. It is the case context that determines which evidentiary patterns are relevant. The forensic method remains preservation, acquisition, examination, analysis, validation, and reporting of digital evidence.

The AI/LLM component is an examiner-assistance layer and must not replace evidence integrity, provenance, or human verification.

## 2. Mobile digital forensics

NIST SP 800-101 Rev. 1 defines mobile device forensics as recovery of digital evidence from mobile devices under forensically sound conditions using accepted methods, and structures the workflow around validation, preservation, acquisition, examination, analysis, and reporting.

Operationalized in LIBERA:

1. **Preservation**
   - freeze final synthetic scenario;
   - record device state;
   - prevent undocumented changes;
   - separate evaluator-only ground truth from examiner evidence.

2. **Acquisition**
   - obtain evidence from the WhatsApp test device/environment using the actual available acquisition method;
   - label the method honestly (logical export, logical copy, backup, filesystem, etc.);
   - create ACQ identifiers and hash manifests.

3. **Examination**
   - extract and normalize message, contact, conversation, timestamp, and attachment artifacts;
   - preserve raw values and provenance;
   - assign ART identifiers.

4. **Analysis**
   - reconstruct timelines;
   - identify actors and relationships;
   - search relevant communications;
   - distinguish substantive evidence from neutral/noise messages;
   - produce investigator findings linked to ART locators.

5. **Reporting**
   - document methods, tools, versions, hashes, limitations, findings, uncertainty, and traceability.

## 3. Digital evidence integrity and provenance

A forensic conclusion is useful only if the examiner can show where the evidence came from and that it was not silently altered.

LIBERA therefore separates:

- **case-design source**;
- **synthetic scenario**;
- **test-device staging**;
- **acquired evidence**;
- **working copy**;
- **extracted artifact**;
- **finding**.

The target trace is:

`FND -> RUN -> CHK -> ART -> ACQ -> DEV`

For non-AI findings:

`FND -> ART -> ACQ -> DEV`

SHA-256 is used as an integrity check for frozen files and evidence packages. Hashes do not prove truth of the message content; they establish byte-level identity/integrity of the recorded artifact at a given stage.

## 4. Chain of custody and reproducibility

Chain of custody records who handled evidence, when, why, where it moved, and whether integrity was verified.

In this academic simulation it is used primarily for:
- reproducibility;
- accountability;
- separation of master and working copies;
- documenting transformations.

It is not presented as a claim of legal admissibility in a real criminal prosecution.

## 5. Human trafficking as the investigative domain

The Palermo Protocol formulation commonly used by UNODC describes trafficking through three components for adults:

- **act**: recruitment, transportation, transfer, harbouring, or receipt of persons;
- **means**: force, coercion, deception, abuse of power/vulnerability, payments or benefits to obtain control;
- **purpose**: exploitation.

LIBERA does not ask the LLM to decide legal guilt. Instead, the examiner searches acquired communications for **digital evidence that may support or contradict investigative hypotheses** around these components.

Possible evidence classes in the WhatsApp scenario include:
- recruitment or re-recruitment communications;
- transport and movement coordination;
- hotel/lodging arrangements;
- pickup/drop-off logistics;
- money, price, payment, or benefit discussions;
- instructions and monitoring;
- threats, pressure, or control;
- attempts to leave, return home, or obtain help;
- family communications;
- coordination among facilitators;
- advertisements/platform references;
- neutral messages that must be distinguished from relevant evidence.

A message is not labelled trafficking evidence merely because it contains one keyword. Interpretation requires context, chronology, actors, and corroborating artifacts.

## 6. Timeline reconstruction

Digital messages are temporal artifacts. A forensic timeline is used to determine:
- what happened first;
- which actor knew what at a given time;
- whether communications support movement or coordination;
- whether two statements are mutually compatible;
- whether an inferred event occurs before supporting evidence.

LIBERA therefore requires both:
- per-chat chronology; and
- global Raka-centric chronology.

Synthetic messages may enrich context but must never overwrite the immutable anchor chronology.

## 7. Relationship and communication analysis

The WhatsApp corpus is modeled as one Raka-centric device with multiple dyadic chats.

Analysis can use:
- participant pairs;
- message frequency;
- temporal bursts;
- direction of communication;
- recurring coordination;
- relationship/event segments;
- links between communication and timeline events.

Communication frequency alone does not establish criminal involvement. Relationship interpretation must be supported by message content and chronology.

## 8. Ground truth and blinded evaluation

Because the dataset is synthetic, LIBERA has a major methodological advantage: evaluator-only ground truth can be defined before the examiner runs the investigation.

Ground truth contains expected actors, events, relationships, relevant messages, and distractors.

The examiner/AI pipeline must not see that mapping before outputs are locked.

This allows evaluation of:
- true-positive findings;
- false-positive findings;
- missed findings;
- evidence attribution accuracy;
- unsupported claims;
- chronology errors;
- over-inference.

## 9. Traditional forensic baseline

AI performance has no meaning without a comparison point.

The baseline investigator uses:
- keyword/search;
- actor/entity analysis;
- timeline reconstruction;
- relationship analysis;
- manual evidence review.

Baseline findings are frozen before AI outputs and ground truth are opened.

## 10. LLM-assisted digital forensics

ForensicLLM motivates the use of local LLMs in digital-forensic workflows because cloud dependency, domain mismatch, hallucination, and source attribution are major concerns.

LIBERA evaluates three AI conditions:

- **A — local LLM only**;
- **B — local LLM + RAG**;
- **C — local LLM + RAG + structured forensic reasoning**.

The study does not assume RAG or structured reasoning is better. It measures whether they improve groundedness, attribution, correctness, relevance, and verifiability.

## 11. Retrieval-augmented generation and evidence grounding

RAG is used to restrict model reasoning to retrieved evidence chunks from acquired/extracted artifacts.

Each chunk must retain:
- CHK ID;
- source ART ID;
- source message IDs/range;
- acquisition provenance;
- retrieval score;
- index version.

The critical evaluation question is not merely whether the answer sounds correct, but whether each investigative claim can be traced back to actual acquired evidence.

## 12. Structured forensic reasoning

Condition C requires the model to separate:
- claim;
- supporting evidence;
- locator;
- uncertainty;
- alternative explanation;
- no-evidence conclusion where appropriate.

This is intended to make the output easier for an investigator to verify, not to expose hidden chain-of-thought.

## 13. Error-focused quality assurance

SOLVE-IT motivates systematic identification of weaknesses, errors, and mitigations in digital-forensic processes.

LIBERA maintains an ERR register across:
- acquisition;
- extraction;
- normalization;
- retrieval;
- context truncation;
- hallucination;
- evidence misattribution;
- chronology;
- over-inference;
- model/tool reproducibility.

Each error should document:
- observed failure;
- evidence;
- cause hypothesis;
- impact;
- mitigation;
- residual risk.

## 14. Core theoretical model

The complete logic of the study is:

```text
Human-trafficking investigative hypothesis
                ↓
Mobile digital evidence
                ↓
Preservation & acquisition
                ↓
Integrity / provenance / chain of custody
                ↓
Extraction & artifact identification
                ↓
Timeline + relationship + content examination
                ↓
Traditional forensic baseline
                ↓
LLM / RAG / structured reasoning assistance
                ↓
Evidence-attributed findings
                ↓
Human verification against blinded ground truth
                ↓
Error analysis, reporting, and limitations
```

The object of evaluation is therefore **not whether an LLM can tell a convincing trafficking story**. The object is whether an AI-assisted examiner can recover correct, relevant, traceable forensic findings from a noisy WhatsApp evidence set while preserving forensic integrity.
