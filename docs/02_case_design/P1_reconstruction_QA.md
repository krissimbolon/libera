# P1 Reconstruction QA

Run before committing reconstructed message rows:

```bash
python src/reconstruction/validate_reconstruction.py
```

Optional test:

```bash
pytest tests/test_reconstruction_schema.py
```

The validator enforces:
- exactly 543 rows;
- unique `original_line` values 1–543;
- only approved reconstruction statuses;
- source references for court-supported message rows;
- no hidden source content inside rows marked `MISSING_FROM_PUBLIC_RECORD`.

It deliberately does not infer missing messages or decide whether a quotation is substantively correct. Human source checking remains required.
