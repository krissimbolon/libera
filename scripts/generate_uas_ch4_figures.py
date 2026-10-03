"""Evidence-based Chapter IV figures from the controlled sandbox experiment."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import ImageDraw

from generate_uas_figures import (ROOT, W, NAVY, TEAL, RED, BLUE, AMBER, MUTED,
                                  F_BODY, F_SMALL, F_SUB, canvas, box, font)

OUT = ROOT / "docs/06_report/bab4_figures"
DATA = ROOT / "docs/06_report/bab4_evidence/experiment.json"


def save(image, name):
    p = OUT / f"{name}.png"
    image.save(p, optimize=True, dpi=(200, 200))
    return p


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    x = json.loads(DATA.read_text(encoding="utf-8"))
    im, d = canvas("IV-01", "Hasil uji sebelum dan sesudah", "Ekstraktor lama dibandingkan dengan pemeriksaan hash dan manifest", "bab4_evidence/experiment.json", "HASIL UJI SANDBOX")
    headers = [("Skenario", 105), ("Sebelum", 800), ("Sesudah", 1250)]
    for title, px in headers: d.text((px, 285), title, font=font(31, True), fill=NAVY)
    rows = [("Salinan asli + manifest", "DITERIMA", "DITERIMA"),
            ("SQLite diubah; struktur tetap OK", "DITERIMA", "DITOLAK: hash"),
            ("Manifest akuisisi hilang", "DITERIMA: UNKNOWN", "DITOLAK: manifest")]
    for i, (name, before, after) in enumerate(rows):
        y = 350 + i * 175
        d.rounded_rectangle((85, y, 1715, y+135), radius=16, fill="white", outline="#d6dfe8", width=2)
        d.text((105, y+36), name, font=F_SUB, fill=NAVY)
        d.text((800, y+37), before, font=F_SUB, fill=RED if i else TEAL)
        d.text((1250, y+37), after, font=F_SUB, fill=TEAL)
    d.text((105, 889), "Seluruh mutasi dilakukan pada salinan sementara; master dan working asli tidak diubah.", font=F_SMALL, fill=MUTED)
    save(im, "IV-01_uji_sebelum_sesudah")

    im, d = canvas("IV-02", "Jejak ancaman manipulasi SQLite", "Satu pesan diubah dalam sandbox; hasil statis dan perilaku ekstraktor", "bab4_evidence/experiment.json", "HASIL UJI SANDBOX")
    t = x["tamper"]
    box(d, (90, 280, 850, 498), "Sampel: salinan working SQLite", [f"Pesan: {t['message_id']}", "Penanda: UAS_CONTROLLED_TAMPER_SAMPLE"], accent=AMBER, body_size=24)
    box(d, (950, 280, 1710, 498), "Analisis statis", ["SHA-256 berubah setelah UPDATE", "SQLite integrity_check tetap: ok"], accent=BLUE)
    box(d, (90, 555, 850, 790), "Sebelum perbaikan", ["Ekstraktor lama: exit 0", "9.997 pesan tetap diekspor", "Mutasi lolos pemeriksaan struktur"], accent=RED)
    box(d, (950, 555, 1710, 790), "Uji ulang", ["Ekstraktor baru: exit 1", "SHA-256 tidak cocok; ekspor ditolak", "Kondisi bersih tetap exit 0"], accent=TEAL)
    d.text((105, 854), f"IoC SHA-256 salinan yang diubah: {t['after_db_sha256']}", font=F_SMALL, fill=NAVY)
    save(im, "IV-02_jejak_ancaman_sqlite")

    im, d = canvas("IV-03", "Karantina referensi AI", "Kesalahan keluaran C tetap tercatat setelah validasi sitasi P9", "P8 output lock; P9 citation validation", "HASIL OBSERVASI")
    c = x["citation"]
    items = [("24", "referensi diajukan"), ("12", "diterima"), ("12", "dikarantina"), ("0", "referensi rusak diberi kredit")]
    for i, (num, label) in enumerate(items):
        xx = 90 + i*420
        d.rounded_rectangle((xx, 315, xx+370, 615), radius=20, fill="white", outline="#d6dfe8", width=2)
        d.text((xx+28, 365), num, font=font(78, True), fill=RED if i==2 else TEAL)
        d.text((xx+28, 505), label, font=F_SMALL, fill=NAVY)
    box(d, (95, 700, 1705, 865), "Batas efektivitas", ["Karantina mencegah sitasi rusak dipakai sebagai bukti; keluaran model asli tetap salah.",
                                             "Validitas identifier bukan ketepatan semantik temuan."], accent=AMBER, body_size=24)
    save(im, "IV-03_karantina_sitasi")
    print(f"Generated 3 Chapter IV images in {OUT}")


if __name__ == "__main__":
    main()
