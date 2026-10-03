# LIBERA: Integritas Bukti Digital dan Evaluasi Bantuan Local LLM pada Laboratorium Forensik

Status naskah: CANDIDATE. Kontrak 1.0. Naskah kerja untuk integrasi UAS, bukan laporan akhir siap dikumpulkan. GATE_REPORT_RESULTS_OPEN masih CLOSED; angka hasil belum diterbitkan. Bagian yang belum mempunyai bukti tercatat eksplisit sebagai BLOCKED, bukan diisi dengan hasil simulasi rekaan.

## Sampul

Program Studi Komputasi Statistik, Program Diploma IV, Politeknik Statistika STIS, 2026. Dosen pengampu: Farid Ridho (tercantum pada soal). Nomor kelompok, nama dan NIM lima anggota memerlukan konfirmasi anggota. Tidak diasumsikan bahwa nomor topik Digital Forensic merupakan nomor kelompok aktual.

# BAB I – Pendahuluan

## 1.1 Latar Belakang

Sistem informasi statistik mengelola data sejak pengumpulan hingga pengolahan dan penyajian. Ketika muncul dugaan perubahan data tanpa izin, organisasi memerlukan pemeriksaan yang mempertahankan sumber asli, menjelaskan asal setiap artefak, dan membedakan pengamatan dari interpretasi. Kerahasiaan melindungi isi bukti; integritas menjaga agar perubahan dapat diketahui; ketersediaan mendukung pemulihan dan pemeriksaan. Kebutuhan ini menempatkan forensik digital sebagai bagian dari pengelolaan insiden, bukan hanya pencarian kata dalam dokumen. NIST SP 800-86 membahas penggunaan teknik forensik dalam konteks insiden teknologi informasi [1].

LIBERA dirancang sebagai laboratorium kasus sintetis berbasis percakapan. Relevansinya bagi sistem informasi statistik berada pada pengamanan alur bukti, kontrol akses, dokumentasi pemeriksaan, dan tata kelola penanganan insiden. Kasus percakapan bukan microdata survei BPS; rancangan penerapan pada sistem statistik dalam Bab V harus dinyatakan sebagai usulan, bukan penerapan produksi.

Local LLM berpotensi membantu pemeriksa merangkum bukti. Namun keluaran yang lancar belum tentu didukung sumber. RAG menyediakan konteks hasil retrieval [2], sementara evaluasi klaim dan sitasi perlu dilakukan secara terpisah [3]–[5]. Eksekusi lokal dapat membatasi pengiriman isi bukti ke layanan eksternal, tetapi tidak dengan sendirinya membuktikan pengamanan perangkat atau kebenaran keluaran. Proyek ini menilai integritas dan keamanan pipeline sekaligus keterlacakan bantuan AI; keputusan pemeriksaan tetap harus ditinjau manusia.

## 1.2 Rumusan Masalah

- RQ1: Bagaimana acquisition dan extraction menghasilkan digital evidence yang dapat ditelusuri ke sumber serta mendeteksi perubahan bukti?
- RQ2: Kelemahan keamanan apa yang dapat direproduksi dalam lab, dan apakah perbaikan bertahan pada uji ulang?
- RQ3: Bagaimana P5 dan eksperimen A, B, C berbeda dalam ketepatan jawaban, dukungan bukti, dan biaya eksekusi pada benchmark terkunci?
- RQ4: Bagaimana rancangan pelindungan data, penanganan insiden, audit, dan arsitektur keamanan mendukung penerapan prinsip LIBERA pada sistem informasi statistik?

## 1.3 Tujuan Proyek

Tujuan terukur yang diusulkan ialah memverifikasi kesesuaian hash dan provenance pipeline; mereproduksi sedikitnya tiga kelemahan serta remediation/retest; membandingkan P5, A, B, C menggunakan task dan metrik yang dibekukan sebelum akses ground truth; dan menghasilkan checklist sedikitnya 15 kontrol serta sedikitnya lima temuan audit berbukti. Angka ini merupakan target persyaratan UAS, bukan hasil yang telah tercapai. W3 menetapkan rumus, denominator, aturan abstention dan batas interpretasi melalui protokol yang disetujui Coordinator.

## 1.4 Manfaat Proyek

