# Streamlit terintegrasi langsung dengan ChatSim

Status: demo lokal selesai dan diverifikasi pada 25 September 2026.

## Menjalankan

Jalankan emulator yang telah terpasang ChatSim dan buka aplikasinya. Dari root repo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_workbench.ps1
```

Buka <http://127.0.0.1:8501>, pilih perangkat, lalu klik **Ambil data terbaru dari ChatSim**.
Port lain dapat dipilih dengan `-Port 8502`.

Setup pertama pada komputer lain:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-demo.txt
```

ADB dicari dari `LIBERA_ADB`, PATH, `ANDROID_HOME`, `ANDROID_SDK_ROOT`, atau Android SDK
standar di LOCALAPPDATA. Perangkat harus berstatus `device`; gunakan debug APK ChatSim
penelitian yang mendukung `run-as`. Jika perlu atur lokasi manual:

```powershell
$env:LIBERA_ADB = 'C:\lokasi\platform-tools\adb.exe'
```

`streamlit run app.py` juga mengarah ke dashboard yang sama. Untuk membuka hasil yang
sudah selesai, gunakan `run_workbench.ps1`. `run_libera_demo.ps1` menjalankan pipeline
eksperimen penuh; jangan menjalankannya ulang untuk sekadar membuka UI setelah GT dibuka.

## Alur data

```text
ChatSim Android (id.libera.chatsim)
  → ADB force-stop + run-as cat databases/libera_messages.db
  → verifikasi hash perangkat dan salinan lokal
  → runtime/chatsim_snapshots/ACQ-SIM-LIVE_.../{master,working}/libera_messages.db
  → query SQLite read-only
  → Streamlit
```

Dashboard tidak membaca atau mengunggah CSV sebagai sumber percakapan. Corpus CSV P2
tetap merupakan bahan pembuatan simulasi dan CSV P4 tetap input historis eksperimen;
integrasi ini tidak mengubah asal-usul penelitian. Dashboard hanya menghitung hash
input historis untuk memeriksa lock, tanpa memuat isi pesan CSV.

Setiap akuisisi membuat folder baru. Master sebelumnya tidak ditimpa. ChatSim dihentikan
agar SQLite konsisten; buka kembali aplikasinya di emulator setelah akuisisi. WAL tidak
kosong ditolak. SQLite diperiksa melalui `integrity_check` dan `foreign_key_check`,
serta hash master, working, dan manifest harus cocok.

Ini adalah **snapshot yang diperbarui lewat tombol**, bukan streaming otomatis.
Perubahan di ChatSim muncul setelah akuisisi berikutnya. Saat emulator offline,
snapshot SQLite lokal yang sudah tersedia tetap dapat diperiksa.

## Tab dashboard

| Tab | Fungsi |
| --- | --- |
| Ringkasan | Jumlah pesan/chat, akuisisi, hash, aktivitas harian |
| Percakapan | Chat kronologis dengan pagination |
| Pencarian | Frasa literal dan filter pengirim |
| Timeline | Pesan per tanggal |
| Jejak bukti | Lookup evidence ID/message ID beserta identitas snapshot |
| Hasil A/B/C | Output asli T01–T10, validasi referensi, bukti retrieval |
| Evaluasi & Laporan | Metrik proxy, karantina, unduh laporan P10 |

`ART-xxxxxx` mengikuti urutan `timestamp,message_id`, sama dengan extractor P4. ID berlaku
dalam satu snapshot. Jika hash SQLite berbeda dari sumber P8, tautan hasil historis ke
pesan snapshot baru dinonaktifkan.

## Integritas dan batas interpretasi

Hasil historis berasal dari `runtime/working/P8_final_v6_20260925` dan
`runtime/working/P9_reconstructed_20260925`. Dashboard memverifikasi seluruh lock P8
serta hash evaluasi/laporan terhadap completion manifest. Folder runtime bersifat lokal
dan diabaikan Git. Checkout baru dapat mengakuisisi ChatSim, tetapi hasil historis
memerlukan artefak run yang sah di lokasi tersebut. Dashboard tidak menjalankan Ollama.

12 referensi C tidak valid tetap tampil pada output asli untuk audit, tetapi dikarantina
dan tidak dikreditkan sebagai bukti benar. Kesalahan model tetap dilaporkan; validitas
referensi C adalah 12/24 (50%). Karantina tidak membuat performa model menjadi sempurna.

Ground truth rekonstruksi adalah **proxy provenance**, bukan anotasi semantik independen.
Ada 1.997 pesan berlabel proxy terakuisisi dan 8.000 tanpa label. Pesan tanpa label tidak
dianggap negatif. Dashboard tidak membaca berkas label privat. Lihat
[metodologi rekonstruksi](../05_validasi/GT_RECONSTRUCTION_P9_P10_20260925.md).

## Verifikasi lokal

- Akuisisi nyata emulator-5554: **9.997 pesan, 25 chat**, SQLite valid.
- Akuisisi lewat tombol browser: `ACQ-SIM-LIVE_20260924T225719_714954Z`.
- Hash sumber P8 dan snapshot identik:
  `6101c21bf0604566afb1b5af7544eba1140b8ab0165f7a32f481f5c83b2be8cc`.
- **38 tes pytest lulus**, termasuk baca SQLite tanpa CSV, manipulasi hash, akuisisi ADB,
  perangkat unauthorized, dan penolakan WAL aktif.
- Streamlit AppTest: tujuh tab tanpa exception, pencarian `parkir` menghasilkan 28 pesan,
  T10 terbuka, ID tidak dikenal ditolak, tautan hilang saat hash berbeda, dan `app.py` berjalan.
- Browser agent-browser: halaman tampil, akuisisi lewat tombol, pencarian, navigasi hasil
  A/B/C dan evaluasi; tidak ada browser error tercatat.
- Screenshot lokal: `runtime/workbench_overview.png`, `runtime/workbench_evaluation.png`.

Implementasi demo selesai. Anotasi semantik independen tetap pekerjaan validasi penelitian
terpisah; hasil proxy tidak boleh dinyatakan sebagai akurasi bukti kunci independen.
