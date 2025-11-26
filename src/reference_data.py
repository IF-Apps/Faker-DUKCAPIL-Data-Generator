"""
Reference Data Module
Static reference data for Indonesian citizen records
"""

from typing import List, Tuple
import random

# ============================================================================
# AGAMA (Religion)
# ============================================================================
AGAMA: List[str] = [
    "Islam",
    "Kristen",
    "Katolik",
    "Hindu",
    "Buddha",
    "Konghucu",
    "Kepercayaan"
]

# Weighted distribution based on BPS Census 2020
# Total: 87.02% Islam, 7.00% Kristen, 2.90% Katolik, 1.69% Hindu, 0.73% Buddha, 0.03% Konghucu, 0.63% Kepercayaan
AGAMA_WEIGHTS: List[float] = [
    0.8702,  # Islam
    0.0700,  # Kristen Protestan
    0.0290,  # Katolik
    0.0169,  # Hindu
    0.0073,  # Buddha
    0.0003,  # Konghucu
    0.0063   # Kepercayaan terhadap Tuhan YME
]

# ============================================================================
# PENDIDIKAN (Education)
# ============================================================================
PENDIDIKAN: List[str] = [
    "Tidak/Belum Sekolah",
    "Belum Tamat SD/Sederajat",
    "Tamat SD/Sederajat",
    "SLTP/Sederajat",
    "SLTA/Sederajat",
    "Diploma I/II",
    "Akademi/Diploma III/Sarjana Muda",
    "Diploma IV/Strata I",
    "Strata II",
    "Strata III"
]

# Weighted distribution based on BPS Susenas 2023 (penduduk 15+ tahun)
# Tidak sekolah ~5.5%, Belum tamat SD ~10.2%, SD ~24.5%, SMP ~21.5%, SMA ~26.8%, D1-D3 ~2.8%, S1/D4 ~7.8%, S2 ~0.8%, S3 ~0.1%
PENDIDIKAN_WEIGHTS: List[float] = [
    0.055,   # Tidak/Belum Sekolah
    0.102,   # Belum Tamat SD/Sederajat
    0.245,   # Tamat SD/Sederajat
    0.215,   # SLTP/Sederajat
    0.268,   # SLTA/Sederajat
    0.010,   # Diploma I/II
    0.018,   # Akademi/Diploma III/Sarjana Muda
    0.078,   # Diploma IV/Strata I
    0.008,   # Strata II
    0.001    # Strata III
]

# ============================================================================
# PEKERJAAN (Occupation) - with realistic Indonesian weights
# Based on BPS data and Indonesian labor statistics
# ============================================================================
PEKERJAAN: List[str] = [
    "Belum/Tidak Bekerja",
    "Mengurus Rumah Tangga",
    "Pelajar/Mahasiswa",
    "Pensiunan",
    "Pegawai Negeri Sipil",
    "Tentara Nasional Indonesia",
    "Kepolisian RI",
    "Perdagangan",
    "Petani/Pekebun",
    "Peternak",
    "Nelayan/Perikanan",
    "Industri",
    "Konstruksi",
    "Transportasi",
    "Karyawan Swasta",
    "Karyawan BUMN",
    "Karyawan BUMD",
    "Karyawan Honorer",
    "Buruh Harian Lepas",
    "Buruh Tani/Perkebunan",
    "Buruh Nelayan/Perikanan",
    "Buruh Peternakan",
    "Pembantu Rumah Tangga",
    "Tukang Cukur",
    "Tukang Listrik",
    "Tukang Batu",
    "Tukang Kayu",
    "Tukang Sol Sepatu",
    "Tukang Las/Pandai Besi",
    "Tukang Jahit",
    "Tukang Gigi",
    "Penata Rias",
    "Penata Busana",
    "Penata Rambut",
    "Mekanik",
    "Seniman",
    "Tabib",
    "Paraji",
    "Perancang Busana",
    "Penterjemah",
    "Imam Masjid",
    "Pendeta",
    "Pastor",
    "Wartawan",
    "Ustadz/Mubaligh",
    "Juru Masak",
    "Promotor Acara",
    "Anggota DPR-RI",
    "Anggota DPD",
    "Anggota DPRD Provinsi",
    "Anggota DPRD Kabupaten/Kota",
    "Dosen",
    "Guru",
    "Pilot",
    "Pengacara",
    "Notaris",
    "Arsitek",
    "Akuntan",
    "Konsultan",
    "Dokter",
    "Bidan",
    "Perawat",
    "Apoteker",
    "Psikiater/Psikolog",
    "Penyiar Televisi",
    "Penyiar Radio",
    "Pelaut",
    "Peneliti",
    "Sopir",
    "Pialang",
    "Paranormal",
    "Pedagang",
    "Perangkat Desa",
    "Kepala Desa",
    "Biarawati",
    "Wiraswasta",
    "Lainnya"
]

# Weighted distribution based on BPS Sakernas 2023 & real Indonesian labor force
# Agriculture 28.3%, Trade 19.2%, Manufacturing 14.2%, Services 12.5%, Construction 6.8%, etc.
# Adjusted for DUKCAPIL population (including non-working age)
PEKERJAAN_WEIGHTS: List[float] = [
    0.0180,  # Belum/Tidak Bekerja (usia kerja tapi tidak bekerja)
    0.1200,  # Mengurus Rumah Tangga (IRT ~24% dari penduduk wanita dewasa)
    0.0850,  # Pelajar/Mahasiswa (~17% populasi di usia sekolah/kuliah)
    0.0180,  # Pensiunan (~3.6% dari usia 60+)
    0.0180,  # Pegawai Negeri Sipil (4.25 juta dari ~140 juta angkatan kerja)
    0.0025,  # Tentara Nasional Indonesia (~400rb personil)
    0.0020,  # Kepolisian RI (~400rb personil)
    0.0320,  # Perdagangan (sektor formal)
    0.0950,  # Petani/Pekebun (sektor pertanian 28.3% tapi banyak buruh tani)
    0.0150,  # Peternak
    0.0120,  # Nelayan/Perikanan (~2.5 juta nelayan)
    0.0250,  # Industri (sektor manufaktur formal)
    0.0230,  # Konstruksi (6.8% angkatan kerja)
    0.0150,  # Transportasi
    0.1100,  # Karyawan Swasta (terbesar di sektor formal)
    0.0050,  # Karyawan BUMN
    0.0020,  # Karyawan BUMD
    0.0100,  # Karyawan Honorer
    0.0400,  # Buruh Harian Lepas (sektor informal besar)
    0.0280,  # Buruh Tani/Perkebunan
    0.0050,  # Buruh Nelayan/Perikanan
    0.0040,  # Buruh Peternakan
    0.0100,  # Pembantu Rumah Tangga
    0.0020,  # Tukang Cukur
    0.0040,  # Tukang Listrik
    0.0080,  # Tukang Batu
    0.0050,  # Tukang Kayu
    0.0005,  # Tukang Sol Sepatu
    0.0025,  # Tukang Las/Pandai Besi
    0.0050,  # Tukang Jahit
    0.0003,  # Tukang Gigi
    0.0020,  # Penata Rias
    0.0005,  # Penata Busana
    0.0025,  # Penata Rambut
    0.0080,  # Mekanik
    0.0012,  # Seniman
    0.0003,  # Tabib
    0.0002,  # Paraji
    0.0005,  # Perancang Busana
    0.0005,  # Penterjemah
    0.0015,  # Imam Masjid
    0.0006,  # Pendeta
    0.0003,  # Pastor
    0.0008,  # Wartawan
    0.0020,  # Ustadz/Mubaligh
    0.0030,  # Juru Masak
    0.0002,  # Promotor Acara
    0.00004, # Anggota DPR-RI (575 orang)
    0.00001, # Anggota DPD (136 orang)
    0.00008, # Anggota DPRD Provinsi (~2,200 orang)
    0.00020, # Anggota DPRD Kabupaten/Kota (~17,000 orang)
    0.0025,  # Dosen (~300rb dosen)
    0.0180,  # Guru (~3 juta guru)
    0.0002,  # Pilot (~8,000 pilot)
    0.0006,  # Pengacara
    0.0004,  # Notaris
    0.0006,  # Arsitek
    0.0012,  # Akuntan
    0.0012,  # Konsultan
    0.0025,  # Dokter (~180rb dokter)
    0.0035,  # Bidan (~230rb bidan)
    0.0055,  # Perawat (~350rb perawat)
    0.0012,  # Apoteker
    0.0003,  # Psikiater/Psikolog
    0.0002,  # Penyiar Televisi
    0.0001,  # Penyiar Radio
    0.0020,  # Pelaut
    0.0006,  # Peneliti
    0.0200,  # Sopir (ojol, taksi, truk, bus)
    0.0003,  # Pialang
    0.0001,  # Paranormal
    0.0550,  # Pedagang (sektor informal besar)
    0.0030,  # Perangkat Desa
    0.0006,  # Kepala Desa (~75rb desa)
    0.0002,  # Biarawati
    0.0600,  # Wiraswasta (UMKM ~65 juta)
    0.0100,  # Lainnya
]

# ============================================================================
# STATUS PERKAWINAN (Marital Status)
# Based on BPS Susenas 2023 - varies significantly by age
# ============================================================================
STATUS_PERKAWINAN: List[str] = [
    "Belum Kawin",
    "Kawin",
    "Cerai Hidup",
    "Cerai Mati"
]

# Age-based marriage probability (based on BPS data)
# Format: {age_range: (belum_kawin, kawin, cerai_hidup, cerai_mati)}
STATUS_PERKAWINAN_BY_AGE = {
    # Usia < 17: 100% belum kawin (by law)
    'child': (1.00, 0.00, 0.00, 0.00),
    # Usia 17-19: kebanyakan belum kawin, sedikit yang sudah menikah
    '17-19': (0.92, 0.08, 0.00, 0.00),
    # Usia 20-24: mulai banyak menikah terutama wanita
    '20-24_L': (0.75, 0.24, 0.01, 0.00),
    '20-24_P': (0.55, 0.44, 0.01, 0.00),
    # Usia 25-29: mayoritas sudah menikah
    '25-29_L': (0.42, 0.56, 0.02, 0.00),
    '25-29_P': (0.25, 0.72, 0.03, 0.00),
    # Usia 30-34: sebagian besar sudah menikah
    '30-34_L': (0.18, 0.79, 0.03, 0.00),
    '30-34_P': (0.12, 0.83, 0.04, 0.01),
    # Usia 35-39: hampir semua sudah menikah
    '35-39_L': (0.10, 0.86, 0.03, 0.01),
    '35-39_P': (0.07, 0.86, 0.05, 0.02),
    # Usia 40-49: stabil menikah, cerai mulai meningkat
    '40-49_L': (0.06, 0.88, 0.04, 0.02),
    '40-49_P': (0.04, 0.85, 0.06, 0.05),
    # Usia 50-59: cerai mati mulai meningkat
    '50-59_L': (0.04, 0.87, 0.04, 0.05),
    '50-59_P': (0.03, 0.78, 0.06, 0.13),
    # Usia 60+: banyak janda/duda
    '60+_L': (0.03, 0.82, 0.03, 0.12),
    '60+_P': (0.02, 0.55, 0.05, 0.38),
}

# ============================================================================
# STATUS HUBUNGAN DALAM KELUARGA (Family Relationship)
# ============================================================================
STATUS_HUBUNGAN: List[str] = [
    "Kepala Keluarga",
    "Suami",
    "Istri",
    "Anak",
    "Menantu",
    "Cucu",
    "Orang Tua",
    "Mertua",
    "Famili Lain",
    "Pembantu",
    "Lainnya"
]

# ============================================================================
# GOLONGAN DARAH (Blood Type)
# ============================================================================
GOLONGAN_DARAH: List[str] = [
    "A",
    "B",
    "AB",
    "O",
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-",
    "Tidak Tahu"
]

GOLONGAN_DARAH_SIMPLE: List[str] = ["A", "B", "AB", "O"]

# ============================================================================
# KEWARGANEGARAAN (Nationality)
# ============================================================================
KEWARGANEGARAAN: List[str] = [
    "WNI",
    "WNA"
]

# ============================================================================
# NAMA (Indonesian Names) - Extended for millions of records
# ============================================================================

