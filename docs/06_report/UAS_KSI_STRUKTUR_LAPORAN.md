# Struktur laporan UAS KSI — Libera (Digital Forensic)

Dokumen ini adalah **kerangka kerja laporan**, disusun dari `Soal_UAS_Keamanan_Sistem_Informasi_Take_Home.pdf` (5 halaman) dan artefak Libera yang tersedia per 3 Oktober 2026. Isi faktual, gambar, dan sitasi akan diisi pada tahap penulisan laporan. Jangan mengubah rencana pengujian menjadi klaim hasil sebelum ada log dan bukti uji.

## Ketentuan penyerahan

- Keluaran akhir: `UAS_KSI_Kelompok[Nomor].pdf`, A4, Times New Roman 12 pt, spasi 1,5; maksimal 30 halaman untuk isi laporan (sampul, daftar pustaka, dan lampiran tidak dihitung).
- Tenggat pada soal: **Senin, 5 Oktober 2026 pukul 13.30 WIB** melalui e-learning.
- Gunakan templat resmi apabila tersedia. Sampul memuat judul, nama dan NIM **lima anggota** sesuai soal, dosen Farid Ridho, Program Studi Komputasi Statistik, Politeknik Statistika STIS, dan tahun 2026. Data internal yang ditemukan baru menyebut empat nama; anggota kelima, NIM, nomor kelompok, dan templat resmi harus diverifikasi.
- Rujukan minimal 10, format IEEE atau APA konsisten. Semua gambar/tabel/tangkapan layar bernomor, berjudul, berketerangan, dan dirujuk di teks. Lampirkan Pernyataan Etika bertanda tangan seluruh anggota dan pengungkapan AI (alat, tujuan, bagian yang dibantu).

**Judul kerja:** *Investigasi Forensik Digital Bukti Percakapan pada Lingkungan Simulasi Android Libera dengan Akuisisi Logis, Rantai Penguasaan Bukti, dan Analisis Berbantuan AI Lokal*.

**Posisi kasus:** corpus percakapan bergaya WhatsApp adalah **data sintetis**. Bukti akuisisi aktual yang tersedia berasal dari aplikasi **Libera ChatSim pada emulator Android** (`DEV-SIM-001`, `ACQ-SIM-001`), bukan akuisisi WhatsApp, ponsel fisik, disk penuh, memori volatil, atau lalu lintas jaringan. Cakupan Tabel 1 pada soal adalah contoh; laporan harus menjelaskan alasan pemilihan bukti aplikasi mobile serta batasnya. Sistem informasi statistik dipakai sebagai **konteks rancangan tata kelola dan skenario ancaman**, bukan klaim bahwa corpus memuat data responden sungguhan.

## Urutan laporan dan alokasi halaman

| Bagian | Isi dan subbagian wajib | Target halaman isi |
|---|---|---:|
| Sampul, pernyataan keaslian/etika, abstrak, daftar isi/gambar/tabel | Ikuti templat resmi; abstrak memisahkan hasil aktual dari rancangan | Di luar/menyesuaikan batas |
| BAB I Pendahuluan | 1.1 Latar belakang: integritas bukti percakapan dan kerahasiaan data statistik; 1.2 rumusan masalah; 1.3 tujuan terukur; 1.4 manfaat; 1.5 ruang lingkup dan batasan | 2–3 |
| BAB II Tinjauan Pustaka | 2.1 CIA, forensik mobile, chain of custody, hash, artefak SQLite, NIST/SWGDE, ISO/IEC 27001, perlindungan data dan AI/RAG; 2.2 perbandingan **3–5** penelitian/proyek; 2.3 tools dan alasan pemilihan | 3–4 |
| BAB III Metodologi | 3.1 alur P1–P10 dengan pemisahan desain, bukti, dan evaluasi; 3.2 diagram arsitektur lab terisolasi dan alur bukti; 3.3 skenario uji, kriteria lulus, metrik; 3.4 RoE: aset, metode, periode, otorisasi, larangan, penanggung jawab | 3–4 |
| BAB IV Hasil Implementasi dan Pengujian | 4.1 pengamanan dan kondisi sebelum–sesudah; 4.2 **minimal tiga** kelemahan terverifikasi, tingkat risiko, akar sebab, perbaikan, uji ulang; 4.3 analisis **statis dan dinamis** satu ancaman/exploit terkendali di sandbox, IoC, pemetaan MITRE ATT&CK, uji deteksi; 4.4 evaluasi terhadap metrik 3.3 | 7–8 |
| BAB V Rancangan Pengelolaan Keamanan Data dan Layanan TI | 5.1 klasifikasi data, DPIA, UU PDP dan kerahasiaan statistik, teknik perlindungan dan ukuran efektivitas; 5.2 IR NIST SP 800-61, playbook, tabletop, notifikasi 3 × 24 jam; 5.3 audit ISO/IEC 27001:2022, **≥15 kontrol dan ≥5 temuan berbukti**; 5.4 arsitektur keamanan sistem informasi statistik, pemetaan Annex A, roadmap risiko | 7–8 |
| BAB VI Jadwal dan Pembagian Tugas | 6.1 rencana versus realisasi per minggu; 6.2 nama, peran, pekerjaan, kontribusi tiap anggota | 1–2 |
| BAB VII Kesimpulan dan Saran | Jawab rumusan masalah satu per satu; nyatakan keterbatasan dan rekomendasi yang mengikuti hasil | 1–2 |
| Daftar pustaka dan lampiran | Minimal 10 rujukan; RoE, etika, chain of custody, konfigurasi/log/hash, gambar, tabel audit lengkap, pengungkapan AI | Di luar batas isi |

