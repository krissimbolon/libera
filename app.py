import streamlit as st
import pandas as pd
import hashlib
import subprocess
import json
import ollama
import folium
from streamlit_folium import st_folium
import math
import platform
import datetime

def check_offline_status():
    """Memastikan sistem berada dalam keadaan offline untuk chain of custody."""
    try:
        # Ping 8.8.8.8 dengan timeout 2 detik
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "1", "-w", "2000", "8.8.8.8"]
        else:
            command = ["ping", "-c", "1", "-W", "2", "8.8.8.8"]
        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Jika return code 0, ping berhasil -> artinya sedang online!
        if result.returncode == 0:
            st.error("🚨 PELANGGARAN ISOLASI FORENSIK: Sistem terdeteksi online. Matikan koneksi internet untuk menjaga chain of custody barang bukti!")
            st.stop()
    except Exception as e:
        # Jika gagal menjalankan ping, asumsikan offline
        pass

def calculate_hash(file_bytes):
    """Menghitung SHA-256 dari bytes file."""
    return hashlib.sha256(file_bytes).hexdigest()

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="LIBERA - Triage Forensik", layout="wide")

st.title("LIBERA - Triage Forensik")
st.markdown("Alat investigasi log percakapan offline berbasis Local LLM (Ollama).")

# 1. Cek Offline Status
check_offline_status()

# 2. Sidebar & File Upload
st.sidebar.header("Manajemen Barang Bukti")
uploaded_file = st.sidebar.file_uploader("Unggah log chat CSV (dari folder libera_evidence)", type=["csv"])