# Nama depan laki-laki (300+ names)
NAMA_DEPAN_PRIA: List[str] = [
    # Common names
    "Ahmad", "Muhammad", "Abdul", "Adi", "Agus", "Andi", "Arif", "Bambang",
    "Budi", "Dedi", "Deni", "Eko", "Fajar", "Gunawan", "Hadi", "Hendra",
    "Irwan", "Joko", "Kurniawan", "Lukman", "Mulyadi", "Nugroho", "Prasetyo",
    "Rachmat", "Rudi", "Slamet", "Sugianto", "Surya", "Teguh", "Wahyu",
    "Yanto", "Zainal", "Rizky", "Dimas", "Bayu", "Galih", "Imam", "Krisna",
    "Lutfi", "Maulana", "Naufal", "Okky", "Pandu", "Qodir", "Reza", "Satria",
    "Taufik", "Umar", "Vino", "Wawan", "Yoga", "Zaki", "Aditya", "Bagus",
    "Cahyo", "Danang", "Erwin", "Faisal", "Gilang", "Hanif", "Ilham", "Jefri",
    "Kevin", "Leo", "Miftah", "Nanda", "Oscar", "Prima", "Raka", "Sigit",
    "Tri", "Ucok", "Vian", "Wisnu", "Yudha", "Zulfikar", "Arman", "Basuki",
    "Chandra", "Damar", "Fadli", "Gani", "Herman", "Ivan", "Johan", "Karim",
    # Extended names
    "Aan", "Aban", "Abbas", "Abdillah", "Abdurrahman", "Abidin", "Abrar", "Abubakar",
    "Achmad", "Adam", "Afdal", "Afif", "Agung", "Ahsan", "Ainul", "Ajat",
    "Akhdan", "Akhtar", "Akmal", "Akram", "Alan", "Aldi", "Aldo", "Alex",
    "Alfan", "Alfath", "Alfian", "Alfi", "Ali", "Alif", "Alim", "Alvin",
    "Aman", "Amar", "Ambon", "Amin", "Amir", "Ammar", "Amrul", "Anang",
    "Andika", "Andri", "Angga", "Anggara", "Anjas", "Annas", "Anton", "Anugrah",
    "Apriadi", "Apriyanto", "Aqil", "Ardiansyah", "Ardian", "Arga", "Ari", "Arief",
    "Arifin", "Arjuna", "Arkan", "Arsyad", "Asep", "Ashari", "Aslan", "Aslam",
    "Asri", "Ato", "Aulia", "Awaludin", "Ayub", "Azhar", "Azis", "Aziz",
    "Azzam", "Bachtiar", "Bagas", "Bahar", "Bahri", "Bahrul", "Bakri", "Bani",
    "Barkah", "Basri", "Bastian", "Beni", "Bima", "Bisri", "Bondan", "Bowo",
    "Burhan", "Burhanudin", "Cakra", "Cecep", "Chairul", "Chairudin", "Christian", "Dadang",
    "Dafa", "Daffa", "Dahlan", "Daiman", "Dani", "Daniel", "Darmawan", "Darwin",
    "Daud", "David", "Dede", "Dedy", "Deny", "Dewa", "Dhani", "Dicky",
    "Didi", "Didin", "Didik", "Diki", "Dimas", "Dino", "Dion", "Dirga",
    "Dodi", "Doni", "Donny", "Drajat", "Dudung", "Dwi", "Edi", "Eddy",
    "Edwin", "Effendi", "Eka", "Elang", "Elyas", "Emir", "Endang", "Endra",
    "Eno", "Erdi", "Erik", "Fadel", "Fadhil", "Fadil", "Fahmi", "Fahri",
    "Faiq", "Faizan", "Fajri", "Fakhriy", "Fandi", "Farel", "Faris", "Farhan",
    "Farrel", "Fatah", "Fathir", "Fathoni", "Fauzan", "Fauzi", "Febri", "Feri",
    "Fikri", "Firman", "Firmansyah", "Frans", "Ganang", "Ganes", "Garin", "Gathan",
    "Gatot", "Ghani", "Ghifari", "Gibran", "Gilbran", "Ginting", "Giri", "Gofar",
    "Habib", "Habibi", "Hafid", "Hafidz", "Hafiz", "Hakim", "Halim", "Hamdan",
    "Hamid", "Hamzah", "Hanafi", "Hanan", "Handoko", "Hanung", "Haris", "Hartawan",
    "Hasan", "Hasbi", "Hasbullah", "Hasim", "Hassan", "Haykal", "Helmi", "Hendri",
    "Hendro", "Hengki", "Henri", "Heri", "Herianto", "Hermanto", "Hidayat", "Hikam",
    "Hilman", "Himawan", "Huda", "Husain", "Husen", "Husni", "Ibrahim", "Ichsan",
    "Idham", "Idris", "Ihsan", "Ikhsan", "Ikhwan", "Ilyas", "Imam", "Imran",
    "Indra", "Irfan", "Irsyad", "Isa", "Ishak", "Iskandar", "Ismail", "Iwan",
    "Iyus", "Jabir", "Jajang", "Jamal", "Jamaludin", "Jauhari", "Jaya", "Jayadi",
    "Jefry", "Jeri", "Jimmy", "Jodi", "Jonathan", "Jono", "Jordi", "Juanda",
    "Julfikar", "Jumadi", "Junaedi", "Junaidi", "Kaka", "Kamil", "Karman", "Karsono",
    "Kasim", "Kemal", "Khalid", "Khairul", "Khairun", "Khoirul", "Komarudin", "Kusuma",
    "Lamhot", "Latif", "Lukito", "Lutfan", "Machfud", "Mahardika", "Mahdi", "Mahendra",
    "Mahmud", "Maman", "Mansur", "Maruf", "Marwan", "Marzuki", "Mas", "Masyhur",
    "Maulidi", "Mawar", "Misran", "Moch", "Mohamad", "Muchlis", "Muchtar", "Mufid",
    "Muhaimin", "Muhajir", "Muhamad", "Mukhlis", "Mukhtar", "Mukti", "Mulya", "Munir",
    "Mursid", "Musa", "Mustofa", "Muzakir", "Nabhan", "Nadhif", "Nafis", "Nabil",
    "Najib", "Nasir", "Nasrul", "Naufal", "Nazar", "Nazri", "Nico", "Nizam",
    "Noor", "Nur", "Nurhadi", "Nurman", "Odi", "Oka", "Omar", "Panji",
    "Pasha", "Prabowo", "Prabu", "Pradana", "Pramono", "Pras", "Prawira", "Puji",
    "Putra", "Qori", "Raden", "Raffi", "Rafi", "Rafid", "Rahadian", "Raihan",
    "Raja", "Rajab", "Rakhmat", "Rama", "Ramadhan", "Ramdani", "Rangga", "Rasya",
    "Rasyid", "Rauf", "Rayhan", "Rehan", "Rendra", "Rendy", "Reno", "Revaldo",
    "Rheza", "Rianto", "Ridho", "Ridwan", "Rifai", "Rifki", "Rifky", "Riski",
    "Rizal", "Rizki", "Rizwan", "Robby", "Rohman", "Rohmani", "Romli", "Ronan",
    "Roni", "Rosid", "Rosihan", "Rouf", "Rozak", "Rudy", "Rusdi", "Ruslan",
    "Sabri", "Safar", "Saiful", "Sakti", "Salman", "Sam", "Samudera", "Sandi",
    "Sanusi", "Saputra", "Satriya", "Setiawan", "Sidik", "Singgih", "Sofyan", "Soleh",
    "Subekti", "Subhan", "Sudarsono", "Suhendar", "Suhendra", "Sulaiman", "Sultan", "Sunaryo",
    "Supardi", "Supriyanto", "Suryana", "Sutrisno", "Syafii", "Syahrul", "Syamsul", "Syarif",
    "Tama", "Tamba", "Tanto", "Taqwa", "Tarmizi", "Taufan", "Taufiq", "Tedi",
    "Thomas", "Tito", "Tomi", "Tommy", "Toni", "Tony", "Topan", "Totok",
    "Tubagus", "Uki", "Ulil", "Ultah", "Ulung", "Usman", "Uzair", "Valdi",
    "Veri", "Vikri", "Wahid", "Wahyudi", "Waldi", "Wawan", "Wendi", "Widi",
    "Widodo", "Wira", "Wiranto", "Wito", "Yahya", "Yan", "Yandi", "Yanuar",
    "Yayan", "Yazid", "Yogi", "Yohan", "Yono", "Yos", "Yosua", "Yuda",
    "Yudi", "Yusran", "Yusril", "Yusron", "Yusuf", "Zaenal", "Zain", "Zainul",
    "Zaki", "Zakki", "Zamzami", "Zikri", "Zul", "Zulfan", "Zulham", "Zulkarnain"
]

# Nama depan perempuan (300+ names)
NAMA_DEPAN_WANITA: List[str] = [
    # Common names
    "Ayu", "Ani", "Dewi", "Dian", "Eka", "Fitri", "Indah", "Kartika",
    "Lestari", "Maya", "Ningsih", "Putri", "Ratna", "Rina", "Sari", "Sri",
    "Siti", "Tri", "Wati", "Yanti", "Yulia", "Zahra", "Amelia", "Bunga",
    "Citra", "Diana", "Elvira", "Fani", "Gita", "Hana", "Intan", "Jasmine",
    "Kartini", "Linda", "Mega", "Nadia", "Oktavia", "Puspita", "Qory",
    "Rosa", "Shinta", "Tika", "Ulfa", "Vera", "Wulan", "Xena", "Yolanda",
    "Zara", "Anggi", "Bella", "Cantika", "Dinda", "Ella", "Fira", "Gracia",
    "Helena", "Ira", "Julia", "Kirana", "Laras", "Mira", "Nabila", "Olivia",
    "Paramita", "Rahma", "Salsa", "Tiara", "Uma", "Vania", "Widya", "Yeni",
    "Zelda", "Aisyah", "Balqis", "Chairani", "Dara", "Evi", "Fadhila",
    "Galuh", "Husna", "Isma", "Jihan", "Kayla", "Lina", "Melati", "Nurul",
    # Extended names
    "Adelia", "Adinda", "Afifah", "Agustina", "Aini", "Ainun", "Ajeng", "Alya",
    "Amanda", "Amelinda", "Amira", "Andin", "Andini", "Angela", "Angelia", "Anisa",
    "Anita", "Anna", "Annisa", "Aprilia", "Arini", "Arista", "Arlita", "Arrum",
    "Asih", "Asri", "Astri", "Astrid", "Atika", "Aurel", "Aurelia", "Aurora",
    "Azizah", "Badriah", "Berliana", "Bintang", "Bulan", "Cahaya", "Cahya", "Calista",
    "Cantik", "Carla", "Carolina", "Cendana", "Ceria", "Chandra", "Chika", "Cici",
    "Cinta", "Clara", "Clarissa", "Cut", "Dahlia", "Damayanti", "Dea", "Delia",
    "Delima", "Della", "Devi", "Dewanti", "Dhea", "Diah", "Dini", "Dita",
    "Diva", "Dwi", "Dyah", "Eka", "Elisa", "Eliza", "Elma", "Elsa",
    "Elvina", "Ema", "Emma", "Endang", "Eni", "Era", "Erma", "Erna",
    "Ersa", "Esa", "Esther", "Eti", "Eva", "Evi", "Evita", "Farah",
    "Farida", "Fatima", "Fatimah", "Feby", "Febi", "Felicia", "Feni", "Fenny",
    "Fia", "Fika", "Fina", "Fitriana", "Fitriani", "Friska", "Gading", "Galih",
    "Ganesha", "Gendis", "Genoveva", "Ghina", "Gina", "Gisela", "Giselle", "Gloria",
    "Grace", "Gresia", "Gustin", "Habibah", "Hafsa", "Hajar", "Halimah", "Hamidah",
    "Hani", "Hanifa", "Hanna", "Hannah", "Happy", "Harum", "Hasna", "Hastuti",
    "Hayati", "Heni", "Henny", "Herlina", "Hermin", "Hesti", "Hidayah", "Hijrah",
    "Hilma", "Ida", "Ika", "Imelda", "Ina", "Indira", "Indriani", "Ines",
    "Ingrid", "Inke", "Irene", "Iriani", "Irine", "Irma", "Isna", "Isti",
    "Ivana", "Ivone", "Jasmin", "Jelita", "Jennifer", "Jessica", "Jovita", "Juita",
    "Juliana", "Junita", "Kamila", "Kania", "Karen", "Karina", "Karlina", "Karolin",
    "Kartini", "Kasih", "Katharina", "Keisha", "Keke", "Kemala", "Kemuning", "Kesya",
    "Khansa", "Kiki", "Kinanti", "Kirani", "Komalasari", "Kristina", "Kurnia", "Kusuma",
    "Laila", "Laksmi", "Lala", "Lalita", "Lastri", "Laura", "Leila", "Lely",
    "Leni", "Lenny", "Lia", "Lidya", "Lika", "Lilis", "Lily", "Lintang",
    "Lisa", "Listya", "Lita", "Livia", "Liza", "Lucia", "Lucy", "Luki",
    "Lulu", "Luna", "Lusiana", "Lutfia", "Lydia", "Mada", "Maharani", "Mahkota",
    "Maimunah", "Maira", "Malika", "Manda", "Marcelina", "Margareta", "Maria", "Mariam",
    "Mariana", "Marice", "Marifah", "Marina", "Marlina", "Marta", "Martha", "Martina",
    "Maryam", "Maudy", "Maulida", "Mawar", "Melani", "Melinda", "Melissa", "Melly",
    "Mentari", "Metha", "Michelle", "Mila", "Milda", "Mimin", "Mita", "Monica",
    "Murti", "Mutia", "Mutiara", "Nabilah", "Nadine", "Nadira", "Nafisa", "Naila",
    "Najwa", "Nana", "Nancy", "Nani", "Naomi", "Naura", "Nella", "Nia",
    "Nika", "Nila", "Nilam", "Nina", "Ninda", "Nisa", "Nita", "Novia",
    "Novi", "Nurani", "Nuri", "Nuriah", "Nurma", "Nurmala", "Nurma", "Octa",
    "Oktaviani", "Olga", "Olyvia", "Oma", "Ona", "Opi", "Padma", "Patricia",
    "Paula", "Pelangi", "Permata", "Pertiwi", "Prita", "Priscilla", "Puspa", "Puteri",
    "Qonita", "Queen", "Rafa", "Rahmania", "Rahmawati", "Raisa", "Raisya", "Rani",
    "Rasmi", "Ratih", "Ratnasari", "Ratu", "Regina", "Reni", "Renny", "Restu",
    "Retno", "Reva", "Riani", "Rianti", "Rica", "Ridha", "Rifa", "Rifka",
    "Rika", "Rima", "Rini", "Ririn", "Risda", "Riska", "Riski", "Rita",
    "Riva", "Rizka", "Rizki", "Rohana", "Rosalina", "Rosana", "Rosiana", "Rosita",
    "Rosma", "Rosmala", "Rukmini", "Rully", "Rumi", "Rusmini", "Ruth", "Saadah",
    "Sabrina", "Safira", "Safitri", "Sahara", "Sakina", "Sakura", "Salma", "Salsabila",
    "Sandra", "Sania", "Santika", "Sarah", "Saras", "Sekar", "Selvi", "Septi",
    "Septy", "Serly", "Shafira", "Shakila", "Sherly", "Shifa", "Silvi", "Silvia",
    "Sintia", "Sisca", "Siska", "Siti", "Sofi", "Sofia", "Soraya", "Stefani",
    "Stella", "Suci", "Sukma", "Sulastri", "Sulis", "Sumarti", "Sumiati", "Sunarni",
    "Sundari", "Suprihatin", "Suri", "Suriani", "Susanti", "Susi", "Syarifah", "Syifa",
    "Tania", "Tari", "Tasya", "Tati", "Tatik", "Tina", "Titi", "Titik",
    "Tria", "Triana", "Tyas", "Ulfah", "Ulfi", "Umi", "Unik", "Untari",
    "Uswatun", "Utami", "Utari", "Valencia", "Valeria", "Vani", "Vanny", "Vega",
    "Vela", "Veni", "Venny", "Veronica", "Vina", "Vinda", "Vinka", "Viola",
    "Vita", "Vivi", "Wahyu", "Wanda", "Weni", "Widiastuti", "Widy", "Wika",
    "Windy", "Windi", "Wirda", "Wiwik", "Wulandari", "Yani", "Yanis", "Yanti",
    "Yasmin", "Yayuk", "Yessi", "Yohana", "Yosephine", "Yudha", "Yuli", "Yuliana",
    "Yunika", "Yuni", "Yunita", "Yusra", "Yustina", "Zaenab", "Zahira", "Zalfa",
    "Zaskia", "Zehra", "Zelda", "Zeni", "Zia", "Zita", "Zulfa", "Zulaikha"
]

# Nama belakang/keluarga (200+ names)
NAMA_BELAKANG: List[str] = [
    # Common surnames
    "Saputra", "Pratama", "Putra", "Setiawan", "Santoso", "Susanto", "Wijaya",
    "Hidayat", "Nugroho", "Utomo", "Prabowo", "Kurniawan", "Hartono", "Suryadi",
    "Wibowo", "Prasetyo", "Permana", "Hermawan", "Gunawan", "Rahman", "Hakim",
    "Siregar", "Nasution", "Sitorus", "Siahaan", "Simanjuntak", "Simbolon",
    "Hutabarat", "Panjaitan", "Manullang", "Situmorang", "Tampubolon", "Sirait",
    "Lubis", "Daulay", "Harahap", "Pulungan", "Batubara", "Rangkuti", "Pohan",
    "Abdullah", "Ibrahim", "Ismail", "Hassan", "Hussein", "Malik", "Karim",
    "Salim", "Bakri", "Basri", "Fauzi", "Hamzah", "Mansur", "Rosyid", "Wahid",
    "Ramadhan", "Syahputra", "Maulana", "Anwar", "Hasan", "Kusuma", "Adiputra",
    "Mahendra", "Sudirman", "Subekti", "Suparman", "Supriyadi", "Sutrisno",
    "Yusuf", "Zainudin", "Firmansyah", "Budiman", "Setiadi", "Hadiwibowo",
    # Extended surnames - Javanese
    "Wicaksono", "Purnomo", "Susilo", "Yudhoyono", "Sukarno", "Suharto",
    "Widodo", "Jatmiko", "Condro", "Kusumo", "Pamungkas", "Pangestu",
    "Puspito", "Raharjo", "Riyanto", "Sarjono", "Sasmito", "Sasongko",
    "Satrio", "Slamet", "Sunarso", "Sunarto", "Suprapto", "Suryanto",
    "Sutanto", "Sutarjo", "Sutikno", "Suwarno", "Wardoyo", "Warsito",
    # Extended surnames - Sundanese
    "Suryatmaja", "Suryawan", "Atmaja", "Mulyana", "Suryaatmaja", "Kartawijaya",
    "Sukarna", "Suganda", "Suherman", "Suhendar", "Sunarya", "Sutisna",
    "Adinata", "Adiwijaya", "Komara", "Koswara", "Permadi", "Sudrajat",
    # Extended surnames - Batak
    "Sinaga", "Turnip", "Siagian", "Napitupulu", "Pardede", "Purba",
    "Silalahi", "Sihombing", "Simatupang", "Tamba", "Tarigan", "Tobing",
    "Aritonang", "Butar-Butar", "Ginting", "Sembiring", "Karo", "Perangin-angin",
    "Bangun", "Barus", "Brahmana", "Depari", "Keliat", "Milala",
    "Munte", "Pinem", "Sitepu", "Sebayang", "Sinulingga", "Tendang",
    # Extended surnames - Minang
    "Chaniago", "Dalimo", "Datuk", "Koto", "Mandailing", "Marajo",
    "Piliang", "Rajo", "Sikumbang", "Tanjung", "Caniago", "Khatib",
    # Extended surnames - Makassar/Bugis
    "Daeng", "Karaeng", "Andi", "Arung", "Datu", "Petta", "Puang",
    # Extended surnames - Arabic origin (common in Indonesia)
    "Alatas", "Algadri", "Alhaddad", "Alhabsyi", "Assegaf", "Barakbah",
    "Bazher", "Syihab", "Shahab", "Shihab", "Jaelani", "Jailani",
    # Extended surnames - Common Indonesian
    "Adipura", "Adinegoro", "Adisaputra", "Agustiawan", "Akbar", "Alam",
    "Alamsyah", "Amrullah", "Andrianto", "Anggraeni", "Ardiansyah", "Arifin",
    "Baharudin", "Budiyanto", "Budiarto", "Cahyono", "Darmawan", "Dermawan",
    "Effendy", "Fadillah", "Fadilah", "Fatahillah", "Febriyanto", "Febrianto",
    "Handayani", "Handoko", "Haryadi", "Haryanto", "Hasibuan", "Hendarto",
    "Hendrawan", "Heryanto", "Hidayanto", "Indarto", "Indrawan", "Irawan",
    "Iskandar", "Iswanto", "Jayadi", "Julianto", "Kartono", "Kristanto",
    "Kurniadi", "Laksmana", "Laksono", "Lukito", "Mahardika", "Mardianto",
    "Mardiyanto", "Martoyo", "Mulyanto", "Mulyono", "Nainggolan", "Nugraha",
    "Nurdin", "Oktaviano", "Pamudji", "Pangaribuan", "Pradipta", "Pramana",
    "Pramono", "Pranata", "Pranoto", "Priyanto", "Priyono", "Purnama",
    "Purwanto", "Putranto", "Rachman", "Rahmanto", "Riyadi", "Rukmana",
    "Ruslan", "Rustam", "Sabirin", "Saefudin", "Saefullah", "Saleh",
    "Sanjaya", "Santosa", "Saputro", "Saptono", "Siswanto", "Soemarno",
    "Soeprapto", "Subroto", "Sudarmanto", "Sudarmono", "Sudarno", "Sugiarto",
    "Suhadi", "Suhardjo", "Suharyanto", "Sukmawan", "Sumantri", "Sunarko",
    "Suprayitno", "Supriyono", "Suryono", "Sutarto", "Sutedja", "Sutomo",
    "Suwardi", "Suwarto", "Suyono", "Syafruddin", "Thamrin", "Triadi",
    "Triyono", "Wahyono", "Wahyudin", "Wardana", "Warsono", "Wibisono",
    "Widayat", "Widiyanto", "Widjaja", "Widjojo", "Winarto", "Wirawan",
    "Wiyono", "Yulianto", "Yunarto", "Zaelani", "Zulkarnain", "Zulkarnaen"
]

