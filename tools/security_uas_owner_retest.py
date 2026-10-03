#!/usr/bin/env python3
"""Coordinator/worker local retest of owner-adopted APIs; synthetic only."""
import argparse,json,subprocess,sys
from pathlib import Path

P4_PROBE = '''
import hashlib,json,sqlite3,tempfile
from pathlib import Path
from src.forensics.extract_artifacts import run,ExtractionError
with tempfile.TemporaryDirectory() as td:
 p=Path(td); db=p/'sample.sqlite'; c=sqlite3.connect(db)
 c.execute('CREATE TABLE messages(message_id,conversation_id,timestamp,sender_id,recipient_id,message_text,message_type,reply_to_message_id,attachment_id)')
 c.execute("INSERT INTO messages VALUES ('SIM-1','SIM','2026-01-01T00:00:00+00:00','A','B','synthetic','text',NULL,NULL)")
 c.commit(); c.close(); digest=hashlib.sha256(db.read_bytes()).hexdigest()
 run(db,p/'intact.csv',p/'intact.json',expected_sha256=digest)
 c=sqlite3.connect(db); c.execute("UPDATE messages SET message_text='synthetic changed'"); c.commit(); c.close()
 blocked=False
 try: run(db,p/'tampered.csv',p/'tampered.json',expected_sha256=digest)
 except ExtractionError: blocked=True
 assert blocked and not (p/'tampered.csv').exists()
 print(json.dumps({'intact_accepted':True,'tamper_rejected':blocked,'tampered_output_absent':True}))
'''
AI_PROBE = '''
import json
from src.ai_rag.local_transport import validate_local_url,LocalTransportError,NoRedirect
from src.ai_rag.validate_output import validate_structured_finding,ValidationError,REQUIRED_FIELDS
blocked=False
try: validate_local_url('https://example.invalid/api/generate')
except LocalTransportError: blocked=True
assert blocked
assert validate_local_url('http://localhost:11434/api/generate').startswith('http://127.0.0.1:11434/')
redirect=False
try: NoRedirect().redirect_request(None,None,302,'redirect',{},'https://example.invalid')
except LocalTransportError: redirect=True
assert redirect
f={k:'' for k in REQUIRED_FIELDS}; f['relevant_evidence']=[{'annotation_notes':'synthetic canary'}]
nested=False
try: validate_structured_finding(f)
except ValidationError: nested=True
assert nested
print(json.dumps({'remote_rejected':blocked,'localhost_literal_rewrite':True,'redirect_rejected':redirect,'nested_gt_rejected':nested,'network_calls':0}))
'''
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--w1',required=True);ap.add_argument('--w3',required=True);ap.add_argument('--output',default='docs/08_uas/evidence/W2/owner_retest.json');a=ap.parse_args()
 results={}
 for owner,root,probe in [('W1',a.w1,P4_PROBE),('W3',a.w3,AI_PROBE)]:
  dirty=subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True)
  assert not dirty, f'{owner} worktree must be committed'
  sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
  proc=subprocess.run([sys.executable,'-c',probe],cwd=root,text=True,capture_output=True)
  assert proc.returncode==0, proc.stderr
  results[owner]={'source_commit':sha,'observed':json.loads(proc.stdout),'exit_code':proc.returncode}
 Path(a.output).write_text(json.dumps(results,indent=2)+'\n'); print(json.dumps(results,indent=2))
if __name__=='__main__':main()