Secara akademis, proyek menyediakan studi tentang hubungan integritas bukti dengan evaluasi keluaran AI. Secara praktis, dokumentasi acquisition, hash, pengujian ulang, dan pemisahan peran dapat membantu pembelajaran penanganan insiden. Manfaat terhadap organisasi statistik masih berupa rancangan yang perlu validasi pada kebutuhan organisasi dan data nyata berizin.

## 1.5 Ruang Lingkup dan Batasan

Objek adalah repository LIBERA dan lab sintetis berizin. Pipeline canonical adalah P2 → P3 → P4 → P5 → P6 → P7 → P8 → LOCK → P9 → P10. P5 adalah traditional deterministic forensic baseline; A Local LLM only; B Local LLM + RAG; C Local LLM + RAG + structured forensic output. A saat ini tidak menerima evidence kasus menurut kontrak; perbandingannya merupakan lower-bound design dan tidak mengisolasi efek retrieval pada input yang setara. Ancaman utama mencakup evidence tampering T1565.001 [8]; rincian ancaman lain mengikuti bukti W2. DEV-SIM/DEV-DRY harus disebut simulasi. Dry-run tidak membuktikan acquisition perangkat fisik maupun performa local LLM. Generalisasi di luar kasus, bahasa, perangkat, dan task yang diuji tidak diasumsikan.

# BAB II – Tinjauan Pustaka

## 2.1 Landasan Teori

CIA diterapkan pada seluruh alur bukti: akses terbatas menjaga kerahasiaan; hash dan pencatatan perubahan mendukung integritas; salinan terkendali dan pemulihan mendukung ketersediaan. Hash yang sama membuktikan kesamaan byte terhadap pembanding yang dipercaya, bukan kebenaran isi percakapan atau keabsahan hukum. Identifier ACQ-* mengacu paket acquisition, DEV-* sumber perangkat, ART-* artefak pemeriksa, dan FND-* interpretasi. Label penyusun corpus atau ground truth tidak boleh diperlakukan sebagai artefak hasil pemeriksaan.

NIST SP 800-86 menyediakan acuan teknik forensik [1]. NIST SP 800-61 Rev. 3 menghubungkan incident response dengan pengelolaan risiko dan menggantikan Rev. 2 [7]. ISO/IEC 27001:2022 adalah acuan sistem manajemen keamanan informasi, bukan sertifikasi yang otomatis diperoleh melalui checklist proyek [9]. NIST SP 800-218 memberi acuan praktik pengembangan aman [10], dan SP 800-53 Rev. 5 menyediakan katalog kontrol keamanan serta privasi [11]. Pemetaan Annex A dan hukum Indonesia harus diverifikasi oleh W4 dari sumber berwenang; naskah ini tidak menyatakan kepatuhan organisasi yang belum diaudit.

RAG memisahkan retrieval atas sumber dengan generation [2]. Supported claim mensyaratkan isi klaim didukung bukti yang dikutip, sedangkan unsupported claim tidak memiliki dukungan memadai atau melampaui bukti. Validitas ART ID dan JSON bukan pemeriksaan semantik. Structured forensic output mendukung keterbacaan dan pemeriksaan otomatis, tetapi tetap memerlukan penilaian isi. Ground truth digunakan evaluator setelah keluaran P8 dikunci, bukan sebagai konteks examiner.

## 2.2 Penelitian/Proyek Terkait

Tabel 2.1. Perbandingan kritis rujukan primer dan implikasi desain LIBERA. Sumber: [2]–[6]; merupakan interpretasi desain, bukan bukti hasil LIBERA.

