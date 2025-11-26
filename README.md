# DUKCAPIL Data Generator

**Generate Data Penduduk Indonesia (Dummy) dengan Format DUKCAPIL Lengkap**

Aplikasi Python untuk generate data penduduk Indonesia secara realistis dengan format DUKCAPIL. Mendukung mode generate per keluarga dengan distribusi wilayah yang fleksibel dan parallel processing untuk jutaan record.

## ✨ Fitur Utama

### 🏠 Mode Keluarga
- Generate data keluarga lengkap (Kepala Keluarga, Istri, Anak)
- NKK (Nomor Kartu Keluarga) konsisten per keluarga
- Relasi keluarga yang realistis (nama ayah/ibu konsisten untuk anak)
- Agama konsisten dalam satu keluarga

### 🆔 NIK & NKK Valid
- NIK 16 digit sesuai format DUKCAPIL resmi
- Validasi tanggal lahir (wanita: DD+40)
- Nomor urut unik per kecamatan
- Format: `[PP][KK][CC][DDMMYY][SSSS]`

### 🗺️ Data Wilayah Lengkap
- 37 Provinsi
- 514 Kabupaten/Kota
- 7.277 Kecamatan
- 83.761 Kelurahan
- Berdasarkan data Kemendagri terbaru

### ⚡ Parallel Processing
- Mode Sequential (single thread) untuk data kecil
- Mode Parallel (multi-core) untuk jutaan record
- Streaming mode untuk hemat memory
- Optimal workers auto-detection

### 📊 Distribusi Data Realistis (BPS)
Semua distribusi data berdasarkan statistik BPS Indonesia:

#### Agama (Sensus BPS 2020)
| Agama | Persentase |
|-------|------------|
| Islam | 87.02% |
| Kristen | 7.00% |
| Katolik | 2.90% |
| Hindu | 1.69% |
| Buddha | 0.73% |
| Konghucu | 0.03% |
| Kepercayaan | 0.63% |

#### Pendidikan (Susenas BPS 2023)
| Tingkat | Persentase |
|---------|------------|
| Tidak/Belum Sekolah | 5.5% |
| Belum Tamat SD | 10.2% |
| Tamat SD | 24.5% |
| SLTP | 21.5% |
| SLTA | 26.8% |
| Diploma I-III | 2.8% |
| Diploma IV/S1 | 7.8% |
| S2 | 0.8% |
| S3 | 0.1% |

#### Status Perkawinan
Berdasarkan usia dan jenis kelamin sesuai data BPS

### 👤 Nama Berbasis Agama
Sistem penamaan cerdas berdasarkan agama:

| Agama | Karakteristik Nama | Contoh |
|-------|-------------------|--------|
| **Islam** | Arab/Islam + marga Jawa/Sunda | Muhammad Ahmad, Fatimah Hidayat |
| **Kristen** | Alkitab + Batak/Manado | Yohanes Simanjuntak, Maria Hutabarat |
| **Katolik** | Santo/Santa + Flores/Portugis | Fransiskus Da Silva, Theresia Fernandes |
| **Hindu** | Bali + Sanskrit | I Wayan Dharma, Ni Made Sari |
| **Buddha** | Tionghoa-Indonesia | Tan Wijaya, Mei Ling Susanto |
| **Konghucu** | Tionghoa tradisional | Wei Ming Tan, Mei Lan Ong |
| **Kepercayaan** | Jawa tradisional | Suryo Wicaksono, Dewi Sri Kusumo |

**Total nama tersedia:**
- 1.393 nama pria
- 1.309 nama wanita
- 629 nama belakang/marga

### 📍 Tempat Lahir Variatif
Distribusi tempat lahir yang realistis:
| Kategori | Persentase | Keterangan |
|----------|------------|------------|
| Domisili | 60% | Lahir di kota tempat tinggal |
| Provinsi sama | 20% | Lahir di kota lain provinsi sama |
| Provinsi tetangga | 15% | Lahir di provinsi tetangga |
| Provinsi lain | 5% | Lahir di provinsi jauh |

**Khusus Anak:** 100% lahir di domisili (sesuai realita)

### 📄 Multi-Format Output
- CSV (dengan UTF-8 BOM)
- Excel (.xlsx)
- JSON
- Export semua format sekaligus

### 🗄️ Export SQL Multi-Database
| Database | Fitur |
|----------|-------|
| Oracle | MERGE statement, sequence |
| PostgreSQL | ON CONFLICT upsert, UUID |
| MariaDB | INSERT IGNORE, auto_increment |
| MySQL | INSERT IGNORE, auto_increment |
| SQL Server | MERGE statement, IDENTITY |
| SQLite | INSERT OR REPLACE |

**Mode SQL:**
1. Structure only (CREATE TABLE)
2. Data only (INSERT)
3. Structure + Data

## 🚀 Instalasi

```bash
# Clone atau download project
cd generate-people

# Buat virtual environment (opsional tapi disarankan)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# atau .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
```
faker>=22.0.0
pandas>=2.0.0
openpyxl>=3.1.0
tqdm>=4.66.0
numpy>=1.24.0
```

## 📖 Penggunaan

### Mode Interaktif (CLI)
```bash
python src/main.py
```

### Contoh Sesi
```
========================================================
         DUKCAPIL DATA GENERATOR v1.0
   Generate Data Penduduk Indonesia (Dummy)
