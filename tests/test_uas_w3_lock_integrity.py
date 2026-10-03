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

    def finding(self):
        return {k:[] if k=='relevant_evidence' else 'synthetic' for k in ('question','relevant_evidence','observed_facts','possible_interpretation','contradicting_evidence','confidence_uncertainty','finding')}

    def test_manifest_mismatch_stops_before_private_gt(self):
        from tools.verify_p8_lock import verify_manifest
        from src.evaluation.evaluate_experiment import EvaluationError
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);artifact=d/'public.csv';artifact.write_text('public canary')
            lock=d/'lock.json';lock.write_text(json.dumps({'status':'P8_OUTPUTS_LOCKED_BEFORE_GROUND_TRUTH','files':{'p4_artifacts':{'path':str(artifact),'sha256':'0'*64},'p5_baseline':{'path':str(d/'baseline.json')},'p8_experiment_output':{'path':str(d/'out.json')}}}))
            # A missing private file cannot be read: public verification has no GT parameter.
            with patch('src.evaluation.evaluate_experiment.load_ground_truth',side_effect=AssertionError('GT read')) as gt:
                with self.assertRaises(EvaluationError): verify_manifest(lock)
                gt.assert_not_called()

    def test_nested_gt_refused(self):
        from src.ai_rag.validate_output import validate_structured_finding, ValidationError
        finding=self.finding();finding['relevant_evidence']=[{'nested':{'annotation_notes':'canary'}}]
        with self.assertRaises(ValidationError): validate_structured_finding(finding)

    def test_incomplete_registered_tasks_refused(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);p=d/'out.json';t=d/'tasks.json'
            rec={'dry_run':False,'output':json.dumps(self.finding()),'model_digest':'synthetic','ollama_version':'synthetic'}
            p.write_text(json.dumps([{'task_id':'T01','question':'q',**{c:rec for c in ('A_llm_only','B_llm_rag','C_llm_rag_structured')}}]))
            t.write_text(json.dumps({'tasks':[{'task_id':'T01','question':'q'},{'task_id':'T02','question':'q2'}]}))
            with self.assertRaisesRegex(ValueError,'incomplete'): validate_real_experiment(p,t)

    def test_registered_model_mismatch_refused(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);p=d/'out.json';c=d/'config.json'
            config=json.loads(Path('configs/p6_p7_config.json').read_text());c.write_text(json.dumps(config))
            rec={**config['ollama'],'dry_run':False,'output':json.dumps(self.finding()),'model_digest':'synthetic','ollama_version':'synthetic','prompt_version':config['prompt']['prompt_version'],'query':'q'}
            rec['model']='wrong:tag'
            row={'task_id':'T01','question':'q','retrieval_trace':{'k':8,'embedding_method':'ollama','embedding_model':'bge-m3'},**{k:rec for k in ('A_llm_only','B_llm_rag','C_llm_rag_structured')}}
            p.write_text(json.dumps([row]))
            with self.assertRaisesRegex(ValueError,'model'): validate_real_experiment(p,config_path=c)

    def test_invalid_c_refused(self):
        with self.assertRaisesRegex(ValueError,'JSON'):
            self.validate({'dry_run':False,'output':'42','model_digest':'synthetic','ollama_version':'synthetic'})

    def test_invalid_task_row_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'out.json';p.write_text('[42]')
            with self.assertRaisesRegex(ValueError,'object'): validate_real_experiment(p)

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
        self.validate({'dry_run':False,'output':json.dumps(self.finding()),'error':None,'model_digest':'synthetic-digest','ollama_version':'synthetic-version'})

    def test_digest_does_not_match_wrong_tag(self):
        with patch('src.ai_rag.ollama_runner._get',return_value={'models':[{'name':'qwen2.5:7b','digest':'wrong'}]}):
            self.assertIsNone(get_model_digest('http://localhost','qwen2.5:1.5b'))

    def test_structured_scalar_does_not_crash(self):
        self.assertEqual(_parse_structured_output('42'),(None,False))

    def test_structured_wrong_evidence_type_refused(self):
        obj={k:'' for k in ('question','relevant_evidence','observed_facts','possible_interpretation','contradicting_evidence','confidence_uncertainty','finding')}
        self.assertFalse(_parse_structured_output(json.dumps(obj))[1])

if __name__=='__main__': unittest.main()
