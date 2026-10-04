# P3 Final Acquisition Checklist — DEV-001 -> ACQ-001

Use this only for the real local-device run. `ACQ-DRY-001` is a software dry-run and must never be relabeled as ACQ-001.

## Before staging
- [ ] Verify frozen corpus SHA-256 equals `a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6`.
- [ ] Use dedicated research WhatsApp account/SIM; do not use the two personal active accounts.
- [ ] Record device model, Android build, WhatsApp version, timezone, displayed time, battery/charging state, network state, storage availability, and lock state.
- [ ] Record workstation OS, ADB version, acquisition-tool exact version/license, and examiner.
- [ ] Confirm device clock vs workstation and document any offset.

## Controlled staging/replay
- [ ] Preserve the frozen CSV unchanged; staging must be downstream only.
- [ ] Document the method used to place/replay messages into the research environment.
- [ ] Record start/end time and any unavoidable device-state changes.
- [ ] Verify expected account identities and chat count before acquisition.
- [ ] Photograph/screenshot the relevant device state for the lab record where permitted.

## Acquisition
- [ ] Assign `DEV-001` and `ACQ-001` before collection.
- [ ] Use the selected logical acquisition method and document exact options.
- [ ] Record every examiner interaction that can change device state.
- [ ] Do not claim physical/full-file-system extraction if only logical/selective extraction was performed.
- [ ] Save the acquisition as master evidence in private storage.
- [ ] Calculate SHA-256 immediately after acquisition.
- [ ] Make the master read-only according to the local storage procedure.
- [ ] Create a working copy and verify its SHA-256 equals the master.

## Chain of custody
- [ ] Date/time of collection.
- [ ] Person creating acquisition.
- [ ] Device and acquisition IDs.
- [ ] Tool/version.
- [ ] Master path (private record only).
- [ ] Master SHA-256.
- [ ] Working-copy SHA-256.
- [ ] Any transfer/copy events and responsible person.

## Handoff to P4
- [ ] Never expose private identifiers in the public repo.
- [ ] P4 input must be a working copy/export, not the protected master.
- [ ] Convert/export acquisition messages to the normalized `messages` contract or directly to examiner ART CSV.
- [ ] P4 examiner evidence must exclude source-provenance and evaluator-ground-truth fields.
