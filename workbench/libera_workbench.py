from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="LIBERA Forensic Workbench", layout="wide")

st.title("LIBERA Forensic Workbench")
st.caption("DEV-001 • WhatsApp-like synthetic evidence • examiner view")

with st.expander("Investigative brief", expanded=False):
    st.markdown(
        """
**Case LIBERA-001 — suspected human-trafficking investigation**

Examine DEV-001 for messaging artifacts relevant to recruitment, movement,
lodging, appointment coordination, money/pricing, coercion/control, attempts
to leave or seek help, and coordination among actors.

This examiner view intentionally does **not** expose construction provenance or
evaluator ground truth. Findings must be traceable to acquired artifacts.
"""
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_artifacts(folder: Path):
    messages_path = folder / "ART-00001_messages.csv"
    chats_path = folder / "ART-00002_chats.csv"
    art_manifest_path = folder / "artifact_manifest.json"
    if not messages_path.exists() or not chats_path.exists() or not art_manifest_path.exists():
        raise FileNotFoundError(
            "Artifact folder harus berisi ART-00001_messages.csv, "
            "ART-00002_chats.csv, dan artifact_manifest.json"
        )

    messages = pd.read_csv(messages_path, dtype=str).fillna("")
    chats = pd.read_csv(chats_path, dtype=str).fillna("")
    art_manifest = json.loads(art_manifest_path.read_text(encoding="utf-8-sig"))

    acq_manifest = None
    acq_manifest_path = folder.parent / "acquisition_manifest.json"
    if acq_manifest_path.exists():
        acq_manifest = json.loads(acq_manifest_path.read_text(encoding="utf-8-sig"))

    return messages, chats, art_manifest, acq_manifest


default_dir = os.environ.get("LIBERA_ARTIFACT_DIR", "")
artifact_dir_text = st.sidebar.text_input(
    "Artifact directory",
    value=default_dir,
    placeholder=r"demo_evidence\ACQ-001_...\artifacts",
)
st.sidebar.caption("Workbench hanya membaca hasil extraction ART, bukan P2 design corpus.")

if not artifact_dir_text:
    st.info("Masukkan folder artifact hasil tools/extract_acquired_chatsim.py di sidebar.")
    st.stop()

artifact_dir = Path(artifact_dir_text).expanduser()

try:
    messages, chats, art_manifest, acq_manifest = load_artifacts(artifact_dir)
except Exception as exc:
    st.error(str(exc))
    st.stop()

messages["timestamp_dt"] = pd.to_datetime(messages["timestamp"], errors="coerce")
messages = messages.sort_values(["timestamp_dt", "message_id"]).reset_index(drop=True)

source_sha = art_manifest.get("source_database_sha256", "")
expected_count = len(messages)
chat_count = len(chats)
first_ts = messages["timestamp"].min() if expected_count else ""
last_ts = messages["timestamp"].max() if expected_count else ""

st.sidebar.success("Evidence loaded")
st.sidebar.metric("Messages", f"{expected_count:,}")
st.sidebar.metric("Chats", f"{chat_count:,}")
st.sidebar.text_input("Working DB SHA-256", source_sha, disabled=True)

if acq_manifest:
    master_hash = acq_manifest.get("master_sha256", "")
    working_hash = acq_manifest.get("working_sha256", "")
    if master_hash and master_hash == working_hash == source_sha:
        st.sidebar.success("Integrity chain verified: MASTER = WORKING = ART source")
    elif master_hash and master_hash == working_hash:
        st.sidebar.warning("MASTER = WORKING, tetapi ART source hash perlu diperiksa.")
    else:
        st.sidebar.warning("Acquisition integrity manifest tidak lengkap/cocok.")

overview, chat_tab, search_tab, timeline_tab, trace_tab = st.tabs(
    ["Overview", "Chats", "Search", "Timeline", "Evidence Trace"]
)

with overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Acquired messages", f"{expected_count:,}")
    c2.metric("Chat pairs", f"{chat_count:,}")
    c3.metric("First timestamp", first_ts[0:16] if first_ts else "-")
    c4.metric("Last timestamp", last_ts[0:16] if last_ts else "-")

    st.subheader("Evidence integrity")
    st.code(
        "\n".join(
            [
                f"ART source DB SHA-256 : {source_sha}",
                f"SQLite integrity      : {art_manifest.get('sqlite_integrity_check', '-')}",
                f"Foreign-key errors    : {art_manifest.get('foreign_key_error_count', '-')}",
                f"Acquisition ID        : {(acq_manifest or {}).get('acquisition_id', 'ACQ-001')}",
                f"Device ID             : {(acq_manifest or {}).get('device_id', 'DEV-001')}",
                f"Acquisition type      : {(acq_manifest or {}).get('acquisition_type', '-')}",
            ]
        )
    )

    st.subheader("Communication volume")
    volume = (
        messages.assign(day=messages["timestamp"].str.slice(0, 10))
        .groupby("day", as_index=False)
        .size()
        .rename(columns={"size": "messages"})
    )
    st.bar_chart(volume.set_index("day"))

with chat_tab:
    chat_options = chats.sort_values("peer_name")["peer_name"].tolist()
    selected_peer = st.selectbox("Open chat", chat_options)

    selected_chat_row = chats.loc[chats["peer_name"] == selected_peer].iloc[0]
    selected_chat_id = selected_chat_row["chat_id"]
    thread = messages.loc[messages["chat_id"] == selected_chat_id].copy()

    st.caption(
        f"{selected_chat_id} • {len(thread):,} messages • "
        f"{thread['timestamp'].min()[0:10]} to {thread['timestamp'].max()[0:10]}"
    )

    limit = st.slider("Messages shown", 20, min(500, max(20, len(thread))), min(100, max(20, len(thread))))
    thread_show = thread.tail(limit)

    for _, row in thread_show.iterrows():
        mine = row["sender_id"] == "AKT-RAKA"
        align = "flex-end" if mine else "flex-start"
        bg = "#DCF8C6" if mine else "#FFFFFF"
        sender = "Raka" if mine else row["sender_name"]
        st.markdown(
            f"""
<div style="display:flex;justify-content:{align};margin:4px 0;">
  <div style="max-width:72%;background:{bg};padding:8px 10px;border-radius:10px;
              box-shadow:0 1px 2px rgba(0,0,0,.12);">
    <div style="font-size:11px;color:#64748b;">{sender}</div>
    <div style="font-size:15px;color:#111827;">{row['message_text']}</div>
    <div style="font-size:10px;color:#6b7280;text-align:right;">
      {row['timestamp'][0:16]} • {row['message_id']}
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

with search_tab:
    st.subheader("Examiner search")
    query = st.text_input("Keyword / phrase")
    actor_choices = ["ALL"] + sorted(
        set(messages["sender_name"].tolist() + messages["recipient_name"].tolist())
    )
    actor = st.selectbox("Actor filter", actor_choices)

    result = messages
    if query.strip():
        result = result.loc[
            result["message_text"].str.contains(query.strip(), case=False, regex=False, na=False)
        ]
    if actor != "ALL":
        result = result.loc[
            (result["sender_name"] == actor) | (result["recipient_name"] == actor)
        ]

    st.write(f"{len(result):,} matching messages")
    st.dataframe(
        result[
            [
                "message_id",
                "timestamp",
                "sender_name",
                "recipient_name",
                "message_text",
                "chat_id",
                "segment_id",
            ]
        ].head(1000),
        use_container_width=True,
        hide_index=True,
    )

with timeline_tab:
    st.subheader("Global Raka-centric timeline")
    day = st.selectbox(
        "Date",
        sorted(messages["timestamp"].str.slice(0, 10).unique().tolist()),
    )
    day_rows = messages.loc[messages["timestamp"].str.startswith(day)]
    st.caption(f"{len(day_rows):,} messages on {day}")
    st.dataframe(
        day_rows[
            [
                "timestamp",
                "sender_name",
                "recipient_name",
                "message_text",
                "chat_id",
                "segment_id",
                "message_id",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with trace_tab:
    st.subheader("FND → ART → ACQ → DEV trace")
    message_id = st.selectbox("Message locator", messages["message_id"].tolist())
    row = messages.loc[messages["message_id"] == message_id].iloc[0]

    st.markdown("#### Selected digital artifact")
    st.json(
        {
            "message_id": row["message_id"],
            "timestamp": row["timestamp"],
            "sender": row["sender_name"],
            "recipient": row["recipient_name"],
            "text": row["message_text"],
            "chat_id": row["chat_id"],
            "segment_id": row["segment_id"],
        }
    )

    acquisition_id = (acq_manifest or {}).get("acquisition_id", "ACQ-001")
    device_id = (acq_manifest or {}).get("device_id", "DEV-001")

    st.code(
        f"MSG {message_id}\n"
        f"  ↓\n"
        f"ART-00001 messages\n"
        f"  ↓\n"
        f"{acquisition_id}  SHA-256 {source_sha[:16]}...\n"
        f"  ↓\n"
        f"{device_id}  LIBERA ChatSim"
    )

    st.caption(
        "Finding IDs (FND-*) are assigned only after investigator review. "
        "The workbench does not expose evaluator ground truth."
    )
