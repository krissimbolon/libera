#!/usr/bin/env python3
"""Isolated synthetic security regression; no external traffic or private GT."""
import hashlib
import json
import sqlite3
import subprocess
import tempfile
from pathlib import Path
from src.forensics.extract_artifacts import extract_sqlite, validate
from src.ai_rag.validate_output import REQUIRED_FIELDS, validate_structured_finding
from src.ai_rag.ollama_runner import _post
from src.security.guards import verify_acquisition, require_loopback_host, validate_secure_finding, SecurityViolation

BASELINE_SHA = '62f8088c9f4833fa6ddf0149c6509a7162eaa9cf'

def frozen_module(path, name):
    source = subprocess.check_output(['git', 'show', f'{BASELINE_SHA}:{path}'], text=True)
    namespace = {'__name__': name, '__package__': name.rsplit('.', 1)[0]}
    exec(compile(source, f'{BASELINE_SHA}:{path}', 'exec'), namespace)
    return namespace

def main():
    target = Path('docs/08_uas/evidence/W2')
    target.mkdir(parents=True, exist_ok=True)
    baseline_extract = frozen_module('src/forensics/extract_artifacts.py', 'src.forensics.frozen_extract')
    baseline_validator = frozen_module('src/ai_rag/validate_output.py', 'src.ai_rag.frozen_validator')
    baseline_runner = frozen_module('src/ai_rag/ollama_runner.py', 'src.ai_rag.frozen_runner')
    result = {'baseline_sha': BASELINE_SHA, 'scope':'isolated synthetic local regression; no physical device or live LLM', 'findings':[]}
    with tempfile.TemporaryDirectory() as td:
        db = Path(td)/'synthetic.sqlite'
        conn = sqlite3.connect(db)
        conn.execute('CREATE TABLE messages(message_id,conversation_id,timestamp,sender_id,recipient_id,message_text,message_type,reply_to_message_id,attachment_id)')
        conn.execute("INSERT INTO messages VALUES ('MSG-SIM-1','CHAT-SIM','2026-01-01T00:00:00+00:00','Alice','Bob','synthetic original','text',NULL,NULL)")
        conn.commit(); conn.close()
        before = hashlib.sha256(db.read_bytes()).hexdigest()
        verify_acquisition(db, before)
        conn = sqlite3.connect(db)
        conn.execute("UPDATE messages SET message_text='synthetic tampered'")
        conn.commit(); conn.close()
        after = hashlib.sha256(db.read_bytes()).hexdigest()
        assert before != after
        (target/'benign_tampered_sample.sqlite').write_bytes(db.read_bytes())
        rows,_ = baseline_extract['extract_sqlite'](db); baseline_extract['validate'](rows)
        blocked=False
        try: verify_acquisition(db,before)
        except SecurityViolation: blocked=True
        result['findings'].append({'id':'SEC-001','technique':'T1565.001','before_sha256':before,'after_sha256':after,'baseline_accepts_tamper':rows[0]['message_text']=='synthetic tampered','guard_blocks_tamper':blocked,'static_ioc':'distinct SHA-256 of benign synthetic changed SQLite; sample-specific only','dynamic_ioc':'SQLite UPDATE messages followed by trusted-hash mismatch; SQL not malicious by itself'})
    # Intercept urlopen: inspect baseline endpoint behavior without making any network request.
    from unittest.mock import patch
    class Response:
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def read(self): return b'{}'
    with patch('urllib.request.urlopen',return_value=Response()) as mock:
        baseline_runner['_post']('https://example.invalid/api/generate',{'prompt':'SYNTHETIC ONLY'},1)
        endpoint=mock.call_args.args[0].full_url
    blocked=False
    try: require_loopback_host('https://example.invalid')
    except SecurityViolation: blocked=True
    result['findings'].append({'id':'SEC-002','baseline_accepts_remote_endpoint':endpoint,'guard_blocks_remote_endpoint':blocked,'network_calls':0,'limitation':'mocked sink demonstrates missing restriction; not observed exfiltration'})
    finding={key:'' for key in REQUIRED_FIELDS}
    finding['relevant_evidence']=[{'annotation_notes':'SYNTHETIC CANARY ONLY'}]
    baseline_validator['validate_structured_finding'](finding)
    blocked=False
    try: validate_secure_finding(finding)
    except SecurityViolation: blocked=True
    result['findings'].append({'id':'SEC-003','baseline_accepts_nested_gt_field':True,'guard_blocks_nested_gt_field':blocked,'limitation':'schema canary only; no private GT accessed; text semantic leaks not detected'})
    test=subprocess.run(['python','-m','unittest','discover','-s','tests','-p','test_uas_w2_*.py','-v'],capture_output=True,text=True)
    (target/'retest.txt').write_text(test.stdout+test.stderr)
    assert all(f.get('guard_blocks_tamper', f.get('guard_blocks_remote_endpoint', f.get('guard_blocks_nested_gt_field', False))) for f in result['findings']), 'Security guard did not reject probe'
    assert result['findings'][0]['baseline_accepts_tamper']
    assert result['findings'][2]['baseline_accepts_nested_gt_field']
    result['test_exit_code']=test.returncode
    tracked=subprocess.check_output(['git','ls-files'],text=True).splitlines()
    result['tracked_sensitive_filename_scan']=[p for p in tracked if Path(p).name in ('.env','id_rsa','id_ed25519') or p.endswith(('.pem','.key'))]
    result['scan_limitation']='filename screening only; no claim of exhaustive secret/dependency scan or absence of historical GT leakage'
    result['p2_sha256']=hashlib.sha256(Path('data/adaptasi_indonesia/corpus_whatsapp_10000.csv').read_bytes()).hexdigest()
    (target/'security_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(test.returncode)
if __name__=='__main__': main()
