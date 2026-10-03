# W2 security assessment — synthetic local simulation

Status: VERIFIED_BY_WORKER. Contract 1.0. Rules of engagement: repository-only review and tests in temporary synthetic SQLite; no production systems, external probing, credential access, physical devices, canonical corpus mutation, or private evaluator GT. Remote transport is mocked. Authorized objective: test confidentiality, evidence integrity and evaluator separation.

Threat model: assets are acquisition master/custody hash, ART evidence, local-model prompts and evaluator labels. Trust boundaries are master → working copy → extractor; evidence → model transport; model JSON → validation/evaluation. Threat actors considered: local file writer, misconfigured operator, and attacker-controlled evidence/output. Assumptions: OS/user permissions and custody records are protected separately. No claim that these assumptions were audited on a member laptop.

| ID | Finding and cause | Risk (qualitative) | Before / after executed result | Remediation and residual limitation |
|---|---|---|---|---|
| SEC-001 | Extractor checks SQLite structural integrity but accepts changed message content without comparing trusted acquisition hash | High integrity risk if working-copy writes are possible | Synthetic UPDATE remains valid and extractable; independent guard rejects mismatch | Call verify_acquisition before P4 with protected custody SHA; guard alone is not wired into P4 and cannot stop attacker replacing both file and trust anchor |
| SEC-002 | Ollama HTTP helper accepts arbitrary destination | High confidentiality risk from operator misconfiguration | Mocked baseline sends synthetic prompt to remote URL; endpoint preflight rejects URL | Require literal loopback/localhost before every model request; no actual exfiltration observed; loopback protection does not authenticate local service or constrain DNS/redirects |
| SEC-003 | Structured validator forbids only top-level GT keys | Medium evaluator-separation risk | Nested synthetic annotation_notes passes baseline; recursive guard rejects it | Call validate_secure_finding; this detects forbidden keys, not prose-level leaked knowledge or unsupported claims |

All three guards are executed and tested as independent preflight functions. Production adoption is pending owner approval; do not describe pipeline weaknesses as fully remediated until integration wiring and retest are verified. No CVSS score claimed because deployment and threat prerequisites have not been established.

## T1565.001 exercise
Benign sample changes one synthetic SQLite message. SHA-256 values are recorded in evidence/W2/security_results.json. Static indicator: sample-specific changed-file digest. Dynamic observation: UPDATE messages followed by custody-hash mismatch. These are tamper detection indicators for this exercise, not general malware signatures. There is no malware execution. MITRE defines T1565.001 as manipulation of stored data: https://attack.mitre.org/techniques/T1565/001/ ; official parent listing verified 2026-10-03: https://attack.mitre.org/techniques/T1565/ . Mapping is an analytical analogy to the test, not attribution to an adversary.

## Scan and retest
Reproduce: `PYTHONPATH=. python tools/security_uas_audit.py`.
Four unittest cases pass, including positive intact/valid input and negative tamper/nested-key/remote-endpoint tests. Tracked sensitive filename scan finds none of .env/id_rsa/id_ed25519/*.pem/*.key at this checkpoint; this limited screen does not establish absence of secrets or leaked labels in history. Full dependency advisory scan not completed by W2. P2 SHA stays canonical. Exact outputs and limitations are in security_results.json and retest.txt.

## Owner adoption retest
Canonical owner APIs executed at W1 a9df81f082ef4528ae7f0e7c1fd2d6aa511a67e6 and W3 64819a36c93cbc58a4654210c70a1f7e1f27f59c. P4 trusted expected hash rejects modified SQLite and produces no tampered output. Local transport rejects remote host and redirects, rewrites localhost to literal loopback. Canonical structured validator rejects nested forbidden GT key. See owner_retest.json. P4 legacy optional hash path remains; final integrated retest has not yet run. The prior pending-adoption description refers to the initial checkpoint only.
