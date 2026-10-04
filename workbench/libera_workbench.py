"""Offline-first forensic examination workbench for LIBERA ChatSim."""
from pathlib import Path
import sys
import html
import math

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import streamlit as st
from workbench.chatsim_data import available_snapshots, capture_snapshot, devices, find_adb, load_research, load_snapshot

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="LIBERA | Forensic Workbench", layout="wide")
st.title("LIBERA · Forensic Workbench")
st.caption("Pemeriksaan evidence percakapan secara lokal · ChatSim → akuisisi → integritas → artifact → examiner → AI assistance → validasi")

with st.sidebar:
    st.header("Sumber evidence")
    adb = find_adb()
    try:
        connected = devices(adb)
    except Exception as exc:
        connected = []
        st.error(str(exc))
    ready = [d["serial"] for d in connected if d["state"] == "device"]
    serial = st.selectbox("Perangkat ChatSim", ready) if ready else None
    if serial:
        st.success("DEV-SIM-001 terhubung")
    else:
        st.info("Jalankan emulator ChatSim atau hubungkan perangkat yang disiapkan untuk simulasi.")
    st.caption("Akuisisi menghentikan ChatSim sementara agar SQLite konsisten. Workbench menganalisis salinan lokal, bukan database yang sedang aktif.")
    if st.button("Akuisisi snapshot baru", disabled=not serial, type="primary"):
        try:
            with st.spinner("Mengambil SQLite, membuat master/working copy, dan memverifikasi hash…"):
                folder = capture_snapshot(adb, serial)
            st.session_state["snapshot_selection"] = str(folder)
            st.session_state["capture_notice"] = "Akuisisi baru selesai dan hash master/working terverifikasi."
            st.rerun()
        except Exception as exc:
            st.error(str(exc))
    options = [str(p) for p in available_snapshots()]
    if not options:
        st.info("Belum ada snapshot evidence. Lakukan akuisisi untuk mulai.")
        st.stop()
    if st.session_state.get("snapshot_selection") not in options:
        st.session_state["snapshot_selection"] = options[0]
    selection = st.selectbox("Acquisition snapshot", options, format_func=lambda p: Path(p).name, key="snapshot_selection")
    st.caption("Setiap snapshot adalah acquisition terpisah. Master sebelumnya tidak ditimpa.")

try:
    data = load_snapshot(selection)
except Exception as exc:
    st.error(f"Snapshot ditolak: {exc}")
    st.stop()

if notice := st.session_state.pop("capture_notice", None):
    st.success(notice)

messages = pd.DataFrame(data["messages"])
if messages.empty:
    st.info("ChatSim belum memiliki pesan.")
    st.stop()

try:
    research = load_research(data["sha256"])
except Exception as exc:
    research = None
    st.warning(f"Hasil eksperimen terkunci tidak ditampilkan: {exc}")

columns = ["evidence_id", "timestamp", "sender_name", "recipient_name", "message_text", "message_id"]
tabs = st.tabs([
    "Kasus & Integritas",
    "Percakapan",
    "Pencarian",
    "Timeline",
    "Jejak Bukti",
    "Pemeriksaan Tradisional",
    "Asisten AI",
    "Validasi & Laporan",
])

with tabs[0]:
    st.subheader("Case workspace")
    for col, label, value in zip(
        st.columns(4),
        ["Evidence artifacts", "Percakapan", "Integritas SQLite", "Mode"],
        [len(messages), len(data["chats"]), "VERIFIED", "LOCAL / OFFLINE-FIRST"],
    ):
        col.metric(label, value)
    st.info(
        "ChatSim adalah controlled Android evidence carrier untuk simulasi penelitian. "
        "Ia bukan WhatsApp dan bukan perangkat sitaan nyata."
    )
    st.markdown(
        "**Alur pemeriksaan:** perangkat → acquisition snapshot → SHA-256 → working copy "
        "→ evidence examination → examiner findings → optional local-AI assistance → validation → report."
    )
    st.write("Device:", data["manifest"].get("device_id", "DEV-SIM-001"))
    st.write("Acquisition:", data["manifest"]["acquisition_id"])
    st.write("Metode:", data["manifest"].get("method", "logical app-private acquisition"))
    st.write("Database kerja:", data["database"])
    st.caption("SHA-256 master dan working copy terverifikasi identik. Analisis dashboard dilakukan read-only pada working copy.")
    st.code(data["sha256"])
    if research:
        if research["matches_snapshot"]:
            st.success("Snapshot ini identik dengan sumber eksperimen P8. Evidence link historis dapat ditelusuri.")
        else:
            st.warning("Snapshot berbeda dari sumber P8. Hasil historis tetap dapat dibaca, tetapi evidence link dinonaktifkan.")
    daily = messages["timestamp"].str[:10].value_counts().sort_index()
    st.bar_chart(daily.rename("Pesan per hari"))

