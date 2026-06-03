"""
=============================================================================
DATA SYNTHESIZER v1.0 — Proyek LIBERA
=============================================================================
Mensintesis 200 file CSV struktur WhatsApp menjadi data simulasi forensik
digital untuk kasus perdagangan manusia.

Referensi:
- Struktur chat  : WhatsApp Anonymized Privacy-focused Interactions.zip
- Pola kriminal  : ctdc-synthetic.csv (Counter-Trafficking Data Collaborative)
- Inspirasi dialog: Laut Bercerita (Leila S. Chudori)

Output:
- libera_ground_truth/ — CSV + kolom is_criminal_signal & modus_operandi_label
- libera_evidence/     — CSV tanpa kolom rahasia (barang bukti buta)

Penggunaan:
    python data_synthesizer.py
=============================================================================
"""

import os
import sys
import random
import zipfile
import io
import re
import hashlib

import pandas as pd
from tqdm import tqdm

# Force UTF-8 output pada Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# =============================================================================
# KONFIGURASI
# =============================================================================
SEED = 42
random.seed(SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = os.path.join(BASE_DIR,
                        "WhatsApp Anonymized Privacy-focused Interactions.zip")
OUTPUT_GROUND_TRUTH = os.path.join(BASE_DIR, "libera_ground_truth")
OUTPUT_EVIDENCE = os.path.join(BASE_DIR, "libera_evidence")

NUM_SIGNAL_FILES = 2
NUM_CRIMINAL_THREADS_PER_SIGNAL = 4  # conversation_id kriminal per file signal

# =============================================================================
# LABEL MEDIA (pesan non-teks)
# =============================================================================
MEDIA_LABELS = {
    "system": "[Pesan sistem]",
    "image/jpeg": "[Foto]",
    "sticker/webp": "[Stiker]",
    "audio": "[Voice Note]",
    "video/mp4": "[Video]",
    "application/pdf": "[Dokumen PDF]",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        "[Dokumen Word]",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        "[Presentasi PPT]",
    "unknown": "[Media tidak dikenal]",
}

# =============================================================================
# PERSONA — GAYA PENULISAN CHAT
# =============================================================================
# Setiap sender_hash mendapat 1 persona yang konsisten sepanjang file.
# Ini menciptakan variasi ketikan antar-pengirim.

def _abbreviate(text):
    """Singkatan ala anak muda Indonesia."""
    subs = [
        (r"\byang\b", "yg"), (r"\bdengan\b", "dgn"), (r"\btidak\b", "gk"),
        (r"\bsudah\b", "udh"), (r"\bbelum\b", "blm"), (r"\buntuk\b", "utk"),
        (r"\bdari\b", "dr"), (r"\bjuga\b", "jg"), (r"\bsaja\b", "aja"),
        (r"\bkalau\b", "klo"), (r"\bbisa\b", "bs"), (r"\bada\b", "ad"),
        (r"\bini\b", "ni"), (r"\bitu\b", "tu"), (r"\blagi\b", "lg"),
        (r"\bnanti\b", "ntr"), (r"\bbanget\b", "bgt"), (r"\bgimana\b", "gmn"),
        (r"\bdimana\b", "dmn"), (r"\bkenapa\b", "knp"), (r"\bkarena\b", "krn"),
        (r"\btapi\b", "tp"), (r"\bsama\b", "sm"), (r"\bkayak\b", "kyk"),
        (r"\bsekarang\b", "skrg"), (r"\bpunya\b", "pny"), (r"\bharus\b", "hrs"),
        (r"\bmasih\b", "msh"), (r"\bkamu\b", "km"), (r"\bsemua\b", "smua"),
        (r"\bsebentar\b", "btr"), (r"\bbagaimana\b", "gmn"),
        (r"\bmengapa\b", "knp"), (r"\bmereka\b", "mrk"),
        (r"\bsampai\b", "smp"), (r"\bpernah\b", "prnh"),
        (r"\bmungkin\b", "mgkn"), (r"\bsebenernya\b", "sbnrnya"),
    ]
    result = text
    for pat, rep in subs:
        result = re.sub(pat, rep, result, flags=re.IGNORECASE)
    return result


def _commafy(text):
    """Koma berlebih ala chat alay."""
    words = text.split()
    out = []
    for i, w in enumerate(words):
        out.append(w)
        if i > 0 and (i + 1) % random.randint(2, 4) == 0 and random.random() < 0.45:
            out[-1] += ",,,"
    return " ".join(out)


def _dotify(text):
    """Titik tiga di mana-mana."""
    words = text.split()
    out = []
    for i, w in enumerate(words):
        out.append(w)
        if i > 0 and (i + 1) % random.randint(3, 5) == 0 and random.random() < 0.5:
            out[-1] += "..."
    return " ".join(out)


def _repeat_tail(text):
    """Ulang huruf terakhir: "siap" → "siaaapp"."""
    words = text.split()
    out = []
    for w in words:
        if len(w) > 2 and random.random() < 0.35 and w[-1].isalpha():
            w += w[-1] * random.randint(1, 3)
        out.append(w)
    return " ".join(out)


def _exclaim(text):
    """Tanda seru berlebih."""
    t = text.rstrip("!.?,")
    if random.random() < 0.5:
        return t + "!!!"
    return t + "!!"


def _typofy(text):
    """Typo ringan: tukar huruf berdekatan di beberapa kata."""
    words = text.split()
    out = []
    for w in words:
        if len(w) > 3 and random.random() < 0.2:
            idx = random.randint(1, len(w) - 2)
            w = w[:idx] + w[idx + 1] + w[idx] + w[idx + 2:]
        out.append(w)
    return " ".join(out)


# (nama, fungsi transformasi)
PERSONAS = [
    ("normal",          lambda t: t),
    ("huruf_kecil",     lambda t: t.lower()),
    ("HURUF_BESAR",     lambda t: t.upper()),
    ("singkatan",       lambda t: _abbreviate(t.lower())),
    ("koma_lebay",      lambda t: _commafy(t.lower())),
    ("titik_tiga",      lambda t: _dotify(t)),
    ("huruf_ulang",     lambda t: _repeat_tail(t.lower())),
    ("seru_terus",      lambda t: _exclaim(t)),
    ("formal",          lambda t: t[0].upper() + t[1:] + "." if t and not t.endswith((".", "!", "?")) else t),
    ("campur_typo",     lambda t: _typofy(_abbreviate(t.lower()))),
    ("singkat_dots",    lambda t: _dotify(_abbreviate(t.lower()))),
    ("kecil_ulang",     lambda t: _repeat_tail(t.lower())),
]


# =============================================================================
# CORPUS NOISE — CHAT BIASA (BAHASA INDONESIA SLANG)
# =============================================================================
# Terinspirasi tema "Laut Bercerita": kehidupan kampus, persahabatan,
# keluarga, nongkrong, dll.

# ---------- 1-10 karakter ----------
SHORT_NORMAL = [
    "ok", "oke", "iya", "yoi", "gas", "siap", "yuk", "wkwk", "haha",
    "hehe", "dah", "otw", "bet", "asli", "gpp", "hmm", "nih", "tuh",
    "nah", "done", "sabi", "bole", "aman", "gaje", "woy", "bener",
    "cuy", "bro", "sis", "yep", "ayok", "sip", "ngab", "lol", "fix",
    "gass", "oii", "woi", "yaa", "hoo", "ooh", "ahh", "emm", "wah",
    "deh", "kok", "kan", "mah", "dong", "trus", "udah", "sama",
    "amin", "wkwkw", "hihi", "cape", "males", "gabut", "ywd",
    "setuju", "pasti", "yess", "nice", "hayuk", "goks", "gila",
    "gini", "gitu", "mager", "woles", "anjay", "noted", "oot",
    "btw", "fyi", "kuy", "sans", "hoki", "bete", "zonk", "jir",
    "njir", "dih", "ih", "eh", "oh", "ah", "hem", "seep",
    "okey", "okk", "yess", "yoii", "siapp", "gassss", "iyaa",
]
SHORT_INTERROGATIVE = [
    "apa?", "mana?", "siapa?", "kapan?", "gmn?", "dimana?", "hah?",
    "bener?", "serius?", "yakin?", "kok?", "masa?", "jadi?", "ikut?",
    "mau?", "udah?", "bisa?", "boleh?", "sampe?", "ready?",
    "dimana?", "napa?", "knp?", "terus?", "gmana?", "jd?",
    "ya?", "gitu?", "yg mn?", "mw?", "ada?", "gk?",
]
SHORT_EXCLAMATORY = [
    "wah!", "asik!", "gila!", "anjir!", "mantap!", "parah!", "keren!",
    "wow!", "yes!", "aduh!", "yay!", "nice!", "sabi!", "goks!",
    "joss!", "top!", "duh!", "astaga!", "serem!", "buset!",
    "edan!", "hebat!", "luar biasa!", "bangke!",  # slang exclamation
]

# ---------- 11-50 karakter ----------
MEDIUM_NORMAL = [
    # -- Kampus & tugas --
    "gw lg ngerjain tugas nih",
    "deadline besok pagi bro",
    "dosen gw galak banget sih",
    "eh tadi kelas seru banget",
    "gw belom mulai tugas",
    "presentasi gw amburadul",
    "matkul ini susah banget",
    "tadi absen ga sih kamu",
    "gw skip kelas hari ini",
    "IPK gw turun semester ini",
    "lab komputer penuh terus",
    "perpus tutup jam berapa ya",
    "gw baru aja dari kampus",
    "seminar tadi lama banget",
    "tugas kelompok bikin pusing",
    "dosen pembimbing susah ditemui",
    "gw mau ambil cuti semester",
    "kelas tambahan hari sabtu sih",
    "proposal skripsi gw ditolak",
    "sidang minggu depan doain ya",
    # -- Makan & warung --
    "gw laper banget nih",
    "lu udah makan belum",
    "warteg depan kampus enak",
    "mie ayam pak kumis juara sih",
    "gw mau pesen gofood dulu",
    "kopi susu yg biasa ya",
    "bakso malang itu buka ga ya",
    "tadi gw makan nasi padang",
    "gw lagi diet tapi gagal mulu",
    "es teh manis satu ya bang",
    "porsi makan gw nambah terus",
    "masak sendiri lebih hemat sih",
    "indomie telor udah cukup kok",
    "gw mau nyoba restoran baru",
    "sarapan dulu baru mikir",
    # -- Nongkrong & jalan --
    "nongkrong yuk di kafe biasa",
    "gw udah di parkiran nih",
    "lu dimana sih lama banget",
    "macet parah di jalan tol",
    "gw naik ojol aja deh",
    "ketemuan di mall jam 3 ya",
    "gw lagi di warkop nih",
    "jangan lupa bawa duit cash",
    "gw ngga bisa ikut malem ini",
    "bsk sore ada waktu ga",
    "kita ketemuan dimana aja deh",
    "rame banget disini cuy",
    "gw nyari parkir dulu bentar",
    "angkot ke sana masih ada ga",
    # -- Gosip & teman --
    "eh denger gosip belum",
    "si itu udah putus katanya",
    "pacarnya baru siapa sih",
    "gw ga percaya sih gosipnya",
    "diem diem ternyata jadian",
    "temenin gw dong besok",
    "gw berantem sama si anu",
    "jangan bilang siapa siapa ya",
    "gw kangen temen temen SMA",
    "reuni kapan ya kita",
    "temen gw sakit masuk RS",
    "gw baru aja ketemu mantan",
    # -- Keluarga --
    "nyokap nanya kapan lulus",
    "bokap gw lagi di luar kota",
    "adek gw masuk SMA tahun ini",
    "mama minta gw pulang weekend",
    "gw kangen masakan rumah",
    "duit bulanan belum dikirim",
    "kakak gw baru aja nikah",
    "keluarga ngumpul lebaran nanti",
    # -- Hiburan --
    "film baru di bioskop bagus ga",
    "gw lagi marathon drakor nih",
    "playlist lo yang mana sih",
    "konser itu mahal banget tiketnya",
    "game baru udah download belum",
    "manga terbaru udah keluar loh",
    "podcast yg lu rekomen mana",
    "gw lagi baca novel baru nih",
    "series itu endingnya zonk bgt",
    "album baru dia enak banget",
    # -- Olahraga --
    "futsal besok jadi ga",
    "gw abis lari pagi tadi",
    "gym hari ini skip deh",
    "badminton yuk sore ini",
    "pertandingan bola tadi malam gila",
    "lu tim mana dukungnya",
    # -- Umum --
    "cuaca hari ini panas banget",
    "hp gw lowbat nih",
    "wifi kampus lemot parah",
    "gw baru ganti nomor btw",
    "bentar ya gw lg di jalan",
    "ntar gw kabarin lagi deh",
    "gw lg sibuk bgt minggu ini",
    "capek banget hari ini asli",
    "gw mau tidur dulu ya",
    "baru bangun nih masih ngantuk",
    "hujan deres ga bawa payung",
    "dompet gw ketinggalan di rumah",
    "charger hp gw rusak lagi",
    "gw lagi di atm sebentar",
    "internet mati lagi di kosan",
]
MEDIUM_INTERROGATIVE = [
    "lu dimana sekarang?",
    "jadi ketemuan ga hari ini?",
    "tugas dikumpul kapan sih?",
    "siapa yang mau ikut?",
    "ada yang punya catetan?",
    "ntar malem ngapain?",
    "gimana kabar lu sekarang?",
    "boleh gw ikut ga?",
    "bawa motor apa naik apa?",
    "bayar berapa sih tadi?",
    "itu beneran apa hoax?",
    "udah sampe belom?",
    "nilai keluar kapan ya?",
    "ada yg mau bareng?",
    "wifi password nya apa sih?",
    "makan apa ntar siang?",
    "kos lu dimana sih tepatnya?",
    "pinjam catetan boleh ga?",
    "kapan terakhir kali ketemu?",
    "jadwal sidang kapan bro?",
    "lu lagi ngapain sih?",
    "itu tempatnya jauh ga?",
    "siapa aja yg dateng?",
    "kenapa ga bales chat gw?",
    "masih bangun ga lu jam segini?",
    "ada sinyal ga disitu?",
    "booking duluan apa langsung aja?",
    "tadi ngomong apa sih dosennya?",
    "mau nitip apa ga?",
    "besok libur bukan sih?",
    "lu punya kontak dia ga?",
    "gw harus bawa apa aja?",
    "bisa jemput gw ga?",
    "masih buka ga warungnya?",
]
MEDIUM_EXCLAMATORY = [
    "gila sih lu bisa gitu!",
    "mantap banget hasilnya!",
    "parah sih tadi kejadiannya!",
    "keren abis presentasinya!",
    "capek banget hari ini!",
    "enak banget makanannya!",
    "gw seneng banget dapet A!",
    "asik besok libur guys!",
    "gw kaget pas denger itu!",
    "sedih banget ceritanya!",
    "seru banget tadi malem!",
    "ngakak gw liat video itu!",
    "stress berat gw sama tugas!",
    "akhirnya kelar juga nih!",
    "gw bangga sama lu bro!",
    "bahaya banget jalanannya!",
    "sumpah itu lucu parah!",
    "gokil abis pertandingannya!",
    "sakit hati gw dengernya!",
    "makasih banget ya semuanya!",
]

# ---------- 51-100 karakter ----------
LONG_NORMAL = [
    "gw baru aja selesai ngerjain tugas sampe jam 3 pagi, mau mati rasanya",
    "eh besok kita jadi ketemuan di kafe deket stasiun kan ya jam 2 siang",
    "gw denger katanya semester depan ada mata kuliah baru yang wajib diambil",
    "tadi gw ketemu dosen pembimbing dan dia minta revisi lagi untuk bab 3",
    "nyokap gw nelfon tadi nanyain kapan pulang, gw bilang aja abis ujian",
    "gw lagi mikirin mau ambil magang di perusahaan mana buat semester depan",
    "kemarin gw ke toko buku beli novel baru sama buku referensi buat skripsi",
    "kosan gw bocor lagi pas hujan semalam, kasur gw basah semua parah banget",
    "gw udah bikin slides presentasi tapi kayaknya masih kurang bagus deh isinya",
    "jangan lupa besok kumpul di lobby kampus jam 8 pagi buat berangkat bareng",
    "gw lagi bingung milih topik skripsi antara dua tema yang sama menariknya",
    "tadi di kantin ketemu anak angkatan bawah yang kenal sama temen SMA gw",
    "gw udah download semua materi kuliah tapi belum sempat baca sama sekali",
    "weekend ini gw mau staycation aja di kosan binge watching series baru",
    "dompet gw ilang kemarin di angkot tapi alhamdulillah ada yang nemuin",
    "gw harus nabung lebih banyak sih buat bayar uang semester yang naik",
    "motor gw mogok di tengah jalan tadi pagi jadi gw telat masuk kelas",
    "temen sekamar gw pindah kosan jadi sekarang gw sendirian di kamar",
    "gw lagi nyoba masak rendang resep nyokap tapi kayaknya gagal total deh",
    "kemarin malem gw begadang nonton bola sampe subuh terus ketiduran",
    "lu harus coba kedai kopi baru di jalan belakang kampus, enak banget",
    "gw baru aja dapet kabar kalo temen kita diterima kerja di luar negeri",
    "hari ini gw ada rapat organisasi sampe sore jadi ga bisa ikut nongkrong",
    "wifi kosan gw lemot banget jadi gw ke perpus aja buat ngerjain tugas",
    "gw pengen banget liburan ke pantai tapi duit lagi tipis banget sekarang",
    "tadi pagi gw olahraga lari keliling kampus 5 putaran badan pegel semua",
    "gw lagi belajar masak sendiri biar ga jajan terus lumayan hemat soalnya",
    "besok ada bazaar di kampus katanya banyak makanan murah, pada ikut ga",
    "gw nonton film dokumenter semalam tentang laut dan ikan, bagus banget",
    "adek gw mau masuk kuliah tahun depan gw harus bantu cariin info jurusan",
    "gw gagal diet lagi soalnya tadi sore diajak makan bakso sama temen",
    "dosen killer itu ternyata baik banget orangnya kalo diajak ngobrol santai",
    "gw baru dapet info beasiswa buat semester depan mau coba daftar deh",
    "semalam hujan gede banget sampe kosan gw mati lampu semaleman gila",
    "gw harus ganti strategi belajar sih soalnya nilai UTS kemarin jelek bgt",
    "tadi gw antri di administrasi kampus 2 jam cuma buat ngurus surat",
    "laptop gw mulai lemot nih kayaknya harus install ulang atau ganti RAM",
    "gw seneng banget akhirnya bisa ketemu temen temen lama setelah lama ga",
    "duit jajan gw abis padahal baru tanggal 15 harus ngirit banget nih",
    "gw lagi dengerin podcast tentang psikologi, lumayan buat nambah wawasan",
]
LONG_INTERROGATIVE = [
    "eh lu udah dapet info jadwal ujian akhir semester belum dari prodi?",
    "menurut lu gw harus ambil mata kuliah pilihan yang mana semester depan?",
    "ada yang tau kenapa kantin kampus tutup lebih awal hari ini ga sih?",
    "gimana caranya biar bisa fokus belajar tanpa main hp terus ya?",
    "lu pernah coba belajar bareng di perpus kota ga, enak ga disana?",
    "siapa sih yang spread gosip itu ke grup sebelah, tau ga orangnya?",
    "kira kira kalo gw apply magang sekarang masih keburu ga ya?",
    "ada yang mau patungan buat beli kado ulang tahun si anu ga?",
    "kenapa ya akhir akhir ini gw susah banget tidur padahal capek?",
    "lu tau ga tempat print yang murah deket kampus buat tugas akhir?",
    "gimana sih caranya bikin proposal penelitian yang bagus menurut dosen?",
    "ada yang punya softcopy buku mata kuliah statistik semester ini ga?",
    "mendingan naik kereta apa bus sih kalo mau ke bandung dari sini?",
    "kapan ya terakhir kali kita semua ngumpul lengkap kayak dulu?",
    "lu percaya ga sih sama berita yang lagi viral di twitter itu?",
]
LONG_EXCLAMATORY = [
    "gila sih dosen gw tiba tiba kasih tugas tambahan padahal besok UAS!",
    "akhirnya selesai juga skripsi gw setelah perjuangan berbulan bulan!",
    "sumpah gw kaget banget pas tau nilai ujian gw ternyata bagus banget!",
    "parah banget macetnya tadi di jalan, gw sampe telat 1 jam ke kampus!",
    "seneng banget gw dapet tawaran magang di perusahaan impian gw!",
    "ngakak parah tadi di kelas ada yang ketiduran pas dosen nerangin!",
    "sedih banget gw harus pisah sama temen kos gw yang udah pindah!",
    "gokil sih makanan di tempat baru itu enak banget harganya murah lagi!",
    "gw bangga banget sama kalian semua yang udah lulus semester ini!",
    "stress level gw udah maximum nih sama tugas yang numpuk kemana mana!",
]

# ---------- 101-500 karakter ----------
XLONG_NORMAL = [
    "jadi ceritanya kemarin gw ke perpustakaan pusat buat nyari bahan referensi skripsi, ternyata bukunya udah dipinjem semua sama anak angkatan sebelah. akhirnya gw cuma bisa fotokopi dari temen yang kebetulan punya. lumayan lah daripada ga dapet sama sekali, tinggal di rangkum aja sisanya",
    "gw lagi galau banget nih soal masa depan. mau lanjut S2 tapi duit ga ada, mau langsung kerja tapi pengalaman masih minim. nyokap bilang terserah gw aja tapi gw tau dia pengen gw cepet kerja biar bisa bantu ekonomi keluarga. bingung banget sih, kayak semua pilihan ada plus minusnya",
    "kemarin malem gw sama temen temen nongkrong di warkop biasa sampe jam 12 malem. kita ngobrol banyak hal dari mulai tugas kuliah, rencana liburan, sampe masalah percintaan. seru sih walau besoknya gw kesiangan masuk kelas pagi dan dosen negur di depan semua orang. malu tapi ya gimana lagi",
    "gw baru aja beres beresin kosan dan nemu barang barang lama dari jaman SMA. ada foto kelas, surat dari mantan, sama buku diary yang isinya cringe banget kalo dibaca sekarang. jadi nostalgia sendiri inget masa masa dulu yang lebih sederhana. kadang kangen juga sih jadi anak SMA lagi tanpa mikirin skripsi",
    "hari ini gw iseng nyoba bikin kopi pake metode V60 yang lagi hype di kalangan anak anak kampus. beli alatnya lumayan mahal sih tapi hasilnya emang beda dari kopi sachet biasa. kopinya lebih smooth dan ga terlalu pahit. kayaknya gw bakal ketagihan nih bikin kopi sendiri tiap pagi sebelum ke kampus",
    "gw pengen curhat sedikit nih. akhir akhir ini gw ngerasa burnout banget sama rutinitas kuliah yang itu itu aja. bangun pagi, kuliah, tugas, tidur, repeat. kadang gw ngerasa kayak robot yang cuma jalan sesuai program tanpa tau tujuan akhirnya apa. mungkin gw butuh liburan beneran buat refresh otak",
    "tadi siang gw makan di warung makan baru deket gerbang belakang kampus. nasi gorengnya lumayan enak dan harganya murah banget cuma 12 ribu udah sama es teh. kayaknya bakal jadi langganan baru deh soalnya warteg biasa gw udah mulai naik harga dan porsinya makin dikit aja",
    "gw baru selesai nonton dokumenter tentang kehidupan nelayan di pesisir utara Jawa. sedih banget liat perjuangan mereka yang harus melaut berhari hari cuma buat dapet ikan yang harganya ga seberapa di pasar. bikin gw makin bersyukur sih sama kehidupan gw sekarang walau kadang ngeluh juga",
    "rencana liburan semester ini gw mau road trip sama temen temen ke Jogja. kita udah patungan buat sewa mobil dan booking penginapan murah di daerah Malioboro. itinerary nya udah gw bikin detail dari hari pertama sampe hari ketiga. tinggal eksekusi aja nih semoga cuaca mendukung dan ga ada halangan",
    "gw lagi belajar coding otodidak dari YouTube buat nambah skill. mulai dari HTML CSS dulu baru pelan pelan ke JavaScript. lumayan susah sih awalnya tapi lama lama mulai paham juga. siapa tau nanti bisa bikin portfolio sendiri dan dapet kerjaan freelance buat nambah uang jajan selama kuliah",
    "kemarin gw ikut kegiatan bakti sosial yang diadain sama BEM fakultas. kita ke panti asuhan di pinggiran kota buat ngajar anak anak dan bagi bagi sembako. seru banget sih dan bikin hati adem. anak anaknya lucu lucu dan semangat banget belajar walau fasilitas mereka terbatas. jadi pengen rutin kesana",
    "minggu lalu gw akhirnya beraniin diri buat ngomong sama dosen pembimbing soal progress skripsi yang mandek. ternyata beliau pengertian banget dan kasih banyak masukan yang berguna. gw nyesel ga ngomong dari awal soalnya selama ini gw cuma takut ditolak atau dimarahin padahal dosennya baik banget",
]
XLONG_INTERROGATIVE = [
    "guys ada yang tau ga sih kenapa sistem registrasi online kampus sering banget error pas masa pengisian KRS? tiap semester selalu gitu bikin stres, mana harus rebutan mata kuliah yang kuotanya dikit banget lagi. apa emang servernya ga kuat ya nampung banyak mahasiswa sekaligus?",
    "gw lagi bimbang nih antara mau ikut organisasi kampus atau fokus ke akademik aja. menurut kalian gimana sih, worth it ga sih ikut organisasi? soalnya gw denger banyak yang bilang bisa nambah soft skill tapi di sisi lain waktu buat belajar jadi berkurang kan, gimana pengalaman kalian?",
    "eh ada yang punya rekomendasi laptop budget 5 jutaan yang bagus buat kuliah dan ngoding ga? laptop gw yang sekarang udah mulai lemot dan sering ngehang kalo buka banyak tab. pengennya sih yang ringan buat dibawa ke kampus tapi tetep kenceng performanya, ada saran?",
    "menurut kalian kenapa ya generasi kita tuh kayaknya lebih gampang stres dan burnout dibanding generasi orang tua kita dulu? apa karena tekanan sosmed atau emang tuntutan hidup yang makin tinggi ya? gw penasaran aja sih soalnya temen temen gw banyak yang ngeluh hal yang sama",
]
XLONG_EXCLAMATORY = [
    "YESSS gw akhirnya dapet nilai A di mata kuliah yang paling gw takutin selama ini! padahal gw udah pasrah banget pas ujian soalnya soalnya susah parah. ternyata tugas dan presentasi gw nilainya bagus jadi bisa nutupin nilai ujian. alhamdulillah banget perjuangan ga sia sia!",
    "gila sih guys tadi pas gw lagi di jalan tiba tiba motor gw diserempet sama mobil yang belok tanpa sein! untung gw ga jatoh tapi spion gw patah dan baret di bodi motor. orangnya langsung kabur lagi ga tanggung jawab! sumpah kesel banget gw sampe sekarang masih gemetaran!",
    "temen temen gw baru aja ngasih surprise ulang tahun yang paling berkesan dalam hidup gw! mereka diem diem booking tempat makan favorit gw dan undang semua temen deket. ada kue tart dan hadiah yang gw pengen dari lama. gw sampe nangis terharu sumpah ga nyangka mereka sebaik itu!",
    "parah banget banjir di daerah kosan gw semalam sampai air masuk ke kamar setinggi betis! barang barang gw banyak yang kerendem termasuk buku kuliah dan sepatu. gw harus ngungsi ke kosan temen dan sekarang lagi bersihin semua barang. semoga ga ada yang rusak parah sih!",
]

# =============================================================================
# CORPUS SIGNAL — PERCAKAPAN KRIMINAL (HUMAN TRAFFICKING)
# =============================================================================
# Modus: False Promises, Withholds Documents, Debt Bondage
# Kata sandi terinspirasi kasus kriminal nyata di Indonesia.

CRIMINAL_CODEWORDS = {
    # Korban / orang
    "victims":    ["bibit", "anak ayam", "burung", "tanaman", "barang kiriman"],
    # Dokumen
    "documents":  ["sertifikat tanah", "surat gudang", "berkas notaris", "materai"],
    # Uang
    "money":      ["pupuk", "biaya panen", "hasil kebun", "tabungan koperasi"],
    # Pergerakan
    "movement":   ["pindah pot", "angkut hasil bumi", "kirim paket", "ekspedisi"],
    # Lokasi
    "location":   ["gudang", "dermaga", "kebun baru", "kandang"],
    # Bos
    "boss":       ["Om Besar", "Pak Haji", "Mandor", "Juragan"],
}

# Koordinat GPS lokasi strategis Indonesia (pelabuhan, perbatasan)
GPS_COORDS = [
    ("-6.1088, 106.8856", "Tanjung Priok"),
    ("-5.9353, 106.0088", "Pelabuhan Merak"),
    ("-5.8706, 105.7476", "Bakauheni"),
    ("1.0456, 104.0305", "Batam"),
    ("1.0133, 109.9655", "Entikong"),
    ("4.1367, 117.6428", "Nunukan"),
    ("-6.8867, 109.6753", "Pelabuhan Tegal"),
    ("-6.7093, 110.4194", "Pelabuhan Semarang"),
    ("-7.2028, 112.7338", "Tanjung Perak Surabaya"),
    ("-8.7467, 116.0753", "Pelabuhan Lembar Lombok"),
]

# ---- Percakapan kriminal per modus operandi ----
# Setiap entry: (teks, num_chars_range_approx)
# "short"=1-10, "medium"=11-50, "long"=51-100, "xlong"=101-500

CRIMINAL_FALSE_PROMISES = {
    "1-10": [
        "siap bos", "oke pak", "lanjut", "gas", "deal", "ready",
        "mantap", "noted", "aman", "cek", "done", "paham",
    ],
    "11-50": [
        "gw ada lowongan kerja kapal",
        "gajinya 15 juta sebulan bersih",
        "dijamin langsung kerja disana",
        "visa semua diurus sama agen",
        "tinggal berangkat aja nanti",
        "kerja di pabrik luar negeri",
        "kontrak 2 tahun bisa perpanjang",
        "udah banyak yg berangkat aman",
        "makan tidur ditanggung semua",
        "gw kenal orang dalem disana",
        "anak ayam dari kampung siap?",
        "bibit baru dari Indramayu ada 8",
        "Mandor minta update cepet",
        "Om Besar mau ketemu besok pagi",
        "bilang ke mereka kerja halal",
        "jangan kasih tau keluarganya",
        "yang penting mereka mau tanda tangan",
        "cewe umur 18-22 yang dicari",
        "lu jemput mereka di terminal",
    ],
    "51-100": [
        "gw udah janji ke 8 orang dari desa, mereka siap berangkat minggu depan",
        "bilang aja ke mereka bakal kerja di restoran, gaji dollar, hidup enak",
        "jangan sampe bocor ke RT setempat, nanti dipersulit urusannya kita",
        "Om Besar udah siapin gudang transit di daerah Cikarang buat nampung",
        "kita kasih uang muka 500 ribu per orang biar mereka percaya dan mau",
        "yang penting mereka ga boleh bawa HP pas di transit, alasan keamanan",
        "Mandor bilang klien di Malaysia butuh 15 orang sebelum akhir bulan ini",
        "koordinasi sama agen di Batam, titik jemput di dermaga belakang jam 2",
        "bibit unggul dari Karawang ada 5 ekor, siap pindah pot minggu depan",
        "bilang ke anak ayam yang baru, ini kesempatan emas ga bakal dapet lagi",
    ],
    "101-500": [
        "gw udah rekrut 12 orang dari 3 desa di Indramayu dan Karawang. semuanya cewe umur 18 sampe 25 tahun, kebanyakan putus sekolah dan butuh duit. gw janji ke mereka bakal kerja di restoran Jepang di Kuala Lumpur dengan gaji 8 juta sebulan plus makan tinggal gratis. tinggal urus dokumen aja sekarang",
        "Juragan minta kita percepat jadwal pengiriman soalnya ada permintaan mendadak dari klien di Johor. target minimal 10 orang dalam 2 minggu. lu fokus area Cirebon dan Brebes, gw handle Subang sama Purwakarta. yang penting cari yang polos dan gampang diiming imingi. kontak gw kalo ada masalah di lapangan",
        "nanti kalo ada yang nanya soal detail kerjaannya, bilang aja kerja jadi waitress di hotel bintang lima, gajinya besar, fasilitasnya lengkap, tiket pesawat PP ditanggung perusahaan. jangan sampe kelepasan ngomong soal kontrak atau potongan gaji. kalo perlu tunjukin foto palsu hotel yang udah gw siapin di flashdisk",
    ],
}

CRIMINAL_WITHHOLD_DOCS = {
    "1-10": [
        "udah?", "aman", "cek", "siap", "noted", "done", "lanjut",
        "beres", "ok bos", "deal", "mantap", "paham",
    ],
    "11-50": [
        "paspor mereka titip gw dulu",
        "KTP sama ijazah taruh di kantor",
        "sertifikat tanah udah aman semua",
        "berkas notaris ada 8 rangkap",
        "jangan kasih balik dulu dokumennya",
        "bilang aja buat proses visa",
        "materai udah ditempel di semua",
        "surat gudang ditaruh di brankas",
        "fotokopi semua identitas mereka",
        "gw pegang dokumen asli semua",
        "tanpa surat mereka ga bisa lari",
        "kunci brankas cuma gw yang pegang",
        "bilang dokumen lagi diproses",
        "Pak Haji minta semua berkas dikirim",
        "scan KTP kirim ke nomor biasa",
    ],
    "51-100": [
        "kumpulin semua paspor dan KTP asli, bilang ke mereka buat proses visa kerja",
        "selama dokumen masih di tangan kita mereka ga bakal berani macam macam",
        "gw udah simpan 12 paspor di brankas kantor, kunci cuma ada 2 satu sama gw",
        "kalo ada yang minta balik dokumennya bilang aja lagi di kedutaan proses visa",
        "Pak Haji mau semua sertifikat tanah dikirim ke alamat gudang sebelum Jumat",
        "pastiin semua fotokopi berkas notaris udah di scan dan backup di hard disk",
        "yang baru dateng dari Cirebon kemarin suruh serahin semua dokumen ke admin",
        "ijazah mereka gw tahan dulu biar ga coba coba kabur sebelum kontrak selesai",
    ],
    "101-500": [
        "paspor dan dokumen identitas dari 15 orang yang baru dateng udah gw kumpulin semua dan taro di brankas lantai 2. gw bilang ke mereka ini prosedur standar buat pengurusan visa dan izin kerja. ada 3 orang yang agak curiga tapi setelah gw kasih liat surat palsu dari kedutaan mereka akhirnya mau nyerahin juga",
        "Mandor minta kita bikin sistem yang lebih rapi buat nyimpen dokumen. sekarang semua KTP paspor dan ijazah harus di scan dulu terus hardcopy nya ditaro di brankas yang beda beda lokasi. jadi kalo satu ketahuan yang lain masih aman. ini pelajaran dari kasus kemarin yang hampir kena razia petugas imigrasi",
        "lu harus pastiin anak anak baru yang dari Brebes itu nyerahin semua surat berharga mereka sebelum naik kapal. bilang aja ini SOP perusahaan dan dokumen mereka bakal dikembaliin setelah sampe di tempat kerja. padahal kita tau sendiri dokumen itu ga bakal balik selama mereka masih ada nilai ekonomis buat kita",
    ],
}

CRIMINAL_DEBT_BONDAGE = {
    "1-10": [
        "bayar", "hutang", "potong", "cicil", "lunas", "bos",
        "tagih", "aman", "deal", "noted", "duit", "cash",
    ],
    "11-50": [
        "hutang mereka total 200 juta",
        "potong gaji 70% tiap bulan",
        "biaya agen 50 juta per orang",
        "belom lunas jangan harap pulang",
        "tabungan koperasi naik lagi bulannya",
        "pupuk udah dikirim 30 karung",
        "biaya panen bulan ini 80 juta",
        "hasil kebun musim ini lumayan",
        "tagih yang nunggak 3 bulan",
        "tambahin biaya makan dan tempat",
        "total biaya transport per orang 25jt",
        "mereka ga sadar hutangnya nambah",
        "bunga 5% per bulan jalan terus",
        "Juragan mau cashflow report minggu ini",
        "kalo kabur hutangnya tetep jalan",
        "keluarga mereka di kampung jadi jaminan",
    ],
    "51-100": [
        "total biaya rekrutmen transport dan akomodasi per orang 50 juta, dipotong gaji 70%",
        "bilang ke mereka hutangnya 25 juta padahal biaya sebenarnya cuma 5 juta per orang",
        "gaji mereka 3 juta per bulan tapi setelah dipotong hutang dan biaya hidup sisa 200rb",
        "kalo ada yang protes soal potongan gaji bilang aja itu udah kesepakatan di kontrak",
        "Om Besar mau kita naikin biaya akomodasi jadi 2 juta per bulan per orang biar untung",
        "yang udah kerja 6 bulan hutangnya malah nambah karena kita tambahin biaya ini itu",
        "Mandor hitung total piutang dari 20 orang sekarang udah tembus 1 miliar lebih",
        "jangan kasih mereka rincian detail potongannya, cukup kasih angka akhir yang diterima",
    ],
    "101-500": [
        "sistem yang kita pake sekarang udah jalan lancar. setiap orang yang berangkat otomatis punya hutang 50 juta ke kita. dari gaji bulanan mereka 3 juta langsung dipotong 70 persen buat cicilan. sisanya mereka pake buat makan dan kebutuhan dasar yang harganya kita markup 3 kali lipat. jadi hutang mereka ga pernah lunas dan mereka terus kerja tanpa henti",
        "ada 3 orang yang mulai protes soal gajinya yang ga pernah cukup. lu tangani pelan pelan, jangan pake kekerasan dulu nanti malah rame. bilang aja kalo mereka sabar 2 tahun lagi hutangnya lunas dan bisa pulang. padahal kita tau sendiri dengan sistem bunga 5 persen per bulan hutang mereka justru makin gede. yang penting mereka tetep kerja dan ga bikin masalah",
        "Juragan minta laporan cashflow bulan ini. total pemasukan dari 25 orang yang kerja sekarang sekitar 75 juta per bulan. setelah dikurangi biaya operasional 15 juta bersih 60 juta. lumayan stabil sih tinggal scale up aja. rencana bulan depan mau tambah 10 orang lagi dari batch Indramayu yang udah di training di gudang transit Cikarang",
    ],
}

# Percakapan koordinasi operasional (dicampur di signal files)
CRIMINAL_COORDINATION = {
    "1-10": [
        "cek", "aman", "clear", "posisi", "gerak", "siap",
        "tunggu", "jalan", "stop", "go",
    ],
    "11-50": [
        "kapal sandar jam 3 subuh besok",
        "cuaca cerah di selat malam ini",
        "perahu udah di dermaga belakang",
        "nelayan berangkat subuh tadi",
        "ombak tenang aman buat nyebrang",
        "titik kumpul di koordinat biasa",
        "polisi patroli lewat jam 10 malem",
        "ganti rute lewat pelabuhan kecil",
        "Pak RT udah di handle sama kita",
        "speedboat cadangan standby di marina",
        "tim penjemput udah siap di seberang",
        "supir truk kontainer udah briefing",
    ],
    "51-100": [
        f"titik jemput di koordinat {gps[0]}, daerah {gps[1]}, jam 2 pagi besok"
        for gps in GPS_COORDS[:5]
    ] + [
        "ombak tenang malam ini, kapal bisa berangkat dari dermaga timur jam 3 subuh",
        "gw udah koordinasi sama kapten kapal, dia minta bayaran naik jadi 20 juta",
        "rute baru lewat selat karimata lebih aman dari patroli coast guard malam ini",
        "supir truk kontainer udah siap di pelabuhan, muatannya ditutup terpal rapat",
        "pastiin semua anak ayam udah di kandang sebelum jam 12 malem biar ga ketauan",
    ],
    "101-500": [
        f"operasi malam ini lewat jalur laut. titik berangkat di koordinat {GPS_COORDS[0][0]} ({GPS_COORDS[0][1]}), titik tujuan di {GPS_COORDS[3][0]} ({GPS_COORDS[3][1]}). kapal berangkat jam 3 subuh pas patroli coast guard lagi ganti shift. semua anak ayam harus udah di dermaga paling telat jam 2. gw handle koordinasi di darat, lu pastiin kapten kapal udah ready. komunikasi pake sinyal radio channel 7 kalo darurat",
        f"rencana evakuasi kalo operasi gagal: anak ayam dibawa balik ke gudang transit di {GPS_COORDS[1][1]} lewat jalan tikus. semua dokumen dimusnahkan pake shredder yang ada di kantor lantai 2. HP burner dibuang ke laut. kita punya waktu 30 menit sebelum polisi bisa trace lokasi dari sinyal. kalo kepepet, kontak pengacara Pak Haji di nomor yang gw kasih kemarin",
    ],
}

# Gabungkan semua corpus kriminal
ALL_CRIMINAL = {
    "False Promises": CRIMINAL_FALSE_PROMISES,
    "Withholds Documents": CRIMINAL_WITHHOLD_DOCS,
    "Debt Bondage": CRIMINAL_DEBT_BONDAGE,
}

# =============================================================================
# FUNGSI UTILITAS
# =============================================================================

def char_range_to_key(num_chars):
    """Konversi num_characters CSV → kunci corpus."""
    mapping = {
        "0": "system",
        "1-10": "1-10",
        "11-50": "11-50",
        "51-100": "51-100",
        "101-500": "101-500",
    }
    return mapping.get(str(num_chars), "11-50")


def pick_noise_text(num_chars, interrogative, exclamatory, topic_id=0):
    """Pilih teks noise berdasarkan panjang karakter & tipe pesan. Memotong array untuk koherensi topik."""
    key = char_range_to_key(num_chars)
    num_topics = 8

    def pick(array):
        if len(array) >= num_topics:
            chunk = max(1, len(array) // num_topics)
            idx = topic_id % num_topics
            start = idx * chunk
            end = len(array) if idx == num_topics - 1 else start + chunk
            return random.choice(array[start:end])
        return random.choice(array)

    if key == "system":
        return ""

    if key == "1-10":
        if interrogative:
            return pick(SHORT_INTERROGATIVE)
        elif exclamatory:
            return pick(SHORT_EXCLAMATORY)
        else:
            return pick(SHORT_NORMAL)

    elif key == "11-50":
        if interrogative:
            return pick(MEDIUM_INTERROGATIVE)
        elif exclamatory:
            return pick(MEDIUM_EXCLAMATORY)
        else:
            return pick(MEDIUM_NORMAL)

    elif key == "51-100":
        if interrogative:
            return pick(LONG_INTERROGATIVE)
        elif exclamatory:
            return pick(LONG_EXCLAMATORY)
        else:
            return pick(LONG_NORMAL)

    else:  # 101-500
        if interrogative:
            return pick(XLONG_INTERROGATIVE)
        elif exclamatory:
            return pick(XLONG_EXCLAMATORY)
        else:
            return pick(XLONG_NORMAL)


def pick_criminal_text(num_chars, modus, interrogative=False, topic_id=0):
    """Pilih teks kriminal berdasarkan panjang & modus operandi."""
    key = char_range_to_key(num_chars)

    if key == "system":
        return ""

    # Pilih dari modus utama atau koordinasi
    corpus = ALL_CRIMINAL.get(modus, CRIMINAL_FALSE_PROMISES)
    coord = CRIMINAL_COORDINATION

    # 30% kemungkinan ambil dari corpus koordinasi untuk variasi
    if random.random() < 0.3 and key in coord:
        pool = coord[key]
    else:
        pool = corpus.get(key, corpus.get("11-50", []))

    if not pool:
        # Fallback ke noise jika pool kosong
        return pick_noise_text(num_chars, interrogative, False, topic_id)

    return random.choice(pool)


def get_media_label(message_type):
    """Label untuk pesan non-teks."""
    return MEDIA_LABELS.get(message_type, f"[{message_type}]")


def assign_personas(sender_hashes):
    """Assign persona unik ke setiap sender."""
    personas = {}
    available = list(PERSONAS)
    for i, sender in enumerate(sender_hashes):
        persona = available[i % len(available)]
        personas[sender] = persona
    return personas


# =============================================================================
# ENGINE UTAMA: GENERATE KONTEN CHAT
# =============================================================================

def synthesize_file(df, is_signal=False, signal_modus_list=None):
    """
    Isi kolom message_content untuk seluruh DataFrame satu file.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame struktur chat WhatsApp (sudah dibaca dari CSV).
    is_signal : bool
        True jika file ini adalah SIGNAL (kriminal).
    signal_modus_list : list[str] or None
        Daftar modus operandi yang di-assign ke conversation_id kriminal.

    Returns
    -------
    df : pd.DataFrame
        DataFrame dengan kolom baru: message_content, is_criminal_signal,
        modus_operandi_label.
    """
    # Inisialisasi kolom baru
    df = df.copy()
    df["message_content"] = ""
    df["is_criminal_signal"] = False
    df["modus_operandi_label"] = ""

    # Ambil semua sender unik dan assign persona
    senders = df["sender_hash"].unique().tolist()
    sender_personas = assign_personas(senders)

    # Tentukan conversation_id mana yang kriminal (untuk signal files)
    criminal_conv_ids = set()
    conv_modus_map = {}
    if is_signal and signal_modus_list:
        all_conv_ids = sorted(df["conversation_id"].unique().tolist())
        # Pilih conversation_id yang cukup besar (punya banyak pesan text)
        conv_sizes = df[df["message_type"] == "text"].groupby(
            "conversation_id").size()
        # Ambil conversation yang punya minimal 5 pesan text
        eligible = conv_sizes[conv_sizes >= 5].index.tolist()
        if len(eligible) < NUM_CRIMINAL_THREADS_PER_SIGNAL:
            eligible = all_conv_ids

        chosen = random.sample(
            eligible,
            min(NUM_CRIMINAL_THREADS_PER_SIGNAL, len(eligible))
        )
        for i, cid in enumerate(chosen):
            criminal_conv_ids.add(cid)
            conv_modus_map[cid] = signal_modus_list[i % len(signal_modus_list)]

    current_topic_id = random.randint(0, 7)
    last_conv_id = None

    # Generate konten per baris
    for idx, row in df.iterrows():
        msg_type = row["message_type"]
        num_chars = row["num_characters"]
        is_q = bool(row.get("interrogative", False))
        is_exc = bool(row.get("exclamatory", False))
        sender = row["sender_hash"]
        conv_id = row["conversation_id"]

        # Topic Coherence Logic: ganti topik bila conversation_id berubah
        if conv_id != last_conv_id:
            current_topic_id = random.randint(0, 7)
            last_conv_id = conv_id

        # Pesan non-teks → label media
        if msg_type != "text":
            df.at[idx, "message_content"] = get_media_label(msg_type)
            continue

        # Pesan sistem (0 karakter)
        if str(num_chars) == "0":
            df.at[idx, "message_content"] = ""
            continue

        # Tentukan apakah baris ini kriminal
        is_criminal = conv_id in criminal_conv_ids
        modus = conv_modus_map.get(conv_id, "")

        if is_criminal:
            text = pick_criminal_text(num_chars, modus, is_q, current_topic_id)
            df.at[idx, "is_criminal_signal"] = True
            df.at[idx, "modus_operandi_label"] = modus
        else:
            text = pick_noise_text(num_chars, is_q, is_exc, current_topic_id)

        # Terapkan persona pengirim
        _, transform_fn = sender_personas.get(sender, PERSONAS[0])
        text = transform_fn(text)

        df.at[idx, "message_content"] = text

    return df


# =============================================================================
# PIPELINE UTAMA
# =============================================================================

def main():
    print("=" * 70)
    print("  DATA SYNTHESIZER v1.0 - Proyek LIBERA")
    print("  Forensik Digital x Perdagangan Manusia")
    print("=" * 70)
    print()

    # --- 1. Buat folder output ---
    os.makedirs(OUTPUT_GROUND_TRUTH, exist_ok=True)
    os.makedirs(OUTPUT_EVIDENCE, exist_ok=True)
    print(f"[OK] Folder output siap:")
    print(f"    >> {OUTPUT_GROUND_TRUTH}")
    print(f"    >> {OUTPUT_EVIDENCE}")
    print()

    # --- 2. Buka ZIP & baca daftar file ---
    print(f"[..] Membuka ZIP: {os.path.basename(ZIP_PATH)}")
    zf = zipfile.ZipFile(ZIP_PATH, "r")
    all_names = [n for n in zf.namelist() if n.endswith(".csv")]
    total_files = len(all_names)
    print(f"[OK] Ditemukan {total_files} file CSV di dalam ZIP")
    print()

    # --- 3. Pilih file SIGNAL secara acak ---
    signal_indices = set(random.sample(range(total_files), NUM_SIGNAL_FILES))
    signal_names = [all_names[i] for i in signal_indices]
    print(f"[**] File SIGNAL (kriminal) terpilih:")
    for sn in signal_names:
        print(f"    >> {sn.split('/')[-1]}")

    # Modus operandi untuk thread-thread kriminal
    modus_pool = ["False Promises", "Withholds Documents", "Debt Bondage"]
    print()

    # --- 4. Proses semua file ---
    print(f"[..] Memulai sintesis {total_files} file chat...")
    print()

    stats = {"total_rows": 0, "signal_rows": 0, "noise_files": 0,
             "signal_files": 0}

    for i, name in enumerate(tqdm(all_names, desc="Sintesis chat",
                                  unit="file", ncols=80)):
        # Baca CSV dari ZIP
        raw = zf.read(name)
        df = pd.read_csv(io.BytesIO(raw), sep=";", encoding="utf-8-sig")

        # Tentukan apakah file ini SIGNAL
        is_signal = i in signal_indices

        if is_signal:
            # Assign modus operandi berbeda ke setiap thread kriminal
            signal_modus = random.sample(
                modus_pool * 2,  # duplikasi pool agar cukup
                NUM_CRIMINAL_THREADS_PER_SIGNAL
            )
            df = synthesize_file(df, is_signal=True,
                                 signal_modus_list=signal_modus)
            stats["signal_files"] += 1
        else:
            df = synthesize_file(df, is_signal=False)
            stats["noise_files"] += 1

        stats["total_rows"] += len(df)
        stats["signal_rows"] += int(df["is_criminal_signal"].sum())

        # Nama file output (tanpa subfolder dari ZIP)
        out_name = name.split("/")[-1]

        # --- Simpan ke ground truth (DENGAN kolom rahasia) ---
        gt_path = os.path.join(OUTPUT_GROUND_TRUTH, out_name)
        df.to_csv(gt_path, sep=";", index=False, encoding="utf-8-sig")

        # --- Simpan ke evidence (TANPA kolom rahasia) ---
        ev_df = df.drop(columns=["is_criminal_signal",
                                  "modus_operandi_label"])
        ev_path = os.path.join(OUTPUT_EVIDENCE, out_name)
        ev_df.to_csv(ev_path, sep=";", index=False, encoding="utf-8-sig")

    zf.close()

    # --- 5. Ringkasan ---
    print()
    print("=" * 70)
    print("  SINTESIS SELESAI")
    print("=" * 70)
    print(f"  Total file diproses  : {stats['noise_files'] + stats['signal_files']}")
    print(f"  File NOISE           : {stats['noise_files']}")
    print(f"  File SIGNAL          : {stats['signal_files']}")
    print(f"  Total baris pesan    : {stats['total_rows']:,}")
    print(f"  Baris kriminal       : {stats['signal_rows']:,}")
    print(f"  Output ground truth  : {OUTPUT_GROUND_TRUTH}/")
    print(f"  Output evidence      : {OUTPUT_EVIDENCE}/")
    print("=" * 70)

    # --- 6. Verifikasi cepat ---
    print()
    print("[..] Verifikasi output...")
    gt_files = [f for f in os.listdir(OUTPUT_GROUND_TRUTH) if f.endswith(".csv")]
    ev_files = [f for f in os.listdir(OUTPUT_EVIDENCE) if f.endswith(".csv")]
    print(f"  Ground truth files: {len(gt_files)}")
    print(f"  Evidence files    : {len(ev_files)}")

    # Cek kolom di ground truth
    sample_gt = pd.read_csv(
        os.path.join(OUTPUT_GROUND_TRUTH, gt_files[0]),
        sep=";", encoding="utf-8-sig", nrows=5
    )
    print(f"  GT columns        : {sample_gt.columns.tolist()}")

    # Cek kolom di evidence
    sample_ev = pd.read_csv(
        os.path.join(OUTPUT_EVIDENCE, ev_files[0]),
        sep=";", encoding="utf-8-sig", nrows=5
    )
    print(f"  EV columns        : {sample_ev.columns.tolist()}")

    # Cek signal files
    signal_count = 0
    for f in gt_files:
        df_check = pd.read_csv(
            os.path.join(OUTPUT_GROUND_TRUTH, f),
            sep=";", encoding="utf-8-sig", usecols=["is_criminal_signal"]
        )
        if df_check["is_criminal_signal"].any():
            signal_count += 1
            print(f"  Signal file found : {f} "
                  f"({int(df_check['is_criminal_signal'].sum())} baris kriminal)")

    assert len(gt_files) == total_files, \
        f"Ground truth: expected {total_files}, got {len(gt_files)}"
    assert len(ev_files) == total_files, \
        f"Evidence: expected {total_files}, got {len(ev_files)}"
    assert "is_criminal_signal" in sample_gt.columns, \
        "Kolom is_criminal_signal tidak ada di ground truth!"
    assert "is_criminal_signal" not in sample_ev.columns, \
        "Kolom is_criminal_signal bocor ke evidence!"
    assert signal_count == NUM_SIGNAL_FILES, \
        f"Expected {NUM_SIGNAL_FILES} signal files, found {signal_count}"

    print()
    print("[OK] Semua verifikasi LULUS. Data siap digunakan.")
    print()


if __name__ == "__main__":
    main()
