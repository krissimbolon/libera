#!/usr/bin/env python3
"""Verify locked public P8 inputs without reading or accepting private GT."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
if __package__ in (None, ''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.evaluation.evaluate_experiment import EvaluationError, verify_p8_lock, load_artifacts, integrity_precheck

def verify_manifest(path: Path, artifacts_override: Path | None = None):
    manifest=json.loads(path.read_text(encoding='utf-8'))
    files=manifest.get('files',{})
    try:
        artifacts=artifacts_override or Path(files['p4_artifacts']['path'])
        baseline=Path(files['p5_baseline']['path'])
        experiment=Path(files['p8_experiment_output']['path'])
    except (KeyError, TypeError) as exc:
        raise EvaluationError('Missing required manifest paths') from exc
    result=verify_p8_lock(path,artifacts,baseline,experiment)
    _,ids,_=load_artifacts(artifacts)
    integrity=integrity_precheck(experiment,set(ids))
    if integrity['retrieval_invalid_evidence_ids'] or any(c['errors'] or c['invalid_citation_count'] for c in integrity['conditions'].values()):
        raise EvaluationError('P8 evidence integrity failed')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock-manifest',required=True)
    parser.add_argument('--artifacts',default=None)
    args=parser.parse_args()
    try:
        result=verify_manifest(Path(args.lock_manifest),Path(args.artifacts) if args.artifacts else None)
    except (EvaluationError,ValueError,OSError,TypeError) as exc:
        parser.exit(1,f'P8 verification failed: {exc}\n')
    print(json.dumps(result))

if __name__=='__main__': main()