# Nama tunggal pria (100+ names) - for regions that use single names
NAMA_TUNGGAL_PRIA: List[str] = [
    "Sukarno", "Suharto", "Habibie", "Sudirman", "Sudharmono", "Sumitro",
    "Suyanto", "Supomo", "Suparjo", "Sutomo", "Purnomo", "Purnawan", "Hartanto",
    "Slamet", "Sugeng", "Surono", "Sarwono", "Sarbini", "Parman", "Parno",
    # Extended single names
    "Adiono", "Agustono", "Ahmadi", "Ajiono", "Ananto", "Andono", "Ariyanto",
    "Bambang", "Basono", "Budiono", "Cahyono", "Darmono", "Darsono", "Djoko",
    "Eko", "Endro", "Giyanto", "Giyono", "Gunadi", "Guntoro", "Hadiono",
    "Handoyo", "Hariadi", "Hartomo", "Haryono", "Hendro", "Hermanto",
    "Ismoyo", "Iswanto", "Jumianto", "Karsono", "Karyono", "Kasino",
    "Kuntoro", "Mardianto", "Margono", "Maryono", "Marsono", "Maryanto",
    "Muhadi", "Mujiono", "Mulyono", "Murjono", "Naryono", "Ngadiman",
    "Ngadino", "Nyono", "Paiman", "Paimin", "Paino", "Paryono",
    "Poniman", "Ponimin", "Poniran", "Prasetyo", "Prayitno", "Purwadi",
    "Purwanto", "Rahardjo", "Rahmadi", "Riyadi", "Riyanto", "Rubiyanto",
    "Rusdi", "Rustamaji", "Sadiman", "Sadino", "Saiman", "Sakiman",
    "Samino", "Samiyono", "Samsuri", "Sandiyo", "Sardi", "Sardjono",
    "Sariman", "Sarmidi", "Sarmini", "Sarno", "Sastro", "Satimin",
    "Sawino", "Sayono", "Siswoyo", "Slamet", "Soeharto", "Soemarno",
    "Soepardi", "Soeparto", "Soetarno", "Soewardi", "Subardi", "Sudarmo",
    "Sudarsono", "Sudjono", "Sugino", "Sugiono", "Sugito", "Suhadi",
    "Suhardjo", "Suharno", "Sujadi", "Sujoko", "Sukamto", "Sukardi",
    "Sukiman", "Sukismo", "Sularto", "Sumadi", "Sumarno", "Sumarto",
    "Sumijo", "Sumitro", "Sunardi", "Sunarto", "Supardi", "Suparno",
    "Supriyadi", "Surahman", "Suradi", "Suranto", "Surono", "Suroso",
    "Susilo", "Sutarjo", "Sutarno", "Suwanto", "Suwardi", "Suwarto",
    "Suwito", "Timbul", "Trisno", "Tugiman", "Tugino", "Tugiyono",
    "Warjono", "Warno", "Warsidi", "Warsito", "Waryono", "Widodo",
    "Winardi", "Wiranto", "Wiryo", "Wiryono", "Wiyono", "Yatno", "Yatiman"
]

# Nama tunggal wanita (100+ names)
NAMA_TUNGGAL_WANITA: List[str] = [
    "Sukarni", "Sulastri", "Sumiati", "Sumiyati", "Supriyati", "Suharti",
    "Suhartini", "Suprapti", "Suparti", "Pariyem", "Parinem", "Wagiyem",
    "Wagini", "Tumini", "Tuminah", "Poniyem", "Painah", "Murtini", "Muryani",
    # Extended single names
    "Aminah", "Amini", "Asih", "Asiyah", "Atun", "Budiyah", "Daliyem",
    "Dami", "Dariyah", "Darmi", "Darsinah", "Darwati", "Dasiyem", "Dasmi",
    "Endang", "Gemi", "Ginem", "Giyanti", "Giyem", "Harti", "Hartini",
    "Haryati", "Ijah", "Inem", "Ipah", "Isah", "Iyah", "Jamilah",
    "Jasmini", "Jumilah", "Jumini", "Jumiyati", "Karsini", "Kasemi",
    "Kasiyah", "Kasmini", "Kasmiyati", "Kati", "Katini", "Katiyem",
    "Kuswanti", "Lastri", "Leginem", "Legiyah", "Marinem", "Marinah",
    "Mariyah", "Mariyem", "Markamah", "Maryati", "Maryatun", "Minem",
    "Minten", "Mujiyem", "Mujiati", "Mulyati", "Murni", "Mursidah",
    "Mursinah", "Murtini", "Narsih", "Narsiyem", "Ngademi", "Ngadinah",
    "Ngadiyem", "Ngatinah", "Ngatini", "Ngatiyem", "Ngatmi", "Ngesti",
    "Nuryati", "Parijah", "Parini", "Pariyah", "Ponijah", "Poniti",
    "Ratiyem", "Ratmi", "Rubiyah", "Rubiyem", "Rubiyati", "Rumini",
    "Rusiyem", "Rustini", "Sakem", "Sakiyah", "Sakinem", "Sami",
    "Saminah", "Samini", "Sanikem", "Sarini", "Sariyah", "Sariyem",
    "Saryati", "Satiyem", "Sayem", "Siami", "Sijem", "Sikem",
    "Sinah", "Sinem", "Siti", "Siwen", "Siyem", "Sriati",
    "Sugiyem", "Sugiyati", "Sukiyah", "Sukiyem", "Sulami", "Sulasmini",
    "Sularti", "Sulikah", "Suliyah", "Sumarsih", "Sumarni", "Sumartini",
    "Sumini", "Sumiyem", "Sunarti", "Sundari", "Sunarti", "Suparmi",
    "Supiyah", "Suprihatin", "Supriyati", "Suranti", "Suratmi", "Suratni",
    "Suriyem", "Suryati", "Sutarmi", "Sutini", "Sutiyem", "Suwanti",
    "Suwarsih", "Suyanti", "Suyatmi", "Tarmi", "Tarwiyah", "Taryati",
    "Tugiyem", "Tugini", "Tukinah", "Tukinah", "Tumilah", "Turiyah",
    "Tursinah", "Tusiyem", "Tusilah", "Waginah", "Wagiyah", "Warsini",
    "Warsiyah", "Wartini", "Widiyanti", "Wiji", "Wijiati", "Yatinah",
    "Yatinem", "Yatmi", "Yatmi", "Yatun", "Yem", "Yuni", "Yuniyati"
]

# ============================================================================
# NAMA BERDASARKAN AGAMA (Religion-based Names)
# ============================================================================

# Islam - Nama bernuansa Arab/Islam (300+ names)
NAMA_ISLAM_PRIA: List[str] = [
    # Nama Nabi & Sahabat
    "Muhammad", "Ahmad", "Mahmud", "Hamid", "Mustafa", "Mukhtar", "Muhsin",
    "Ali", "Umar", "Usman", "Hasan", "Husein", "Ibrahim", "Ismail", "Ishaq",
    "Yusuf", "Yakub", "Musa", "Harun", "Isa", "Daud", "Sulaiman", "Ayyub",
    "Yunus", "Ilyas", "Ilyasa", "Dzulkifli", "Zakariya", "Yahya", "Idris",
    "Nuh", "Hud", "Shaleh", "Luth", "Syuaib", "Adam", "Abubakar", "Bilal",
    # Nama -din
    "Zainuddin", "Nuruddin", "Fakhruddin", "Syamsuddin", "Tajuddin", "Bahauddin",
    "Saifuddin", "Alauddin", "Jamaluddin", "Kamaluddin", "Nizamuddin", "Nashiruddin",
    "Jalaluddin", "Shihabuddin", "Imaduddin", "Muhyiddin", "Taqiyuddin", "Izzuddin",
    "Badruddin", "Nashruddin", "Shamsuddin", "Mujahiddin", "Waliuddin", "Saaduddin",
    # Nama -llah
    "Abdullah", "Abdurrahman", "Abdulaziz", "Abdurahim", "Abdulmalik", "Abdulkarim",
    "Abdulhalim", "Abdulhadi", "Abdulwahab", "Abdullatif", "Abdulghani", "Abdulghofur",
    "Abdulmajid", "Abdulfattah", "Abdulqodir", "Abdulsalam", "Abdulhakim", "Abdulwahid",
    "Hidayatullah", "Rahmatullah", "Habibullah", "Saifullah", "Nasrullah", "Fadhlullah",
    "Akhirullah", "Hizbullah", "Nurullah", "Aminullah", "Ruhullah", "Khalilullah",
    # Nama umum Islam
    "Arifin", "Hidayat", "Rahmat", "Ridwan", "Taufik", "Taufiq", "Maulana",
    "Muchlis", "Mukti", "Fajar", "Fajri", "Fadil", "Fadhil", "Fadlan", "Fahmi",
    "Faisal", "Farhan", "Faris", "Fikri", "Fuad", "Ghani", "Ghofur", "Hafiz",
    "Hakim", "Halim", "Hamid", "Hanif", "Haris", "Hasbi", "Ikram", "Ilham",
    "Irfan", "Iqbal", "Ihsan", "Ikhsan", "Jafar", "Jamil", "Khoirul", "Khairul",
    "Lutfi", "Mahdi", "Malik", "Mansur", "Mukhlis", "Munir", "Nabil", "Nadhif",
    "Nafis", "Najib", "Nasir", "Naufal", "Qodir", "Rafi", "Rafiq", "Raihan",
    "Rasyid", "Ridho", "Rizki", "Sholeh", "Syafii", "Syahrul", "Syamsul",
    "Syarif", "Taqwa", "Wahid", "Wahyu", "Yazid", "Zaki", "Zainal", "Zulfan",
    "Zulfikar", "Zulkarnain", "Akbar", "Ashraf", "Azzam", "Bashir", "Burhan",
    "Dzaki", "Fakhri", "Ghazali", "Haidar", "Hamdan", "Harits", "Imran",
    "Ja'far", "Kamil", "Labib", "Maher", "Nashir", "Qais", "Rakan", "Sami",
    "Tariq", "Ubaid", "Walid", "Yasser", "Ziyad", "Anas", "Asad", "Ayman",
    "Bilal", "Dani", "Ehsan", "Farid", "Gibran", "Habib", "Iskandar", "Jawad",
    "Kamal", "Luqman", "Mahir", "Naim", "Omar", "Qasim", "Rashad", "Saad",
    "Tahir", "Usamah", "Wafi", "Yaman", "Zahir", "Adnan", "Bassam", "Darwish",
    "Elias", "Faiz", "Ghalib", "Hadi", "Idris", "Jamal", "Kareem", "Latif",
    "Mazin", "Nabeel", "Othman", "Qutaiba", "Raed", "Salim", "Tamim", "Usama",
    "Wassim", "Yasir", "Zubair", "Affan", "Bakr", "Daud", "Ezzat", "Fawaz",
    "Ghayth", "Hazim", "Ihab", "Jibril", "Khalil", "Laith", "Marwan", "Nader",
    "Osama", "Qusay", "Rami", "Saud", "Taha", "Uwais", "Wael", "Yahya",
    "Zain", "Abbas", "Baraka", "Dawud", "Emad", "Fahad", "Ghassan", "Hatim",
    "Imad", "Junaid", "Khaled", "Louay", "Murad", "Nawaf", "Obaid", "Qassem"
]

NAMA_ISLAM_WANITA: List[str] = [
    # Nama istri/putri Nabi
    "Aisyah", "Fatimah", "Khadijah", "Maryam", "Halimah", "Aminah", "Zainab",
    "Hafshah", "Ruqayah", "Ummu Kulsum", "Juwairiyah", "Shafiyyah", "Maimunah",
    "Sawdah", "Hindun", "Ramlah", "Zaynab", "Asma", "Sumayyah", "Khaulah",
    # Nama Nur-
    "Nur", "Nurul", "Nurhayati", "Nurjanah", "Nurhaliza", "Nurlela", "Nurmalasari",
    "Nurafni", "Nurasiah", "Nuraini", "Nurbaiti", "Nurdiana", "Nurelita", "Nurfadilah",
    "Nurgita", "Nurhidayah", "Nurika", "Nurjannah", "Nurkhalisa", "Nurlina",
    "Nurmala", "Nurnadia", "Nurpita", "Nurqolbi", "Nursafitri", "Nurtika",
    "Nurwahidah", "Nurzahra", "Nurazizah", "Nurbadriah", "Nurcahaya", "Nurdini",
    # Nama Siti-
    "Siti", "Siti Aisyah", "Siti Aminah", "Siti Fatimah", "Siti Hajar",
    "Siti Khadijah", "Siti Maryam", "Siti Nurhaliza", "Siti Rahayu", "Siti Sarah",
    "Siti Zahra", "Siti Zainab", "Siti Aminah", "Siti Badriah", "Siti Cholijah",
    # Nama umum Islam
    "Fitri", "Fitriani", "Fitriyah", "Zahra", "Zahrah", "Zakiah", "Zakiyah",
    "Ulfah", "Ulfa", "Azizah", "Hasanah", "Salamah", "Rahmah", "Rahma",
    "Rahmania", "Rahmawati", "Hidayah", "Mutiah", "Muthiah", "Latifah",
    "Badriah", "Kamilah", "Jamilah", "Syarifah", "Safitri", "Safira",
    "Shafira", "Nabila", "Nabilah", "Nadira", "Nafisa", "Naila", "Najwa",
    "Salma", "Salsabila", "Syifa", "Wafiq", "Wardah", "Yasmin", "Yusra",
    "Afifah", "Aini", "Ainun", "Aliyah", "Aqila", "Bilqis", "Balqis",
    "Fadhilah", "Fahira", "Fathimah", "Hanifah", "Husna", "Iffah", "Inayah",
    "Isnaini", "Khansa", "Laila", "Lutfiah", "Mahira", "Malika", "Mufidah",
    "Mursyidah", "Naura", "Qonita", "Raisya", "Raudhah", "Rifka", "Rizka",
    "Rumaisha", "Saidah", "Sakina", "Sakinah", "Sumayyah", "Aafia", "Abidah",
    "Adiba", "Afnan", "Aisha", "Akifa", "Alina", "Amani", "Amira", "Anisa",
    "Arwa", "Asiya", "Atika", "Ayesha", "Azra", "Bushra", "Daliya", "Dania",
    "Dina", "Duha", "Elham", "Farah", "Farida", "Fatin", "Ghaniya", "Habiba",
    "Hadiya", "Hafsa", "Haifa", "Hala", "Hamida", "Hana", "Haniya", "Hawa",
    "Hayfa", "Hibah", "Huda", "Inas", "Jannah", "Karima", "Lamia", "Lamis",
    "Lina", "Lubna", "Madiha", "Mahasin", "Maisara", "Majida", "Malak",
    "Mariam", "Marwa", "Maysun", "Muna", "Munira", "Nabihan", "Nada", "Nadiya",
    "Nahla", "Naima", "Nasreen", "Noor", "Noura", "Qamar", "Rania", "Rawda",
    "Rayhan", "Reem", "Ruqayyah", "Sabah", "Sabira", "Sahar", "Sakeena",
    "Samira", "Sana", "Sara", "Shadia", "Shakira", "Shamsa", "Siham",
    "Suha", "Tahira", "Tamara", "Taqiya", "Thana", "Warda", "Yara", "Yasira",
    "Yusra", "Zaida", "Zakia", "Zamzam", "Zara", "Zubaida", "Zulfa", "Zulaikha"
]

