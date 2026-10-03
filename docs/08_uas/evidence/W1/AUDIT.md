# W1 forensic foundation audit
Status: VERIFIED_BY_WORKER. Contract 1.0. Integration source: 5b13f4b.

## Executed evidence
`python docs/08_uas/evidence/W1/reproduce.py` executes frozen synthetic P2 → controlled software P3 SQLite → P4 → deterministic P5. It uses a temporary directory; no private GT or case-design labels are read. Summary is runtime_summary.json. P2 remains pinned to a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6. This proves software contracts for simulated evidence, not real Android acquisition.

`python -m pytest -q tests/test_uas_w1_foundation.py`: six tests passed. New tests cover actual 10,000-row extraction and baseline repeatability, same-path/symlink/hardlink rejection and corpus preservation. Full `python -m pytest -q`: 19 tests passed; historical tests include stub AI and evaluator precheck, which are not performance evaluation or GT release.

## Changes
- P3/P4 reject input/output/manifest aliasing before writes. Real filesystem hardlinks and symlinks are checked. This prevents accidental overwrite when outputs are misconfigured; it is not a full hostile filesystem race defense.
- Workbench now uses ARTFILE-00001_messages.csv and ARTFILE-00002_chats.csv, matching current ChatSim extractor. Static interface checked; Streamlit package unavailable, so graphical execution is BLOCKED.
- Legacy root test_llm.py is explicitly a manual optional smoke check. Optional ollama import is deferred and pytest no longer treats it as an automatic network-dependent test. Existing script CLI behavior retained. Coordinator explicitly authorized this hygiene change.

## Schema and paths inventory
P4: runtime/working/P4/artifacts.csv and artifact_manifest.json; canonical fields recorded in runtime_summary.json. No construction provenance columns exposed.
P5: runtime/working/P5/{baseline_findings.json,baseline_manifest.json,entities.csv,relationships.csv,timeline.csv}.
P5 finding: finding_id,task_id,question,method,keywords,candidate_count,evidence. Evidence fields: evidence_id,message_id,timestamp,sender,receiver,matched_keywords,score,text. These are deterministic search candidates; human validation is still required before calling a finding supported.
ChatSim extraction additionally exports ARTFILE-00001_messages.csv, ARTFILE-00002_chats.csv, ARTFILE-00003_device_metadata.csv. Container IDs and ART message IDs are different namespaces.

## Hygiene and limitations
500 tracked paths at bootstrap, no tracked runtime/ or Python cache paths (hygiene_inventory.json). Demo dependency requirements are lower bounds, not an exact lock; Python pipeline uses standard library, tests require pytest. Streamlit runtime and actual emulator/phone acquisition are not verified here. Historical documentation may remain stale; no destructive mass cleanup undertaken. Public corpus construction history can defeat retrospective blindness; removing columns from P4 does not undo exposure. W2 owns comprehensive leak/secret scan. No P5 human review/lock is asserted; no benchmark results asserted.

## Approved W2 trusted-digest adoption checkpoint
Coordinator approved W2_PREFLIGHT_ADOPTION. P4 `run(input_db, output_csv, manifest_path, expected_sha256=None)` and CLI `--expected-sha256` compare the working acquisition against an externally trusted expected digest before extraction and check for input changes before output publication. The UAS reproduction explicitly supplies P3 acquisition-record digest. Valid SQLite tampering is rejected before output creation; intact supplied hash is accepted. Malformed expected digest is rejected.
Legacy callers may omit expected_sha256 for compatibility. Their manifest now declares LEGACY_NO_TRUSTED_DIGEST; this mode does not establish custody integrity and is insufficient for UAS integrity claims. Expected digest authenticity and immutability must be established separately; hashing an already tampered source is not a trust anchor. No hostile filesystem race or signed custody claim.
`python -m pytest -q`: 21 passed (trusted_hash_tests.txt). Updated UAS runtime is trusted_runtime_summary.json. Prior runtime_summary.json remains historical evidence from pre-adoption checkpoint.

## Approved Windows wrapper wiring checkpoint
Coordinator authorized scripts/run_libera_local.ps1 and run_libera_demo.ps1 changes. Main wrapper refuses GroundTruthPath for all modes and directs separate run_p9_final.ps1. Both wrappers refuse an existing final P8 lock before acquisition, extraction or manifest copies. Supplied AcquisitionPath requires AcquisitionSha256 from separate trusted custody record; fresh simulated P3 reads its just-created manifest digest and passes --expected-sha256. Supplied ArtifactsPath warns that provenance/integrity is operator-verified and bypasses acquisition verification. ChatSim demo compares working hash to fresh master/working custody digests before extraction.
DryRun skips final lock and performs no-GT precheck; it never unlocks GT. Real mode creates lock then only no-GT precheck, leaving private evaluation to the separate final script. Demo final messaging now distinguishes stub/no-lock mode.
Static regression checks confirm ordering/hash wiring; 9 W1 tests passed (wrapper_static_tests.txt). `pwsh` is unavailable, so Windows PowerShell execution is BLOCKED and these checks do not prove runtime script execution. No model downloads or Windows acquisition executed. Cross-worker message sent to W3 with wrapper contract; no schema changes.
