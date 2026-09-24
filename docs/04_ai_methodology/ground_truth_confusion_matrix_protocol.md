# Ground-Truth and TP/FP/TN/FN Evaluation Protocol — LIBERA

## 1. Why this protocol is fixed before experimentation

Metric definitions are locked before BASE/A/B/C results are inspected.

LIBERA follows the logic of:
- NIST CFReDS: known simulated evidence contents permit comparison of examiner/tool outputs against documented ground truth;
- CFTT: forensic tools should be tested against explicit requirements, assertions, test cases, and known test sets;
- Bollé et al. (2020): TP/TN/FP/FN and derived metrics are useful for automated forensic systems only when the classification unit and meaning of positive/negative are clearly defined.

## 2. Do not equate provenance with forensic relevance

The following are construction labels:
- ADAPTED_FROM_GALLOWAY
- SYNTHETIC_BRIDGE
- SYNTHETIC_CONTEXT
- SYNTHETIC_DISTRACTOR

They are **not** automatically the positive/negative classes.

Examples:
- an anchor may be contextually irrelevant to a particular investigative task;
- a bridge may be essential evidence for chronology;
- a context message may corroborate location or control;
- a distractor is expected to be non-relevant, but the evaluator must verify this rather than use provenance as a shortcut.

The examiner/AI never sees evaluator-only labels.

## 3. Evaluation Layer A — Message-level evidence relevance

### Universe

The universe is bounded and fixed:

`U = all 10,000 final messages`

For each investigative task, the evaluator defines before unblinding:

`GT_positive(task) = messages judged relevant/supporting that task`

All other messages in U are negative for that specific task.

A message can be positive for one task and negative for another.

### Prediction rule

A message is predicted positive when the examiner/system:
- retrieves it into the evidence set; or
- explicitly cites/selects it as supporting evidence for the task.

Predicted negative means it is not selected/cited for that task.

### Confusion matrix

- **TP** — ground-truth relevant message correctly selected/cited.
- **FP** — ground-truth non-relevant message incorrectly selected/cited as evidence.
- **FN** — ground-truth relevant message not selected/cited.
- **TN** — ground-truth non-relevant message correctly left unselected.

Because U is exactly 10,000 messages, TN is well-defined here.