NAMA_BELAKANG_ISLAM: List[str] = [
    "Abdullah", "Ibrahim", "Ismail", "Hassan", "Hussein", "Malik", "Karim",
    "Salim", "Bakri", "Basri", "Fauzi", "Hamzah", "Mansur", "Rosyid", "Wahid",
    "Ramadhan", "Syahputra", "Maulana", "Anwar", "Hasan", "Hidayat", "Rahman",
    "Alatas", "Algadri", "Alhaddad", "Alhabsyi", "Assegaf", "Barakbah", "Bazher",
    "Syihab", "Shahab", "Shihab", "Jaelani", "Jailani", "Lubis", "Daulay",
    "Harahap", "Pulungan", "Batubara", "Rangkuti", "Pohan", "Nasution", "Siregar",
    "Tanjung", "Chaniago", "Piliang", "Fadillah", "Zulkarnain", "Syafruddin",
    "Nurdin", "Baharudin", "Amin", "Amir", "Ansari", "Azhari", "Bahri", "Djalil",
    "Djamil", "Effendi", "Fadhil", "Fikri", "Ghazali", "Habib", "Hafidzh",
    "Haikal", "Hakiki", "Hamdi", "Hanafi", "Idris", "Ihsan", "Ilyas", "Imran",
    "Jamil", "Kamil", "Karim", "Latif", "Mahdi", "Majid", "Mubarok", "Mubarak",
    "Muhaimin", "Muhajir", "Mukmin", "Munawir", "Muqorrobin", "Mustofa", "Mutakin",
    "Muzakir", "Nabhan", "Nashir", "Qomar", "Qudsi", "Rasyidi", "Salam", "Salman",
    "Soleh", "Subhan", "Sultoni", "Syukur", "Tholib", "Ulwan", "Usman", "Yusuf",
    "Zaini", "Zubair", "Zuhdi", "Habibi", "Rifa'i", "Dimyati", "Ghofar"
]

# Kristen - Nama bernuansa Kristen/Biblika (200+ names)
NAMA_KRISTEN_PRIA: List[str] = [
    # Nama Alkitab
    "Yohanes", "Petrus", "Paulus", "Yakobus", "Andreas", "Filipus", "Tomas",
    "Matius", "Barnabas", "Stefanus", "Timotius", "Titus", "Lukas", "Markus",
    "Daniel", "Samuel", "David", "Salomo", "Elias", "Elisa", "Natanael",
    "Simon", "Kornelius", "Lazarus", "Zakheus", "Nehemia", "Ezra", "Yosua",
    "Kaleb", "Gideon", "Simson", "Boas", "Rut", "Obed", "Yesse", "Yonatan",
    "Absalom", "Yoab", "Abner", "Benyamin", "Ruben", "Levi", "Yehuda", "Zebulon",
    "Asyer", "Dan", "Naftali", "Gad", "Manasye", "Efraim", "Yobel", "Abel",
    # Nama Barat/Kristen umum
    "Christian", "Christopher", "Joshua", "Jonathan", "Michael", "Gabriel",
    "Rafael", "Emmanuel", "Immanuel", "Kevin", "Steven", "Stephen", "Andrew",
    "Anthony", "Benjamin", "Caleb", "Elijah", "Ezra", "Felix", "George",
    "Henry", "Isaac", "Jacob", "Jason", "Joel", "John", "Joseph", "Justin",
    "Kenneth", "Levi", "Lucas", "Mark", "Matthew", "Nathan", "Nicholas",
    "Noah", "Oliver", "Patrick", "Paul", "Peter", "Philip", "Raymond",
    "Richard", "Robert", "Samuel", "Sebastian", "Thomas", "Timothy", "Victor",
    "William", "Yosef", "Aaron", "Adam", "Adrian", "Alan", "Albert", "Alex",
    "Alfred", "Allen", "Arnold", "Arthur", "Bernard", "Brandon", "Brian",
    "Bruce", "Bryan", "Carl", "Charles", "Chris", "Clarence", "Colin",
    "Connor", "Craig", "Curtis", "Dale", "Danny", "Darren", "Dean", "Dennis",
    "Derek", "Dominic", "Donald", "Douglas", "Dylan", "Edgar", "Edward",
    "Edwin", "Eric", "Ernest", "Eugene", "Evan", "Francis", "Frank", "Fred",
    "Gary", "Gerald", "Glenn", "Gordon", "Graham", "Gregory", "Harold",
    "Harry", "Howard", "Hugh", "Ian", "Ivan", "Jack", "James", "Jeffrey",
    "Jeremy", "Jerome", "Jesse", "Jimmy", "Joe", "Johnny", "Jordan", "Josh",
    "Keith", "Kelly", "Kent", "Kyle", "Larry", "Lawrence", "Leonard", "Leon",
    "Leslie", "Lewis", "Lloyd", "Louis", "Malcolm", "Marcus", "Martin",
    "Maurice", "Max", "Melvin", "Milton", "Morris", "Neil", "Nelson",
    "Norman", "Oscar", "Owen", "Percy", "Perry", "Ralph", "Randy", "Ray",
    "Reginald", "Rex", "Rodney", "Roger", "Roland", "Ronald", "Ross", "Roy",
    "Russel", "Ryan", "Scott", "Shane", "Sidney", "Stanley", "Stuart",
    "Ted", "Terrance", "Terry", "Theodore", "Tony", "Travis", "Trevor",
    "Vincent", "Walter", "Warren", "Wayne", "Wesley", "Wilbur", "Willis",
    # Nama Latin/Katolik
    "Adrianus", "Albertus", "Alexander", "Antonius", "Benediktus", "Cornelius",
    "Dominikus", "Fransiskus", "Gregorius", "Hieronimus", "Ignatius", "Xaverius"
]

NAMA_KRISTEN_WANITA: List[str] = [
    # Nama Alkitab
    "Maria", "Elisabeth", "Marta", "Magdalena", "Rut", "Ester", "Debora",
    "Sarah", "Hana", "Rahel", "Lea", "Rebeka", "Naomi", "Priskila", "Tabita",
    "Lidia", "Eunika", "Dina", "Tamar", "Delila", "Yael", "Hagar", "Zilpa",
    "Bilha", "Ketura", "Yiska", "Milka", "Tikwa", "Hulda", "Miriam", "Zippora",
    # Nama Barat/Kristen umum
    "Christine", "Christina", "Grace", "Faith", "Hope", "Joy", "Charity",
    "Angela", "Angelina", "Angelica", "Catherine", "Cecilia", "Clara",
    "Dorothy", "Eleanor", "Emily", "Eva", "Evelyn", "Gloria", "Hannah",
    "Helena", "Irene", "Jessica", "Joanna", "Judith", "Julia", "Karen",
    "Katherine", "Laura", "Linda", "Lydia", "Margaret", "Martha", "Mary",
    "Michelle", "Monica", "Nancy", "Natalie", "Olivia", "Patricia",
    "Priscilla", "Rachel", "Rebecca", "Regina", "Rosa", "Rosalinda", "Ruth",
    "Sandra", "Stephanie", "Susan", "Susanna", "Teresa", "Theresa",
    "Victoria", "Virginia", "Abigail", "Adelaide", "Agnes", "Alice", "Alicia",
    "Amanda", "Amy", "Andrea", "Anna", "Anne", "Audrey", "Barbara", "Beatrice",
    "Betty", "Beverly", "Bonnie", "Brenda", "Bridget", "Carol", "Caroline",
    "Carolyn", "Cathy", "Charlotte", "Cheryl", "Cindy", "Claudia", "Colleen",
    "Connie", "Constance", "Crystal", "Cynthia", "Daisy", "Dana", "Danielle",
    "Darlene", "Dawn", "Debbie", "Deborah", "Denise", "Diana", "Diane",
    "Dolores", "Donna", "Doris", "Edith", "Edna", "Eileen", "Elaine", "Eliza",
    "Ellen", "Elsie", "Emma", "Esther", "Ethel", "Eunice", "Florence", "Frances",
    "Geraldine", "Gertrude", "Gina", "Gladys", "Glenda", "Gwendolyn", "Harriet",
    "Hazel", "Heather", "Helen", "Holly", "Ida", "Irma", "Isabel", "Jacqueline",
    "Jane", "Janet", "Janice", "Jean", "Jeanette", "Jennifer", "Jenny", "Jill",
    "Joan", "Joanne", "Josephine", "Joyce", "Judy", "June", "Karin", "Kate",
    "Kathleen", "Kathryn", "Katie", "Kay", "Kelly", "Kim", "Kimberly", "Kristen",
    "Kristin", "Lauren", "Leslie", "Lillian", "Lisa", "Lois", "Loretta",
    "Lorna", "Lorraine", "Louise", "Lucille", "Lucy", "Lynn", "Mabel", "Madeleine",
    "Mae", "Marcia", "Marian", "Marie", "Marilyn", "Marion", "Marjorie",
    "Marlene", "Marsha", "Maryann", "Maureen", "Maxine", "Megan", "Melanie",
    "Melissa", "Meredith", "Mildred", "Minnie", "Miriam", "Molly", "Muriel",
    "Myrtle", "Nadine", "Nell", "Nicole", "Nina", "Nora", "Norma", "Pamela",
    "Paula", "Pauline", "Pearl", "Peggy", "Penny", "Phyllis", "Rachael",
    "Ramona", "Renee", "Rhonda", "Rita", "Roberta", "Robin", "Rosemary",
    "Sally", "Samantha", "Sara", "Sharon", "Sheila", "Sherry", "Shirley",
    "Sophia", "Stacy", "Stella", "Sue", "Suzanne", "Sylvia", "Tamara", "Tammy",
    "Tanya", "Thelma", "Tiffany", "Tracy", "Valerie", "Vanessa", "Vera",
    "Veronica", "Vicky", "Viola", "Violet", "Vivian", "Wanda", "Wendy",
    "Whitney", "Wilma", "Yolanda", "Yvonne", "Anastasia", "Benedikta"
]

NAMA_BELAKANG_KRISTEN: List[str] = [
    # Marga Batak Toba
    "Simanjuntak", "Simbolon", "Hutabarat", "Panjaitan", "Manullang",
    "Situmorang", "Tampubolon", "Sirait", "Sinaga", "Turnip", "Siagian",
    "Napitupulu", "Pardede", "Purba", "Silalahi", "Sihombing", "Simatupang",
    "Tamba", "Tarigan", "Tobing", "Aritonang", "Butar-Butar", "Sitorus",
    "Siahaan", "Lumban", "Marpaung", "Nainggolan", "Pangaribuan", "Hutagalung",
    "Hutapea", "Hutasoit", "Hutauruk", "Manurung", "Nababan", "Pakpahan",
    "Pasaribu", "Rajagukguk", "Sagala", "Samosir", "Saragih", "Sidabalok",
    "Sidabutar", "Sibagariang", "Sibuea", "Siburian", "Sidauruk", "Sihaloho",
    "Sijabat", "Silaban", "Simangunsong", "Simorangkir", "Sinambela", "Sipayung",
    "Sitanggang", "Sitio", "Situmeang", "Sormin", "Tambunan", "Togatorop",
    # Marga Batak Karo
    "Ginting", "Sembiring", "Karo", "Perangin-angin", "Bangun", "Barus",
    "Brahmana", "Depari", "Keliat", "Milala", "Munte", "Pinem", "Sitepu",
    "Sebayang", "Sinulingga", "Tarigan", "Tendang", "Meliala", "Kaban",
    # Marga Batak Simalungun
    "Damanik", "Saragih", "Sinaga", "Purba", "Girsang",
    # Marga Batak Mandailing/Angkola
    "Lubis", "Nasution", "Harahap", "Siregar", "Daulay", "Pulungan",
    "Batubara", "Rangkuti", "Dalimunthe", "Matondang", "Hasibuan", "Rambe"
]

# Katolik - Nama Santo/Santa (200+ names)
NAMA_KATOLIK_PRIA: List[str] = [
    # Santo-santo terkenal
    "Yohanes", "Petrus", "Paulus", "Fransiskus", "Antonius", "Dominikus",
    "Ignatius", "Xaverius", "Benediktus", "Gregorius", "Augustinus", "Thomas",
    "Albertus", "Bernardus", "Bonifatius", "Cornelius", "Damianus", "Eduardus",
    "Feliks", "Gerardus", "Hieronimus", "Jacobus", "Josephus", "Laurentius",
    "Ludovikus", "Martinus", "Nikolaus", "Patricius", "Pius", "Robertus",
    "Sebastianus", "Stefanus", "Valentinus", "Vincentius", "Adrianus", "Alexius",
    "Amadeus", "Ambrosius", "Andreas", "Bartholomeus", "Caelestinus", "Carolus",
    "Christophorus", "Clemens", "Damaskus", "Didakus", "Emmanuel", "Eugenius",
    "Ferdinandus", "Florentinus", "Gabriel", "Henrikus", "Hubertus", "Hugo",
    "Johannes", "Julius", "Leo", "Lucas", "Marcus", "Matheus", "Maximilianus",
    "Michael", "Pascalis", "Philippus", "Raimundus", "Raphael", "Theodorus",
    # Nama Latin tambahan
    "Aloysis", "Anastasius", "Anselmus", "Athanasius", "Aurelius", "Basilius",
    "Bruno", "Caietanus", "Camillus", "Casimirus", "Cyrillus", "Dionisius",
    "Erasmus", "Fabianus", "Faustinus", "Fidelis", "Flavianus", "Franciscus",
    "Fulgentius", "Gallus", "Germanus", "Godefridus", "Gratianus", "Gregorius",
    "Guido", "Guillelmus", "Hadrianus", "Honoratus", "Hormisdas", "Hyacinthus",
    "Irenaeus", "Isidorus", "Januarius", "Joachimus", "Julianus", "Justinus",
    "Lambertus", "Laurus", "Lazarus", "Leander", "Leonardus", "Longinus",
    "Lotharius", "Lucianus", "Malachias", "Marcellinus", "Marcellus", "Marianus",
    "Mauritius", "Methodius", "Modestus", "Narcissus", "Nazarius", "Nicodemus",
    "Norbertus", "Odilo", "Optatus", "Pancratius", "Paulinus", "Peregrinus",
    "Polycarpus", "Prosper", "Quirinus", "Radulfus", "Remigius", "Richardus",
    "Romanus", "Romualdus", "Rufinus", "Rupertus", "Sabinus", "Sergius",
    "Severinus", "Silvanus", "Silverius", "Silvester", "Simplicius", "Sixtus",
    "Stanislaus", "Tarcisius", "Telesphorus", "Tertullianus", "Timotheus",
    "Urbanus", "Valerius", "Venantius", "Vigilius", "Vitalis", "Wenceslaus",
    "Wolfgangus", "Zacharias", "Zenobius", "Zephyrinus", "Aloysius", "Cassius"
]