|Rujukan|Fokus yang diverifikasi|Implikasi bagi LIBERA|Batas transfer|
|---|---|---|---|
|Lewis et al. [2]|RAG menggabungkan model parametrik dengan memory hasil retrieval|Sediakan evidence ART sebagai konteks B/C|Eksperimen Wikipedia/open-domain tidak membuktikan akurasi forensik Indonesia|
|Es et al. [3]|Ragas memisahkan dimensi retrieval dan generation tanpa selalu membutuhkan anotasi GT|Laporkan kualitas retrieval dan dukungan keluaran secara terpisah|LLM judge bukan pengganti evaluator independen; metric LIBERA tidak otomatis bernama Ragas|
|Min et al. [4]|FActScore menilai dukungan pada klaim atomik|Pisahkan satu jawaban menjadi klaim yang dapat diperiksa|Skor biografi dan knowledge source berbeda dari relevansi bukti kasus; metode adaptasi harus dijelaskan|
|Gao et al. [5]|ALCE menilai correctness dan citation quality|Periksa kecocokan isi klaim dengan ART, bukan sekadar keberadaan ID|Sitasi valid secara struktur belum tentu lengkap atau mendukung kesimpulan hukum|
|Liu et al. [6]|Posisi informasi dalam konteks panjang memengaruhi pemanfaatannya|Catat urutan chunk, batas konteks, dan retrieval trace|Temuan paper bukan bukti top-k tertentu optimal untuk LIBERA|

Kelima studi ini menunjukkan perlunya memisahkan akses bukti, kualitas retrieval, ketepatan jawaban, dan dukungan klaim. Kontribusi yang hendak diuji LIBERA adalah penggabungan evaluasi tersebut dengan provenance serta kontrol integritas lab. Kebaruan ilmiah atau keunggulan performa belum dinyatakan sebelum pengujian dan telaah tambahan.

## 2.3 Teknologi dan Tools

Pemilihan komponen mengikuti fungsi yang dapat diuji: Python untuk pipeline dan evaluasi; hash SHA-256 untuk pembanding integritas; Git untuk versioning kode serta evidence publik yang disanitasi; local LLM runtime untuk eksekusi inference; retrieval untuk menyediakan ART; schema keluaran untuk validasi struktur. Nama model, digest, versi runtime, platform dan dependensi harus berasal dari manifest W1/W3. Scan kode mendukung pencarian kelemahan [10], tetapi setiap temuan memerlukan verifikasi W2. Pustaka, model atau perangkat yang hanya direncanakan tidak ditulis sebagai telah digunakan.

# BAB III – Metodologi

## 3.1 Tahapan Pelaksanaan

Studi literatur dan kontrak mendahului pemeriksaan fondasi W1, uji keamanan W2, dan registrasi benchmark W3. P8 harus selesai dengan runtime sebenarnya serta manifest hash sebelum Coordinator membuka GATE_GT_ACCESS. Evaluasi P9 tidak mengubah keluaran P8. W4 menyusun governance berdasarkan bukti dan W5 mengintegrasikan fakta yang dipromosikan.

## 3.2 Arsitektur/Desain Sistem

BLOCKED untuk diagram final sampai inventory W1 dan diagram W4 diterima. Diagram wajib membedakan boundary examiner/evaluator, penyimpanan bukti asli/working, runtime lokal, dan keluaran publik. Klaim lab terisolasi memerlukan konfigurasi dan evidence eksekusi, bukan hanya gambar.

## 3.3 Skenario Pengujian

BLOCKED untuk tabel skenario final sampai protokol W1/W2/W3 diterima. Setiap skenario harus berisi ID, target, prasyarat, langkah aman, hasil diharapkan, ukuran keberhasilan, evidence dan batasan. Metrik AI wajib menyebut unit analisis, denominator dan aturan jawaban kosong. Waktu eksekusi memerlukan mesin dan konfigurasi; jangan membandingkan dry-run dengan inference.

## 3.4 Etika Pengujian dan Rules of Engagement

BLOCKED untuk RoE final sampai target, jadwal dan penanggung jawab nyata disetujui. Pengujian hanya pada salinan sintetis dan target lab yang diizinkan; bukan layanan publik. Pernyataan Etika perlu tanda tangan seluruh anggota. Worker AI bukan penandatangan atau anggota kelompok.

# BAB IV – Hasil Implementasi dan Pengujian

## 4.1 Implementasi Pengamanan

BLOCKED: integrasikan konfigurasi before/after W1/W2 dengan command, versi dan hash evidence setelah verifikasi Coordinator.

## 4.2 Hasil Pengujian dan Analisis Kerentanan

BLOCKED: sedikitnya tiga finding terverifikasi W2, masing-masing dengan kondisi, risiko beserta alasan, akar penyebab, remediation, retest dan keterbatasan. Rencana uji tidak dihitung sebagai temuan.

## 4.3 Analisis Malware/Ancaman

