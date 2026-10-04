"""Guards against competing sources of truth in the archived snapshot."""
import csv
import hashlib
import json
from pathlib import Path

from src.ai_rag import ollama_runner

ROOT = Path(__file__).resolve().parents[1]
CORPUS_SHA = "a014a02ebad298a33267da8631f3a2d1906a537ae558c1849622904c225467e6"


def test_frozen_corpus_matches_all_declarations():
    corpus = ROOT / "data/adaptasi_indonesia/corpus_whatsapp_10000.csv"
    manifest = json.loads((ROOT / "data/adaptasi_indonesia/corpus_freeze_manifest.json").read_text(encoding="utf-8"))
    config = json.loads((ROOT / "configs/p6_p7_config.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(corpus.read_bytes()).hexdigest() == CORPUS_SHA
    assert manifest["corpus_sha256"] == config["frozen_p2"]["sha256"] == CORPUS_SHA
    with corpus.open(encoding="utf-8", newline="") as handle:
        assert sum(1 for _ in csv.DictReader(handle)) == manifest["final_row_count"] == 10000
    for doc in ("README.md",):
        assert CORPUS_SHA in (ROOT / doc).read_text(encoding="utf-8"), doc


def test_registered_config_matches_runner_defaults():
    config = json.loads((ROOT / "configs/p6_p7_config.json").read_text(encoding="utf-8"))
    ollama = config["ollama"]
    assert ollama["model"] == ollama_runner.DEFAULT_MODEL
    assert ollama["temperature"] == ollama_runner.DEFAULT_TEMPERATURE
    assert ollama["seed"] == ollama_runner.DEFAULT_SEED
    assert ollama["num_ctx"] == ollama_runner.DEFAULT_NUM_CTX
    assert ollama["num_predict"] == ollama_runner.DEFAULT_NUM_PREDICT
    assert ollama["repeat_penalty"] == ollama_runner.DEFAULT_REPEAT_PENALTY
    assert ollama["repeat_last_n"] == ollama_runner.DEFAULT_REPEAT_LAST_N
    source = (ROOT / "src/ai_rag/run_experiment.py").read_text(encoding="utf-8")
    assert f'default="{config["prompt"]["prompt_version"]}"' in source