========================================================

Loading data wilayah...
✓ Data loaded: 37 provinsi, 514 kab/kota
  7277 kecamatan, 83761 kelurahan

Masukkan kode wilayah: 7371
✓ KOTA MAKASSAR (15 kecamatan, 153 kelurahan)

Masukkan jumlah keluarga: 1000

Pilih distribusi keluarga:
  1. Merata (setiap kelurahan dapat jumlah KK sama)
  2. Merata dengan jumlah KK acak per kelurahan
  3. Random (kelurahan dipilih secara acak)
Pilihan [1-3]: 2

Pilih mode processing:
  1. Sequential (single thread)
  2. Parallel (multi-core, optimal untuk jumlah besar)
Pilihan [1-2]: 2

  Jumlah CPU core: 8
  Rekomendasi workers: 6

  Gunakan streaming mode (hemat memory untuk jutaan record)?
  [y/N]: n

Pilih format output:
  1. CSV
  2. Excel
  3. JSON
  4. Semua format (CSV, Excel, JSON)
Pilihan [1-4]: 4

Export SQL? [Y/n]: Y
Pilih jenis database:
  1. Oracle
  2. PostgreSQL
  3. MariaDB
  4. MySQL
  5. SQL Server
  6. SQLite
Pilihan [1-6]: 2

Pilih isi SQL:
  1. Structure only (CREATE TABLE)
  2. Data only (INSERT)
  3. Structure + Data
Pilihan [1-3]: 3

🚀 Mode: Parallel (6 workers)
Generating families: 100%|████████████████████| 1000/1000 [00:02<00:00, 450.12KK/s]

✓ Output tersimpan di:
  - output/dukcapil_7371_20241126_143052.csv
  - output/dukcapil_7371_20241126_143052.xlsx
  - output/dukcapil_7371_20241126_143052.json
  - output/dukcapil_7371_20241126_143052_postgresql.sql

=== REKAP GENERASI ===
Wilayah: KOTA MAKASSAR (7371)
Total Keluarga: 1,000
Total Penduduk: 4,057
```

## 🗺️ Kode Wilayah

Kode wilayah mengikuti format Kemendagri:

| Level | Digit | Contoh | Keterangan |
|-------|-------|--------|------------|
| Provinsi | 2 | `32` | Jawa Barat |
| Kab/Kota | 4 | `3201` | Kabupaten Bogor |
| Kecamatan | 6 | `320101` | Kec. Cibinong |

### Contoh Kode Wilayah Populer
| Kode | Nama |
|------|------|
| `31` | DKI Jakarta |
| `32` | Jawa Barat |
| `33` | Jawa Tengah |
| `35` | Jawa Timur |
| `3171` | Kota Adm. Jakarta Pusat |
| `3172` | Kota Adm. Jakarta Utara |
| `3173` | Kota Adm. Jakarta Barat |
| `3174` | Kota Adm. Jakarta Selatan |
| `3175` | Kota Adm. Jakarta Timur |
| `3201` | Kabupaten Bogor |
| `3273` | Kota Bandung |
| `3374` | Kota Semarang |
| `3578` | Kota Surabaya |
| `7371` | Kota Makassar |

## 🆔 Format NIK

NIK 16 digit dengan format: `[PP][KK][CC][DDMMYY][SSSS]`

| Bagian | Digit | Keterangan |
|--------|-------|------------|
| PP | 2 | Kode Provinsi |
| KK | 2 | Kode Kabupaten/Kota |
| CC | 2 | Kode Kecamatan |
| DDMMYY | 6 | Tanggal Lahir (wanita: DD+40) |
| SSSS | 4 | Nomor urut |

**Contoh:**
- Pria lahir 15 Jan 1990 di Makassar: `737101150190xxxx`
- Wanita lahir 15 Jan 1990 di Makassar: `737101550190xxxx` (55 = 15+40)

## 📋 Data Fields

| No | Field | Tipe | Deskripsi |
|----|-------|------|-----------|
| 1 | NKK | String(16) | Nomor Kartu Keluarga |
| 2 | NIK | String(16) | Nomor Induk Kependudukan |
| 3 | NAMA | String | Nama lengkap |
| 4 | JENIS_KELAMIN | String(1) | L = Laki-laki, P = Perempuan |
| 5 | TEMPAT_LAHIR | String | Kota kelahiran (UPPERCASE) |
| 6 | TANGGAL_LAHIR | String | Format DD-MM-YYYY |
| 7 | AGAMA | String | 7 agama resmi + Kepercayaan |
| 8 | PENDIDIKAN | String | 10 tingkat pendidikan |
| 9 | PEKERJAAN | String | 60+ jenis pekerjaan |
| 10 | STATUS_PERKAWINAN | String | Belum Kawin/Kawin/Cerai Hidup/Cerai Mati |
| 11 | STATUS_HUBUNGAN | String | Kepala Keluarga/Istri/Anak/dll |
| 12 | GOLONGAN_DARAH | String | A/B/AB/O/Tidak Tahu |
| 13 | KEWARGANEGARAAN | String | WNI/WNA |
| 14 | NAMA_AYAH | String | Nama ayah kandung |
| 15 | NAMA_IBU | String | Nama ibu kandung |
| 16 | ALAMAT | String | Alamat lengkap dengan nama jalan |
| 17 | RT | String(3) | Nomor RT (001-020) |
| 18 | RW | String(3) | Nomor RW (001-015) |
| 19 | KELURAHAN | String | Nama kelurahan/desa |
| 20 | KECAMATAN | String | Nama kecamatan |
| 21 | KABUPATEN | String | Nama kabupaten/kota |
| 22 | PROVINSI | String | Nama provinsi |

## 🏗️ Struktur Keluarga

Setiap keluarga di-generate dengan struktur:

```
KELUARGA
├── Kepala Keluarga (L, 25-60 tahun)
├── Istri (P, usia kepala ±5 tahun) [jika menikah]
└── Anak (0-5 orang, usia sesuai rentang)
    ├── Anak 1
    ├── Anak 2
    └── ...
