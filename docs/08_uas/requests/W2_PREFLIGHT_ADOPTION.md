# Cross-worker request: security guard adoption
Status: CANDIDATE; requires Coordinator approval and owning worker implementation.
W1: call src.security.guards.verify_acquisition before extraction, using a separately protected expected acquisition SHA-256. Do not trust hash recomputed from the potentially changed input.
W3: call require_loopback_host before transport and validate_secure_finding for structured outputs. Loopback check also needs redirect refusal (stdlib follows redirects), protected localhost resolution or explicit literal IPs; reject remote redirects. W2 baseline probe was mocked and no external request ran.
W2 intentionally does not change src/forensics or src/ai_rag. Integration acceptance requires owner tests and W2 retest against adopted path. Independent guards are already executed, not evidence that canonical runner is protected.
