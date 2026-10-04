"""Render exact Chapter IV run outputs into legible report images.

These are labelled excerpts of recorded stdout/JSON, not fabricated terminal
screenshots. The source files are retained beside the report for inspection.
"""
from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/06_report/bab4_run_figures"
EXP = ROOT / "docs/06_report/bab4_evidence/experiment.json"
ACQ = ROOT / "demo_evidence/ACQ-SIM-001_20260925_010848"
P9 = ROOT / "runtime/working/P9_reconstructed_20260925/evaluation.json"
W, H = 1900, 1150


def font(size, bold=False, mono=False):
    names = (["consolab.ttf", "lucon.ttf"] if bold else ["consola.ttf", "lucon.ttf"]) if mono else (["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"])
    for name in names:
        p = Path("C:/Windows/Fonts") / name
        if p.exists(): return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


TITLE, BODY, MONO, SMALL = font(43, True), font(23), font(24, mono=True), font(21)


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def panel(title, subtitle, source, sections):
    image = Image.new("RGB", (W, H), "#f4f6f9")
    d = ImageDraw.Draw(image)
    d.rectangle((0, 0, W, 14), fill="#007d80")
    d.text((75, 46), title, font=TITLE, fill="#17253d")
    d.text((78, 110), subtitle, font=BODY, fill="#566477")
    d.rounded_rectangle((72, 181, 1828, 1000), radius=17, fill="#141a25")
    d.rounded_rectangle((72, 181, 1828, 230), radius=17, fill="#293447")
    d.text((101, 190), "CUPLIKAN OUTPUT EKSEKUSI · teks dari log/JSON asli", font=SMALL, fill="#e5eef6")
    y = 256
    for heading, lines in sections:
        d.text((106, y), heading, font=font(24, True, mono=True), fill="#7fe5d9")
        y += 38
        for line in lines:
            for wrapped in textwrap.wrap(str(line), width=111, break_long_words=False, break_on_hyphens=False) or [""]:
                d.text((106, y), wrapped, font=MONO, fill="#f1f5f9")
                y += 34
        y += 25
    d.text((76, 1030), "Sumber: " + source, font=SMALL, fill="#566477")
    d.text((76, 1065), "Gambar adalah render teks output, bukan tangkapan layar terminal.", font=SMALL, fill="#9a5e20")
    return image


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    x = json.loads(EXP.read_text(encoding="utf-8"))
    acq = json.loads((ACQ / "acquisition_manifest.json").read_text(encoding="utf-8-sig"))
    ext = json.loads((ACQ / "artifacts/artifact_manifest.json").read_text(encoding="utf-8-sig"))
    p9 = json.loads(P9.read_text(encoding="utf-8"))
    master = sha(ACQ / "master/libera_messages.db")
    working = sha(ACQ / "working/libera_messages.db")
    assert master == working == acq["master_sha256"]
    assert sha(ACQ / "artifacts/artifacts.csv") == ext["normalized_artifacts_sha256"]

    panel("Gambar IV.1 · Verifikasi hash akuisisi",
          "Output pemeriksaan ulang master dan working copy ACQ-SIM-001",
          "acquisition_manifest.json; dua berkas SQLite asli",
          [("PERINTAH / METODE", ["SHA-256(master/libera_messages.db)", "SHA-256(working/libera_messages.db)"]),
           ("HASIL", [f"master  = {master}", f"working = {working}",
                      f"manifest.master_sha256 = {acq['master_sha256']}",
                      f"working_matches_master = {str(acq['working_matches_master']).lower()}",
                      f"acquisition_type = {acq['acquisition_type']}"])])\
        .save(OUT / "IV-01_hash_run.png", dpi=(200, 200), optimize=True)

    clean_output = x["clean"]["remediated"]["stdout"]
    clean_json = json.loads(clean_output)
    panel("Gambar IV.2 · Output ekstraksi P4",
          "Ekstraktor diperbaiki dijalankan pada salinan bersih dan manifest valid",
          "experiment.json: clean.remediated.stdout; artifact_manifest.json",
          [("EKSEKUSI BERSIH", [f"exit_code = {x['clean']['remediated']['exit_code']}",
                                 f"status = {clean_json['status']}",
                                 f"source_sha256 = {clean_json['source_sha256']}",
                                 f"messages = {clean_json['messages']}",
                                 f"chats = {clean_json['chats']}"]),
           ("MANIFEST EKSTRAKSI HISTORIS", [f"sqlite_integrity_check = {ext['sqlite_integrity_check']}",
                                            f"foreign_key_error_count = {ext['foreign_key_error_count']}",
                                            f"normalized_artifacts_sha256 = {ext['normalized_artifacts_sha256']}"])])\
        .save(OUT / "IV-02_ekstraksi_run.png", dpi=(200, 200), optimize=True)

    panel("Gambar IV.3 · Uji ulang dua temuan",
          "Exit code dan stderr dari eksekusi ekstraktor lama vs perbaikan",
          "experiment.json: clean, tamper, missing_manifest",
          [("KONTROL BERSIH", [f"lama exit={x['clean']['legacy']['exit_code']}; baru exit={x['clean']['remediated']['exit_code']}"]),
           ("F-01 · DATABASE DIUBAH", [f"lama exit={x['tamper']['legacy']['exit_code']}; baru exit={x['tamper']['remediated']['exit_code']}",
                                      x["tamper"]["remediated"]["stderr"].strip()]),
           ("F-02 · MANIFEST HILANG", [f"lama exit={x['missing_manifest']['legacy']['exit_code']}; baru exit={x['missing_manifest']['remediated']['exit_code']}",
                                        "Acquisition manifest not found (path sementara disingkat)."])])\
        .save(OUT / "IV-03_retest_run.png", dpi=(200, 200), optimize=True)

    t = x["tamper"]
    panel("Gambar IV.4 · Output ancaman terkendali",
          "Log statis dan dinamis dari manipulasi satu pesan pada salinan sementara",
          "experiment.json: tamper; scripts/run_uas_ch4_sandbox.py",
          [("SAMPEL / IOC", [f"message_id = {t['message_id']}", f"marker = {t['marker']}",
                              f"before_db_sha256 = {t['before_db_sha256']}",
                              f"after_db_sha256  = {t['after_db_sha256']}"]),
           ("PERILAKU SAAT DIJALANKAN", [f"sqlite_integrity_check = {t['sqlite_integrity_check']}",
                                          f"message_count_after = {t['message_count_after']}",
                                          f"legacy extractor exit_code = {t['legacy']['exit_code']}",
                                          f"remediated extractor exit_code = {t['remediated']['exit_code']}",
                                          "detector = Working-copy SHA-256 mismatch"])])\
        .save(OUT / "IV-04_ancaman_run.png", dpi=(200, 200), optimize=True)

    c = p9["integrity"]["conditions"]
    panel("Gambar IV.5 · Output validasi P9",
          "Angka diambil dari evaluation.json dan kebijakan karantina sitasi",
          "runtime/working/P9_reconstructed_20260925/evaluation.json",
          [("STATUS", [f"{p9['status']}",
                       f"labeled_rows = {p9['ground_truth_evaluation']['labeled_rows']}",
                       f"reference_target = {p9['ground_truth_evaluation']['reference_target']}"]),
           ("KONDISI A / B / C", [f"A: outputs={c['A_llm_only']['outputs']}; cited={c['A_llm_only']['unique_cited_artifacts']}",
                                    f"B: outputs={c['B_llm_rag']['outputs']}; cited={c['B_llm_rag']['unique_cited_artifacts']}; invalid={c['B_llm_rag']['invalid_citation_count']}",
                                    f"C: outputs={c['C_llm_rag_structured']['outputs']}; cited={c['C_llm_rag_structured']['unique_cited_artifacts']}; invalid={c['C_llm_rag_structured']['invalid_citation_count']}",
                                    f"C: structured_json_valid={c['C_llm_rag_structured']['structured_json_valid']}"])])\
        .save(OUT / "IV-05_evaluasi_run.png", dpi=(200, 200), optimize=True)
    print(f"Generated 5 run-output figures in {OUT}")


if __name__ == "__main__":
    main()
