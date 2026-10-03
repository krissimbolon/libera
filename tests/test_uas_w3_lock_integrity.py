"""Synthetic harness tests only: never actual LLM or private GT evaluation."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from src.ai_rag.local_transport import validate_local_url, LocalTransportError, NoRedirect
from tools.lock_p8_outputs import validate_real_experiment
from src.ai_rag.ollama_runner import get_model_digest
from src.evaluation.evaluate_experiment import _parse_structured_output

class LockTests(unittest.TestCase):
    def validate(self, rec):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'experiment.json'
            p.write_text(json.dumps([{'task_id':'T01', **{k:rec for k in ('A_llm_only','B_llm_rag','C_llm_rag_structured')}}]))
            validate_real_experiment(p)

    def test_remote_host_refused(self):
        for url in ('https://example.org/api/generate', 'http://127.0.0.1@evil.invalid', 'http://127.0.0.1.evil.invalid'):
            with self.assertRaises(LocalTransportError): validate_local_url(url)

    def test_localhost_pinned(self):
        self.assertEqual(validate_local_url('http://localhost:11434/api/tags'),'http://127.0.0.1:11434/api/tags')

    def test_redirect_refused(self):
        with self.assertRaises(LocalTransportError): NoRedirect().redirect_request(None,None,302,'',{},'http://evil.invalid')

    def test_stub_refused(self):
        with self.assertRaises(ValueError): self.validate({'dry_run':True,'output':'stub'})

    def test_error_refused(self):
        with self.assertRaises(ValueError): self.validate({'dry_run':False,'error':'refused','output':''})

    def test_missing_provenance_refused(self):
        with self.assertRaises(ValueError): self.validate({'dry_run':False,'output':'x'})

    def test_synthetic_valid_record_schema(self):
        self.validate({'dry_run':False,'output':'x','error':None,'model_digest':'synthetic-digest','ollama_version':'synthetic-version'})

    def test_digest_does_not_match_wrong_tag(self):
        with patch('src.ai_rag.ollama_runner._get',return_value={'models':[{'name':'qwen2.5:7b','digest':'wrong'}]}):
            self.assertIsNone(get_model_digest('http://localhost','qwen2.5:1.5b'))

    def test_structured_scalar_does_not_crash(self):
        self.assertEqual(_parse_structured_output('42'),(None,False))

    def test_structured_wrong_evidence_type_refused(self):
        obj={k:'' for k in ('question','relevant_evidence','observed_facts','possible_interpretation','contradicting_evidence','confidence_uncertainty','finding')}
        self.assertFalse(_parse_structured_output(json.dumps(obj))[1])

if __name__=='__main__': unittest.main()