NAMA_KATOLIK_WANITA: List[str] = [
    # Santa-santa terkenal
    "Maria", "Theresia", "Bernadette", "Katharina", "Margaretha", "Elisabeth",
    "Agnes", "Anna", "Barbara", "Brigitta", "Caecilia", "Clara", "Dorothea",
    "Felicitas", "Francisca", "Gratia", "Helena", "Ignatia", "Johanna",
    "Josephina", "Klara", "Lucia", "Ludovica", "Magdalena", "Monica", "Natalia",
    "Patricia", "Paula", "Regina", "Rosa", "Scholastika", "Sophia", "Ursula",
    "Veronica", "Virginia", "Adelheid", "Anastasia", "Angela", "Benedikta",
    "Brigida", "Carmela", "Christina", "Claudia", "Constantia", "Cornelia",
    "Dominica", "Editha", "Euphemia", "Gabriela", "Gertrude", "Hildegard",
    "Immaculata", "Juliana", "Laurentia", "Martina", "Michaela", "Perpetua",
    "Philomena", "Rafaela", "Seraphina",
    # Nama Latin tambahan
    "Adela", "Adelaide", "Adriana", "Agatha", "Alberta", "Albina", "Alexandra",
    "Alma", "Amalia", "Amata", "Angelica", "Antonia", "Apollonia", "Augusta",
    "Aurelia", "Beatrix", "Benedicta", "Bianca", "Blandina", "Candida",
    "Caritas", "Carlotta", "Carmelita", "Casilda", "Catherina", "Coletta",
    "Columba", "Conrada", "Consolata", "Cordelia", "Crescentia", "Daria",
    "Diana", "Donata", "Emerentiana", "Eugenia", "Eulalia", "Fabiana",
    "Faustina", "Fidelia", "Flavia", "Flora", "Florentina", "Fortunata",
    "Gemma", "Genoveva", "Gianna", "Gisela", "Gregoria", "Hedwig", "Henrietta",
    "Honoria", "Ignatia", "Ines", "Irma", "Jacinta", "Januaria", "Jolanda",
    "Jovita", "Julitta", "Justina", "Laetitia", "Lea", "Leona", "Leonora",
    "Libera", "Livia", "Louisa", "Luciana", "Luisa", "Lydia", "Madeleine",
    "Marcella", "Margarita", "Marianna", "Marita", "Mathilda", "Maxima",
    "Melania", "Modesta", "Monika", "Narcisa", "Nicola", "Octavia", "Oliva",
    "Olympia", "Ottilia", "Pascuala", "Petronella", "Pia", "Prisca", "Renata",
    "Ricarda", "Rosalia", "Rosaria", "Rosina", "Rufina", "Sabina", "Salome",
    "Sebastiana", "Serena", "Simona", "Solangia", "Susanna", "Symphorosa",
    "Tarsicia", "Tatiana", "Thea", "Theodora", "Valentina", "Vincentia",
    "Walburga", "Xaviera", "Zenobia", "Zita", "Zosima", "Bertha", "Blanche"
]

NAMA_BELAKANG_KATOLIK: List[str] = [
    # Marga Batak
    "Simanjuntak", "Simbolon", "Hutabarat", "Panjaitan", "Manullang",
    "Situmorang", "Tampubolon", "Sirait", "Sinaga", "Siagian", "Napitupulu",
    "Pardede", "Purba", "Silalahi", "Sihombing", "Tarigan", "Tobing",
    "Aritonang", "Ginting", "Sembiring", "Nainggolan", "Pangaribuan",
    # Nama Portugis/Timor (banyak Katolik)
    "Da Costa", "De Fretes", "De Lima", "Dos Santos", "Fernandes", "Gomes",
    "Lopez", "Martins", "Pereira", "Rodrigues", "Silva", "Soares", "Carvalho",
    "De Araujo", "De Jesus", "De Oliveira", "De Souza", "Freitas", "Goncalves",
    "Henriques", "Lopes", "Mendes", "Monteiro", "Nunes", "Pinto", "Ramos",
    "Ribeiro", "Santos", "Tavares", "Teixeira", "Vieira", "Almeida", "Andrade",
    "Baptista", "Correia", "Da Conceicao", "Da Luz", "Da Silva", "De Deus",
    "Maia", "Marques", "Nogueira", "Piedade", "Reis", "Rosario", "Xavier"
]

# Hindu - Nama bernuansa Bali/Hindu (200+ names)
NAMA_HINDU_PRIA: List[str] = [
    # Nama urutan kelahiran Bali
    "Wayan", "Made", "Nyoman", "Ketut", "Putu", "Kadek", "Komang", "Gede",
    "Nengah", "Iluh", "Luh",
    # Gelar/Kasta Bali
    "Agung", "Bagus", "Dewa", "Gusti", "Ngurah", "Anak", "Cokorda", "Ida",
    "Anak Agung", "I Gusti", "I Dewa", "Tjokorda", "I Gede", "I Made",
    "I Nyoman", "I Ketut", "I Wayan", "I Kadek", "I Komang", "I Putu",
    # Nama Pewayangan/Mitologi
    "Arjuna", "Bima", "Yudhistira", "Nakula", "Sadewa", "Kresna", "Rama",
    "Wisnu", "Brahma", "Siwa", "Ganesha", "Indra", "Surya", "Bayu", "Durga",
    "Hanoman", "Gatotkaca", "Abimanyu", "Parikesit", "Bhisma", "Drona",
    "Karna", "Duryudana", "Srikandi", "Dewi Kunti", "Dewi Gandari",
    # Nama bernuansa Sanskerta
    "Dharma", "Darma", "Satya", "Yoga", "Yadnya", "Widya", "Chandra",
    "Purnama", "Sukma", "Tirta", "Weda", "Puja", "Pande", "Pasek", "Dalem",
    "Kubayan", "Tangkas", "Bandesa", "Jero", "Mangku", "Pemangku", "Pedanda",
    "Arya", "Bharata", "Darmika", "Eka", "Gana", "Hari", "Jati", "Kala",
    "Laksana", "Maha", "Naga", "Paramartha", "Raka", "Soma", "Teja", "Udayana",
    "Vajra", "Wardana", "Yasa", "Ananda", "Bhaskara", "Cakra", "Danendra",
    "Ekaputra", "Girideva", "Harsha", "Isana", "Jayendra", "Kalidasa",
    "Laksmana", "Madhava", "Narada", "Omkara", "Pradnya", "Ratnadeva",
    "Sadhana", "Tantra", "Uttama", "Vedanta", "Waisya", "Yadava", "Aditya",
    "Bhagavan", "Chakra", "Devendra", "Ekadasa", "Govinda", "Harindra",
    "Ishwara", "Jagannath", "Kalpataru", "Lokendra", "Mahendra", "Narendra",
    "Parameshwara", "Raghava", "Sahadeva", "Trisna", "Upendra", "Vikrama"
]

NAMA_HINDU_WANITA: List[str] = [
    # Nama urutan/gelar Bali
    "Ni", "Ayu", "Luh", "Desak", "Dayu", "Sagung", "Gusti", "Anak",
    "Ni Luh", "Ni Made", "Ni Nyoman", "Ni Ketut", "Ni Wayan", "Ni Kadek",
    "Ni Komang", "Ni Putu", "A.A.", "Anak Agung", "Dewa Ayu", "Ida Ayu",
    # Nama Dewi/Mitologi
    "Sri", "Dewi", "Devi", "Shakti", "Saraswati", "Lakshmi", "Durga",
    "Gayatri", "Sita", "Radha", "Parvati", "Uma", "Ganga", "Yamuna",
    "Padma", "Ratih", "Sukma", "Shanti", "Prema", "Bhakti", "Candra",
    "Purnama", "Putri", "Galuh", "Citra", "Mega", "Bintang", "Cahya", "Sari",
    "Kirana", "Puspa", "Melati", "Seruni", "Mawar", "Cempaka", "Kenanga",
    "Anggrek", "Wijaya", "Pratiwi", "Utami", "Lestari", "Pertiwi", "Karunia",
    # Nama Sanskerta
    "Ananda", "Bhavani", "Chandra", "Damayanti", "Devika", "Gauri", "Hema",
    "Indira", "Janaki", "Kamala", "Lalita", "Malini", "Nandini", "Padmini",
    "Rani", "Savitri", "Tara", "Usha", "Vasanti", "Yasoda", "Ambika",
    "Bhairavi", "Champa", "Dharini", "Ekta", "Gita", "Harini", "Ishani",
    "Jayanti", "Kalpana", "Lavanya", "Madhuri", "Nalini", "Pallavi",
    "Ragini", "Shobha", "Tripura", "Urmila", "Vani", "Yamini", "Aruna",
    "Bhanu", "Chitra", "Dipti", "Esha", "Girija", "Himani", "Indrani",
    "Jyoti", "Kaveri", "Leela", "Meenakshi", "Nirmala", "Priya", "Rekha",
    "Sumitra", "Tanuja", "Urvashi", "Vidya", "Yashoda", "Ambuja", "Bindiya"
]

NAMA_BELAKANG_HINDU: List[str] = [
    "Putra", "Kusuma", "Wijaya", "Dharma", "Darma", "Karma", "Surya",
    "Chandra", "Purnama", "Sukma", "Tirta", "Weda", "Puja", "Pranata",
    "Atmaja", "Jaya", "Sakti", "Darmawan", "Suryawan", "Indrayana",
    "Adnyana", "Aryawan", "Bagaskara", "Citrapati", "Danendra", "Ekaputra",
    "Girinata", "Harsananda", "Iswaradeva", "Jayaningrat", "Kamadhatu",
    "Laksanabumi", "Mahardika", "Narendrapati", "Paramitha", "Rajendra",
    "Satyabhakti", "Tejapati", "Udayana", "Wedadharma", "Yudistira",
    "Abhimanyu", "Baladewa", "Candradiputra", "Darmayasa", "Gangga",
    "Mayura", "Kesuma", "Sanjaya", "Bhaskara", "Madhava", "Narayana"
]

# Buddha - Nama bernuansa Tionghoa/Buddha (200+ names)
NAMA_BUDDHA_PRIA: List[str] = [
    # Nama Indonesia-Tionghoa
    "Susanto", "Wijaya", "Hartono", "Gunawan", "Sutrisno", "Suryanto",
    "Kurniawan", "Santoso", "Wibowo", "Hendra", "Hendri", "Benny", "Denny",
    "Budi", "Rudy", "Eddy", "Teddy", "Freddy", "Andy", "Sanjaya", "Dharma",
    "Bodhi", "Raharja", "Rahardja", "Jaya", "Setia", "Wijanto", "Sugianto",
    "Sugiarto", "Sutanto", "Sutejo", "Suwanto", "Suwandi", "William",
    "Vincent", "Steven", "Kevin", "Eric", "Edwin", "Edward", "Albert",
    "Christianto", "Handoko", "Sudargo", "Sudirgo", "Tandiono", "Tanuwidjaja",
    "Tanusaputra", "Tjahjadi", "Wongso", "Yuwono", "Lauwanto", "Liauw",
    # Marga/Nama Tionghoa
    "Lim", "Tan", "Ong", "Koh", "Tio", "Lie", "Oey", "The", "Go", "Kwik",
    "Kwee", "Ang", "Chua", "Gan", "Goh", "Ho", "Hoo", "Kho", "Kim", "Lee",
    "Leong", "Lew", "Liong", "Low", "Ng", "Pang", "Phua", "Poh", "Sia",
    "Sim", "Sio", "Siow", "Tang", "Tay", "Teo", "Thio", "Tjia", "Tjong",
    "Wong", "Yap", "Yeo", "Yeoh", "Wee", "Teh", "Chong", "Lau", "Chen",
    "Loh", "Chuang", "Chew", "Chai", "Loke", "Phang", "Yong", "Koay",
    # Nama Buddha/Pali
    "Siddhartha", "Gotama", "Ananda", "Rahula", "Moggallana", "Sariputta",
    "Kassapa", "Upali", "Anuruddha", "Mahakassapa", "Sumedha", "Sujata",
    "Vipassi", "Sikhi", "Vessabhu", "Kakusandha", "Konagamana", "Dipankara",
    # Nama modern
    "Jason", "Justin", "Jeremy", "Jeffrey", "Jonathan", "Jordan", "Joshua",
    "Kenneth", "Leonard", "Lawrence", "Martin", "Nicholas", "Patrick",
    "Richard", "Raymond", "Ronald", "Stanley", "Stephen", "Thomas", "Victor"
]

NAMA_BUDDHA_WANITA: List[str] = [
    # Nama Indonesia-Tionghoa
    "Lianawati", "Susanti", "Yuliana", "Yuliani", "Yunita", "Indrawati",
    "Wati", "Sari", "Dewi", "Lina", "Tina", "Rina", "Sinta", "Linda",
    "Yanti", "Yenny", "Jenny", "Fenny", "Henny", "Melly", "Kelly", "Sally",
    "Nancy", "Cindy", "Wendy", "Windy", "Mandy", "Sandy", "Lily", "Shirley",
    "Sherly", "Sherlyn", "Celine", "Michelle", "Christine", "Christina",
    "Cecilia", "Caroline", "Catherine", "Felicia", "Melissa", "Patricia",
    "Jessica", "Natalie", "Stephanie", "Angeline", "Evangeline", "Jacqueline",
    "Josephine", "Katherine", "Madeleine", "Geraldine", "Bernadette", "Antoinette",
    # Nama Tionghoa
    "Mei", "Mei Ling", "Mei Lan", "Mei Hui", "Mei Fang", "Li Hua", "Xiao Mei",
    "Xiao Ling", "Xiao Hui", "Xiao Fang", "Hui Ling", "Hui Lan", "Siu Mei",
    "Siu Lan", "Ai Ling", "Ai Mei", "Bao Zhu", "Bao Ling", "Bao Yu",
    "Chen", "Cui", "Dan", "Fang", "Fen", "Hong", "Hua", "Jia", "Jing",
    "Juan", "Lan", "Li", "Lian", "Lin", "Ling", "Min", "Ming", "Na",
    "Ning", "Ping", "Qing", "Rong", "Shan", "Shu", "Ting", "Wei", "Wen",
    "Xia", "Xiao", "Xin", "Xiu", "Yan", "Ying", "Yu", "Yuan", "Yue",
    "Yun", "Zhen", "Zhi", "Chun", "Fei", "Gui", "Huan", "Hui", "Jiao",
    "Jin", "Lei", "Lien", "Lu", "Man", "Mei Fen", "Mei Yu", "Pei",
    "Qian", "Qiu", "Ru", "Shui", "Si", "Su", "Wan", "Xue", "Ya", "Yi"
]

NAMA_BELAKANG_BUDDHA: List[str] = [
    "Susanto", "Wijaya", "Hartono", "Gunawan", "Sutrisno", "Suryanto",
    "Kurniawan", "Santoso", "Wibowo", "Widjaja", "Widjojo", "Raharja",
    "Rahardja", "Jaya", "Setia", "Tanaka", "Hidayat", "Nugraha", "Tanujaya",
    "Tanuwijaya", "Tanuwidjaja", "Tandiono", "Sudargo", "Sudirgo", "Sudarno",
    "Lauwanto", "Liauw", "Liemena", "Lukito", "Koeswoyo", "Kusnadi",
    "Handoko", "Halim", "Hadianto", "Hadisurya", "Gondokusumo", "Djajaatmadja",
    "Budiono", "Budiarto", "Budianto", "Budisantoso", "Budiman", "Ang",
    "Chua", "Gan", "Goh", "Ho", "Kho", "Kim", "Lee", "Lim", "Ng",
    "Ong", "Tan", "Tay", "Teo", "Wong", "Yap", "Yeo", "Yeoh", "Kwee"
]