Target total isi: **24–29 halaman**. Bab IV dan V mendapat ruang terbesar karena merupakan inti rubrik.

## Rancangan isi per bab

### BAB I — Pendahuluan

1. **Latar belakang:** peran sistem informasi statistik, risiko kebocoran dan manipulasi bukti, kebutuhan integritas dan ketertelusuran. Jelaskan Libera sebagai laboratorium simulasi pesan, bukan investigasi insiden nyata.
2. **Rumusan masalah:** (a) bagaimana akuisisi dan ekstraksi menjaga integritas bukti; (b) bagaimana linimasa dan temuan dapat ditelusuri ke `ART-*`; (c) bagaimana pengamanan dan pengujian kelemahan bekerja setelah perbaikan; (d) bagaimana ancaman manipulasi/eksfiltrasi bukti dideteksi; (e) bagaimana rancangan tata kelola data statistik merespons risikonya.
3. **Tujuan terukur:** hash master–working cocok; validasi SQLite/artefak; hasil baseline dan AI lokal terukur; tiga kelemahan terverifikasi dan diuji ulang; satu ancaman disimulasikan; DPIA, tabletop, 15 kontrol dan 5 temuan audit terdokumentasi.
4. **Manfaat:** pembelajaran forensik yang dapat direproduksi dan rancangan kontrol untuk sistem statistik.
5. **Batasan:** emulator dan aplikasi milik peneliti, akuisisi logis SQLite, data sintetis, satu corpus, satu konfigurasi model; tidak mengklaim forensik memori/jaringan atau data pribadi sungguhan bila tidak diuji.

### BAB II — Tinjauan Pustaka

- Tabel pembanding 3–5 karya: fokus, sumber bukti, metode akuisisi/analisis, evaluasi, perbedaan Libera. Pilih dari daftar rujukan proyek setelah memverifikasi bibliografinya.
- Tabel tools aktual: Android Emulator/ADB, ChatSim, SQLite dan SHA-256, Python, Ollama, BGE-M3, Qwen2.5 1.5B, dashboard Streamlit; versi hanya diisi bila tercatat.
- Jelaskan bahwa AI adalah alat bantu analisis; sitasi artefak harus valid dan keputusan akhir ditinjau pemeriksa.

### BAB III — Metodologi

- **Alur:** corpus P2 beku → staging di ChatSim → akuisisi `ACQ-SIM-001` → verifikasi hash master/working → ekstraksi P4 `ART-*` → baseline P5 → retrieval P6 → tiga kondisi P8 → evaluasi P9. Tunjukkan batas akses ground truth.
- **RoE:** hanya emulator, aplikasi, database, dan salinan kerja milik proyek; isolasi jaringan sesuai uji; waktu dan pelaksana dicatat; tidak menyentuh akun WhatsApp pribadi, perangkat pihak ketiga, atau layanan produksi.
- **Matriks skenario dan metrik:** integritas SHA-256; jumlah dan validitas artefak; akurasi/konsistensi linimasa yang bisa diverifikasi; keberhasilan tiga perbaikan pada uji ulang; deteksi IoC ancaman; validitas sitasi AI. Bedakan metrik **proxy provenance** P9 dari akurasi bukti kunci semantik.
- **Diagram:** arsitektur lab dan rantai bukti; diagram harus diberi label jelas mana rancangan dan mana komponen yang benar-benar dijalankan.

### BAB IV — Hasil Implementasi dan Pengujian

