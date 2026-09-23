# Document 547 — Initial Exhibit 1A Reference Audit

Source: `SRC-001` — Document 547, 44 pages, filed 2021-04-29.

SHA-256 of the team-supplied PDF:
`5314377fcdc14d205dc0a14008d772b2dea6a24f5faca699ff4b0d1f1363edb0`

## What the document establishes
Document 547 describes Government Exhibit 1A as a catalogue of incoming and outgoing text messages recovered from Cornelius Galloway's phone, using color coding to identify message authors. The court then presents selected message clusters rather than the entire exhibit.

## Automated reference scan
A conservative scan of parenthetical Exhibit/line references found:
- 112 line-reference occurrences in the document;
- 530 distinct line numbers within the nominal 1–543 range referenced at least once;
- this is **not** equivalent to 530 uniquely recoverable messages, because some references repeat or conflict.

## Reference issues requiring QA before line-level reconstruction
1. **Lines 93–94** are referenced in more than one message context. These cannot be assigned blindly from Document 547 alone.
2. **Lines 382–389** are printed in one T.S. block on page 22, but later pages assign 382–386, 387, 388 and 389 onward to different M.V./Juvenile J messages. Treat this as an internal reference conflict until corroborated by Exhibit 1A or another filing.
3. **Page 23** prints `(Id, lines 117-117)` after a two-message exchange. Do not silently infer line 116.
4. **Page 39** prints `(Id, lines 511-5521)`, which exceeds the stated 1–543 exhibit range and overlaps later references beginning at 522. Treat as a source typographical anomaly; do not normalize it without corroboration.
5. Repeated references such as 333–336 and line 355 may simply be narrative cross-references rather than conflicts and should be distinguished from contradictory message assignments.

## Reconstruction rule
The public repository will store only provenance/status metadata and QA findings. Verbatim victim communications and the raw PDF stay in restricted local storage.

No LLM is allowed to resolve these conflicts. Resolution requires source corroboration or an explicitly labeled human inference.