# Konghucu - Nama Tionghoa tradisional (200+ names)
NAMA_KONGHUCU_PRIA: List[str] = [
    # Marga Tionghoa umum
    "Tan", "Lim", "Ong", "Koh", "Tio", "Lie", "Oey", "The", "Go", "Kwik",
    "Kwee", "Ang", "Chua", "Gan", "Goh", "Ho", "Hoo", "Kho", "Kim", "Lee",
    "Leong", "Lew", "Liong", "Low", "Ng", "Pang", "Phua", "Poh", "Sia",
    "Sim", "Sio", "Siow", "Tang", "Tay", "Teo", "Thio", "Tjia", "Tjong",
    "Wong", "Yap", "Yeo", "Yeoh", "Wee", "Teh", "Chong", "Lau", "Chen",
    "Loh", "Chuang", "Chew", "Chai", "Loke", "Phang", "Yong", "Koay",
    "Beh", "Cheah", "Chiong", "Chia", "Chiam", "Choo", "Chou", "Foo",
    "Guan", "Han", "Heng", "Hia", "Hiew", "Hong", "Hu", "Hua", "Hwang",
    "Kam", "Kang", "Kek", "Khaw", "Khor", "Khoo", "Khu", "Ko", "Kong",
    "Koo", "Ku", "Kuan", "Kuek", "Lai", "Lam", "Lan", "Lau", "Leng",
    "Leow", "Lian", "Liew", "Lok", "Lu", "Lua", "Mah", "Mok", "Neo",
    "Nio", "Niu", "Ow", "Ow Yong", "Pan", "Peh", "Png", "Quek", "Quah",
    # Nama depan Tionghoa
    "Wei", "Wei Ming", "Jian", "Jian Wei", "Ming", "Ming Hui", "Cheng",
    "Hong", "Jun", "Kai", "Li", "Long", "Sheng", "Xin", "Yang", "Beng",
    "Chuan", "Fatt", "Guan", "Hock", "Huat", "Keat", "Keng", "Kheng",
    "Kian", "Kok", "Leong", "Liang", "Meng", "Seng", "Tat", "Teck",
    "Wah", "Yew", "Yong", "Zheng", "Zhi", "Zong", "An", "Bo", "Chang",
    "Chen", "Chun", "Da", "De", "Dong", "En", "Fa", "Feng", "Fu", "Gang",
    "Guo", "Hai", "Han", "Hao", "He", "Hua", "Hui", "Jia", "Jie", "Jin",
    "Jing", "Kun", "Lei", "Lin", "Lun", "Ming", "Nan", "Ning", "Peng"
]

NAMA_KONGHUCU_WANITA: List[str] = [
    # Nama tradisional Tionghoa
    "Mei Ling", "Mei Lan", "Mei Hui", "Mei Fang", "Mei Xia", "Li Hua",
    "Li Mei", "Li Ying", "Xiao Mei", "Xiao Ling", "Xiao Hui", "Xiao Fang",
    "Hui Ling", "Hui Lan", "Siu Mei", "Siu Lan", "Ai Ling", "Ai Mei",
    "Bao Zhu", "Bao Ling", "Bao Yu", "Chen", "Cui", "Dan", "Fang", "Fen",
    "Hong", "Hua", "Jia", "Jing", "Juan", "Lan", "Li", "Lian", "Lin",
    "Ling", "Mei", "Min", "Ming", "Na", "Ning", "Ping", "Qing", "Rong",
    "Shan", "Shu", "Ting", "Wei", "Wen", "Xia", "Xiao", "Xin", "Xiu",
    "Yan", "Ying", "Yu", "Yuan", "Yue", "Yun", "Zhen", "Zhi",
    # Nama tambahan
    "Ah Mei", "Ah Ling", "Ah Lan", "Ah Lian", "Ah Huay", "Ah Keng",
    "Ah Leng", "Ah Sim", "Ah Tin", "Bee Choo", "Bee Hoon", "Bee Leng",
    "Bee Lin", "Cheng Cheng", "Chia Chia", "Chiew Ching", "Chin Chin",
    "Choo Choo", "Chu Chu", "Chui Ling", "Chun Hua", "Fang Fang", "Fei Fei",
    "Feng Ling", "Gui Hua", "Gui Ying", "Hai Ling", "Hai Yan", "Hong Mei",
    "Hsiu Mei", "Hua Hua", "Hui Hui", "Jia Hui", "Jia Ling", "Jia Min",
    "Jia Ying", "Jiao Jiao", "Jin Hua", "Jin Ling", "Jin Mei", "Jing Jing",
    "Ju Hua", "Jun Hua", "Kai Ling", "Kai Xin", "Lan Hua", "Lan Lan",
    "Lan Ying", "Lei Lei", "Li Li", "Li Ling", "Li Na", "Li Ping", "Li Qin",
    "Li Xia", "Lian Hua", "Liang Liang", "Lin Lin", "Ling Ling", "Lu Lu",
    "Mei Feng", "Mei Hua", "Mei Juan", "Mei Li", "Mei Qin", "Mei Xiang",
    "Mei Yun", "Mei Zhen", "Miao Miao", "Min Min", "Ming Hua", "Ming Zhu",
    "Na Na", "Ning Ning", "Pei Ling", "Ping Ping", "Qi Qi", "Qian Qian"
]

NAMA_BELAKANG_KONGHUCU: List[str] = [
    "Tan", "Lim", "Ong", "Koh", "Tio", "Lie", "Oey", "The", "Go", "Kwik",
    "Kwee", "Ang", "Chua", "Gan", "Goh", "Ho", "Hoo", "Kho", "Kim", "Lee",
    "Leong", "Lew", "Liong", "Low", "Ng", "Pang", "Phua", "Poh", "Sia",
    "Sim", "Sio", "Siow", "Tang", "Tay", "Teo", "Thio", "Tjia", "Tjong",
    "Wong", "Yap", "Yeo", "Yeoh", "Wee", "Teh", "Chong", "Lau", "Chen",
    "Loh", "Chuang", "Chew", "Chai", "Loke", "Phang", "Yong", "Koay",
    "Beh", "Cheah", "Chiong", "Chia", "Chiam", "Choo", "Chou", "Foo",
    "Guan", "Han", "Heng", "Hia", "Hiew", "Hong", "Hu", "Hua", "Hwang"
]

# Kepercayaan - Nama Jawa tradisional (banyak penganut kepercayaan di Jawa) - 200+ names
NAMA_KEPERCAYAAN_PRIA: List[str] = [
    # Nama Jawa umum dengan awalan Su-
    "Suryo", "Surya", "Suyono", "Suyanto", "Suyadi", "Suyatno", "Suyitno",
    "Sujono", "Sujadi", "Sujatno", "Sujitno", "Suhono", "Suhadi", "Suharto",
    "Suherman", "Suparno", "Suparman", "Supardi", "Suparto", "Supriyono",
    "Supriyadi", "Supriadi", "Supriyanto", "Suprayitno", "Suprapto", "Suparto",
    "Sukarno", "Sukardi", "Sukarto", "Sukiman", "Sukino", "Sukiyono",
    "Sulardi", "Sularto", "Suliman", "Sulino", "Suliyo", "Sulistyo",
    "Sunardi", "Sunarto", "Sunaryo", "Sunaryono", "Sunarso", "Sunarsono",
    "Susilo", "Susanto", "Sutomo", "Sutanto", "Sutarjo", "Sutarno",
    "Sutrisno", "Sutejo", "Sutikno", "Sutino", "Sutiyo", "Sutiyono",
    # Nama Jawa dengan awalan Bam-/Har-/Wid-
    "Bambang", "Bambang Tri", "Bambang Eko", "Bambang Dwi", "Bambang Joko",
    "Hartono", "Hartanto", "Haryono", "Haryanto", "Hariyadi", "Hariyanto",
    "Widodo", "Widodo Tri", "Widodo Eko", "Widodo Dwi", "Widiyono",
    "Widiyanto", "Widiyadi", "Widianto", "Widiadi", "Widigdo", "Widjojo",
    # Nama Jawa dengan awalan agama/kepercayaan
    "Budi", "Budiono", "Budiarto", "Budiman", "Budianto", "Budiyono",
    "Teguh", "Teguh Prasetyo", "Teguh Widodo", "Teguh Santoso",
    "Wahyu", "Wahyudi", "Wahyudin", "Wahyono", "Wahyanto", "Wahyuono",
    # Nama urutan kelahiran Jawa
    "Eko", "Eko Prasetyo", "Eko Wahyudi", "Eko Widodo", "Eko Santoso",
    "Dwi", "Dwi Prasetyo", "Dwi Wahyudi", "Dwi Widodo", "Dwi Santoso",
    "Tri", "Tri Prasetyo", "Tri Wahyudi", "Tri Widodo", "Tri Santoso",
    "Catur", "Catur Prasetyo", "Catur Wahyudi", "Catur Widodo",
    "Panca", "Panca Prasetyo", "Panca Wahyudi", "Panca Widodo",
    # Nama bangsawan/tradisional Jawa
    "Raden", "Raden Mas", "Mas", "Pangeran", "Aryo", "Ario", "Kanjeng",
    "Ngabehi", "Tumenggung", "Demang", "Adipati", "Prabu", "Rama",
    # Nama tokoh/sejarah Jawa
    "Joko", "Joko Widodo", "Djoko", "Djoko Wahyudi", "Diponegoro",
    "Hayam Wuruk", "Gajah Mada", "Kertanegara", "Airlangga", "Brawijaya",
    "Ken Arok", "Ken Dedes", "Tribhuwana", "Majapahit", "Mataram",
    # Nama wayang/pewayangan Jawa
    "Semar", "Gareng", "Petruk", "Bagong", "Punakawan", "Werkudara",
    "Arjuna", "Puntadewa", "Nakula", "Sadewa", "Yudhistira", "Bima",
    "Kresna", "Rama", "Laksmana", "Barata", "Satriya", "Pandawa",
    # Nama Jawa modern
    "Agus", "Agung", "Adi", "Aji", "Anang", "Anda", "Andri", "Anton",
    "Bagas", "Bagus", "Bakti", "Bangun", "Baskara", "Basuki", "Bekti",
    "Cahyo", "Cahyono", "Cipto", "Condro", "Danang", "Darmaji", "Darmo",
    "Endro", "Fajar", "Galih", "Gatot", "Gunadi", "Gunawan", "Hari",
    "Hendro", "Heru", "Imam", "Indarto", "Indra", "Iswanto", "Jatmiko",
    "Kunto", "Laksono", "Langgeng", "Legowo", "Lukito", "Manto", "Margono",
    "Marjono", "Marsono", "Martono", "Maryono", "Mulyono", "Murjono",
    "Nugroho", "Pamungkas", "Pangestu", "Pardi", "Parto", "Prasetyo",
    "Pratomo", "Prawiro", "Purnomo", "Purwanto", "Rahardjo", "Raharjo",
    "Riyanto", "Riyadi", "Rukmono", "Sarjono", "Sasmito", "Sasongko",
    "Satrio", "Sigit", "Slamet", "Sriyono", "Sugeng", "Sugiono", "Sumarno",
    "Sumarto", "Sunarno", "Suratno", "Swasono", "Taufik", "Tjokro", "Tomo",
    "Triono", "Triyono", "Warsito", "Warsono", "Wiranto", "Wisnu", "Yanto",
    "Yatno", "Yitno", "Yono", "Yoyok", "Yuono"
]

NAMA_KEPERCAYAAN_WANITA: List[str] = [
    # Nama Jawa dengan awalan Su-
    "Sulastri", "Sulistyowati", "Sulasmi", "Sulasih", "Sulaswati",
    "Suhartini", "Suharti", "Suharni", "Suharsih", "Suharwati",
    "Sumarti", "Sumarti", "Sumarni", "Sumarsih", "Sumarwati",
    "Sumiati", "Sumiatun", "Sumini", "Suminah", "Sumiyati",
    "Sunarti", "Sunarsih", "Sunarni", "Sunarwati", "Sunaryati",
    "Sundari", "Sundarti", "Sundarini", "Sundarwati", "Sundarsih",
    "Suprapti", "Supraptini", "Supraptiningsih", "Suprapto", "Supratmi",
    "Suprihatin", "Suprihatini", "Supriharti", "Supriharsih", "Suprihati",
    "Supriyati", "Supriyatini", "Supriyani", "Supriyarti", "Supriyanti",
    "Susilowati", "Susilawati", "Susilastri", "Susiani", "Susiyanti",
    "Sutinah", "Sutini", "Sutirah", "Sutiyah", "Sutiyem",
    # Nama Jawa dengan awalan Wa-
    "Waginah", "Wagini", "Wagirah", "Wagiyem", "Wagiyah",
    "Wahyuni", "Wahyuningsih", "Wahyuning", "Wahyuningtyas", "Wahyuningsih",
    "Widayati", "Widayanti", "Widayaning", "Widayaningsih", "Widayatmi",
    "Widyastuti", "Widyastutik", "Widyastutiningsih", "Widyasari", "Widyawati",
    "Wulandari", "Wulandarini", "Wulandarsih", "Wulan", "Wulansari",
    # Nama dewi/mitologi Jawa
    "Dewi", "Dewi Sri", "Dewi Ratih", "Dewi Sinta", "Dewi Kunti",
    "Dewi Anjani", "Dewi Shinta", "Dewi Ayu", "Dewi Pertiwi", "Dewi Lestari",
    "Sri", "Sri Mulyani", "Sri Wahyuni", "Sri Rahayu", "Sri Rejeki",
    "Sri Lestari", "Sri Handayani", "Sri Utami", "Sri Hartati", "Sri Suwarni",
    "Ratna", "Ratna Dewi", "Ratna Sari", "Ratna Wulan", "Ratna Ayu",
    # Nama tokoh/sejarah Jawa
    "Kartini", "Kartika", "Kartikawati", "Kartikasari", "Kartiningsih",
    "Sartini", "Sartika", "Sartikawati", "Sartikasari", "Sartiningsih",
    "Srikandi", "Srikandini", "Srikandiningsih", "Srikandiwati", "Srikandisari",
    # Nama urutan kelahiran Jawa
    "Eka", "Eka Wahyuni", "Eka Wulandari", "Eka Sari", "Eka Dewi",
    "Dwi", "Dwi Wahyuni", "Dwi Wulandari", "Dwi Sari", "Dwi Dewi",
    "Tri", "Tri Wahyuni", "Tri Wulandari", "Tri Sari", "Tri Dewi",
    # Nama akhiran -em/-inah/-iyah
    "Wagiyem", "Suwarni", "Sularti", "Sumarni", "Sumiyem",
    "Sutiyem", "Sarinem", "Sariyem", "Rubinem", "Rubiyem",
    "Ponirah", "Poniyem", "Pariyem", "Parinem", "Parinah",
    "Maryani", "Maryanti", "Maryatun", "Maryem", "Maryati",
    "Tuminah", "Tumini", "Tuminten", "Tumiyem", "Tumiyati",
    # Nama Jawa modern
    "Endang", "Ening", "Estri", "Fitri", "Hastuti", "Heni", "Ika",
    "Indah", "Ira", "Ismi", "Iswati", "Juni", "Kurnia", "Lilis",
    "Lina", "Lilik", "Luluk", "Murti", "Nanik", "Nani", "Ningsih",
    "Nur", "Nuri", "Nurul", "Parmi", "Parti", "Partini", "Puji",
    "Purwanti", "Rahayu", "Retno", "Rini", "Rukmini", "Rusmi",
    "Sari", "Sarwi", "Septiani", "Siti", "Tatik", "Titi", "Titik",
    "Trisnawati", "Tuti", "Tutik", "Umi", "Utami", "Wati", "Wiji",
    "Winarti", "Winarsih", "Yani", "Yanti", "Yati", "Yuli", "Yulia",
    "Yunita", "Lestari", "Handayani", "Setyowati", "Rejeki", "Murni"
]

