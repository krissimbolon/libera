"""W1 independent forensic pipeline and evidence preservation regression checks."""
import csv
from pathlib import Path
import pytest
from src.forensics import acquisition_simulator as acq, extract_artifacts as ext
from src.baseline import traditional_baseline as baseline

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'data/adaptasi_indonesia/corpus_whatsapp_10000.csv'

def test_p3_p4_p5_foundation(tmp_path):
    before = acq.sha256_file(CORPUS)
    db = tmp_path / 'source.sqlite'
    p3 = acq.run(CORPUS, db, tmp_path / 'acq.json')
    source_hash = acq.sha256_file(db)
    artifacts = tmp_path / 'artifacts.csv'
    p4 = ext.run(db, artifacts, tmp_path / 'p4.json')
    p5 = baseline.run(artifacts, ROOT / 'configs/investigation_tasks.json', tmp_path / 'P5')
    assert before == acq.CANONICAL_SHA256 == acq.sha256_file(CORPUS)
    assert source_hash == acq.sha256_file(db)
    assert p3['is_real_device_acquisition'] is False
    assert p4['artifact_count'] == p5['message_count'] == 10000
    assert p4['chat_count'] == 26 and p5['task_count'] == 10
    with artifacts.open() as f:
        rows = list(csv.DictReader(f))
    assert len({r['artifact_id'] for r in rows}) == 10000
    assert 'source_provenance' not in rows[0]
    assert 'ground_truth' not in rows[0]
    findings = (tmp_path / 'P5/baseline_findings.json').read_bytes()
    baseline.run(artifacts, ROOT / 'configs/investigation_tasks.json', tmp_path / 'P5')
    assert findings == (tmp_path / 'P5/baseline_findings.json').read_bytes()

@pytest.mark.parametrize('alias', ['same','symlink','hardlink'])
def test_p4_rejects_input_alias(tmp_path, alias):
    db = tmp_path / 'input.sqlite'
    db.write_bytes(b'evidence-preserve')
    output = db
    if alias != 'same':
        output = tmp_path / 'output.csv'
        if alias == 'symlink': output.symlink_to(db)
        else: output.hardlink_to(db)
    with pytest.raises(ext.ExtractionError, match='distinct'):
        ext.run(db, output, tmp_path / 'manifest.json')
    assert db.read_bytes() == b'evidence-preserve'

def test_p3_rejects_frozen_input_as_output(tmp_path):
    before = acq.sha256_file(CORPUS)
    with pytest.raises(acq.AcquisitionSimulationError, match='distinct'):
        acq.run(CORPUS, CORPUS, tmp_path / 'manifest.json')
    assert acq.sha256_file(CORPUS) == before

def test_workbench_uses_current_container_names():
    source = (ROOT / 'workbench/libera_workbench.py').read_text()
    extractor = (ROOT / 'tools/extract_acquired_chatsim.py').read_text()
    for filename in ['ARTFILE-00001_messages.csv','ARTFILE-00002_chats.csv']:
        assert filename in source and filename in extractor
