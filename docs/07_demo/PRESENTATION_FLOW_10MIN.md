# LIBERA — Presentation Flow 10 Menit

Tujuan presentasi: membuat audiens memahami LIBERA sebagai **workflow pemeriksaan forensik digital offline**, bukan sebagai demo model AI.

## Cerita inti

**Masalah:** examiner menghadapi ribuan pesan. Bagaimana menemukan evidence penting tanpa kehilangan hubungan ke barang bukti asli?

**Jawaban LIBERA:** acquisition dan examination tetap forensic-first; AI baru dipakai setelah evidence diperoleh dan tetap harus menunjuk kembali ke artifact yang dapat diverifikasi.

## 0:00–1:00 — Hook

Pembuka:

> Dari hampir 10.000 pesan di sebuah perangkat, bagaimana examiner menemukan percakapan yang penting—dan bagaimana memastikan bahwa bantuan AI tidak mengarang bukti?

Perkenalkan Raka sebagai tokoh utama pada skenario sintetis LIBERA. Jangan menyatakan bersalah secara hukum.

## 1:00–2:00 — Kasus dan sumber data

- Struktur kasus berasal dari rekonstruksi sumber publik, lalu diadaptasi menjadi skenario sintetis Indonesia.
- Corpus final berisi 10.000 pesan dan kemudian dibekukan.
- ChatSim hanya menjadi controlled Android evidence carrier untuk membawa skenario ke lingkungan device yang dapat diakuisisi.
- ChatSim bukan WhatsApp dan bukan perangkat sitaan nyata.

Kalimat transisi:

> Setelah corpus dibekukan, kami berhenti memperlakukannya sebagai data generasi dan mulai memperlakukannya sebagai sumber evidence dalam simulasi forensik.

## 2:00–4:00 — Bagian digital forensics

Tunjukkan alur:

**DEV-SIM-001 → acquisition → master/working copy → SHA-256 → SQLite → ART evidence**

Actual run:

- 9,997 acquired message artifacts.
- 25 chats.
- SQLite integrity verified.
- Master dan working copy memiliki hash yang sama.

Demo singkat:

1. buka ChatSim;
2. di Workbench klik acquisition snapshot baru atau tunjukkan snapshot yang sudah ada;
3. tunjukkan acquisition ID dan SHA-256;
4. buka satu artifact `ART-*` dan tunjukkan timestamp, pengirim, penerima, isi pesan, acquisition asal.

Pesan utama:

> Analisis dilakukan pada working copy; artifact dapat ditelusuri kembali ke acquisition yang sama.

## 4:00–5:30 — Examiner sebelum AI

Buka tab **Pemeriksaan Tradisional**.

Jelaskan bahwa examiner lebih dulu melakukan:

- literal search;
- timeline;
- actor/pair activity;
- candidate evidence review.

Actual P5 human QC:

- 12 candidate artifacts;
- 6 SUPPORTED;
- 4 NOT_SUPPORTED;
- 2 UNCERTAIN.

Tekankan:

> Ini adalah baseline dan human QC sebelum model AI digunakan.

## 5:30–7:00 — AI hanya sebagai copilot

Jelaskan A/B/C sebagai eksperimen, bukan workflow:

- **A:** AI tanpa case evidence — negative control.
- **B:** AI + retrieved evidence — BGE-M3 mengambil evidence lokal yang relevan.
- **C:** evidence sama dengan B, tetapi output dipaksa ke structured forensic format.

Konfigurasi final cukup disebut singkat:

- Qwen2.5-1.5B lokal melalui Ollama;
- BGE-M3 lokal;
- seluruh case data tetap berada di laptop.

Jangan menjalankan full inference saat demo. Tampilkan locked historical result.

## 7:00–8:30 — Hasil yang paling penting

Tampilkan empat angka:

- **30/30** real A/B/C responses selesai;
- **10/10** output C lolos schema;
- **14/14** P8 lock hashes verified;
- **12/24** evidence references C valid.

Headline:

> **Format yang rapi belum tentu bukti yang valid.**

Jelaskan:

- B tidak menghasilkan invalid evidence reference pada final run.
- C menghasilkan 24 submitted evidence references: 12 valid, 12 dikarantina.
- Model output tidak diedit setelah diketahui salah.
- Invalid references tetap dipertahankan sebagai hasil error analysis.

Jangan menyebut angka proxy sebagai semantic accuracy.

## 8:30–9:30 — Makna hasil dan literatur

Hubungkan dengan literatur:

- LLM paling relevan pada examination, analysis, dan presentation.
- acquisition/preservation tetap menggunakan proses forensic yang deterministik.
- local deployment membantu menjaga kerahasiaan evidence.
- human oversight dan validation tetap diperlukan karena LLM probabilistik.

Posisikan LIBERA:

> Workbench adalah forensic evidence platform; Qwen adalah copilot di dalam platform tersebut.

## 9:30–10:00 — Kesimpulan

Penutup:

> LIBERA menunjukkan bahwa local AI dapat ditempatkan di dalam workflow forensic tanpa menjadikannya sumber bukti. Nilai utamanya bukan sekadar model dapat menjawab pertanyaan, tetapi setiap claim harus dapat diperiksa kembali terhadap artifact asli. Final run kami juga menunjukkan bahwa structured output saja tidak cukup: evidence reference tetap harus divalidasi.

## Jika dosen bertanya tentang ground truth

Jawab:

> Independent semantic ground truth awalnya direncanakan, tetapi label final tidak tersedia. Kami tidak membuat label baru setelah melihat output model karena itu berisiko menjadi circular evaluation. Karena itu hasil final yang kami klaim adalah acquisition integrity, examiner baseline, experiment execution, output locking, dan citation validation. Provenance proxy dilaporkan terpisah dan tidak disebut semantic accuracy.

## Jika dosen bertanya kenapa offline

Jawab:

> Evidence percakapan sensitif tidak perlu dikirim ke layanan cloud. ChatSim, acquisition, Workbench, BGE-M3, dan Qwen berjalan pada laptop penelitian setelah seluruh dependency tersedia.

## Jika dosen bertanya kenapa synthetic

Jawab:

> Kami membutuhkan skenario yang dapat direproduksi, dapat dikontrol, dan tidak mengekspos data pribadi nyata. Karena itu hasilnya kami posisikan sebagai controlled research simulation, bukan validasi operasional pada kasus nyata.

## Yang tidak perlu ditunjukkan dalam 10 menit

- seluruh P1–P10 sebagai daftar teknis;
- semua T01–T10;
- command PowerShell panjang;
- riwayat run v3/v4/v5;
- proxy precision/recall/F1 sebagai headline;
- seluruh file audit dan handoff;
- full embedding atau full model inference secara live.
