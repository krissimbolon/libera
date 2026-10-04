"""Generate report figures from Libera's recorded artifacts.

The script reads evidence but never edits acquisition masters or runtime results.
Figures depicting future exercises are explicitly labelled as plans.
"""

from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "06_report" / "uas_figures"
ACQ = ROOT / "demo_evidence" / "ACQ-SIM-001_20260925_010848"
W, H = 1800, 1050
NAVY = "#17253d"
BLUE = "#176b9a"
TEAL = "#007d80"
RED = "#b64749"
AMBER = "#a36816"
PAPER = "#f5f7fa"
MUTED = "#566477"
LINE = "#d6dfe8"


def font(size: int, bold: bool = False):
    names = (["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"])
    for name in names:
        for base in [Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")]:
            p = base / name
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


F_TITLE, F_SUB, F_BODY, F_SMALL, F_BIG = font(46, True), font(25), font(29), font(22), font(57, True)


def canvas(code: str, title: str, subtitle: str, source: str, badge: str):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 17), fill=TEAL)
    d.text((84, 52), f"{code}  {title}", font=F_TITLE, fill=NAVY)
    d.text((86, 122), subtitle, font=F_SUB, fill=MUTED)
    d.rounded_rectangle((83, 955, 1717, 1018), radius=15, fill="#e8eef3")
    d.text((105, 972), f"SUMBER  {source}", font=F_SMALL, fill=MUTED)
    bw = d.textbbox((0, 0), badge, font=F_SMALL)[2] + 38
    d.rounded_rectangle((W - bw - 84, 183, W - 84, 229), radius=14, fill=TEAL if badge == "HASIL OBSERVASI" else AMBER)
    d.text((W - bw - 65, 193), badge, font=F_SMALL, fill="white")
    return im, d


def box(d, xy, title, lines=(), fill="white", accent=TEAL, title_size=29, body_size=23):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=19, fill=fill, outline=LINE, width=2)
    d.rounded_rectangle((x1, y1, x1 + 11, y2), radius=6, fill=accent)
    d.text((x1 + 31, y1 + 25), title, font=font(title_size, True), fill=NAVY)
    y = y1 + 79
    for line in lines:
        d.text((x1 + 31, y), str(line), font=font(body_size), fill=MUTED)
        y += body_size + 13


def arrow(d, start, end, label=None, color=TEAL):
    d.line((start, end), fill=color, width=7)
    x1, y1 = start
    x2, y2 = end
    import math

    a = math.atan2(y2 - y1, x2 - x1)
    h = 20
    d.polygon([(x2, y2), (x2 - h * math.cos(a - .55), y2 - h * math.sin(a - .55)),
               (x2 - h * math.cos(a + .55), y2 - h * math.sin(a + .55))], fill=color)
    if label:
        d.text(((x1 + x2) / 2 - 80, (y1 + y2) / 2 - 42), label, font=F_SMALL, fill=color)