BLOCKED: analisis ancaman safe evidence tampering memerlukan sampel sintetis, hash, static/dynamic evidence, IoC dan pemetaan T1565.001 [8]. Sebut sebagai simulasi ancaman, jangan menyebut malware nyata jika tidak digunakan.

## 4.4 Evaluasi

BLOCKED: GATE_REPORT_RESULTS_OPEN CLOSED. Tidak ada tabel hasil final. Setelah dibuka, setiap angka ditautkan claim_id, artefak sumber, commit, denominator, dan script perhitungan. Jangan menuliskan peningkatan, keunggulan atau keberhasilan tanpa hasil yang mendukung.

# BAB V – Rancangan Pengelolaan Keamanan Data dan Layanan TI

## 5.1 Pelindungan Data Pribadi dan Kerahasiaan Data Statistik

BLOCKED untuk integrasi klasifikasi, DPIA, UU 27/2022, UU 16/1997 dan pengukuran pelindungan W4. Data sintetis tidak membuktikan hilangnya risiko pada data statistik riil.

## 5.2 Penanganan Insiden

BLOCKED untuk playbook dan catatan tabletop W4. Gunakan NIST SP 800-61 Rev. 3 [7]; jika fase Rev. 2 dipakai untuk kemudahan, jelaskan pemetaan dan status superseded. Bedakan tabletop agen dari tabletop yang benar-benar dijalankan anggota kelompok.

## 5.3 Audit Keamanan

BLOCKED untuk >=15 kontrol dan >=5 temuan W4 dengan kondisi–kriteria–penyebab–akibat–rekomendasi, evidence, dan status desain/implementasi.

## 5.4 Rancangan Keamanan Sistem Informasi Statistik

BLOCKED untuk arsitektur W4. Pisahkan kontrol yang telah diuji di lab dari roadmap organisasi; tautkan prioritas risiko dengan finding Bab IV/V.

# BAB VI – Jadwal Pelaksanaan dan Pembagian Tugas

## 6.1 Jadwal Pelaksanaan

Soal dibagikan 1 Oktober 2026 dan deadline 5 Oktober 2026 pukul 13.30 WIB. Tanggal tersebut merupakan ketentuan soal, bukan sejarah pekerjaan tim. Jadwal mingguan aktual dan rencana belum tersedia; git timestamp menunjukkan catatan perubahan, bukan bukti jam kerja anggota. Tabel realisasi final BLOCKED sampai log kegiatan dikonfirmasi tim.

|Periode yang perlu direkonsiliasi|Rencana yang perlu bukti|Realisasi yang perlu bukti|Sumber otorisasi|
|---|---|---|---|
|Minggu sebelum dan saat UAS|Rencana kelompok asli|Kegiatan anggota dan checkpoint|Log anggota, commit dan approval|

## 6.2 Pembagian Tugas

Ownership Worker dalam kontrak adalah pembagian workstream AI, bukan kontribusi lima mahasiswa. Nama, NIM, peran nyata dan persentase kontribusi BLOCKED sampai tim menyatakan dan menyetujui pembagiannya. Persentase tidak diambil dari jumlah commit atau diasumsikan 20% per orang.

# BAB VII – Kesimpulan dan Saran

Belum tersedia dasar untuk menyatakan seluruh tujuan tercapai. Kesimpulan final BLOCKED hingga gate hasil dibuka. Kerangka jawaban yang wajib diisi berbukti:

|RQ|Evidence yang diperlukan|Kondisi kesimpulan|
|---|---|---|
|RQ1|Manifest acquisition/extraction, hash, provenance dan uji tampering W1/W2|Nyatakan apa yang benar-benar terlacak; bedakan sumber simulasi/perangkat fisik|
|RQ2|Finding, perbaikan dan retest W2|Jawab kelemahan mana selesai dan residual risk|
|RQ3|P8 lock, manifest model, metric P9 W3|Bandingkan hasil sesuai denominator dan batas fairness A|
|RQ4|DPIA, tabletop, audit, arsitektur W4|Bedakan rancangan dengan efektivitas kontrol teruji|

Keterbatasan yang sudah perlu dipertimbangkan adalah kasus sintetis, kemungkinan paparan informasi desain kasus pada repository, A tanpa evidence kasus, serta kebutuhan validasi manusia. Keterbatasan aktual execution dicatat setelah integrasi. Saran yang diusulkan mencakup study baru dengan corpus belum terpapar, input baseline yang sebanding dan validasi pada data berizin; saran bukan komitmen implementasi.

