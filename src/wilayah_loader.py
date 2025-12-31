"""
Wilayah Loader Module
Load and manage Indonesian regional data from CSV files
"""

import os
import csv
import random
from typing import Dict, List, Optional, Tuple


class WilayahLoader:
    """Load and manage Indonesian regional hierarchy data"""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize WilayahLoader with data directory
        
        Args:
            data_dir: Path to directory containing CSV files
        """
        if data_dir is None:
            # Default to data folder relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        
        self.data_dir = data_dir
        self.provinces: Dict[str, str] = {}
        self.regencies: Dict[str, dict] = {}
        self.districts: Dict[str, dict] = {}
        self.villages: Dict[str, dict] = {}
        self.rt_rw_data: Dict[str, List[dict]] = {}  # kelurahan_kode -> list of RT/RW records
        
        self._load_data()
    
    def _load_data(self):
        """Load all CSV data files"""
        self._load_provinces()
        self._load_regencies()
        self._load_districts()
        self._load_villages()
        self._load_rt_rw()
    
    def _load_provinces(self):
        """Load provinces from CSV"""
        filepath = os.path.join(self.data_dir, 'provinces.csv')
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                code = row['id'].strip()
                name = row['name'].strip().strip('"')
                self.provinces[code] = name
    
    def _load_regencies(self):
        """Load regencies (kabupaten/kota) from CSV"""
        filepath = os.path.join(self.data_dir, 'regencies.csv')
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                code = row['id'].strip()
                province_id = row['province_id'].strip()
                name = row['name'].strip().strip('"')
                self.regencies[code] = {
                    'name': name,
                    'province_id': province_id
                }
    
    def _load_districts(self):
        """Load districts (kecamatan) from CSV"""
        filepath = os.path.join(self.data_dir, 'districts.csv')
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                code = row['id'].strip()
                regency_id = row['regency_id'].strip()
                name = row['name'].strip().strip('"')
                self.districts[code] = {
                    'name': name,
                    'regency_id': regency_id
                }
    
    def _load_villages(self):
        """Load villages (kelurahan/desa) from CSV"""
        filepath = os.path.join(self.data_dir, 'villages.csv')
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                code = row['id'].strip()
                district_id = row['district_id'].strip()
                name = row['name'].strip().strip('"')
                self.villages[code] = {
                    'name': name,
                    'district_id': district_id
                }
    
    def _load_rt_rw(self):
        """Load RT/RW coordinate data from CSV if available"""
        filepath = os.path.join(self.data_dir, 'koordinat_rt_rw.csv')
        if not os.path.exists(filepath):
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                kelurahan_kode = row.get('kelurahan_kode', '').strip()
                if not kelurahan_kode:
                    continue
                
                # Parse coordinates - skip invalid ones ("." or empty)
                lat_str = row.get('rt_latitude', '').strip()
                lon_str = row.get('rt_longitude', '').strip()
                
                latitude = None
                longitude = None
                
                if lat_str and lat_str != '.' and lon_str and lon_str != '.':
                    try:
                        latitude = float(lat_str)
                        longitude = float(lon_str)
                    except ValueError:
                        pass  # Keep as None if invalid
                
                # Parse jalan and lorong
                jalan = row.get('meliputi_jalan', '').strip()
                lorong = row.get('meliputi_lorong', '').strip()
                
                # Parse jalan/lorong into lists (split by &)
                jalan_list = self._parse_multi_value(jalan)
                lorong_list = self._parse_multi_value(lorong)
                
                rt_rw_record = {
                    'kode': row.get('kode', '').strip(),
                    'kelurahan_kode': kelurahan_kode,
                    'rw': row.get('rw', '').strip().zfill(3),
                    'rt': row.get('rt', '').strip().zfill(3),
                    'jalan_list': jalan_list,
                    'lorong_list': lorong_list,
                    'latitude': latitude,
                    'longitude': longitude
                }
                
                if kelurahan_kode not in self.rt_rw_data:
                    self.rt_rw_data[kelurahan_kode] = []
                self.rt_rw_data[kelurahan_kode].append(rt_rw_record)
    
    def _parse_multi_value(self, value: str) -> list:
        """Parse value that may contain multiple items separated by &"""
        if not value:
            return []
        
        # Split by & and clean each part
        parts = [p.strip() for p in value.split('&')]
        # Filter out empty strings
        return [p for p in parts if p]
    
    def _build_alamat(self, jalan: str, lorong: str) -> str:
        """Build street address from jalan and lorong"""
        parts = []
        
        if jalan:
            # Clean up jalan name
            jalan_clean = jalan.strip()
            if jalan_clean:
                parts.append(jalan_clean)
        
        if lorong:
            # Clean up lorong
            lorong_clean = lorong.strip()
            if lorong_clean:
                # Add "Lorong" prefix if not already present
                if not lorong_clean.upper().startswith('LORONG') and not lorong_clean.upper().startswith('LR'):
                    lorong_clean = f"Lorong {lorong_clean}"
                parts.append(lorong_clean)
        
        if parts:
            return ', '.join(parts)
        return ''
    
    def get_rt_rw_data(self, kelurahan_kode: str) -> Optional[dict]:
        """
        Get random RT/RW data for a kelurahan
        
        Args:
            kelurahan_kode: 10-digit kelurahan code
            
        Returns:
            Dict with rt, rw, alamat, latitude, longitude or None if not available
        """
        records = self.rt_rw_data.get(kelurahan_kode, [])
        if not records:
            return None
        
        record = random.choice(records)
        
        # Pick one random jalan and lorong (if multiple exist)
        jalan = random.choice(record['jalan_list']) if record['jalan_list'] else ''
        lorong = random.choice(record['lorong_list']) if record['lorong_list'] else ''
        
        # Build alamat dynamically
        alamat = self._build_alamat(jalan, lorong)
        
        return {
            'rt': record['rt'],
            'rw': record['rw'],
            'alamat': alamat,
            'latitude': record['latitude'],
            'longitude': record['longitude']
        }
    
    def get_rt_rw_coverage(self) -> dict:
        """
        Get RT/RW data coverage statistics
        
        Returns:
            Dict with coverage statistics
        """
        total_records = sum(len(records) for records in self.rt_rw_data.values())
        kelurahan_count = len(self.rt_rw_data)
        
        # Count records with valid coordinates
        records_with_coords = 0
        for records in self.rt_rw_data.values():
            for record in records:
                if record['latitude'] is not None and record['longitude'] is not None:
                    records_with_coords += 1
        
        return {
            'total_records': total_records,
            'kelurahan_with_data': kelurahan_count,
            'records_with_coordinates': records_with_coords,
            'total_kelurahan': len(self.villages)
        }
    
    def has_rt_rw_data(self, kelurahan_kode: str) -> bool:
        """Check if kelurahan has RT/RW data available"""
        return kelurahan_kode in self.rt_rw_data
    
    def validate_code(self, code: str) -> Tuple[bool, Optional[dict]]:
        """
        Validate a regional code and return its info
        
        Args:
            code: Regional code (2, 4, or 6 digits)
            
        Returns:
            Tuple of (is_valid, info_dict)
        """
        code = str(code).strip()
        
        # Check province (2 digits)
        if len(code) == 2:
            if code in self.provinces:
                # Count sub-regions
                regencies = [r for r in self.regencies if self.regencies[r]['province_id'] == code]
                districts = [d for d in self.districts if self.districts[d]['regency_id'] in regencies]
                villages = [v for v in self.villages if self.villages[v]['district_id'] in districts]
                
                return True, {
                    'level': 'provinsi',
                    'code': code,
                    'name': self.provinces[code],
                    'regency_count': len(regencies),
                    'district_count': len(districts),
                    'village_count': len(villages)
                }
        
        # Check regency (4 digits)
        elif len(code) == 4:
            if code in self.regencies:
                regency = self.regencies[code]
                province_code = regency['province_id']
                
                districts = [d for d in self.districts if self.districts[d]['regency_id'] == code]
                villages = [v for v in self.villages if self.villages[v]['district_id'] in districts]
                
                return True, {
                    'level': 'kabupaten/kota',
                    'code': code,
                    'name': regency['name'],
                    'province_code': province_code,
                    'province_name': self.provinces.get(province_code, ''),
                    'district_count': len(districts),
                    'village_count': len(villages)
                }
        
        # Check district (6 digits)
        elif len(code) == 6:
            if code in self.districts:
                district = self.districts[code]
                regency_code = district['regency_id']
                regency = self.regencies.get(regency_code, {})
                province_code = regency.get('province_id', '')
                
                villages = [v for v in self.villages if self.villages[v]['district_id'] == code]
                
                return True, {
                    'level': 'kecamatan',
                    'code': code,
                    'name': district['name'],
                    'regency_code': regency_code,
                    'regency_name': regency.get('name', ''),
                    'province_code': province_code,
                    'province_name': self.provinces.get(province_code, ''),
                    'village_count': len(villages)
                }
        
        return False, None
    
    def get_sub_regions(self, code: str) -> List[dict]:
        """
        Get all villages under a given regional code
        
        Args:
            code: Regional code (2, 4, or 6 digits)
            
        Returns:
            List of village info dicts with full hierarchy
        """
        code = str(code).strip()
        villages_list = []
        
        if len(code) == 2:
            # Province level - get all villages in province
            for reg_code, regency in self.regencies.items():
                if regency['province_id'] == code:
                    for dist_code, district in self.districts.items():
                        if district['regency_id'] == reg_code:
                            for vil_code, village in self.villages.items():
                                if village['district_id'] == dist_code:
                                    villages_list.append(self._build_village_info(vil_code))
        
        elif len(code) == 4:
            # Regency level - get all villages in regency
            for dist_code, district in self.districts.items():
                if district['regency_id'] == code:
                    for vil_code, village in self.villages.items():
                        if village['district_id'] == dist_code:
                            villages_list.append(self._build_village_info(vil_code))
        
        elif len(code) == 6:
            # District level - get all villages in district
            for vil_code, village in self.villages.items():
                if village['district_id'] == code:
                    villages_list.append(self._build_village_info(vil_code))
        
        return villages_list
    
    def _build_village_info(self, village_code: str) -> dict:
        """Build complete village info with hierarchy"""
        village = self.villages[village_code]
        district_code = village['district_id']
        district = self.districts[district_code]
        regency_code = district['regency_id']
        regency = self.regencies[regency_code]
        province_code = regency['province_id']
        
        return {
            'village_code': village_code,
            'village_name': village['name'],
            'district_code': district_code,
            'district_name': district['name'],
            'regency_code': regency_code,
            'regency_name': regency['name'],
            'province_code': province_code,
            'province_name': self.provinces[province_code]
        }
    
    def list_provinces(self) -> List[Tuple[str, str]]:
        """List all provinces with their codes"""
        return sorted([(code, name) for code, name in self.provinces.items()], key=lambda x: x[0])
    
    def list_regencies(self, province_code: str = None) -> List[Tuple[str, str]]:
        """List regencies, optionally filtered by province"""
        result = []
        for code, data in self.regencies.items():
            if province_code is None or data['province_id'] == province_code:
                result.append((code, data['name']))
        return sorted(result, key=lambda x: x[0])
    
    def list_districts(self, regency_code: str = None) -> List[Tuple[str, str]]:
        """List districts, optionally filtered by regency"""
        result = []
        for code, data in self.districts.items():
            if regency_code is None or data['regency_id'] == regency_code:
                result.append((code, data['name']))
        return sorted(result, key=lambda x: x[0])
    
    def get_province_name(self, code: str) -> str:
        """Get province name by code"""
        return self.provinces.get(code, '')
    
    def get_regency_name(self, code: str) -> str:
        """Get regency name by code"""
        regency = self.regencies.get(code, {})
        return regency.get('name', '')
    
    def get_district_name(self, code: str) -> str:
        """Get district name by code"""
        district = self.districts.get(code, {})
        return district.get('name', '')
    
    def get_village_name(self, code: str) -> str:
        """Get village name by code"""
        village = self.villages.get(code, {})
        return village.get('name', '')
    
    def get_nik_codes(self, village_code: str) -> Tuple[str, str, str]:
        """
        Get province, regency, district codes for NIK generation
        Returns 2-digit codes for each level
        
        Args:
            village_code: Full village code (10 digits)
            
        Returns:
            Tuple of (province_code_2d, regency_code_2d, district_code_2d)
        """
        village = self.villages.get(village_code, {})
        district_code = village.get('district_id', '')
        district = self.districts.get(district_code, {})
        regency_code = district.get('regency_id', '')
        regency = self.regencies.get(regency_code, {})
        province_code = regency.get('province_id', '')
        
        # Extract 2-digit codes
        prov_2d = province_code[:2] if province_code else '00'
        reg_2d = regency_code[2:4] if len(regency_code) >= 4 else '00'
        dist_2d = district_code[4:6] if len(district_code) >= 6 else '00'
        
        return prov_2d, reg_2d, dist_2d


# Singleton instance for easy import
_loader_instance = None

def get_loader(data_dir: str = None) -> WilayahLoader:
    """Get or create WilayahLoader singleton instance"""
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = WilayahLoader(data_dir)
    return _loader_instance


def load_nkk_simulasi(data_dir: str = None) -> Dict[str, int]:
    """
    Load NKK simulation data from CSV file.
    
    Format CSV: kode,nkk (with header)
    
    Args:
        data_dir: Path to data directory containing Kelurahan-nkk-simulasi.csv
        
    Returns:
        Dict mapping village_code to NKK count
    """
    if data_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    
    filepath = os.path.join(data_dir, 'Kelurahan-nkk-simulasi.csv')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File simulasi tidak ditemukan: {filepath}")
    
    simulation_data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # Use DictReader to handle header
        for row in reader:
            village_code = row['kode'].strip()
            try:
                nkk_count = int(row['nkk'].strip())
                simulation_data[village_code] = nkk_count
            except (ValueError, KeyError):
                continue  # Skip invalid rows
    
    return simulation_data