```

**Aturan:**
- Kepala Keluarga selalu laki-laki (kecuali janda)
- Istri ada jika status kawin
- Anak mengikuti agama orang tua
- Nama ayah/ibu anak = nama kepala keluarga & istri
- Semua anggota satu alamat (NKK sama)

## 🏃 Mode Processing

### Sequential Mode
- Cocok untuk < 10.000 keluarga
- Menggunakan 1 thread
- Memory usage rendah

### Parallel Mode
- Cocok untuk > 10.000 keluarga
- Multi-core processing
- 3-4x lebih cepat

### Streaming Mode
- Untuk jutaan record
- Write langsung ke CSV
- Hemat memory (tidak load ke RAM)

## 📊 Mode Distribusi

| Mode | Keterangan | Use Case |
|------|------------|----------|
| **1. Merata** | Setiap kelurahan dapat jumlah KK sama | Testing, data seimbang |
| **2. Merata Random** | Merata tapi jumlah per kelurahan acak | Simulasi natural |
| **3. Random** | Kelurahan dipilih acak sepenuhnya | Worst case testing |

## 📁 Struktur Project

```
generate-people/
├── data/
│   ├── provinces.csv      # 37 provinsi
│   ├── regencies.csv      # 514 kab/kota
│   ├── districts.csv      # 7,277 kecamatan
│   └── villages.csv       # 83,761 kelurahan
├── src/
│   ├── __init__.py
│   ├── main.py            # CLI entry point
│   ├── wilayah_loader.py  # Load & validasi wilayah
│   ├── reference_data.py  # Data referensi Indonesia
│   ├── id_generator.py    # NIK & NKK generator
│   ├── family_generator.py # Generate keluarga (sequential)
│   ├── parallel_generator.py # Generate keluarga (parallel)
│   ├── tempat_lahir.py    # Tempat lahir distribution
│   └── sql_exporter.py    # Export SQL multi-database
├── output/                # Hasil generate (auto-created)
├── requirements.txt
└── README.md
```

## 🔧 Penggunaan Programatik

### Basic Usage
```python
from src.family_generator import FamilyGenerator
from src.wilayah_loader import get_loader

# Initialize
loader = get_loader()
gen = FamilyGenerator(loader)

# Generate 100 keluarga di Kota Makassar
data = gen.generate_families('7371', 100)

# Hasil: list of dict
print(f"Generated {len(data)} records")
```

### Parallel Processing
```python
from src.parallel_generator import ParallelFamilyGenerator

gen = ParallelFamilyGenerator(loader, num_workers=8)
data = gen.generate_families_parallel(
    region_code='32',
    num_families=100000,
    distribution_mode=2
)
```

### Streaming Mode
```python
gen.generate_families_streaming(
    region_code='32',
    num_families=1000000,
    output_path='output/million.csv'
)
```

## 📈 Performance

| Jumlah KK | Mode | Waktu | Record/detik |
|-----------|------|-------|--------------|
| 1,000 | Sequential | ~2s | 2,000 |
| 10,000 | Sequential | ~15s | 2,600 |
| 10,000 | Parallel (8 core) | ~5s | 8,000 |
| 100,000 | Parallel (8 core) | ~45s | 9,000 |
| 1,000,000 | Streaming (8 core) | ~7min | 10,000 |

## ⚠️ Disclaimer

Data yang dihasilkan adalah **DUMMY/FAKE** untuk keperluan:
- Testing aplikasi
- Demo/presentasi
- Development
- Edukasi

**TIDAK BOLEH** digunakan untuk:
- Penipuan identitas
- Pemalsuan dokumen
- Kegiatan ilegal lainnya

## 📝 Lisensi

MIT License - Silakan digunakan untuk keperluan edukasi dan development.

## 🤝 Kontribusi

Pull requests welcome! Untuk perubahan besar, silakan buka issue dulu.

---

**Made with ❤️ for Indonesian developers**