# Daftar Pustaka (IEEE)

Metadata dan relevansi diverifikasi melalui halaman primer pada 3 Oktober 2026. Untuk paper, tahun merujuk versi arXiv yang dicantumkan; venue tidak direka.

[1] K. Kent, S. Chevalier, T. Grance, and H. Dang, “Guide to Integrating Forensic Techniques into Incident Response,” NIST SP 800-86, 2006. https://csrc.nist.gov/pubs/sp/800/86/final

[2] P. Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” arXiv:2005.11401, 2020. https://arxiv.org/abs/2005.11401

[3] S. Es, J. James, L. Espinosa-Anke, and S. Schockaert, “Ragas: Automated Evaluation of Retrieval Augmented Generation,” arXiv:2309.15217, 2023. https://arxiv.org/abs/2309.15217

[4] S. Min et al., “FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation,” arXiv:2305.14251, 2023. https://arxiv.org/abs/2305.14251

[5] T. Gao, H. Yen, J. Yu, and D. Chen, “Enabling Large Language Models to Generate Text with Citations,” arXiv:2305.14627, 2023. https://arxiv.org/abs/2305.14627

[6] N. F. Liu et al., “Lost in the Middle: How Language Models Use Long Contexts,” arXiv:2307.03172, 2023. https://arxiv.org/abs/2307.03172

[7] A. Nelson, S. Rekhi, M. Souppaya, and K. Scarfone, “Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile,” NIST SP 800-61 Rev. 3, 2025. https://csrc.nist.gov/pubs/sp/800/61/r3/final

[8] MITRE, “Stored Data Manipulation: T1565.001,” MITRE ATT&CK, accessed Oct. 3, 2026. https://attack.mitre.org/techniques/T1565/001/

[9] ISO, “ISO/IEC 27001:2022 — Information security management systems,” 2022. https://www.iso.org/standard/27001

[10] M. Souppaya, K. Scarfone, and D. Dodson, “Secure Software Development Framework (SSDF) Version 1.1,” NIST SP 800-218, 2022. https://csrc.nist.gov/pubs/sp/800/218/final

[11] NIST, “Security and Privacy Controls for Information Systems and Organizations,” NIST SP 800-53 Rev. 5, 2020, updates documented by publisher. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

# Lampiran dan Pengungkapan AI

Lampiran wajib: RoE, Pernyataan Etika bertanda tangan, cuplikan konfigurasi/log, screenshot autentik bernomor dan bersumber, hash sampel ancaman sintetis, checklist audit serta pengungkapan AI. Tidak tersedia lampiran tanda tangan; jangan membuat tanda tangan sintetis.

Pengungkapan sesi ini: ChatGPT Work digunakan sebagai alat bantu koordinasi, penelusuran sumber primer, penyusunan draf Bab I/II/VI/VII, pemeriksaan struktur UAS dan daftar evidence yang diperlukan. Draf belum merupakan persetujuan penulis manusia. Penggunaan AI oleh sesi/anggota lain harus ditambahkan dari catatan nyata beserta alat, tujuan dan bagian yang dibantu.

# Checklist penerbitan W5

- Semua hasil numerik harus mempunyai CANONICAL_VERIFIED claim_id dan sumber yang dapat dihitung ulang.
- Semua RQ dijawab pada VII dengan bukti IV/V; usulan tidak disebut telah diterapkan.
- Verifikasi citation in-text ↔ bibliography, nomor gambar/tabel, judul dan keterangan.
- Terapkan templat dosen asli; A4, Times New Roman 12 pt, spasi 1,5.
- Hitung halaman isi I–VII pada PDF hasil render; maksimum 30, kecuali sampul/daftar pustaka/lampiran.
- Konfirmasi seluruh identitas, nomor kelompok, realisasi dan kontribusi serta tanda tangan.
- Pastikan tidak ada BLOCKED atau placeholder pada laporan yang diberi label final; jika masih ada, nyatakan pekerjaan belum selesai.
- Nama PDF final mengikuti UAS_KSI_Kelompok[Nomor].pdf setelah nomor sah tersedia.
