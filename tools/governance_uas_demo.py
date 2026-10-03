"""Safe synthetic-only governance demonstration; never ingests project evidence or GT."""
import argparse, hashlib, json, os, tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output', required=True); args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    synthetic={'name':'DEMO PERSON','phone':'080000000000','nik':'0000000000000000','age':27,'district':'DEMO DISTRICT'}
    released={k:v for k,v in synthetic.items() if k in ('age','district')}
    identifiers=('name','phone','nik')
    with tempfile.TemporaryDirectory() as td:
        vault=Path(td)/'vault'; vault.mkdir(mode=0o700)
        master=vault/'master.json'; master.write_text(json.dumps(synthetic)); master.chmod(0o600)
        original=master.read_bytes(); expected=hashlib.sha256(original).hexdigest()
        backup=vault/'backup.json'; backup.write_bytes(original); backup.chmod(0o600)
        working=vault/'working.json'; working.write_bytes(original+b' ')
        detected=hashlib.sha256(working.read_bytes()).hexdigest()!=expected
        working.write_bytes(backup.read_bytes())
        recovered=hashlib.sha256(working.read_bytes()).hexdigest()==expected
        start=datetime(2026,10,3,11,0,tzinfo=timezone.utc)
        elapsed=(start+timedelta(hours=2)-start).total_seconds()/3600
        result={'exercise_type':'AUTOMATED_SYNTHETIC_TABLETOP_NOT_TEAM_DRILL','executed_at':datetime.now(timezone.utc).isoformat(),'real_personal_data':False,'real_network_or_notifications':False,'privacy':{'fixture_records':1,'direct_identifier_fields_before':3,'direct_identifier_fields_after':sum(k in released for k in identifiers),'retained_fields':list(released),'vault_mode':oct(vault.stat().st_mode&0o777),'master_mode':oct(master.stat().st_mode&0o777),'anonymity_proven':False,'encryption_tested':False},'integrity':{'tamper_detected':detected,'backup_restored_exact_hash':recovered,'expected_sha256':expected},'tabletop':{'scenario':'Synthetic working-copy alteration and hypothetical confidentiality disclosure','simulated_events':[{'t_hours':0,'decision':'Stop analysis; preserve master and isolate working copy'},{'t_hours':0.25,'decision':'Declare integrity incident; preserve hashes and timeline'},{'t_hours':1,'decision':'Assess hypothetical personal-data breach and authorization; prepare notification draft'},{'t_hours':2,'decision':'Simulated controller approves draft to subject and institution; send nothing'},{'t_hours':4,'decision':'Restore verified backup, rerun extraction, keep experiment lock invalidated pending separate study'}],'simulated_notification_decision_hours':elapsed,'statutory_window_hours':72,'within_window':elapsed<=72,'notification_sent':False,'legal_clock_rule':'Conservative internal clock starts at first detection; statutory text says paling lambat 3 x 24 jam, confirm legal trigger for actual case.'},'limitations':['One synthetic fixture; no live ACL bypass test, key management, real recovery SLA, real breach notification or human participants.','Field suppression retains quasi-identifiers and is not proof of anonymization.','Demonstration does not harden canonical pipeline.']}
        assert detected
        assert recovered
        assert result['privacy']['direct_identifier_fields_after']==0
        assert vault.stat().st_mode&0o777 == 0o700 and master.stat().st_mode&0o777 == 0o600
        assert result['tabletop']['within_window']
    (out/'governance_demo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checks':5,'tamper_detected':detected,'recovered':recovered,'released_direct_identifiers':0,'synthetic_only':True}))
if __name__=='__main__': main()