NAMA_BELAKANG_KEPERCAYAAN: List[str] = [
    # Nama marga/belakang Jawa tradisional
    "Wicaksono", "Wicaksana", "Purnomo", "Purwanto", "Purwadi", "Purwoko",
    "Susilo", "Susanto", "Sutanto", "Sutrisno", "Sutejo", "Sutikno",
    "Widodo", "Widadi", "Widyono", "Widiyanto", "Widyanto", "Widiyono",
    "Jatmiko", "Jatmika", "Jatmika", "Jatikusumo", "Jatipamungkas",
    "Condro", "Condronegoro", "Condrowangsan", "Condroningrat", "Condroatmojo",
    "Kusumo", "Kusumaningrum", "Kusumawardani", "Kusumodiningrat", "Kusumajaya",
    "Pamungkas", "Pangestu", "Pangudiono", "Panguripan", "Pangeran",
    "Raharjo", "Raharjono", "Rahardjo", "Rahardja", "Raharsono",
    "Riyanto", "Riyadi", "Riyadhi", "Riyono", "Riyadi",
    "Sarjono", "Sardjono", "Sarjiman", "Sarjoko", "Sarjito",
    "Sasmito", "Sasmita", "Sasmitohardjo", "Sasmitoningrum", "Sasmitowati",
    "Sasongko", "Sasangka", "Saswito", "Sasmodjo", "Sasono",
    "Satrio", "Satriono", "Satriyono", "Satriyo", "Satriawan",
    "Sunarso", "Sunarsono", "Sunardi", "Sunardjo", "Sunarno",
    "Sunarto", "Sunaryono", "Sunaryo", "Sunarsa", "Sunarti",
    "Suprapto", "Suprapta", "Supraptono", "Supratnyo", "Supratno",
    "Sutarjo", "Sutarno", "Sutarman", "Sutarmin", "Sutardjo",
    "Suwarno", "Suwarni", "Suwandi", "Suwanto", "Suwandono",
    "Wardoyo", "Wardono", "Wardoyo", "Wardhono", "Wardhani",
    "Warsito", "Warsono", "Warsidin", "Warsini", "Warsiman",
    # Nama marga Jawa keraton
    "Hadiningrat", "Hadisuryo", "Hadiwijoyo", "Hadikusumo", "Hadipranoto",
    "Mangkupraja", "Mangkunegara", "Mangkuatmaja", "Mangkudilaga", "Mangkubumi",
    "Danuredjo", "Danusubroto", "Danukusumo", "Danuatmojo", "Danupranoto",
    "Notodiharjo", "Notosusanto", "Notodiningrat", "Notoprojo", "Notosoegondo",
    "Tjokrodiningrat", "Tjokropranolo", "Tjokroadikusumo", "Tjokroaminoto",
    "Surjohadiprojo", "Surjopranoto", "Surjomentaram", "Surjokusuma",
    # Nama marga Jawa umum
    "Prasetyo", "Prasetya", "Prasetiya", "Prasetio", "Prastiyo",
    "Prabowo", "Praptono", "Pramono", "Prawiro", "Pratomo",
    "Setiawan", "Setiawanto", "Setiadi", "Setiabudi", "Setiaji",
    "Hartono", "Haryono", "Hariyanto", "Haryanto", "Hardjono",
    "Budiono", "Budiarto", "Budiman", "Budianto", "Budiyono",
    "Suryono", "Suryanto", "Suryana", "Suryadinata", "Suryadharma",
    "Cahyono", "Cahyanto", "Cahyadi", "Cahyadi", "Cahyana",
    "Nugroho", "Nugraha", "Nugraheni", "Nugrohadi", "Nugrahanto"
]

# Dictionary untuk mapping agama ke nama
NAMA_AGAMA_PRIA = {
    "Islam": NAMA_ISLAM_PRIA,
    "Kristen": NAMA_KRISTEN_PRIA,
    "Katolik": NAMA_KATOLIK_PRIA,
    "Hindu": NAMA_HINDU_PRIA,
    "Buddha": NAMA_BUDDHA_PRIA,
    "Konghucu": NAMA_KONGHUCU_PRIA,
    "Kepercayaan": NAMA_KEPERCAYAAN_PRIA
}

NAMA_AGAMA_WANITA = {
    "Islam": NAMA_ISLAM_WANITA,
    "Kristen": NAMA_KRISTEN_WANITA,
    "Katolik": NAMA_KATOLIK_WANITA,
    "Hindu": NAMA_HINDU_WANITA,
    "Buddha": NAMA_BUDDHA_WANITA,
    "Konghucu": NAMA_KONGHUCU_WANITA,
    "Kepercayaan": NAMA_KEPERCAYAAN_WANITA
}

NAMA_BELAKANG_AGAMA = {
    "Islam": NAMA_BELAKANG_ISLAM,
    "Kristen": NAMA_BELAKANG_KRISTEN,
    "Katolik": NAMA_BELAKANG_KATOLIK,
    "Hindu": NAMA_BELAKANG_HINDU,
    "Buddha": NAMA_BELAKANG_BUDDHA,
    "Konghucu": NAMA_BELAKANG_KONGHUCU,
    "Kepercayaan": NAMA_BELAKANG_KEPERCAYAAN
}


def get_random_status_perkawinan(age: int, gender: str) -> str:
    """
    Get random marital status based on age and gender
    Based on BPS Susenas 2023 data
    
    Args:
        age: Person's age
        gender: 'L' for male, 'P' for female
    """
    if age < 17:
        return "Belum Kawin"
    elif age <= 19:
        weights = STATUS_PERKAWINAN_BY_AGE['17-19']
    elif age <= 24:
        key = f'20-24_{gender}'
        weights = STATUS_PERKAWINAN_BY_AGE.get(key, STATUS_PERKAWINAN_BY_AGE['20-24_L'])
    elif age <= 29:
        key = f'25-29_{gender}'
        weights = STATUS_PERKAWINAN_BY_AGE.get(key, STATUS_PERKAWINAN_BY_AGE['25-29_L'])
    elif age <= 34:
        key = f'30-34_{gender}'
        weights = STATUS_PERKAWINAN_BY_AGE.get(key, STATUS_PERKAWINAN_BY_AGE['30-34_L'])
    elif age <= 39:
        key = f'35-39_{gender}'
        weights = STATUS_PERKAWINAN_BY_AGE.get(key, STATUS_PERKAWINAN_BY_AGE['35-39_L'])
    elif age <= 49:
        key = f'40-49_{gender}'
        weights = STATUS_PERKAWINAN_BY_AGE.get(key, STATUS_PERKAWINAN_BY_AGE['40-49_L'])
    elif age <= 59:
        key = f'50-59_{gender}'
        weights = STATUS_PERKAWINAN_BY_AGE.get(key, STATUS_PERKAWINAN_BY_AGE['50-59_L'])
    else:
        key = f'60+_{gender}'
        weights = STATUS_PERKAWINAN_BY_AGE.get(key, STATUS_PERKAWINAN_BY_AGE['60+_L'])
    
    return random.choices(STATUS_PERKAWINAN, weights=weights, k=1)[0]


def get_random_agama(weighted: bool = True) -> str:
    """Get random religion, optionally weighted by demographics"""
    if weighted:
        return random.choices(AGAMA, weights=AGAMA_WEIGHTS, k=1)[0]
    return random.choice(AGAMA)


def get_random_pendidikan(weighted: bool = True, min_age: int = 0) -> str:
    """
    Get random education level based on age
    Based on realistic Indonesian education system and BPS data
    
    Args:
        weighted: Use weighted distribution for adults
        min_age: Person's age
    """
    if min_age < 5:
        return "Tidak/Belum Sekolah"
    elif min_age < 7:
        # TK/PAUD age - some in preschool
        return random.choices(
            ["Tidak/Belum Sekolah", "Belum Tamat SD/Sederajat"],
            weights=[0.6, 0.4], k=1
        )[0]
    elif min_age < 12:
        # SD age (7-11 tahun)
        return random.choices(
            ["Belum Tamat SD/Sederajat", "Tamat SD/Sederajat"],
            weights=[0.85, 0.15], k=1
        )[0]
    elif min_age < 15:
        # SMP age (12-14 tahun)
        return random.choices(
            ["Tamat SD/Sederajat", "SLTP/Sederajat"],
            weights=[0.4, 0.6], k=1
        )[0]
    elif min_age < 18:
        # SMA age (15-17 tahun)
        return random.choices(
            ["Tamat SD/Sederajat", "SLTP/Sederajat", "SLTA/Sederajat"],
            weights=[0.05, 0.45, 0.50], k=1
        )[0]
    elif min_age < 22:
        # Kuliah age (18-21 tahun)
        return random.choices(
            ["SLTP/Sederajat", "SLTA/Sederajat", "Diploma I/II", "Akademi/Diploma III/Sarjana Muda"],
            weights=[0.10, 0.70, 0.08, 0.12], k=1
        )[0]
    elif min_age < 25:
        # Fresh graduate age (22-24 tahun)
        return random.choices(
            ["SLTP/Sederajat", "SLTA/Sederajat", "Diploma I/II", "Akademi/Diploma III/Sarjana Muda", "Diploma IV/Strata I"],
            weights=[0.08, 0.55, 0.05, 0.12, 0.20], k=1
        )[0]
    else:
        # Adults 25+
        if weighted:
            return random.choices(PENDIDIKAN, weights=PENDIDIKAN_WEIGHTS, k=1)[0]
        return random.choice(PENDIDIKAN)


def get_random_pekerjaan(age: int, gender: str, pendidikan: str, weighted: bool = True) -> str:
    """
    Get random occupation based on age, gender, education
    Follows realistic Indonesian employment patterns from BPS Sakernas 2023
    
    Args:
        age: Person's age
        gender: 'L' for male, 'P' for female  
        pendidikan: Education level
        weighted: Use weighted distribution
    """
    # Anak-anak (0-6 tahun)
    if age < 7:
        return "Belum/Tidak Bekerja"
    
    # Usia sekolah SD-SMA (7-17 tahun)
    elif age < 18:
        # Sebagian kecil usia 15-17 sudah bekerja (child labor reality)
        if age >= 15 and random.random() < 0.08:  # 8% usia 15-17 bekerja
            if gender == "L":
                return random.choice(["Buruh Harian Lepas", "Petani/Pekebun", "Pedagang", "Nelayan/Perikanan"])
            else:
                return random.choice(["Pembantu Rumah Tangga", "Pedagang", "Buruh Harian Lepas"])
        return "Pelajar/Mahasiswa"
    
    # Usia kuliah (18-24 tahun)
    elif age < 25:
        # Check if still studying
        if "Strata" in pendidikan or "Diploma" in pendidikan or "Akademi" in pendidikan:
            if random.random() < 0.65:  # 65% masih kuliah/baru lulus
                return random.choices(
                    ["Pelajar/Mahasiswa", "Belum/Tidak Bekerja"],
                    weights=[0.7, 0.3], k=1
                )[0]
        # Yang tidak kuliah atau sudah bekerja
        if gender == "P":
            return random.choices(
                ["Karyawan Swasta", "Pedagang", "Mengurus Rumah Tangga", "Buruh Harian Lepas",
                 "Wiraswasta", "Belum/Tidak Bekerja", "Pelajar/Mahasiswa"],
                weights=[0.25, 0.12, 0.20, 0.10, 0.13, 0.10, 0.10], k=1
            )[0]
        else:
            return random.choices(
                ["Karyawan Swasta", "Buruh Harian Lepas", "Pedagang", "Wiraswasta",
                 "Sopir", "Belum/Tidak Bekerja", "Pelajar/Mahasiswa", "Petani/Pekebun"],
                weights=[0.28, 0.15, 0.12, 0.15, 0.08, 0.07, 0.08, 0.07], k=1
            )[0]
    
    # Usia produktif utama (25-54 tahun)
    elif age <= 54:
        if gender == "P":
            # Wanita: ~52% bekerja, ~48% IRT (BPS 2023)
            if random.random() < 0.48:  # 48% ibu rumah tangga
                return "Mengurus Rumah Tangga"
            # Yang bekerja
            if "Strata" in pendidikan or "Diploma" in pendidikan:
                return random.choices(
                    ["Karyawan Swasta", "Pegawai Negeri Sipil", "Guru", "Perawat", "Bidan",
                     "Wiraswasta", "Pedagang", "Dokter", "Dosen", "Akuntan"],
                    weights=[0.25, 0.15, 0.18, 0.10, 0.08, 0.10, 0.06, 0.03, 0.03, 0.02], k=1
                )[0]
            else:
                return random.choices(
                    ["Pedagang", "Buruh Harian Lepas", "Petani/Pekebun", "Wiraswasta",
                     "Karyawan Swasta", "Pembantu Rumah Tangga", "Tukang Jahit", "Industri"],
                    weights=[0.22, 0.18, 0.20, 0.15, 0.10, 0.07, 0.04, 0.04], k=1
                )[0]
        else:
            # Pria: ~83% bekerja (BPS 2023)
            if random.random() < 0.05:  # 5% tidak bekerja
                return "Belum/Tidak Bekerja"
            if "Strata" in pendidikan or "Diploma" in pendidikan:
                return random.choices(
                    ["Karyawan Swasta", "Pegawai Negeri Sipil", "Wiraswasta", "Guru", "Dosen",
                     "Dokter", "Karyawan BUMN", "Konsultan", "Pedagang", "Tentara Nasional Indonesia"],
                    weights=[0.30, 0.18, 0.15, 0.10, 0.05, 0.04, 0.06, 0.04, 0.05, 0.03], k=1
                )[0]
            else:
                return random.choices(
                    ["Petani/Pekebun", "Karyawan Swasta", "Buruh Harian Lepas", "Pedagang",
                     "Wiraswasta", "Sopir", "Konstruksi", "Nelayan/Perikanan", "Mekanik", "Tukang Batu"],
                    weights=[0.22, 0.18, 0.14, 0.12, 0.10, 0.07, 0.06, 0.04, 0.04, 0.03], k=1
                )[0]
    
    # Usia pra-pensiun (55-59 tahun)
    elif age <= 59:
        if gender == "P":
            return random.choices(
                ["Mengurus Rumah Tangga", "Pedagang", "Petani/Pekebun", "Pensiunan",
                 "Wiraswasta", "Pegawai Negeri Sipil"],
                weights=[0.40, 0.18, 0.15, 0.12, 0.10, 0.05], k=1
            )[0]
        else:
            return random.choices(
                ["Petani/Pekebun", "Wiraswasta", "Pedagang", "Pensiunan", "Karyawan Swasta",
                 "Pegawai Negeri Sipil", "Sopir", "Buruh Harian Lepas"],
                weights=[0.25, 0.18, 0.15, 0.15, 0.10, 0.07, 0.05, 0.05], k=1
            )[0]
    
    # Usia pensiun (60-69 tahun)
    elif age <= 69:
        if gender == "P":
            return random.choices(
                ["Mengurus Rumah Tangga", "Pensiunan", "Pedagang", "Petani/Pekebun", "Wiraswasta"],
                weights=[0.45, 0.25, 0.12, 0.10, 0.08], k=1
            )[0]
        else:
            return random.choices(
                ["Pensiunan", "Petani/Pekebun", "Wiraswasta", "Pedagang", "Mengurus Rumah Tangga"],
                weights=[0.35, 0.25, 0.18, 0.12, 0.10], k=1
            )[0]
    
    # Lansia (70+ tahun)
    else:
        if gender == "P":
            return random.choices(
                ["Mengurus Rumah Tangga", "Pensiunan", "Belum/Tidak Bekerja"],
                weights=[0.50, 0.30, 0.20], k=1
            )[0]
        else:
            return random.choices(
                ["Pensiunan", "Petani/Pekebun", "Mengurus Rumah Tangga", "Wiraswasta", "Belum/Tidak Bekerja"],
                weights=[0.35, 0.20, 0.20, 0.10, 0.15], k=1
            )[0]


def get_random_golongan_darah() -> str:
    """Get random blood type"""
    return random.choice(GOLONGAN_DARAH_SIMPLE)


