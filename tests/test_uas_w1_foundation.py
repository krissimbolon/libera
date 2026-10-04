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
    p4 = ext.run(db, artifacts, tmp_path / 'p4.json', expected_sha256=p3['acquisition_sha256'])
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
    # The forensic-first workbench (merged from libera-presentasi) reads the
    # acquired ChatSim SQLite snapshot read-only instead of artifact CSVs. The
    # original W1 intent is preserved: no stale ART-0000x container names, and
    # the extractor still writes the ARTFILE-* containers.
    source = (ROOT / 'workbench/libera_workbench.py').read_text(encoding='utf-8')
    source += (ROOT / 'workbench/chatsim_data.py').read_text(encoding='utf-8')
    extractor = (ROOT / 'tools/extract_acquired_chatsim.py').read_text(encoding='utf-8')
    for stale in ['ART-00001_messages.csv', 'ART-00002_chats.csv']:
        assert stale not in source and stale not in extractor
    for filename in ['ARTFILE-00001_messages.csv','ARTFILE-00002_chats.csv']:
        assert filename in extractor
    assert 'mode=ro' in source  # acquired snapshot is opened read-only


def test_p4_trusted_digest_rejects_structurally_valid_tampering(tmp_path):
    import sqlite3
    db = tmp_path / 'source.sqlite'
    p3 = acq.run(CORPUS, db, tmp_path / 'acq.json')
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE messages SET message_text='synthetic tamper test' WHERE message_id=(SELECT message_id FROM messages LIMIT 1)")
    with pytest.raises(ext.ExtractionError, match='trusted expected digest'):
        ext.run(db, tmp_path / 'artifacts.csv', tmp_path / 'p4.json', expected_sha256=p3['acquisition_sha256'])
    assert not (tmp_path / 'artifacts.csv').exists()
    assert not (tmp_path / 'p4.json').exists()


def test_p4_rejects_malformed_trusted_digest(tmp_path):
    db = tmp_path / 'source.sqlite'
    db.write_bytes(b'synthetic')
    with pytest.raises(ext.ExtractionError, match='64 hex'):
        ext.run(db, tmp_path / 'artifacts.csv', tmp_path / 'p4.json', expected_sha256='invalid')


def test_windows_wrapper_static_gate_order_and_hash_wiring():
    local = (ROOT / 'scripts/run_libera_local.ps1').read_text()
    demo = (ROOT / 'scripts/run_libera_demo.ps1').read_text()
    first_stage = local.index('Write-Host "=== Libera')
    assert local.index('if ($GroundTruthPath)') < first_stage
    assert local.index('if (Test-Path "runtime/working/P8/p8_lock_manifest.json")') < first_stage
    assert '--expected-sha256 $AcquisitionSha256' in local
    assert '--expected-sha256 $freshAcquisition.acquisition_sha256' in local
    lock = local.index('Run-Python tools/lock_p8_outputs.py')
    assert local.rfind('} else {', 0, lock) > local.index('if ($DryRun)', local.index('Write-Host "[P6]'))
    assert '--ground-truth' not in local
    assert demo.index('if (Test-Path "runtime/working/P8/p8_lock_manifest.json")') < demo.index('& powershell -ExecutionPolicy')
    assert demo.index('$workingSha256 -ne $freshCustody.master_sha256') < demo.index('& py -3 tools/extract_acquired_chatsim.py')
