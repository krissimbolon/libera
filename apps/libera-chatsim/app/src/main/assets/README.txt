Generated assets live here.

Run from repository root before building the Android app:

  python tools/build_demo_seed.py

This creates:
  messages_seed.jsonl
  source_anomalies.jsonl
  seed_manifest.json

Do not hand-edit generated seed data.
Do not include evaluator-only ground-truth labels in DEV-001.