def get_random_nama(gender: str, num_words: int = None, agama: str = None) -> str:
    """
    Generate random Indonesian name with 1-3 words, optionally based on religion
    
    Args:
        gender: 'L' for male, 'P' for female
        num_words: Number of words in name (1, 2, or 3). None for random
        agama: Religion to use for name generation. None for general names
    """
    if num_words is None:
        # Random distribution: 15% single, 55% double, 30% triple
        num_words = random.choices([1, 2, 3], weights=[0.15, 0.55, 0.30], k=1)[0]
    
    # Use religion-based names if agama is specified
    if agama and agama in NAMA_AGAMA_PRIA:
        if gender == "L":
            nama_depan = NAMA_AGAMA_PRIA.get(agama, NAMA_DEPAN_PRIA)
            nama_belakang = NAMA_BELAKANG_AGAMA.get(agama, NAMA_BELAKANG)
        else:
            nama_depan = NAMA_AGAMA_WANITA.get(agama, NAMA_DEPAN_WANITA)
            nama_belakang = NAMA_BELAKANG_AGAMA.get(agama, NAMA_BELAKANG)
        
        if num_words == 1:
            # Single name - just pick from religion-specific first names
            return random.choice(nama_depan)
        elif num_words == 2:
            first = random.choice(nama_depan)
            last = random.choice(nama_belakang)
            return f"{first} {last}"
        else:  # 3 words
            first = random.choice(nama_depan)
            middle = random.choice(nama_depan + nama_belakang)
            last = random.choice(nama_belakang)
            return f"{first} {middle} {last}"
    
    # Default behavior (no religion specified) - use general names
    if gender == "L":
        if num_words == 1:
            return random.choice(NAMA_TUNGGAL_PRIA)
        elif num_words == 2:
            first = random.choice(NAMA_DEPAN_PRIA)
            last = random.choice(NAMA_BELAKANG)
            return f"{first} {last}"
        else:  # 3 words
            first = random.choice(NAMA_DEPAN_PRIA)
            middle = random.choice(NAMA_DEPAN_PRIA + NAMA_BELAKANG)
            last = random.choice(NAMA_BELAKANG)
            return f"{first} {middle} {last}"
    else:
        if num_words == 1:
            return random.choice(NAMA_TUNGGAL_WANITA)
        elif num_words == 2:
            first = random.choice(NAMA_DEPAN_WANITA)
            last = random.choice(NAMA_BELAKANG)
            return f"{first} {last}"
        else:  # 3 words
            first = random.choice(NAMA_DEPAN_WANITA)
            middle = random.choice(NAMA_DEPAN_WANITA + NAMA_BELAKANG)
            last = random.choice(NAMA_BELAKANG)
            return f"{first} {middle} {last}"


def get_random_nama_ayah(agama: str = None) -> str:
    """Generate random father name, optionally based on religion"""
    return get_random_nama("L", agama=agama)


def get_random_nama_ibu(agama: str = None) -> str:
    """Generate random mother name, optionally based on religion"""
    return get_random_nama("P", agama=agama)


# ============================================================================
# NAMA JALAN (500+ unique street names for diversity)
# ============================================================================
NAMA_JALAN: List[str] = [
    # === Pahlawan Nasional ===
    "Sudirman", "Gatot Subroto", "Diponegoro", "Ahmad Yani", "Cut Nyak Dien",
    "Imam Bonjol", "Hasanuddin", "Sultan Agung", "Pangeran Antasari", "Urip Sumoharjo",
    "Teuku Umar", "Mohammad Hatta", "Soekarno", "Ki Hajar Dewantara", "Kartini",
    "Dewi Sartika", "Martha Christina Tiahahu", "Pattimura", "Tuanku Imam Bonjol",
    "Sultan Hasanuddin", "Pangeran Diponegoro", "Teuku Cik Di Tiro", "Cut Meutia",
    "Nyi Ageng Serang", "Raden Ajeng Kartini", "Mohammad Yamin", "Agus Salim",
    "Wahid Hasyim", "Abdul Muis", "Tan Malaka", "Sutan Sjahrir", "Adam Malik",
    "Ali Sastroamidjojo", "Hamengkubuwono IX", "Sri Sultan HB IX", "Oto Iskandar Di Nata",
    "Sam Ratulangi", "Johannes Latuharhary", "Andi Pettarani", "Wolter Monginsidi",
    "Robert Wolter Monginsidi", "I Gusti Ngurah Rai", "Ngurah Rai", "Ida Bagus Mantra",
    
    # === Tokoh Militer ===
    "Jenderal Sudirman", "Letjen S Parman", "Letjen MT Haryono", "Mayjen Sutoyo",
    "Mayjen DI Panjaitan", "Brigjen Katamso", "Kolonel Sugiono", "Kapten Tendean",
    "Kapten Pierre Tendean", "Ade Irma Suryani Nasution", "Ahmad Dahlan", "Suprapto",
    "Sisingamangaraja", "Sisingamangaraja XII", "Tuanku Tambusai", "Tuanku Rao",
    "Tjut Nyak Meutia", "Teungku Chik Di Tiro", "Sultan Thaha", "Sultan Mahmud Badaruddin",
    "Pangeran Hidayatullah", "Sultan Ageng Tirtayasa", "Sultan Syarif Kasim",
    
    # === Nama Tempat/Geografis ===
    "Merdeka", "Proklamasi", "Kemerdekaan", "Indonesia", "Nusantara", "Pancasila",
    "Bhinneka", "Garuda", "Merah Putih", "Nasional", "Pembangunan", "Persatuan",
    "Kebangsaan", "Patriot", "Pejuang", "Pahlawan", "Veteran", "Pejuang 45",
    "Pemuda", "Pelajar", "Mahasiswa", "Warga", "Rakyat", "Gotong Royong",
    
    # === Bunga ===
    "Mawar", "Melati", "Kenanga", "Dahlia", "Anggrek", "Cempaka", "Flamboyan",
    "Teratai", "Tulip", "Sakura", "Seroja", "Wijaya Kusuma", "Kamboja", "Bougenville",
    "Kemuning", "Sedap Malam", "Kantil", "Gardenia", "Magnolia", "Lavender",
    "Krisan", "Aster", "Lily", "Jasmine", "Rose", "Lotus", "Orchid", "Sunflower",
    "Bunga Matahari", "Bunga Sepatu", "Alamanda", "Adenium", "Amarilis", "Anthurium",
    "Azalea", "Begonia", "Camellia", "Carnation", "Chrysanthemum", "Daffodil",
    "Eucalyptus", "Frangipani", "Geranium", "Hibiscus", "Hydrangea", "Iris",
    "Jasmine", "Kembang Sepatu", "Kembang Kertas", "Kumis Kucing", "Lidah Mertua",
    
    # === Buah ===
    "Mangga", "Jeruk", "Rambutan", "Durian", "Kelapa", "Pinang", "Jambu",
    "Nangka", "Pisang", "Pepaya", "Salak", "Manggis", "Duku", "Langsat",
    "Sawo", "Kedondong", "Belimbing", "Sirsak", "Alpukat", "Apel", "Anggur",
    "Semangka", "Melon", "Strawberry", "Blueberry", "Cherry", "Kiwi", "Lemon",
    "Markisa", "Nanas", "Kurma", "Delima", "Persik", "Plum", "Pir",
    "Ceri", "Kesemek", "Lengkeng", "Kelengkeng", "Leci", "Sukun", "Menteng",
    "Kemang", "Kawista", "Buni", "Gandaria", "Matoa", "Cempedak", "Tampoi",
    
    # === Pohon ===
    "Beringin", "Jati", "Mahoni", "Akasia", "Cemara", "Pinus", "Bambu",
    "Palem", "Kelapa Sawit", "Karet", "Sengon", "Trembesi", "Ketapang",
    "Asam", "Asem", "Jambu Air", "Randu", "Kapuk", "Waru", "Sawo Kecik",
    "Tanjung", "Glodokan", "Bungur", "Tamarind", "Eboni", "Sonokeling",
    "Meranti", "Merbau", "Ulin", "Kayu Putih", "Cendana", "Gaharu",
    
    # === Perumahan/Komplek ===
    "Nusa Indah", "Bukit Indah", "Griya Asri", "Taman Sari", "Puri Indah",
    "Bumi Asri", "Graha Indah", "Pesona", "Permata", "Mutiara", "Intan",
    "Berlian", "Safir", "Zamrud", "Ruby", "Topaz", "Emerald", "Diamond",
    "Golden", "Silver", "Platinum", "Grand", "Royal", "Elite", "Prima",
    "Megah", "Jaya", "Sentosa", "Sejahtera", "Makmur", "Bahagia", "Damai",
    "Harmoni", "Selaras", "Tentram", "Nyaman", "Asri", "Lestari", "Hijau",
    
    # === Arah Mata Angin ===
    "Utara", "Selatan", "Timur", "Barat", "Tengah", "Pusat",
    "Utara I", "Utara II", "Selatan I", "Selatan II", "Timur I", "Timur II",
    "Barat I", "Barat II", "Tengah I", "Tengah II",
    
    # === Angka/Numerik ===
    "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan",
    "Sembilan", "Sepuluh", "Sebelas", "Dua Belas",
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    
    # === Profesi ===
    "Guru", "Dokter", "Insinyur", "Arsitek", "Hakim", "Jaksa", "Polisi",
    "Tentara", "Nelayan", "Petani", "Pedagang", "Pengusaha", "Seniman",
    "Wartawan", "Perawat", "Bidan", "Apoteker", "Pilot", "Pelaut", "Penerbang",
    
    # === Hewan ===
    "Elang", "Rajawali", "Garuda", "Merak", "Cendrawasih", "Jalak", "Merpati",
    "Kutilang", "Kenari", "Parkit", "Kakatua", "Nuri", "Beo", "Bangau",
    "Angsa", "Bebek", "Ayam", "Kuda", "Sapi", "Kambing", "Domba", "Kelinci",
    "Kucing", "Anjing", "Harimau", "Singa", "Gajah", "Badak", "Tapir",
    "Rusa", "Kijang", "Banteng", "Kerbau", "Lumba-lumba", "Paus", "Hiu",
    "Penyu", "Buaya", "Komodo", "Biawak", "Ular", "Katak", "Kodok",
    "Kupu-kupu", "Capung", "Lebah", "Semut", "Kumbang", "Belalang", "Jangkrik",
    
    # === Alam ===
    "Gunung", "Bukit", "Lembah", "Pantai", "Laut", "Sungai", "Danau",
    "Telaga", "Rawa", "Hutan", "Padang", "Savana", "Tundra", "Gletser",
    "Air Terjun", "Mata Air", "Sumur", "Teluk", "Selat", "Tanjung", "Pulau",
    "Karang", "Pasir", "Batu", "Kerikil", "Tanah", "Lumpur", "Gambut",
    "Pegunungan", "Perbukitan", "Dataran", "Ngarai", "Jurang", "Tebing", "Gua",
    
    # === Cuaca/Langit ===
    "Matahari", "Bulan", "Bintang", "Langit", "Awan", "Pelangi", "Hujan",
    "Angin", "Badai", "Petir", "Kilat", "Guruh", "Embun", "Kabut", "Salju",
    "Fajar", "Senja", "Malam", "Siang", "Pagi", "Dini Hari", "Tengah Malam",
    "Aurora", "Galaksi", "Nebula", "Komet", "Meteor", "Saturnus", "Jupiter",
    "Mars", "Venus", "Merkurius", "Neptunus", "Uranus", "Pluto", "Andromeda",
    
    # === Warna ===
    "Merah", "Kuning", "Hijau", "Biru", "Ungu", "Jingga", "Pink", "Coklat",
    "Hitam", "Putih", "Abu-abu", "Emas", "Perak", "Perunggu", "Tembaga",
    
    # === Musik/Seni ===
    "Gamelan", "Angklung", "Sasando", "Kolintang", "Tifa", "Gong", "Kendang",
    "Suling", "Seruling", "Rebab", "Kecapi", "Siter", "Bonang", "Saron",
    "Gitar", "Piano", "Biola", "Harmonika", "Organ", "Drum", "Bass",
    
    # === Tokoh Budaya/Seniman ===
    "WR Supratman", "Ismail Marzuki", "Gesang", "Ibu Sud", "AT Mahmud",
    "Wage Rudolf Supratman", "Cornel Simanjuntak", "Kusbini", "Mochtar Lubis",
    "Pramoedya Ananta Toer", "Chairil Anwar", "Sapardi Djoko Damono",
    "Rendra", "Taufiq Ismail", "Goenawan Mohamad", "Amir Hamzah", "Sutan Takdir",
    "Affandi", "Raden Saleh", "Basuki Abdullah", "S Sudjojono", "Hendra Gunawan",
    
    # === Agama/Spiritual ===
    "Masjid", "Musholla", "Gereja", "Kapel", "Pura", "Vihara", "Klenteng",
    "Surau", "Langgar", "Pesantren", "Madrasah", "Seminari",
    
    # === Industri/Ekonomi ===
    "Industri", "Pabrik", "Gudang", "Pelabuhan", "Bandara", "Stasiun", "Terminal",
    "Pasar", "Mall", "Plaza", "Trade Center", "Business Park", "Kawasan Industri",
    "Perdagangan", "Niaga", "Bisnis", "Komersial", "Ekonomi", "Keuangan",
    
    # === Pendidikan ===
    "Universitas", "Kampus", "Sekolah", "Akademi", "Institut", "Politeknik",
    "Perguruan", "Pendidikan", "Ilmu", "Pengetahuan", "Riset", "Penelitian",
    
    # === Kesehatan ===
    "Rumah Sakit", "Klinik", "Puskesmas", "Apotek", "Laboratorium",
    "Kesehatan", "Medis", "Farmasi", "Rehabilitasi",
    
    # === Olahraga ===
    "Stadion", "Gelanggang", "Arena", "Lapangan", "Kolam Renang",
    "Sepak Bola", "Basket", "Voli", "Badminton", "Tenis", "Golf",
    "Atletik", "Renang", "Tinju", "Silat", "Karate", "Taekwondo",
    
    # === Tambahan Unik ===
    "Cendana", "Gading", "Ivory", "Kristal", "Jade", "Opal", "Amethyst",
    "Citrine", "Aquamarine", "Turquoise", "Garnet", "Peridot", "Alexandrite",
    "Tanzanite", "Morganite", "Kunzite", "Spinel", "Zircon", "Tourmaline",
    
    # === Nama Daerah Terkenal ===
    "Menteng", "Kebayoran", "Kemang", "Senayan", "Kuningan", "Sudirman",
    "Thamrin", "Rasuna Said", "Casablanca", "Mangga Dua", "Glodok", "Kota",
    "Ancol", "Kelapa Gading", "Sunter", "Pulo Gadung", "Cakung", "Cilandak",
    "Pondok Indah", "Permata Hijau", "Simprug", "Cipete", "Fatmawati", "Blok M",
    "Tebet", "Pancoran", "Kalibata", "Pasar Minggu", "Jagakarsa", "Depok",
    "Cibubur", "Bekasi", "Tangerang", "Serpong", "BSD", "Bintaro", "Ciputat",
]

def get_random_alamat() -> str:
    """Generate random street address with high uniqueness"""
    jalan_prefix = random.choice(["Jl.", "Jalan", "Gg.", "Gang", "Komp.", "Perumahan", "Perum.", "Puri", "Griya", "Taman"])
    
    nama_jalan = random.choice(NAMA_JALAN)
    
    nomor = random.randint(1, 200)
    
    # Variasi format alamat
    format_type = random.random()
    if format_type < 0.25:
        # Dengan blok
        blok = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"])
        return f"{jalan_prefix} {nama_jalan} Blok {blok} No. {nomor}"
    elif format_type < 0.45:
        # Dengan nomor blok
        blok_num = random.randint(1, 20)
        return f"{jalan_prefix} {nama_jalan} Blok {blok_num} No. {nomor}"
    elif format_type < 0.60:
        # Dengan kavling
        kav = random.randint(1, 50)
        return f"{jalan_prefix} {nama_jalan} Kav. {kav}"
    elif format_type < 0.70:
        # Dengan RT/RW inline
        rt = random.randint(1, 20)
        rw = random.randint(1, 15)
        return f"{jalan_prefix} {nama_jalan} No. {nomor} RT {rt:02d}/RW {rw:02d}"
    elif format_type < 0.80:
        # Dengan sektor/cluster
        sector = random.choice(["Sektor", "Cluster", "Blok", "Area"])
        sector_id = random.choice(["A", "B", "C", "D", "E", "1", "2", "3", "4", "5"])
        return f"{jalan_prefix} {nama_jalan} {sector} {sector_id} No. {nomor}"
    else:
        # Standard
        return f"{jalan_prefix} {nama_jalan} No. {nomor}"


def get_random_rt() -> str:
    """Generate random RT number"""
    return f"{random.randint(1, 20):03d}"


def get_random_rw() -> str:
    """Generate random RW number"""
    return f"{random.randint(1, 15):03d}"