def save(im, name):
    p = OUT / f"{name}.png"
    im.save(p, optimize=True, dpi=(200, 200))
    return p


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    a = json.loads((ACQ / "acquisition_manifest.json").read_text(encoding="utf-8-sig"))
    e = json.loads((ACQ / "artifacts" / "artifact_manifest.json").read_text(encoding="utf-8-sig"))
    p9 = json.loads((ROOT / "runtime/working/P9_reconstructed_20260925/evaluation.json").read_text(encoding="utf-8-sig"))
    master = ACQ / "master/libera_messages.db"
    working = ACQ / "working/libera_messages.db"
    artifact = ACQ / "artifacts/artifacts.csv"
    assert sha(master) == a["master_sha256"] == sha(working)
    assert sha(artifact) == e["normalized_artifacts_sha256"]
    files = []

    im, d = canvas("G-01", "Arsitektur laboratorium Libera", "Komponen yang dijalankan dan batas data penelitian", "README.md; acquisition_manifest.json", "DIAGRAM REKONSTRUKSI")
    box(d, (84, 300, 420, 530), "Corpus sintetis", ["P2: 10.000 pesan", "SHA-256 dibekukan"])
    box(d, (530, 300, 900, 530), "Emulator Android", ["Libera ChatSim", "DEV-SIM-001"])
    box(d, (1010, 300, 1390, 530), "Akuisisi logis", ["ADB + run-as", "ACQ-SIM-001"])
    box(d, (1420, 300, 1715, 530), "Artefak", ["SQLite → ART-*", "9.997 pesan"])
    for x1, x2 in [(420, 530), (900, 1010), (1390, 1420)]: arrow(d, (x1, 415), (x2, 415))
    box(d, (410, 650, 835, 880), "Analisis baseline", ["P5: linimasa / relasi", "salinan kerja"], accent=BLUE)
    box(d, (960, 650, 1390, 880), "AI lokal + evaluasi", ["P6–P8: Ollama / RAG", "P9: evaluasi proxy"], accent=BLUE)
    d.line((1560, 535, 1560, 605, 620, 605), fill=TEAL, width=7)
    arrow(d, (620, 605), (620, 650))
    arrow(d, (1170, 605), (1170, 650))
    files.append(save(im, "G-01_arsitektur_lab"))

    im, d = canvas("G-02", "Rantai bukti dan analisis", "Urutan artefak dengan pemisahan desain, bukti, dan evaluasi", "P2 hash; manifest P3/P4; lock P8", "DIAGRAM REKONSTRUKSI")
    stages = [("P2", "Desain kasus", "10.000 pesan"), ("DEV-SIM-001", "Pembawa bukti", "ChatSim emulator"),
              ("ACQ-SIM-001", "Master / working", "hash identik"), ("ART-*", "Ekstraksi P4", "9.997 pesan"),
              ("P5–P8", "Analisis", "baseline + AI"), ("P9", "Evaluasi", "proxy provenance")]
    for i, (key, label, detail) in enumerate(stages):
        x = 85 + (i if i < 3 else 5-i) * 560
        y = 285 + (i // 3) * 315
        box(d, (x, y, x + 455, y + 210), key, [label, detail], accent=TEAL if i < 4 else BLUE)
        if i < 2: arrow(d, (x + 455, y + 105), (x + 545, y + 105))
        if 3 <= i < 5: arrow(d, (x, y + 105), (x - 105, y + 105))
    arrow(d, (1490, 500), (1490, 590))
    d.text((94, 868), "Ground truth privat tidak masuk ke P5–P8; output P8 dikunci sebelum P9.", font=F_BODY, fill=NAVY)
    files.append(save(im, "G-02_rantai_bukti"))

    im, d = canvas("G-03", "Workbench ChatSim (arsip)", "Tampilan asli yang tersimpan pada 25 September 2026", "runtime/workbench_overview.png", "TANGKAPAN LAYAR ARSIP")
    shot = Image.open(ROOT / "runtime/workbench_overview.png").convert("RGB")
    redact = ImageDraw.Draw(shot)
    redact.rounded_rectangle((371, 518, 1218, 585), radius=8, fill="#222630")
    redact.text((390, 533), "Path lokal disamarkan untuk laporan", font=font(23), fill="white")
    shot.thumbnail((1490, 690))
    x = (W - shot.width) // 2
    im.paste(shot, (x, 247))
    d.rectangle((x-2, 245, x+shot.width+2, 249+shot.height), outline=LINE, width=3)
    d.text((90, 895), "Snapshot UI ACQ-SIM-LIVE; bukan tangkapan layar emulator atau ACQ-SIM-001.", font=F_SMALL, fill=RED)
    files.append(save(im, "G-03_workbench_arsip"))

    im, d = canvas("G-04", "Integritas master dan salinan kerja", "Hash dihitung ulang dari dua berkas SQLite yang tersedia", "acquisition_manifest.json; master dan working DB", "HASIL OBSERVASI")
    box(d, (95, 280, 830, 535), "MASTER", ["master/libera_messages.db", f"{a['master_size_bytes']:,} byte"], accent=BLUE)
    box(d, (970, 280, 1705, 535), "WORKING COPY", ["working/libera_messages.db", "SHA-256 cocok dengan master"], accent=TEAL)
    arrow(d, (830, 415), (970, 415), "salin")
    box(d, (95, 620, 1705, 852), "SHA-256 terverifikasi", [a["master_sha256"], "Kelas akuisisi: logis, emulator Android; bukan WhatsApp / full filesystem."], accent=TEAL, body_size=27)
    files.append(save(im, "G-04_integritas_akuisisi"))

    im, d = canvas("G-05", "Hasil ekstraksi bukti", "Pemeriksaan artefak dari salinan kerja ACQ-SIM-001", "artifact_manifest.json; artifacts.csv", "HASIL OBSERVASI")
    metrics = [(f"{e['normalized_artifact_count']:,}".replace(",", "."), "artefak pesan"),
               (str(e["chat_count"]), "chat"), (e["sqlite_integrity_check"].upper(), "SQLite integrity"),
               (str(e["foreign_key_error_count"]), "foreign key error")]
    for i, (v, label) in enumerate(metrics):
        x = 90 + i * 420
        d.rounded_rectangle((x, 305, x+370, 600), radius=20, fill="white", outline=LINE, width=2)
        d.text((x+28, 355), v, font=font(77, True), fill=TEAL)
        d.text((x+28, 475), label, font=F_BODY, fill=NAVY)
    box(d, (95, 675, 1705, 872), "ARTIFACT CSV SHA-256", [e["normalized_artifacts_sha256"], "Input examiner P4; tidak berisi label ground truth evaluator."], accent=BLUE, body_size=26)
    files.append(save(im, "G-05_ekstraksi_p4"))

    relations = []
    with open(ROOT / "runtime/working/P5/relationships.csv", encoding="utf-8-sig", newline="") as f:
        relations = list(csv.DictReader(f))
    top = sorted(relations, key=lambda x: int(x["message_count"]), reverse=True)[:7]
    im, d = canvas("G-06", "Relasi komunikasi teratas", "Jumlah pesan per pasangan aktor pada baseline P5", "runtime/working/P5/relationships.csv", "HASIL OLAH DATA")
    maxv = max(int(r["message_count"]) for r in top)
    for i, r in enumerate(top):
        y = 285 + i * 86
        label = f"{r['actor_a']} ↔ {r['actor_b']}"
        d.text((100, y), label, font=F_SUB, fill=NAVY)
        d.rounded_rectangle((640, y+3, 1550, y+39), radius=8, fill="#e3e9ef")
        d.rounded_rectangle((640, y+3, 640+round(910*int(r["message_count"])/maxv), y+39), radius=8, fill=BLUE)
        d.text((1590, y), r["message_count"], font=F_SUB, fill=NAVY)
    files.append(save(im, "G-06_relasi_aktor_p5"))

    im, d = canvas("G-07", "Matriks bukti uji kelemahan", "Tiga slot pengujian Bab IV.2; belum ada bukti perbaikan dan uji ulang lengkap", "struktur laporan UAS; status bukti per 3 Okt 2026", "RENCANA UJI")
    rows = [
        ("F-01", "Akses DB via build debug", "uji akses → batasi → uji ulang"),
        ("F-02", "Perubahan / kehilangan artefak", "mutasi salinan → deteksi hash → uji ulang"),
        ("F-03", "Referensi AI tidak valid", "12 referensi C → karantina → verifikasi"),
    ]
    for i, (code, title, desc) in enumerate(rows):
        y = 286 + i * 195
        box(d, (95, y, 1705, y+165), f"{code}  {title}", [desc], accent=AMBER)
        d.text((1380, y+103), "STATUS: PERLU UJI", font=F_SMALL, fill=RED)
    files.append(save(im, "G-07_matriks_uji_belum_selesai"))

    im, d = canvas("G-08", "Skenario ancaman manipulasi artefak", "Alur eksperimen sandbox yang perlu dieksekusi untuk Bab IV.3", "rencana pengujian; belum ada hasil eksekusi", "RENCANA UJI")
    steps = [("1", "Salinan uji", "Duplikasi working DB"), ("2", "Ancaman", "Ubah satu baris di sandbox"),
             ("3", "IoC", "Hash / row diff / log"), ("4", "Deteksi", "Bandingkan manifest"),
             ("5", "Pemulihan", "Pulihkan dari master")]
    for i, (num, title, detail) in enumerate(steps):
        x = 90 + i * 344
        box(d, (x, 355, x+290, 640), f"{num}. {title}", [detail], accent=AMBER, title_size=27, body_size=21)
        if i < 4: arrow(d, (x+290, 495), (x+335, 495))
    d.text((108, 735), "Analisis statis, dinamis, hash sampel, dan pemetaan ATT&CK harus bersumber dari uji nyata.", font=F_SUB, fill=RED)
    files.append(save(im, "G-08_rencana_ancaman_sandbox"))

    im, d = canvas("G-09", "Sitasi hasil eksperimen A/B/C", "Jumlah referensi valid dan dikarantina pada 30 respons nyata", "P8 v6; P9 reconstructed evaluation.json", "HASIL OLAH DATA")
    conditions = p9["integrity"]["conditions"]
    vals = []
    for label, key in [("A · LLM", "A_llm_only"), ("B · RAG", "B_llm_rag"),
                       ("C · RAG + struktur", "C_llm_rag_structured")]:
        record = conditions[key]
        invalid = record["invalid_citation_count"]
        vals.append((label, record["unique_cited_artifacts"] - invalid, invalid))
    for i, (label, valid, invalid) in enumerate(vals):
        y = 315 + i * 170
        d.text((110, y), label, font=F_BODY, fill=NAVY)
        d.rounded_rectangle((520, y-5, 1510, y+62), radius=13, fill="#e4e9ef")
        if valid: d.rectangle((520, y-5, 520+valid*38, y+62), fill=TEAL)
        if invalid: d.rectangle((520+valid*38, y-5, 520+(valid+invalid)*38, y+62), fill=RED)
        d.text((1540, y+5), f"{valid} / {invalid}", font=F_BODY, fill=NAVY)
    d.rectangle((520, 844, 555, 874), fill=TEAL); d.text((570, 843), "valid", font=F_SMALL, fill=MUTED)
    d.rectangle((740, 844, 775, 874), fill=RED); d.text((790, 843), "dikarantina", font=F_SMALL, fill=MUTED)
    d.text((1140, 842), "Bukan metrik akurasi semantik", font=F_SMALL, fill=RED)
    files.append(save(im, "G-09_sitasi_abc"))

    im, d = canvas("G-10", "Alur perlindungan data statistik", "Rancangan klasifikasi dan batas akses untuk penerapan di sistem statistik", "rancangan Bab V.1; bukan kondisi operasional", "DIAGRAM RANCANGAN")
    stages = [("Pengumpulan", "minimisasi"), ("Penyimpanan", "klasifikasi + enkripsi"),
              ("Pemrosesan", "akses berbasis peran"), ("Analisis", "pseudonimisasi"),
              ("Publikasi", "kontrol disclosure")]
    for i, (title, detail) in enumerate(stages):
        x = 90 + i * 344
        box(d, (x, 350, x+286, 625), title, [detail], accent=TEAL, title_size=26, body_size=21)
        if i < 4: arrow(d, (x+286, 485), (x+335, 485))
    box(d, (230, 730, 1560, 878), "Lintas tahap", ["retensi • audit log • pengendalian akses • respons insiden"], accent=BLUE)
    files.append(save(im, "G-10_alur_perlindungan_data"))

    im, d = canvas("G-11", "Alur tabletop penanganan insiden", "Rancangan simulasi kebocoran atau manipulasi bukti", "rancangan Bab V.2; simulasi belum terdokumentasi", "RENCANA TABLETOP")
    phases = [("T0", "Deteksi & triase"), ("T+2 jam", "Preservasi bukti"), ("T+8 jam", "Penahanan"),
              ("T+24 jam", "Penilaian dampak"), ("≤3×24 jam", "Keputusan notifikasi")]
    d.line((185, 500, 1600, 500), fill=BLUE, width=8)
    for i, (t, name) in enumerate(phases):
        x = 185 + i * 352
        d.ellipse((x-16, 484, x+16, 516), fill=TEAL)
        d.text((x-70, 375 if i%2 == 0 else 560), t, font=font(31, True), fill=NAVY)
        d.text((x-90, 423 if i%2 == 0 else 608), name, font=F_SMALL, fill=MUTED)
    d.text((115, 780), "Waktu di atas adalah target latihan, bukan kronologi insiden yang telah terjadi.", font=F_SUB, fill=RED)
    files.append(save(im, "G-11_rencana_tabletop"))

    im, d = canvas("G-12", "Arsitektur keamanan target", "Kontrol berlapis untuk sistem informasi statistik", "rancangan Bab V.4; pemetaan Annex A dalam tabel laporan", "DIAGRAM RANCANGAN")
    box(d, (115, 280, 500, 520), "Identitas & akses", ["MFA; least privilege", "pemisahan peran"])
    box(d, (710, 280, 1095, 520), "Data & bukti", ["enkripsi; hash", "backup; retensi"])
    box(d, (1310, 280, 1695, 520), "Aplikasi & API", ["validasi; build release", "logging"])
    box(d, (410, 650, 825, 860), "Monitoring", ["audit log; alert; IoC"], accent=BLUE)
    box(d, (980, 650, 1395, 860), "Respons insiden", ["playbook; preservasi", "tabletop; pemulihan"], accent=BLUE)
    arrow(d, (890, 520), (890, 655)); arrow(d, (825, 755), (980, 755))
    files.append(save(im, "G-12_arsitektur_keamanan_target"))

    lines = ["# Indeks gambar UAS Libera", "", "Dibuat otomatis dengan `python scripts/generate_uas_figures.py`.",
             "Gambar berukuran 1800×1050 px, 200 DPI. Semua berkas PNG dapat disisipkan ke laporan.", "",
             "**Keterangan status:** G-03 adalah screenshot arsip asli dari ACQ-SIM-LIVE; G-07, G-08, G-11 adalah rencana, bukan hasil pengujian. G-10 dan G-12 adalah rancangan target. G-01/G-02 merekonstruksi alur dari berkas proyek. G-04/G-05/G-06/G-09 berasal dari artefak hasil aktual.", ""]
    for f in files:
        lines.append(f"- [{f.stem}]({f.name})")
    lines += ["", "G-03 tidak membuktikan kondisi emulator saat ACQ-SIM-001. Screenshot emulator asli baru dapat diambil saat emulator tersedia. Bukti perbaikan/uji ulang, analisis ancaman dinamis, dan tabletop belum boleh diklaim selesai dari gambar rencana ini."]
    (OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    archive = OUT.parent / "UAS_KSI_GAMBAR_LIBERA.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for item in [OUT / "README.md", *files]:
            z.write(item, arcname=item.name)
    print(f"Generated {len(files)} figures in {OUT}")
    print(f"Bundled figures in {archive}")


if __name__ == "__main__":
    main()
