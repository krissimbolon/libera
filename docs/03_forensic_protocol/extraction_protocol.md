# P4 Extraction Protocol — LIBERA

Tujuan: mengubah working copy acquisition menjadi artifact terstruktur tanpa kehilangan traceability.

## Input gate

P4 hanya memakai working copy dari ACQ package yang hash-nya sudah diverifikasi. Master evidence tidak dipakai langsung untuk examination.

## Artifact identity

Setiap output bermakna diberi `ART-#####`.

Contoh kategori:
- message table;
- contact/actor table;
- conversation table;
- attachment index;
- timestamp/timeline table;
- app/export metadata;
- parser/extraction log.

## Wajib dicatat per ART

- artifact_id;
- acquisition_id;
- source path/object;
- source hash bila berupa file;
- extraction method;
- tool/script;
- tool version / git commit;
- extraction timestamp;
- output path;
- output SHA-256;
- row/object count;
- timezone interpretation;
- transformation notes;
- known limitations.

## Message normalization

Jangan silently overwrite raw extracted values.

Jika field perlu dinormalisasi:
- simpan raw value;
- simpan normalized value pada field terpisah;
- catat transformasi.

Timestamp:
- pertahankan raw timestamp;
- dokumentasikan timezone;
- buat normalized timestamp hanya sebagai derived field.

## QA extraction

Minimum:
- parser selesai tanpa silent dropped rows;
- row count dicatat;
- duplicate artifact key diperiksa;
- timestamp parse failures dicatat;
- sender/recipient/conversation integrity diperiksa;
- reply/reference integrity diperiksa bila tersedia;
- output hash dibuat;
- spot-check raw vs extracted dilakukan anggota kedua.

## Blinding

Artifact examiner tidak boleh memiliki:
- ground-truth labels;
- hidden provenance labels yang tidak mungkin diperoleh examiner;
- source court reconstruction;
- indikator “relevant/distractor” evaluator.

Data internal tersebut boleh ada hanya pada evaluator package terpisah untuk P9.

## Handoff

P5/P6/P7 menerima ART tables + provenance ke ACQ, bukan P2 design corpus.
