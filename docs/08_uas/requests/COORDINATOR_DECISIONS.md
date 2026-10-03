# Coordinator integration decisions

2026-10-03: W2_PREFLIGHT_ADOPTION approved for owning W1 P4 trusted digest and W3 transport/nested validator. W1 preserved old run signature with optional expected_sha256 and manifest declares LEGACY_NO_TRUSTED_DIGEST; UAS evidence reproduction supplies trusted digest. W3 uses dependency-neutral local_transport to avoid circular security/AI dependency, disables proxies and redirects, and recursively rejects GT keys. Coordinator executed integrated APIs; positive intact evidence accepted, modified copy rejected without outputs; remote/redirect/nested-field probes rejected, no external network calls.

W3 lock enhancements approved: reject dry/error/incomplete tasks and parameter/provenance mismatches, verify all six inputs before evaluator access. These changes are tested on synthetic fixtures, not a real P8 study. Real P8/P9 and final benchmark remain BLOCKED. W4 GOVERNANCE_GAPS remain scoped roadmap requests; do not claim institution controls deployed.

Current targeted scanner identified publicly tracked ground-truth schema filename. It screened header signatures, did not use evaluator labels or score ground truth. Do not remove/rewrite history or open private labels to investigate before P8. Complete exposure/private-label audit remains BLOCKED; public construction context already prevents an unqualified strict-blindness claim.