- **4.1:** kontrol integritas corpus P2, pemisahan master/working, hash, log akuisisi, pembatasan ground truth, locking output AI, validasi sitasi. Untuk tiap kontrol sajikan acuan, konfigurasi/langkah, *sebelum*, *sesudah*, bukti berkas, serta akibatnya terhadap risiko. Fakta saat ini: master dan working SQLite sama-sama SHA-256 `6101c21bf0604566afb1b5af7544eba1140b8ab0165f7a32f481f5c83b2be8cc`; ekstraksi menghasilkan 9.997 pesan dan 25 chat dari 10.000 pesan desain. Penyebab tiga pesan tidak terakuisisi perlu dijelaskan berdasar log, jangan ditebak.
- **4.2:** tabel F-01 sampai F-03 dengan objek, cara reproduksi, bukti, skor/tingkat risiko dan alasan, akar sebab, perbaikan, uji ulang. Kandidat yang patut diuji meliputi akses database debug melalui `run-as`, perubahan/ketidaklengkapan database atau artefak, dan referensi bukti AI yang tidak valid. Ketiganya **belum otomatis menjadi temuan kerentanan** hanya karena tercatat dalam proyek. Pilih minimal tiga yang benar-benar diuji dan diperbaiki; bila suatu temuan hanya kelemahan mutu analisis, sebut demikian dan jangan paksa skor CVSS.
- **4.3:** gunakan satu **sampel ancaman/exploit aman dan terkendali** yang relevan, misalnya percobaan manipulasi salinan SQLite/artefak atau akses tidak sah ke build debug dalam lab. Catat SHA-256 sampel, struktur/perilaku statis, urutan eksekusi dan log dinamis, IoC, teknik ATT&CK yang diverifikasi, hasil deteksi sebelum/sesudah. Bagian ini belum didukung eksperimen lengkap pada repo saat ini; jangan mengganti analisis malware dengan narasi umum atau mengklaim sampel malware sungguhan.
- **4.4:** tabel target–hasil–status–bukti untuk seluruh metrik. P8 aktual: 30 respons untuk T01–T10; 12 dari 24 referensi kondisi C dikarantina; angka proxy P9 hanya mengukur pemilihan anchor terhadap distractor, bukan precision/recall bukti kunci semantik.

### BAB V — Rancangan Pengelolaan Keamanan Data dan Layanan TI

- **5.1:** klasifikasi corpus sintetis, artefak forensik, metadata perangkat, ground truth privat, akun/kredensial, dan contoh data statistik bila sistem ini diterapkan. DPIA: alur data, tujuan, risiko subjek data, dasar dan minimisasi, kontrol, risiko residu, pemilik risiko. Kaitkan UU No. 27/2022 dan UU No. 16/1997 secara tepat setelah verifikasi pasal. Uji teknik pseudonimisasi/redaksi pada salinan laporan dan ukur kebocoran identifier atau risiko reidentifikasi yang sesuai.
- **5.2:** peran dan eskalasi; playbook kebocoran/manipulasi evidence store; tabletop berwaktu (deteksi, triase, preservasi, penahanan, pemulihan, keputusan dan bukti notifikasi dalam 3 × 24 jam bila syarat hukumnya terpenuhi, pelajaran). Nyatakan tabletop sebagai simulasi.
- **5.3:** ruang lingkup audit, kriteria ISO/IEC 27001:2022, sumber bukti, pemilik kontrol; lampirkan checklist ≥15 kontrol. Sajikan ≥5 temuan berbukti dengan format kondisi–kriteria–penyebab–akibat–rekomendasi. Pisahkan gap desain atau dokumentasi dari kegagalan kontrol yang teramati.
- **5.4:** arsitektur target untuk sistem informasi statistik: pengumpulan → penyimpanan terklasifikasi → pemrosesan → analisis → publikasi; IAM, enkripsi, audit log, backup, retensi, pemantauan, respons insiden dan pelestarian bukti. Tabel pemetaan risiko/temuan → Annex A → pemilik → prioritas → target waktu → indikator keberhasilan.

### BAB VI dan VII

- Jadwal realisasi dari log/commit proyek, dibandingkan dengan rencana per minggu; jangan membuat tanggal pelaksanaan fiktif.
- Pembagian kontribusi diverifikasi oleh tim. Data internal menyebut Chris, Bela, Meldiro, Daffa; soal meminta lima anggota pada sampul. Gunakan persentase kontribusi yang disepakati anggota.
- Kesimpulan menjawab kelima rumusan masalah. Keterbatasan utama: simulasi, bukti ChatSim dan bukan WhatsApp, akuisisi logis emulator, kehilangan GT semantik independen, serta kekurangan uji apa pun yang belum tuntas.

