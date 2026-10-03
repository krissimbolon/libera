"""Security preflight. Hash trust anchor must come from separately protected custody record."""
from __future__ import annotations
import hashlib
import ipaddress
from pathlib import Path
from urllib.parse import urlsplit
from src.ai_rag.validate_output import FORBIDDEN_GT_FIELDS, validate_structured_finding

class SecurityViolation(ValueError):
    pass

def verify_acquisition(path: Path, expected_sha256: str) -> str:
    if len(expected_sha256) != 64 or any(c not in '0123456789abcdef' for c in expected_sha256.lower()):
        raise SecurityViolation('Missing or malformed trusted acquisition SHA-256')
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected_sha256.lower():
        raise SecurityViolation('Acquisition hash differs from trusted custody record')
    return actual

def require_loopback_host(host: str) -> str:
    parsed = urlsplit(host)
    if parsed.scheme not in ('http', 'https') or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('', '/'):
        raise SecurityViolation('Invalid local model endpoint')
    name = parsed.hostname or ''
    try:
        local = ipaddress.ip_address(name).is_loopback
    except ValueError:
        local = name.lower() == 'localhost'
    if not local:
        raise SecurityViolation('Model endpoint must be literal loopback or localhost')
    return host

def validate_no_nested_gt(value, path='$'):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_GT_FIELDS:
                raise SecurityViolation(f'Forbidden GT field at {path}.{key}')
            validate_no_nested_gt(child, f'{path}.{key}')
    elif isinstance(value, list):
        for i, child in enumerate(value):
            validate_no_nested_gt(child, f'{path}[{i}]')

def validate_secure_finding(finding):
    validate_no_nested_gt(finding)
    validate_structured_finding(finding)
