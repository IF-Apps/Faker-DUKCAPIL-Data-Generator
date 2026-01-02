#!/usr/bin/env python3
"""
Faker DUKCAPIL Data Generator - Main CLI
Generate Indonesian citizen data with DUKCAPIL format
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from typing import List, Optional
from multiprocessing import cpu_count

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.wilayah_loader import WilayahLoader, get_loader, load_nkk_simulasi
from src.family_generator import FamilyGenerator, generate_recap
from src.parallel_generator import ParallelFamilyGenerator, get_optimal_workers
from src.sql_exporter import SQLExporter, export_to_sql


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print application header"""
    print()
    print("=" * 55)
    print("         DUKCAPIL DATA GENERATOR v1.0")
    print("   Generate Data Penduduk Indonesia (Dummy)")
    print("=" * 55)
    print()


def get_input(prompt: str, valid_options: List[str] = None, allow_empty: bool = False) -> str:
    """Get validated user input"""
    while True:
        value = input(prompt).strip()
        
        if not value and not allow_empty:
            print("❌ Input tidak boleh kosong!")
            continue
        
        if valid_options and value not in valid_options:
            print(f"❌ Pilihan tidak valid. Pilih dari: {', '.join(valid_options)}")
            continue
        
        return value


def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Get validated integer input"""
    while True:
        try:
            value = int(input(prompt).strip())
            
            if min_val is not None and value < min_val:
                print(f"❌ Nilai minimal adalah {min_val}")
                continue
            
            if max_val is not None and value > max_val:
                print(f"❌ Nilai maksimal adalah {max_val}")
                continue
            
            return value
        except ValueError:
            print("❌ Masukkan angka yang valid!")


def validate_region_code(loader: WilayahLoader, code: str) -> tuple:
    """
    Validate region code and return info
    
    Returns:
        Tuple of (is_valid, info_dict or error_message)
    """
    is_valid, info = loader.validate_code(code)
    
    if is_valid:
        return True, info
    
    return False, f"Kode wilayah '{code}' tidak ditemukan"


def show_region_list(loader: WilayahLoader, level: str = 'province'):
    """Show list of available regions"""
    print()
    
    if level == 'province':
        print("Daftar Provinsi:")
        print("-" * 40)
        provinces = loader.list_provinces()
        for i, (code, name) in enumerate(provinces):
            print(f"  {code} - {name}")
            if (i + 1) % 10 == 0 and i < len(provinces) - 1:
                cont = input("\nTekan Enter untuk lanjut, atau 'q' untuk kembali: ").strip().lower()
                if cont == 'q':
                    break
    elif level == 'regency':
        print("Daftar Kabupaten/Kota (ketik kode provinsi untuk filter):")
        prov_code = input("Kode Provinsi (kosongkan untuk semua): ").strip()
        regencies = loader.list_regencies(prov_code if prov_code else None)
        
        print("-" * 50)
        for i, (code, name) in enumerate(regencies[:50]):  # Limit to 50
            print(f"  {code} - {name}")
        
        if len(regencies) > 50:
            print(f"\n... dan {len(regencies) - 50} lainnya")


def get_region_code(loader: WilayahLoader) -> tuple:
    """Get and validate region code from user"""
    while True:
        code = input("Masukkan kode wilayah: ").strip()
        
        if not code:
            print("❌ Kode wilayah tidak boleh kosong!")
            continue
        
        is_valid, result = validate_region_code(loader, code)
        
        if is_valid:
            info = result
            print()
            if info['level'] == 'provinsi':
                print(f"✓ {info['name']}")
                print(f"  ({info['regency_count']} kab/kota, {info['district_count']} kecamatan, {info['village_count']} kelurahan)")
            elif info['level'] == 'kabupaten/kota':
                print(f"✓ {info['name']}")
                print(f"  Provinsi: {info['province_name']}")
                print(f"  ({info['district_count']} kecamatan, {info['village_count']} kelurahan)")
            else:  # kecamatan
                print(f"✓ Kec. {info['name']}")
                print(f"  {info['regency_name']}, {info['province_name']}")
                print(f"  ({info['village_count']} kelurahan)")
            print()
            return code, info
        
        print(f"\n❌ {result}")
        print("\nPilih opsi:")
        print("  1. Coba lagi")
        print("  2. Lihat daftar provinsi")
        print("  3. Lihat daftar kabupaten/kota")
        
        choice = get_input("Pilihan [1-3]: ", ['1', '2', '3'])
        
        if choice == '2':
            show_region_list(loader, 'province')
        elif choice == '3':
            show_region_list(loader, 'regency')
        print()


def get_distribution_mode() -> tuple:
    """
    Get distribution mode from user
    
    Returns:
        Tuple of (mode, correction_percent, simulation_data)
        - mode: 1-4
        - correction_percent: Only for mode 4, otherwise 0
        - simulation_data: Only for mode 4, otherwise None
    """
    print("Pilih distribusi keluarga:")
    print("  1. Merata (setiap kelurahan dapat jumlah KK sama)")
    print("  2. Merata dengan jumlah KK acak per kelurahan")
    print("  3. Random (kelurahan dipilih secara acak)")
    print("  4. Simulasi (berdasarkan file data/Kelurahan-nkk-simulasi.csv)")
    
    choice = get_input("Pilihan [1-4]: ", ['1', '2', '3', '4'])
    mode = int(choice)
    
    if mode == 4:
        # Load simulation data
        try:
            simulation_data = load_nkk_simulasi()
            print(f"\n✓ Data simulasi loaded: {len(simulation_data)} kelurahan")
        except FileNotFoundError as e:
            print(f"\n❌ {e}")
            print("Kembali ke mode distribusi merata.")
            return 1, 0, None
        
        # Ask for correction percentage
        print("\nMasukkan persentase koreksi jumlah KK:")
        print("  -100 = 0% (tidak ada KK)")
        print("     0 = 100% (sesuai data simulasi)")
        print("   100 = 200% (dua kali lipat)")
        print("  1000 = 1100% (sebelas kali lipat)")
        
        correction = get_int_input("Koreksi [-100 s/d 1000]: ", min_val=-100, max_val=1000)
        
        return mode, correction, simulation_data
    
    return mode, 0, None


def get_processing_mode() -> tuple:
    """Get processing mode (sequential or parallel) from user"""
    print("\nPilih mode processing:")
    print(f"  1. Sequential (single thread)")
    print(f"  2. Parallel (multi-core, optimal untuk jumlah besar)")
    
    choice = get_input("Pilihan [1-2]: ", ['1', '2'])
    
    if choice == '2':
        optimal = get_optimal_workers()
        print(f"\n  Jumlah CPU core: {cpu_count()}")
        print(f"  Rekomendasi workers: {optimal}")
        print(f"  Masukkan jumlah workers (kosongkan untuk default {optimal}): ", end="")
        worker_input = input().strip()
        
        if worker_input:
            try:
                num_workers = int(worker_input)
                if num_workers < 1:
                    num_workers = 1
                elif num_workers > cpu_count():
                    print(f"  ⚠ Lebih dari CPU count, menggunakan {cpu_count()}")
                    num_workers = cpu_count()
            except ValueError:
                num_workers = optimal
        else:
            num_workers = optimal
        
        # Ask for streaming mode for large datasets
        print("\n  Gunakan streaming mode (hemat memory untuk jutaan record)?")
        streaming = input("  [y/N]: ").strip().lower()
        use_streaming = streaming in ['y', 'yes', 'ya']
        
        return 'parallel', num_workers, use_streaming
    
    return 'sequential', 1, False


def get_output_format() -> tuple:
    """Get output format from user"""
    print("\nPilih format output:")
    print("  1. CSV")
    print("  2. Excel")
    print("  3. JSON")
    print("  4. Semua format (CSV, Excel, JSON)")
    
    choice = get_input("Pilihan [1-4]: ", ['1', '2', '3', '4'])
    format_choice = int(choice)
    
    # Ask for column name case
    print("\nPilih format nama kolom:")
    print("  1. UPPERCASE (NKK, NIK, NAMA, ...)")
    print("  2. lowercase (nkk, nik, nama, ...)")
    
    case_choice = get_input("Pilihan [1-2]: ", ['1', '2'])
    use_lowercase = (case_choice == '2')
    
    return format_choice, use_lowercase


def get_sql_options() -> Optional[tuple]:
    """Get SQL export options from user"""
    print()
    sql_choice = input("Export SQL? [Y/n]: ").strip().lower()
    
    if sql_choice in ['n', 'no', 'tidak']:
        return None
    
    print("\n=== Opsi SQL ===")
    print("Pilih jenis database:")
    
    db_options = SQLExporter.get_database_options()
    for num, _, name in db_options:
        print(f"  {num}. {name}")
    
    db_choice = get_int_input("Pilihan [1-6]: ", 1, 6)
    db_type = db_options[db_choice - 1][1]
    
    print("\nPilih isi SQL:")
    mode_options = SQLExporter.get_mode_options()
    for num, _, desc in mode_options:
        print(f"  {num}. {desc}")
    print("  4. Semua (Structure, Data, Structure+Data)")
    
    mode_choice = get_int_input("Pilihan [1-4]: ", 1, 4)
    
    return db_type, mode_choice


def save_outputs(
    data: List[dict],
    output_format: int,
    sql_options: Optional[tuple],
    region_code: str,
    output_dir: str
) -> List[str]:
    """
    Save data to specified formats
    
    Returns:
        List of saved file paths
    """
    saved_files = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = f"dukcapil_{region_code}_{timestamp}"
    
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert to DataFrame for easy export
    df = pd.DataFrame(data)
    
    # Save CSV
    if output_format in [1, 4]:
        csv_path = os.path.join(output_dir, f"{base_name}.csv")
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        saved_files.append(csv_path)
    
    # Save Excel
    if output_format in [2, 4]:
        xlsx_path = os.path.join(output_dir, f"{base_name}.xlsx")
        df.to_excel(xlsx_path, index=False, engine='openpyxl')
        saved_files.append(xlsx_path)
    
    # Save JSON
    if output_format in [3, 4]:
        json_path = os.path.join(output_dir, f"{base_name}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        saved_files.append(json_path)
    
    # Save SQL
    if sql_options:
        db_type, mode = sql_options
        
        if mode == 4:  # Semua mode
            # Generate all 3 SQL modes
            mode_suffixes = {
                1: 'structure',
                2: 'data', 
                3: 'full'
            }
            for m, suffix in mode_suffixes.items():
                sql_content = export_to_sql(data, db_type, m)
                sql_path = os.path.join(output_dir, f"{base_name}_{db_type}_{suffix}.sql")
                with open(sql_path, 'w', encoding='utf-8') as f:
                    f.write(sql_content)
                saved_files.append(sql_path)
        else:
            sql_content = export_to_sql(data, db_type, mode)
            sql_path = os.path.join(output_dir, f"{base_name}_{db_type}.sql")
            with open(sql_path, 'w', encoding='utf-8') as f:
                f.write(sql_content)
            saved_files.append(sql_path)
    
    return saved_files


def main():
    """Main application entry point"""
    clear_screen()
    print_header()
    
    # Initialize loader
    print("Loading data wilayah...")
    try:
        loader = get_loader()
        print(f"✓ Data loaded: {len(loader.provinces)} provinsi, {len(loader.regencies)} kab/kota")
        print(f"  {len(loader.districts)} kecamatan, {len(loader.villages)} kelurahan")
        
        # Show RT/RW coverage
        rt_rw_coverage = loader.get_rt_rw_coverage()
        if rt_rw_coverage['total_records'] > 0:
            print(f"✓ RT/RW data: {rt_rw_coverage['total_records']:,} records, "
                  f"{rt_rw_coverage['kelurahan_with_data']:,} kelurahan")
            print(f"  {rt_rw_coverage['records_with_coordinates']:,} records dengan koordinat")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)
    
    print()
    
    # Get region code
    region_code, region_info = get_region_code(loader)
    
    # Get distribution mode (returns tuple for mode 4)
    distribution_mode, correction_percent, simulation_data = get_distribution_mode()
    
    # For mode 4, we don't need num_families input - calculate from simulation data
    if distribution_mode == 4 and simulation_data:
        # Get villages for this region to calculate preview
        villages = loader.get_sub_regions(region_code)
        village_codes = {v['village_code'] for v in villages}
        
        # Calculate matched villages and totals
        matched_villages = []
        total_base = 0
        total_corrected = 0
        
        for village in villages:
            vc = village['village_code']
            if vc in simulation_data:
                base_count = simulation_data[vc]
                corrected_count = int(base_count * (1 + correction_percent / 100))
                if corrected_count > 0:
                    matched_villages.append({
                        'code': vc,
                        'name': village.get('village_name', vc),
                        'base': base_count,
                        'corrected': corrected_count
                    })
                    total_base += base_count
                    total_corrected += corrected_count
        
        # Show preview
        print()
        print("=" * 55)
        print("           PREVIEW SIMULASI")
        print("=" * 55)
        print(f"  Kelurahan di wilayah       : {len(villages)}")
        print(f"  Kelurahan dalam simulasi   : {len(matched_villages)}")
        print(f"  Kelurahan tidak termasuk   : {len(villages) - len(matched_villages)}")
        print()
        print(f"  Total KK (data simulasi)   : {total_base:,}")
        print(f"  Koreksi                    : {correction_percent:+d}%")
        print(f"  Total KK (setelah koreksi) : {total_corrected:,}")
        print("=" * 55)
        
        if len(matched_villages) == 0:
            print("\n❌ Tidak ada kelurahan yang cocok dengan data simulasi!")
            print("   Pastikan file data/Kelurahan-nkk-simulasi.csv berisi")
            print(f"   kode kelurahan untuk wilayah {region_code}")
            sys.exit(1)
        
        # Ask for confirmation
        print()
        confirm = input("Lanjutkan generate? [Y/n]: ").strip().lower()
        if confirm in ['n', 'no', 'tidak']:
            print("\n👋 Dibatalkan.")
            sys.exit(0)
        
        num_families = total_corrected  # Use corrected total
        print()
    else:
        # Get number of families (no upper limit) for non-simulation modes
        num_families = get_int_input("Masukkan jumlah keluarga: ", min_val=1)
        print()
    
    # Get processing mode
    proc_mode, num_workers, use_streaming = get_processing_mode()
    
    # Get output format
    output_format, use_lowercase = get_output_format()
    
    # Get SQL options
    sql_options = get_sql_options()
    
    print()
    print("-" * 55)
    
    # Prepare output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = f"dukcapil_{region_code}_{timestamp}"
    
    # Generate data
    try:
        if proc_mode == 'parallel':
            print(f"\n🚀 Mode: Parallel ({num_workers} workers)")
            generator = ParallelFamilyGenerator(loader, num_workers=num_workers)
            
            if use_streaming:
                # Streaming mode - writes directly to CSV
                csv_path = os.path.join(output_dir, f"{base_name}.csv")
                generator.generate_families_streaming(
                    region_code=region_code,
                    num_families=num_families,
                    output_path=csv_path,
                    distribution_mode=distribution_mode,
                    show_progress=True,
                    simulation_data=simulation_data,
                    correction_percent=correction_percent
                )
                
                # Read CSV back for other formats if needed
                if output_format in [2, 3, 4] or sql_options:
                    print("\n📖 Loading data untuk konversi format lain...")
                    # Specify dtype for LATITUDE/LONGITUDE to avoid mixed type warning
                    data = pd.read_csv(csv_path, dtype={
                        'LATITUDE': 'float64',
                        'LONGITUDE': 'float64'
                    }, low_memory=False).to_dict('records')
                else:
                    data = None
                    
                # Mark CSV as already saved
                streaming_csv_saved = True
            else:
                # In-memory mode
                data = generator.generate_families_parallel(
                    region_code=region_code,
                    num_families=num_families,
                    distribution_mode=distribution_mode,
                    show_progress=True,
                    simulation_data=simulation_data,
                    correction_percent=correction_percent
                )
                streaming_csv_saved = False
        else:
            print("\n📝 Mode: Sequential")
            generator = FamilyGenerator(loader)
            data = generator.generate_families(
                region_code=region_code,
                num_families=num_families,
                distribution_mode=distribution_mode,
                show_progress=True,
                simulation_data=simulation_data,
                correction_percent=correction_percent
            )
            streaming_csv_saved = False
    except Exception as e:
        print(f"\n❌ Error generating data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Save outputs
    saved_files = []
    
    # Helper function to convert keys to lowercase
    def convert_keys_lowercase(records):
        return [{k.lower(): v for k, v in record.items()} for record in records]
    
    # Handle streaming CSV case
    if proc_mode == 'parallel' and use_streaming and streaming_csv_saved:
        if output_format in [1, 4]:
            # If lowercase needed, read and rewrite the CSV
            if use_lowercase:
                import pandas as pd
                df_temp = pd.read_csv(csv_path)
                df_temp.columns = [c.lower() for c in df_temp.columns]
                df_temp.to_csv(csv_path, index=False, encoding='utf-8-sig')
            saved_files.append(csv_path)
    
    # Save other formats if we have data in memory
    if data is not None:
        # Convert to lowercase if needed
        if use_lowercase:
            data = convert_keys_lowercase(data)
        
        # CSV (if not already saved via streaming)
        if output_format in [1, 4] and not streaming_csv_saved:
            df = pd.DataFrame(data)
            csv_path = os.path.join(output_dir, f"{base_name}.csv")
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            saved_files.append(csv_path)
        
        # Excel
        if output_format in [2, 4]:
            df = pd.DataFrame(data) if 'df' not in dir() else df
            xlsx_path = os.path.join(output_dir, f"{base_name}.xlsx")
            df.to_excel(xlsx_path, index=False, engine='openpyxl')
            saved_files.append(xlsx_path)
        
        # JSON
        if output_format in [3, 4]:
            json_path = os.path.join(output_dir, f"{base_name}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            saved_files.append(json_path)
        
        # SQL
        if sql_options:
            db_type, mode = sql_options
            
            if mode == 4:  # Semua mode
                # Generate all 3 SQL modes
                mode_suffixes = {
                    1: 'structure',
                    2: 'data', 
                    3: 'full'
                }
                for m, suffix in mode_suffixes.items():
                    sql_content = export_to_sql(data, db_type, m)
                    sql_path = os.path.join(output_dir, f"{base_name}_{db_type}_{suffix}.sql")
                    with open(sql_path, 'w', encoding='utf-8') as f:
                        f.write(sql_content)
                    saved_files.append(sql_path)
            else:
                sql_content = export_to_sql(data, db_type, mode)
                sql_path = os.path.join(output_dir, f"{base_name}_{db_type}.sql")
                with open(sql_path, 'w', encoding='utf-8') as f:
                    f.write(sql_content)
                saved_files.append(sql_path)
    
    # Print saved files
    print()
    print("✓ Output tersimpan di:")
    for filepath in saved_files:
        print(f"  - {filepath}")
    
    # Print recap
    stats = generator.get_statistics()
    region_name = region_info['name']
    recap = generate_recap(stats, region_name, region_code)
    print(recap)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Dibatalkan oleh user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
