import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path
from src.forensics.extract_artifacts import extract_sqlite, validate
from src.ai_rag.validate_output import validate_structured_finding, REQUIRED_FIELDS
from src.security.guards import SecurityViolation, verify_acquisition, require_loopback_host, validate_secure_finding

from tools.security_uas_audit import frozen_module

class SecurityTests(unittest.TestCase):
    def test_tamper_structurally_valid_but_hash_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td)/'synthetic.sqlite'
            con = sqlite3.connect(db)
            con.execute('CREATE TABLE messages(message_id,conversation_id,timestamp,sender_id,recipient_id,message_text,message_type,reply_to_message_id,attachment_id)')
            con.execute("INSERT INTO messages VALUES ('MSG-SIM-1','CHAT-SIM','2026-01-01T00:00:00+00:00','Alice','Bob','synthetic original','text',NULL,NULL)")
            con.commit(); con.close()
            trusted = hashlib.sha256(db.read_bytes()).hexdigest()
            verify_acquisition(db, trusted)
            con = sqlite3.connect(db)
            con.execute("UPDATE messages SET message_text='synthetic tampered'")
            con.commit(); con.close()
            baseline = frozen_module('src/forensics/extract_artifacts.py', 'src.forensics.frozen_test_extract')
            rows, _ = baseline['extract_sqlite'](db)
            baseline['validate'](rows)
            self.assertEqual(rows[0]['message_text'], 'synthetic tampered')
            with self.assertRaises(SecurityViolation): verify_acquisition(db, trusted)
    def test_local_host_restriction(self):
        for host in ['http://localhost:11434','http://127.0.0.1:11434','http://[::1]:11434']:
            require_loopback_host(host)
        for host in ['https://example.invalid','http://127.0.0.1.example.invalid','http://user@localhost','file:///tmp/model','http://localhost/?redirect=remote']:
            with self.assertRaises(SecurityViolation): require_loopback_host(host)
    def test_nested_gt_rejection(self):
        finding = {key: '' for key in REQUIRED_FIELDS}
        finding['relevant_evidence'] = [{'annotation_notes': 'SYNTHETIC CANARY ONLY'}]
        baseline = frozen_module('src/ai_rag/validate_output.py', 'src.ai_rag.frozen_test_validator')
        baseline['validate_structured_finding'](finding)
        with self.assertRaises(SecurityViolation): validate_secure_finding(finding)
    def test_valid_finding(self):
        finding = {key: '' for key in REQUIRED_FIELDS}
        finding['relevant_evidence'] = ['ART-000001']
        validate_secure_finding(finding)