with tabs[1]:
    st.subheader("Percakapan pada working copy")
    chat_names = {c["chat_id"]: c["peer_name"] for c in data["chats"]}
    chat = st.selectbox("Pilih percakapan", list(chat_names), format_func=lambda c: f"{chat_names[c]} · {c}")
    subset = messages[messages.chat_id == chat]
    limit = st.selectbox("Pesan per halaman", [25, 50, 100])
    page = st.number_input("Halaman", min_value=1, max_value=max(1, math.ceil(len(subset) / limit)), value=1, key=f"page_{chat}_{limit}")
    st.caption(f"{len(subset)} pesan · urutan waktu terlama ke terbaru")
    for row in subset.iloc[(page - 1) * limit:page * limit].to_dict("records"):
        with st.container(border=True):
            st.markdown(f"**{html.escape(row['sender_name'])}** → {html.escape(row['recipient_name'])}")
            st.text(row["message_text"])
            st.caption(f"{row['timestamp']} · {row['evidence_id']} · {row['message_id']}")

with tabs[2]:
    st.subheader("Pencarian evidence")
    query = st.text_input("Kata atau frasa")
    actor = st.selectbox("Pengirim", ["Semua"] + sorted(messages.sender_name.dropna().unique().tolist()))
    found = messages
    if query:
        found = found[found.message_text.str.contains(query, case=False, regex=False, na=False)]
    if actor != "Semua":
        found = found[found.sender_name == actor]
    st.caption(f"{len(found)} hasil · menampilkan maksimal 1.000 baris")
    st.dataframe(found[columns].head(1000), hide_index=True)

with tabs[3]:
    st.subheader("Timeline")
    day = st.selectbox("Tanggal", sorted(messages.timestamp.str[:10].unique()))
    day_rows = messages.loc[messages.timestamp.str.startswith(day), columns]
    st.caption(f"{len(day_rows)} artifact pada {day}")
    st.dataframe(day_rows, hide_index=True)

with tabs[4]:
    st.subheader("Trace satu artifact ke acquisition")
    evidence = st.text_input("Evidence ID atau message ID", "ART-000001").strip()
    match = messages[(messages.evidence_id == evidence) | (messages.message_id == evidence)]
    if match.empty:
        st.warning("ID tidak ditemukan dalam snapshot ini.")
    else:
        st.json(match.iloc[0].to_dict())
        st.caption(f"Akuisisi: {data['manifest']['acquisition_id']} · SHA-256: {data['sha256']}")
    st.caption("Evidence ID mengikuti urutan timestamp dan message_id; ID berlaku dalam snapshot acquisition yang dipilih.")

with tabs[5]:
    st.subheader("Pemeriksaan tradisional sebelum AI")
    st.caption(
        "Bagian ini memprioritaskan fakta yang dapat dihitung langsung dari evidence: pencarian literal, "
        "timeline, aktor, pasangan komunikasi, lalu human QC terhadap candidate evidence. AI tidak diperlukan."
    )
    pair_frame = messages[["sender_name", "recipient_name"]].copy()
    pair_frame["pair"] = pair_frame.apply(
        lambda r: " ↔ ".join(sorted([str(r["sender_name"]), str(r["recipient_name"])])),
        axis=1,
    )
    pair_counts = pair_frame["pair"].value_counts().head(15).rename_axis("Pasangan aktor").reset_index(name="Jumlah pesan")
    actor_counts = pd.concat([messages["sender_name"], messages["recipient_name"]]).value_counts().head(15).rename_axis("Aktor").reset_index(name="Keterlibatan pesan")
    left, right = st.columns(2)
    with left:
        st.markdown("**Pasangan komunikasi paling aktif**")
        st.dataframe(pair_counts, hide_index=True, use_container_width=True)
    with right:
        st.markdown("**Aktor paling sering muncul**")
        st.dataframe(actor_counts, hide_index=True, use_container_width=True)

    p5_path = ROOT / "runtime/working/P5/p5_examiner_packet.csv"
    if p5_path.is_file():
        packet = pd.read_csv(p5_path)
        decisions = packet.get("examiner_decision", pd.Series(dtype=str)).fillna("").astype(str)
        counts = {d: int((decisions == d).sum()) for d in ["SUPPORTED", "NOT_SUPPORTED", "UNCERTAIN"]}
        st.markdown("**Human examiner QC (P5)**")
        for col, label, value in zip(
            st.columns(3),
            ["SUPPORTED", "NOT SUPPORTED", "UNCERTAIN"],
            [counts["SUPPORTED"], counts["NOT_SUPPORTED"], counts["UNCERTAIN"]],
        ):
            col.metric(label, value)
        keep = [c for c in ["review_order", "evidence_id", "primary_task_id", "sender", "receiver", "text", "examiner_decision", "examiner_note"] if c in packet.columns]
        st.dataframe(packet[keep], hide_index=True, use_container_width=True)
        st.caption("P5 examiner packet adalah time-boxed QC/triage terhadap candidate evidence, bukan semantic ground truth.")
    else:
        st.info("P5 examiner packet tidak ditemukan pada workstation ini. Pemeriksaan deskriptif di atas tetap berasal langsung dari acquired SQLite.")

