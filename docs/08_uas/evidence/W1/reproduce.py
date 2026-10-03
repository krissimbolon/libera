"""Run from repository root: python docs/08_uas/evidence/W1/reproduce.py."""
import csv
import hashlib
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from src.forensics import acquisition_simulator as acq, extract_artifacts as ext
from src.baseline import traditional_baseline as base
root = Path(__file__).resolve().parents[4]
corpus = root / 'data/adaptasi_indonesia/corpus_whatsapp_10000.csv'
results = {'is_physical_acquisition': False, 'gt_accessed': False}
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    db = d / 'source.sqlite'
    before = acq.sha256_file(corpus)
    p3 = acq.run(corpus, db, d / 'acq.json')
    db_hash = acq.sha256_file(db)
    arts = d / 'artifacts.csv'
    p4 = ext.run(db, arts, d / 'p4.json')
    p5 = base.run(arts, root / 'configs/investigation_tasks.json', d / 'P5')
    with arts.open() as f: rows = list(csv.DictReader(f))
    first = (d / 'P5/baseline_findings.json').read_bytes()
    base.run(arts, root / 'configs/investigation_tasks.json', d / 'P5')
    results.update(corpus_sha256=before, corpus_preserved=before==acq.sha256_file(corpus), acquisition_sha256=db_hash, acquisition_preserved=db_hash==acq.sha256_file(db), artifact_count=len(rows), unique_artifact_ids=len({r['artifact_id'] for r in rows}), chat_count=p4['chat_count'], task_count=p5['task_count'], actor_count=p5['actor_count'], relationship_count=p5['relationship_count'], artifacts_sha256=p4['output_sha256'], baseline_findings_sha256=hashlib.sha256(first).hexdigest(), deterministic_findings=first==(d/'P5/baseline_findings.json').read_bytes(), output_fields=list(rows[0]), p5_output_files=sorted(p.name for p in (d/'P5').iterdir()))
    rejected=[]
    for alias in ['same','symlink','hardlink']:
        target=db
        if alias!='same':
            target=d/alias
            if alias=='symlink': target.symlink_to(db)
            else: target.hardlink_to(db)
        try: ext.run(db,target,d/'reject.json')
        except ext.ExtractionError: rejected.append(alias)
    results['p4_aliases_rejected']=rejected
    try: acq.run(corpus,corpus,d/'reject.json')
    except acq.AcquisitionSimulationError: results['p3_corpus_alias_rejected']=True
    results['workbench_current_names']=all(n in (root/'workbench/libera_workbench.py').read_text() for n in ['ARTFILE-00001_messages.csv','ARTFILE-00002_chats.csv'])
    assert all(results[k] for k in ['corpus_preserved','acquisition_preserved','deterministic_findings','p3_corpus_alias_rejected','workbench_current_names'])
    assert len(rejected)==3 and len(rows)==10000 and p4['chat_count']==26 and p5['task_count']==10
print(json.dumps(results,indent=2))
