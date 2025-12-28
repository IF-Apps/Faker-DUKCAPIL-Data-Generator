# DUKCAPIL Data Generator - AI Coding Instructions

## Project Overview

Python CLI application for generating realistic Indonesian citizen data (NIK, NKK, family relationships) following official DUKCAPIL format. Data includes 100% unique NIK identifiers, consistent family relationships, and demographically accurate distributions based on BPS (Badan Pusat Statistik) census data.

## Architecture

```
src/
├── main.py              # CLI entry point - interactive prompts & CLI args
├── family_generator.py  # Sequential family generation with relationships
├── parallel_generator.py # Multi-process generation for millions of records
├── id_generator.py      # NIK/NKK generation with uniqueness guarantee
├── wilayah_loader.py    # Regional data loader (CSV → in-memory dicts)
├── reference_data.py    # Static data: names, occupations, religions (BPS-weighted)
├── tempat_lahir.py      # Birth place distribution logic
└── sql_exporter.py      # Multi-database SQL export (Oracle, PostgreSQL, MySQL, etc.)
```

**Data flow**: `main.py` → `WilayahLoader` (loads CSVs) → `FamilyGenerator`/`ParallelFamilyGenerator` → `SQLExporter` → output files

## Key Patterns

### NIK/NKK Uniqueness Guarantee
- `IDGenerator` uses thread-safe sequence tracking with `threading.Lock()`
- Both NIK and NKK are tracked in `_used_niks` and `_used_nkks` sets to guarantee 100% uniqueness
- `ProcessLocalIDGenerator` in parallel mode uses worker-specific sequence ranges (`worker_id * 1000 + local_seq`)
- Never generate NIK/NKK manually; always use `id_generator.generate_nik()` and `id_generator.generate_nkk()`

### Family Consistency
All family members share:
- Same NKK (via `generate_nkk()` called once per family)
- Same religion (drawn once, applied to all members)
- Same address (RT/RW/alamat) and village
- Parent names used consistently for children's `NAMA_AYAH`/`NAMA_IBU`

### NKK Consistency Rules (Enforced)
**Business Rules**: Every NKK must have:
1. Exactly 1 member with `STATUS_HUBUNGAN = 'Kepala Keluarga'`
2. All members with the same `AGAMA`
3. All members with the same address (ALAMAT, RT, RW, KODE_KELURAHAN, etc.)

**Two-layer validation with auto-fix:**
1. **Per-family assertion** (`_validate_and_fix_single_family()`) - validates immediately after each family is generated
2. **Post-generation validation** (`validate_and_fix_families()`) - final check on all data before output

**Auto-fix behavior (with logging):**

| Issue | Auto-fix Action |
|-------|-----------------|
| NKK with 0 Kepala Keluarga | Oldest male (or oldest member) promoted to Kepala Keluarga |
| NKK with >1 Kepala Keluarga | First one kept, others changed to "Famili Lain" |
| Different AGAMA in NKK | All members set to Kepala Keluarga's AGAMA |
| Different address in NKK | All members set to Kepala Keluarga's address |

All fixes are logged with `logger.warning()` for debugging.

### Weighted Random Selection
All demographic data uses weighted distributions from `reference_data.py`:
```python
# Example: get_random_agama() uses AGAMA_WEIGHTS from BPS 2020 census
random.choices(AGAMA, weights=AGAMA_WEIGHTS, k=1)[0]
```

### Regional Data
- CSV files in `data/` use semicolon (`;`) delimiter
- Hierarchy: provinces → regencies → districts → villages (via `*_id` foreign keys)
- Optional RT/RW + GPS coordinates from `koordinat_rt_rw.csv`

## Running the Application

```bash
# Interactive mode (recommended)
python src/main.py

# CLI mode with arguments
python src/main.py --region 7371 --families 1000 --format csv --parallel --workers 4
```

## Adding New Fields

1. Add column to `SQLExporter.COLUMNS` in [sql_exporter.py](src/sql_exporter.py)
2. Add data source in `reference_data.py` with realistic weights
3. Generate value in `_generate_person()` method (both `family_generator.py` and `parallel_generator.py`)
4. Include in person dict returned by generators

## Modifying Distributions

All statistical weights are in [reference_data.py](src/reference_data.py):
- `AGAMA_WEIGHTS` - Religion (BPS 2020)
- `PENDIDIKAN_WEIGHTS` - Education levels (Susenas 2023)
- `PEKERJAAN_WEIGHTS` - Occupations (Sakernas 2023)
- Name pools organized by religion (e.g., `NAMA_PRIA_ISLAM`, `NAMA_WANITA_HINDU`)

## Testing Data Generation

Generate small samples first to validate:
```bash
python src/main.py --region 7371 --families 10 --format csv
```

Check output in `output/` directory for:
- NIK uniqueness (16 digits, women have DD+40)
- NKK consistency within families
- Parent-child age gaps (17-45 years)

## Database Export

SQL exporter supports: `oracle`, `postgresql`, `mariadb`, `mysql`, `sqlserver`, `sqlite`

Export modes: structure-only, data-only, or combined (via `SQLExporter.STRUCTURE_AND_DATA`)