with tabs[6]:
    st.subheader("AI sebagai copilot setelah evidence tersedia")
    st.caption(
        "A/B/C adalah eksperimen metode, bukan tiga tahapan forensik. "
        "A adalah kontrol tanpa case evidence; B dan C memakai retrieval evidence yang sama."
    )
    if not research:
        st.info("Hasil eksperimen terkunci belum tersedia.")
    else:
        tasks = {t["task_id"]: t for t in research["experiment"]}
        task_id = st.selectbox("Investigation question", list(tasks))
        task = tasks[task_id]
        st.write(task["question"])
        st.caption("Hasil P8 bersifat historis dan terkunci; membuka halaman ini tidak menjalankan ulang model.")

        configs = [
            ("A_llm_only", "A · TANPA CASE EVIDENCE", "Kontrol negatif: model hanya menerima pertanyaan. Bukan mode pemeriksaan yang direkomendasikan."),
            ("B_llm_rag", "B · + RETRIEVED EVIDENCE", "Model menerima top-k artifact hasil retrieval lokal."),
            ("C_llm_rag_structured", "C · + STRUCTURED OUTPUT", "Evidence retrieval sama dengan B, tetapi jawaban dipaksa ke schema yang lebih mudah diaudit."),
        ]
        for col, (key, label, note) in zip(st.columns(3), configs):
            with col:
                st.subheader(label)
                st.caption(note)
                output = task[key]["output"]
                if isinstance(output, (dict, list)):
                    st.json(output)
                else:
                    st.text(output)

        evaluation = research["evaluation"]
        if evaluation:
            st.warning(
                "Structured output tidak otomatis berarti evidence valid. "
                "Pada final run, 12 reference string kondisi C dikarantina; output asli tidak diperbaiki."
            )
            records = evaluation.get("citation_validation", {}).get("records", [])
            records = [r for r in records if r.get("task_id") == task_id]
            if records:
                st.dataframe(pd.DataFrame(records), hide_index=True)

        if research["matches_snapshot"]:
            ids = task.get("retrieval_trace", {}).get("retrieved_evidence_ids", [])
            if ids:
                selected_id = st.selectbox("Telusuri retrieved artifact ke SQLite", ids)
                st.dataframe(messages.loc[messages.evidence_id == selected_id, columns], hide_index=True)
        else:
            st.warning("Penelusuran artifact dinonaktifkan karena hash snapshot berbeda dari sumber eksperimen.")

with tabs[7]:
    st.subheader("Validasi & laporan")
    if not research or not research["evaluation"]:
        st.info("Evaluasi terkunci belum tersedia.")
    else:
        evaluation = research["evaluation"]
        conditions = evaluation.get("integrity", {}).get("conditions", {})
        b_invalid = conditions.get("B_llm_rag", {}).get("invalid_citation_count", 0)
        c_invalid = conditions.get("C_llm_rag_structured", {}).get("invalid_citation_count", 0)

        st.markdown("**Yang divalidasi terlebih dahulu adalah hubungan output AI dengan artifact yang benar-benar ada.**")
        for col, label, value in zip(
            st.columns(3),
            ["P8 lock", "Invalid citation B", "Invalid citation C"],
            ["VERIFIED", b_invalid, c_invalid],
        ):
            col.metric(label, value)
        st.warning(
            "Temuan utama: output C dapat valid secara schema tetapi tetap mengandung evidence reference yang tidak valid. "
            "Reference yang gagal validasi dikarantina dan tidak diperlakukan sebagai bukti."
        )

        gt = evaluation.get("ground_truth_evaluation")
        if gt:
            with st.expander("Eksperimen provenance proxy — bukan semantic ground truth"):
                st.warning(
                    "Referensi rekonstruksi hanya membedakan provenance anchor/distractor pada subset berlabel. "
                    "Ia tidak membuktikan semantic accuracy untuk key forensic evidence."
                )
                st.code(evaluation.get("status", ""))
                for col, label, value in zip(
                    st.columns(2),
                    ["Pesan berlabel proxy", "Pesan tanpa label"],
                    [gt.get("labeled_rows", 0), gt.get("ground_truth_rows_unlabeled", 0)],
                ):
                    col.metric(label, value)
                metric_columns = ["TP", "FP", "FN", "TN", "precision", "recall", "f1", "predictions_outside_labeled_universe"]
                metrics = pd.DataFrame(gt.get("metrics", {})).T
                available = [c for c in metric_columns if c in metrics.columns]
                if available:
                    st.dataframe(metrics[available])
                st.caption("Independent human semantic ground truth belum tersedia; karena itu dashboard tidak menyebut proxy metrics sebagai final semantic accuracy.")

        st.download_button("Unduh laporan P10", research["report"], file_name="LIBERA_P10_report.md", mime="text/markdown")
        with st.expander("Baca laporan lengkap"):
            st.markdown(research["report"])
