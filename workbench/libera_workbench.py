"""Read-only ChatSim SQLite workbench and locked research results."""
from pathlib import Path
import sys
import html
import math

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import streamlit as st
from workbench.chatsim_data import available_snapshots, capture_snapshot, devices, find_adb, load_research, load_snapshot

st.set_page_config(page_title="LIBERA | ChatSim Workbench", layout="wide")
st.title("LIBERA · ChatSim Workbench")
st.caption("Data percakapan langsung dari SQLite ChatSim melalui ADB · Pemeriksaan read-only")
with st.sidebar:
    st.header("Koneksi ChatSim")
    adb = find_adb()
    try:
        connected = devices(adb)
    except Exception as exc:
        connected = []
        st.error(str(exc))
    ready = [d["serial"] for d in connected if d["state"] == "device"]
    serial = st.selectbox("Perangkat", ready) if ready else None
    if serial:
        st.success("Perangkat terhubung")
    else:
        st.info("Jalankan emulator ChatSim atau hubungkan perangkat dengan USB debugging.")
    st.caption("Akuisisi menghentikan ChatSim agar SQLite konsisten. Buka kembali ChatSim di emulator setelah akuisisi.")
    if st.button("Ambil data terbaru dari ChatSim", disabled=not serial, type="primary"):
        try:
            with st.spinner("Mengambil dan memverifikasi SQLite…"):
                folder = capture_snapshot(adb, serial)
            st.session_state["snapshot_selection"] = str(folder)
            st.session_state["capture_notice"] = "Snapshot baru berhasil diambil langsung dari ChatSim."
            st.rerun()
        except Exception as exc:
            st.error(str(exc))
    options = [str(p) for p in available_snapshots()]
    if not options:
        st.info("Belum ada snapshot. Ambil data dari ChatSim untuk mulai.")
        st.stop()
    if st.session_state.get("snapshot_selection") not in options:
        st.session_state["snapshot_selection"] = options[0]
    selection = st.selectbox("Snapshot SQLite", options, format_func=lambda p: Path(p).name, key="snapshot_selection")
    st.caption("Snapshot adalah salinan pada waktu akuisisi. Tekan tombol di atas untuk mengambil perubahan terbaru.")
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
    st.warning(f"Hasil eksperimen tidak ditampilkan: {exc}")
columns = ["evidence_id", "timestamp", "sender_name", "recipient_name", "message_text", "message_id"]
tabs = st.tabs(["Ringkasan", "Percakapan", "Pencarian", "Timeline", "Jejak bukti", "Hasil A/B/C", "Evaluasi & Laporan"])
with tabs[0]:
    for col, label, value in zip(st.columns(4), ["Pesan", "Percakapan", "Integritas SQLite", "Sumber data"], [len(messages), len(data["chats"]), "OK", "SQLite"]):
        col.metric(label, value)
    st.info("ChatSim adalah aplikasi pembawa bukti simulasi penelitian.")
    st.markdown("**Alur:** ChatSim → ADB → snapshot SQLite → percakapan, pencarian, dan jejak bukti.")
    st.write("Akuisisi:", data["manifest"]["acquisition_id"])
    st.write("Database:", data["database"])
    st.caption("SHA-256 master dan working terverifikasi identik")
    st.code(data["sha256"])
    if research:
        if research["matches_snapshot"]:
            st.success("Snapshot cocok dengan sumber eksperimen P8–P10. Tautan bukti dapat digunakan.")
        else:
            st.warning("Snapshot berbeda dari sumber eksperimen P8–P10. Hasil historis tetap ditampilkan, tetapi tautan bukti dinonaktifkan.")
    daily = messages["timestamp"].str[:10].value_counts().sort_index()
    st.bar_chart(daily.rename("Pesan per hari"))
with tabs[1]:
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
    day = st.selectbox("Tanggal", sorted(messages.timestamp.str[:10].unique()))
    st.dataframe(messages.loc[messages.timestamp.str.startswith(day), columns], hide_index=True)
with tabs[4]:
    evidence = st.text_input("Evidence ID atau message ID", "ART-000001").strip()
    match = messages[(messages.evidence_id == evidence) | (messages.message_id == evidence)]
    if match.empty:
        st.warning("ID tidak ditemukan dalam snapshot ini.")
    else:
        st.json(match.iloc[0].to_dict())
        st.caption(f"Akuisisi: {data['manifest']['acquisition_id']} · SHA-256: {data['sha256']}")
    st.caption("Evidence ID mengikuti urutan timestamp dan message_id; ID ini berlaku dalam snapshot yang dipilih.")
with tabs[5]:
    if not research:
        st.info("Hasil eksperimen terkunci belum tersedia.")
    else:
        tasks = {t["task_id"]: t for t in research["experiment"]}
        task_id = st.selectbox("Pertanyaan eksperimen", list(tasks))
        task = tasks[task_id]
        st.write(task["question"])
        st.caption("Hasil historis P8 terkunci; memilih snapshot tidak menjalankan ulang model.")
        for col, key, label in zip(st.columns(3), ["A_llm_only", "B_llm_rag", "C_llm_rag_structured"], ["A · LLM", "B · LLM + RAG", "C · RAG terstruktur"]):
            with col:
                st.subheader(label)
                output = task[key]["output"]
                if isinstance(output, (dict, list)):
                    st.json(output)
                else:
                    st.text(output)
        evaluation = research["evaluation"]
        if evaluation:
            st.warning("12 referensi tidak valid pada kondisi C dikarantina dan tidak dikreditkan sebagai bukti. Output asli tetap ditampilkan untuk audit.")
            records = evaluation["citation_validation"].get("records", [])
            records = [r for r in records if r.get("task_id") == task_id]
            if records:
                st.dataframe(pd.DataFrame(records), hide_index=True)
        if research["matches_snapshot"]:
            ids = task.get("retrieval_trace", {}).get("retrieved_evidence_ids", [])
            if ids:
                selected_id = st.selectbox("Telusuri bukti retrieval di SQLite", ids)
                st.dataframe(messages.loc[messages.evidence_id == selected_id, columns], hide_index=True)
        else:
            st.warning("Penelusuran bukti dinonaktifkan: hash snapshot berbeda dari sumber eksperimen.")
with tabs[6]:
    if not research or not research["evaluation"]:
        st.info("Evaluasi terkunci belum tersedia.")
    else:
        evaluation = research["evaluation"]
        gt = evaluation["ground_truth_evaluation"]
        st.warning("Ground truth rekonstruksi adalah proxy provenance, bukan ground truth semantik independen. Metrik ini belum membuktikan akurasi penemuan bukti kunci.")
        st.code(evaluation["status"])
        for col, label, value in zip(st.columns(3), ["Pesan berlabel proxy", "Pesan tanpa label", "Referensi C dikarantina"], [gt["labeled_rows"], gt["ground_truth_rows_unlabeled"], evaluation["integrity"]["conditions"]["C_llm_rag_structured"]["invalid_citation_count"]]):
            col.metric(label, value)
        metric_columns = ["TP", "FP", "FN", "TN", "precision", "recall", "f1", "predictions_outside_labeled_universe"]
        st.dataframe(pd.DataFrame(gt["metrics"]).T[metric_columns])
        st.caption("Referensi tidak valid tidak menjadi TP. Pesan tanpa label tidak dianggap negatif. Berkas label privat tidak dibaca oleh dashboard.")
        st.download_button("Unduh laporan P10", research["report"], file_name="LIBERA_P10_report.md", mime="text/markdown")
        with st.expander("Baca laporan lengkap"):
            st.markdown(research["report"])