## Rencana gambar dokumentasi

Paket gambar hasil generasi tersedia pada [indeks gambar](uas_figures/README.md). Gambar yang berstatus rencana belum membuktikan hasil pengujian.

| Kode kerja | Penempatan | Gambar yang akan dibuat/dikumpulkan | Dasar bukti dan aturan |
|---|---|---|---|
| G-01 | III.2 | Diagram arsitektur lab terisolasi dan batas akses | Digambar dari arsitektur proyek; diberi label **diagram rancangan** |
| G-02 | III.2 | Diagram rantai `P2 → DEV-SIM-001 → ACQ-SIM-001 → ART-* → analisis → P9` | Diagram dari manifest dan dokumen protokol |
| G-03 | IV.1 | Dokumentasi keadaan ChatSim/emulator saat akuisisi | Tangkapan layar asli dengan waktu/konteks; jika tidak ada, tidak direka |
| G-04 | IV.1 | Manifest akuisisi dan kesamaan hash master–working | Potongan manifest asli, informasi privat disamarkan |
| G-05 | IV.1 | Validasi ekstraksi: SQLite integrity, 9.997 artefak, 25 chat | `artifact_manifest.json` dan hasil verifikasi ulang |
| G-06 | IV.1/IV.4 | Linimasa serta hubungan aktor hasil baseline | Divisualkan dari `runtime/working/P5/`, beri identitas sumber |
| G-07 | IV.2 | Bukti tiga uji kelemahan: sebelum, perbaikan, dan uji ulang | Screenshot/log autentik per uji; belum tersedia lengkap |
| G-08 | IV.3 | Urutan ancaman sandbox, perubahan artefak/IoC, hasil deteksi | Dari eksperimen terisolasi yang benar-benar dijalankan |
| G-09 | IV.4 | Grafik A/B/C: respons, sitasi valid/karantina; label proxy terpisah | Dari run P8 final dan laporan P9 yang terkunci |
| G-10 | V.1 | Alur data dan titik klasifikasi/redaksi | Diagram rancangan; metrik redaksi dari uji nyata |
| G-11 | V.2 | Linimasa tabletop dan titik keputusan eskalasi | Diagram dari berita acara simulasi |
| G-12 | V.4 | Arsitektur keamanan target dan roadmap berbasis risiko | Diagram rancangan, bukan kondisi saat ini |

Setiap gambar final diberi nomor urut bab, judul, sumber berkas/tanggal, dan keterangan apakah **hasil observasi**, **hasil olah data**, atau **rancangan**. Screenshot UI lama `runtime/workbench_overview.png` dan `runtime/workbench_evaluation.png` boleh dipakai hanya setelah cocok dengan run yang dilaporkan dan informasi sensitif disunting. Gambar hasil generator tidak boleh dipakai untuk berpura-pura sebagai tangkapan layar pengujian.

## Lampiran yang harus disiapkan

1. RoE dan otorisasi pengujian pada lingkungan lab.
2. Pernyataan Etika bertanda tangan seluruh anggota.
3. Form chain of custody, inventaris perangkat, manifest/hash master–working, log tool dan perubahan state.
4. Cuplikan konfigurasi dan log akuisisi, ekstraksi, pengamanan, pengujian tiga kelemahan dan uji ulang.
5. Analisis ancaman: hash sampel, hasil statis/dinamis, IoC, peta ATT&CK, bukti deteksi.
6. DPIA, hasil uji perlindungan data, berita acara tabletop, checklist audit ≥15 kontrol dan ≥5 temuan lengkap.
7. Tabel hasil eksperimen AI dan batas evaluasi proxy, dengan referensi ke artefak yang terkunci.
8. Pengungkapan penggunaan AI generatif untuk penyusunan naskah/diagram/analisis, alat, tujuan, bagian yang dibantu, serta verifikasi manusia.

## Kesenjangan sebelum laporan final

- Templat resmi, nomor kelompok, NIM dan identitas anggota kelima belum tersedia dalam repo.
- Belum ada bukti lengkap tiga pengujian kelemahan beserta perbaikan dan uji ulang, analisis statis/dinamis satu ancaman, tabletop, DPIA terukur, checklist dan lima temuan audit. Semua harus dihasilkan/dibuktikan sebelum diklaim sebagai hasil.
- Ground truth semantik evaluator independen hilang. Hasil P9 yang ada adalah **proxy provenance pasca-eksperimen** dan harus tetap dilabeli demikian.
- Referensi hukum, standar, dan identitas teknik MITRE ATT&CK harus diverifikasi pada sumber resminya saat menulis isi penuh.