if uploaded_file is not None:
    # Hashing File (Integrity Check)
    file_bytes = uploaded_file.getvalue()
    file_hash = calculate_hash(file_bytes)
    st.sidebar.success("File Terverifikasi.")
    st.sidebar.text_input("SHA-256 Hash", file_hash, disabled=True)
    
    # 3. Data Pre-processing
    df = pd.read_csv(uploaded_file, sep=";")
    
    # Sortir berdasarkan relative_time_seconds jika ada
    if "relative_time_seconds" in df.columns:
        df = df.sort_values(by="relative_time_seconds").reset_index(drop=True)
    
    total_rows = len(df)
    st.sidebar.info(f"Total Baris: {total_rows}")
    
    # Chunking / Sliding Window
    chunk_size = 500
    total_chunks = math.ceil(total_rows / chunk_size)
    
    if total_chunks > 0:
        chunk_options = []
        for i in range(total_chunks):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, total_rows)
            chunk_options.append(f"Baris {start+1} - {end}")
        
        selected_chunk_str = st.sidebar.selectbox("Pilih Rentang Baris (Chunk) untuk Dianalisis", chunk_options)
        chunk_idx = chunk_options.index(selected_chunk_str)
        
        start_idx = chunk_idx * chunk_size
        end_idx = min((chunk_idx + 1) * chunk_size, total_rows)
        
        df_chunk = df.iloc[start_idx:end_idx]
    else:
        df_chunk = df
    
    # Preview Data
    with st.expander("Preview Data Mentah (Rentang Pilihan)"):
        st.dataframe(df_chunk)
    
    # Tombol Eksekusi
    if st.sidebar.button("Eksekusi Analisis Golden Hour", type="primary"):
        
        # Gabungkan data menjadi satu string panjang
        chat_logs = []
        for _, row in df_chunk.iterrows():
            waktu = row.get("relative_time_seconds", "")
            pengirim = str(row.get("sender_hash", ""))[:8] # Potong hash agar tidak memakan token berlebih
            pesan = row.get("message_content", "")
            chat_logs.append(f"[Waktu: {waktu}] [Pengirim: {pengirim}] - Pesan: {pesan}")
            
        chat_text = "\n".join(chat_logs)
        
        # 4. Two-Stage Prompting via Ollama
        st.markdown("### Analisis Forensik")
        
        # Tahap 1: Ekstraksi JSON
        with st.spinner("Tahap 1: Mengekstraksi Entitas & Indikator (Ollama gemma:2b)..."):
            prompt_tahap1 = f"""Anda adalah asisten forensik digital.
Tugas Anda adalah mengekstrak entitas dari log chat berikut ini.
Cari indikasi kejahatan perdagangan manusia (human trafficking).
Cari entitas ini:
1. "sandi_mencurigakan": array of string (kata-kata sandi atau perumpamaan yang mungkin merujuk pada korban, uang, atau dokumen rahasia).
2. "modus_operandi": string (misal: penahanan dokumen, hutang, janji palsu, perekrutan, atau "TIDAK ADA" jika chat terlihat normal).
3. "koordinat": object berisi "latitude" (float) dan "longitude" (float) jika ada penyebutan lokasi koordinat geografis. Jika tidak ada koordinat, isi null.

Balas HANYA dengan format JSON yang valid tanpa ada awalan atau akhiran teks lain.

Log Chat:
{chat_text}
"""
            try:
                # Memanggil ollama lokal
                response1 = ollama.chat(model='gemma:2b', messages=[
                    {'role': 'user', 'content': prompt_tahap1}
                ], format='json')
                
                json_result = response1['message']['content']
                
                # Coba parse JSON
                try:
                    extracted_data = json.loads(json_result)
                except:
                    # Terkadang model masih bandel memberikan markdown block ````json ... ````
                    cleaned = json_result.replace("```json", "").replace("```", "").strip()
                    extracted_data = json.loads(cleaned)
                    
            except Exception as e:
                st.error(f"Gagal memanggil Ollama (Tahap 1): {e}")
                st.stop()
                
        st.success("Tahap 1 Selesai!")
        with st.expander("Lihat Hasil Ekstraksi (JSON)"):
            st.json(extracted_data)
            
        # Tahap 2: Sintesis Laporan
        with st.spinner("Tahap 2: Menyusun Laporan Intelijen (Ollama gemma:2b)..."):
            prompt_tahap2 = f"""Berdasarkan temuan JSON berikut ini, buatkan satu paragraf Laporan Intelijen Investigasi singkat, formal, dan profesional dalam bahasa Indonesia.

Data JSON:
{json.dumps(extracted_data, indent=2)}

Laporan harus fokus menjelaskan apakah terdapat aktivitas mencurigakan, apa modus operandinya, dan temuan kunci lainnya. Jika tidak ada temuan, nyatakan bahwa log bersih. Jangan mengulang format JSON.
"""
            try:
                response2 = ollama.chat(model='gemma:2b', messages=[
                    {'role': 'user', 'content': prompt_tahap2}
                ])
                laporan = response2['message']['content']
            except Exception as e:
                st.error(f"Gagal memanggil Ollama (Tahap 2): {e}")
                st.stop()
                
        st.success("Tahap 2 Selesai!")
        st.info(laporan)
        
        # Tombol Unduh Laporan
        report_content = f"""# LAPORAN INTELIJEN INVESTIGASI FORENSIK
Waktu Analisis : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Hash Barang Bukti (SHA-256): {file_hash}

## Hasil Analisis (Ollama gemma:2b)
{laporan}
"""
        st.download_button(
            label="Unduh Laporan Investigasi (TXT)",
            data=report_content,
            file_name=f"Laporan_Investigasi_{file_hash[:8]}.txt",
            mime="text/plain"
        )
        
        # 5. Visualisasi Spasial (Folium)
        koordinat = extracted_data.get("koordinat")
        if koordinat and isinstance(koordinat, dict):
            lat = koordinat.get("latitude")
            lon = koordinat.get("longitude")
            
            if lat is not None and lon is not None:
                st.markdown("### Visualisasi Spasial")
                st.write("Titik Rencana Eksekusi Sindikat:")
                
                # Render Peta Folium
                m = folium.Map(location=[lat, lon], zoom_start=10)
                folium.Marker(
                    [lat, lon], 
                    popup="Titik Terdeteksi", 
                    tooltip="Lokasi Sindikat",
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)
                
                st_folium(m, width=800, height=450)
else:
    st.info("Silakan unggah file CSV di sidebar untuk memulai.")