### Primary metrics

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 * Precision * Recall / (Precision + Recall)`

`Specificity = TN / (TN + FP)`

`FPR = FP / (FP + TN)`

`FNR = FN / (FN + TP)`

Accuracy may be reported only as secondary information because large numbers of irrelevant/noise messages can make accuracy appear excellent even when relevant evidence is missed.

Report class prevalence for every task.

## 4. Evaluation Layer B — Finding-level recovery

### Universe

Before the experiment, evaluator defines a finite list of expected findings:

`GT_FINDINGS = {F01, F02, ... Fn}`

Each finding includes:
- finding category;
- canonical factual claim;
- minimum supporting evidence;
- acceptable alternative wording;
- disallowed overstatement;
- related ground-truth message/artifact IDs.

### Categories may include

- recruitment / re-recruitment;
- prospective-client/appointment coordination;
- advertisement/platform coordination;
- transport/movement;
- lodging/hotel coordination;
- financial/price/payment control;
- instruction/monitoring/control;
- coercion/threat;
- attempts to leave / obtain help;
- family/support communication relevant to movement/control;
- co-actor coordination;
- contradictions or uncertainty that an examiner should recognize.

### Finding scoring

- **TP finding** — a predefined expected finding is recovered and supported by sufficient acquired evidence.
- **FP finding** — the examiner/system proposes a substantive finding that is unsupported, contradicted, or materially overstates the acquired evidence.
- **FN finding** — an expected ground-truth finding is not recovered.

### No TN at finding level

TN is **not reported** at finding level because the universe of all possible findings the examiner could have invented is not naturally bounded.

Therefore finding-level primary metrics are:
- precision;
- recall;
- F1;
- raw TP/FP/FN.

Do not compute finding-level accuracy.

## 5. Evaluation Layer C — Evidence-attribution quality

For each factual claim produced by BASE/A/B/C:

Record:
- claim_id;
- finding_id;
- cited ART/message IDs;
- whether cited artifact exists;
- whether it comes from acquired evidence;
- whether it actually supports the claim;
- whether contrary evidence was ignored;
- whether wording overstates the evidence.

Metrics:

### Citation validity
Valid locator count / total cited locators.

### Attribution precision
Claims with sufficient supporting evidence / all evidence-backed claims made.

### Expected-evidence coverage
Ground-truth supporting artifacts recovered / ground-truth supporting artifacts expected.

### Unsupported claim rate
Unsupported factual claims / total factual claims.

## 6. Evaluation Layer D — Timeline and actor-state correctness

For predefined ground-truth events:

- event recovered correctly;
- correct actors;
- correct temporal ordering;
- correct location/state where known;
- no impossible state introduced;
- uncertainty preserved where source is ambiguous.

Report:
- event recall;
- chronology error count;
- actor attribution error count;
- over-inference count.

## 7. Evaluation Layer E — Case-level conclusion

The Raka synthetic scenario has an evaluator-side intended resolution derived from the adjudicated Galloway outcome.

However there is only one case.

Therefore do **not** claim statistical accuracy for a one-case guilty/not-guilty classification.

Instead score whether the final examiner conclusion is:

- concordant with ground truth;
- partially concordant;
- unsupported/overstated;
- contradicted by ground truth.

The examiner's wording should concern evidentiary support, not legal adjudication.

## 8. Ground-truth construction procedure

Before AI runs:

1. Freeze final 10,000-message corpus.
2. Freeze evaluator-only case-resolution statement.
3. Define investigative tasks T01–T10.
4. Build expected finding list.
5. Map each expected finding to minimum supporting message IDs/artifacts.
6. Build task-specific message relevance labels.
7. Double-review labels by two team members.
8. Resolve disagreements and log adjudication.
9. Hash/version the ground-truth package.
10. Keep it inaccessible to BASE examiner and A/B/C systems until outputs are frozen.

## 9. Suggested ground-truth files

Private/evaluator-only:

- `ground_truth_case_resolution.json`
- `ground_truth_findings.csv`
- `ground_truth_message_relevance.csv`
- `ground_truth_event_timeline.csv`
- `ground_truth_actor_relations.csv`

Do not commit sensitive/restricted evaluator content to public repo if it leaks the answer used in the experiment.

## 10. Message relevance schema

Suggested fields:

- message_id
- task_id
- is_relevant
- relevance_category
- expected_finding_id
- relevance_rationale
- minimum_or_corroborative
- adjudicator_1
- adjudicator_2
- adjudication_status

## 11. Finding ground-truth schema

Suggested fields:

- expected_finding_id
- category
- canonical_claim
- minimum_supporting_message_ids
- corroborating_message_ids
- acceptable_scope
- forbidden_overstatement
- case_significance
- adjudication_status

## 12. Reporting results

For each condition BASE/A/B/C report separately:

### Message level
- positive prevalence;
- TP / FP / FN / TN;
- precision;
- recall;
- F1;
- specificity/FPR;
- accuracy only as secondary.

### Finding level
- TP / FP / FN;
- precision;
- recall;
- F1;
- no TN/accuracy.

### Attribution
- locator validity;
- attribution precision;
- expected-evidence coverage;
- unsupported claim rate.

### Operational
- total review time;
- time to first relevant evidence;
- number of artifacts/messages requiring human review.

## 13. Interpretation priority

In a forensic setting:
- high FP wastes examiner time and can create misleading allegations;
- high FN risks missing probative or exculpatory evidence.

Therefore precision and recall must be discussed separately even when F1 is also reported.

A single composite score must never replace review of the actual FP/FN examples.

## 14. References

- SRC-007 — NIST CFReDS.
- NIST CFTT methodology.
- SRC-008 — Bollé et al. (2020), automated-system evaluation in forensic analysis.
- SRC-002 — ForensicLLM, for local-LLM/RAG evaluation context.
