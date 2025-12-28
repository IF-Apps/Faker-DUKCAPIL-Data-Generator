"""
ID Generator Module
Generate NIK (Nomor Induk Kependudukan) and NKK (Nomor Kartu Keluarga)
"""

from datetime import date, datetime
from typing import Dict, Tuple
import threading


class IDGenerator:
    """
    Generate valid NIK and NKK numbers according to DUKCAPIL format
    
    NIK Format (16 digits): PPKKCC DDMMYY SSSS
    - PP: Province code (2 digits)
    - KK: Regency/City code (2 digits)  
    - CC: District code (2 digits)
    - DDMMYY: Birth date (DD+40 for female)
    - SSSS: Sequence number (4 digits)
    
    NKK Format (16 digits): PPKKCC DDMMYY SSSS
    - Same structure but date is KK issuance date
    """
    
    def __init__(self):
        # Track used NIKs and NKKs to avoid duplicates
        self._used_niks: set = set()
        self._used_nkks: set = set()
        
        # Sequence counters per district+date combination
        self._nik_sequences: Dict[str, int] = {}
        self._nkk_sequences: Dict[str, int] = {}
        
        # Thread lock for thread safety
        self._lock = threading.Lock()
    
    def generate_nik(
        self,
        province_code: str,
        regency_code: str,
        district_code: str,
        birth_date: date,
        gender: str
    ) -> str:
        """
        Generate a valid NIK
        
        Args:
            province_code: 2-digit province code
            regency_code: 2-digit regency code (from full code position 3-4)
            district_code: 2-digit district code (from full code position 5-6)
            birth_date: Date of birth
            gender: 'L' for male, 'P' for female
            
        Returns:
            16-digit NIK string
        """
        with self._lock:
            # Format date part
            day = birth_date.day
            if gender == 'P':  # Female: add 40 to day
                day += 40
            
            date_str = f"{day:02d}{birth_date.month:02d}{birth_date.year % 100:02d}"
            
            # Build base key for sequence tracking
            base_key = f"{province_code}{regency_code}{district_code}{date_str}"
            
            # Get next sequence number
            if base_key not in self._nik_sequences:
                self._nik_sequences[base_key] = 0
            
            # Find next available sequence
            while True:
                self._nik_sequences[base_key] += 1
                sequence = self._nik_sequences[base_key]
                
                if sequence > 9999:
                    # Reset and try with different approach
                    sequence = 1
                    self._nik_sequences[base_key] = 1
                
                nik = f"{province_code}{regency_code}{district_code}{date_str}{sequence:04d}"
                
                if nik not in self._used_niks:
                    self._used_niks.add(nik)
                    return nik
                
                # Safety check to avoid infinite loop
                if self._nik_sequences[base_key] > 9999:
                    raise ValueError(f"NIK sequence exhausted for {base_key}")
    
    def generate_nkk(
        self,
        province_code: str,
        regency_code: str,
        district_code: str,
        issue_date: date = None
    ) -> str:
        """
        Generate a valid NKK
        
        Args:
            province_code: 2-digit province code
            regency_code: 2-digit regency code
            district_code: 2-digit district code
            issue_date: Date of NKK issuance (defaults to today)
            
        Returns:
            16-digit NKK string
        """
        with self._lock:
            if issue_date is None:
                issue_date = date.today()
            
            date_str = f"{issue_date.day:02d}{issue_date.month:02d}{issue_date.year % 100:02d}"
            
            # Build base key for sequence tracking
            base_key = f"NKK_{province_code}{regency_code}{district_code}{date_str}"
            
            # Get next sequence number
            if base_key not in self._nkk_sequences:
                self._nkk_sequences[base_key] = 0
            
            # Find next available unique NKK (same pattern as NIK)
            while True:
                self._nkk_sequences[base_key] += 1
                sequence = self._nkk_sequences[base_key]
                
                if sequence > 9999:
                    raise ValueError(f"NKK sequence exhausted for {base_key}")
                
                nkk = f"{province_code}{regency_code}{district_code}{date_str}{sequence:04d}"
                
                if nkk not in self._used_nkks:
                    self._used_nkks.add(nkk)
                    return nkk
    
    def reset(self):
        """Reset all sequences and used NIKs/NKKs"""
        with self._lock:
            self._used_niks.clear()
            self._used_nkks.clear()
            self._nik_sequences.clear()
            self._nkk_sequences.clear()
    
    def get_stats(self) -> dict:
        """Get generator statistics"""
        return {
            'total_niks_generated': len(self._used_niks),
            'total_nkks_generated': len(self._used_nkks),
            'unique_nik_prefixes': len(self._nik_sequences),
            'unique_nkk_prefixes': len(self._nkk_sequences)
        }


def validate_nik(nik: str) -> Tuple[bool, str]:
    """
    Validate NIK format
    
    Args:
        nik: NIK string to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not nik:
        return False, "NIK kosong"
    
    if not nik.isdigit():
        return False, "NIK harus berupa angka"
    
    if len(nik) != 16:
        return False, f"NIK harus 16 digit, ditemukan {len(nik)} digit"
    
    # Extract components
    province_code = nik[0:2]
    regency_code = nik[2:4]
    district_code = nik[4:6]
    day = int(nik[6:8])
    month = int(nik[8:10])
    year = int(nik[10:12])
    sequence = int(nik[12:16])
    
    # Validate day (1-31 for male, 41-71 for female)
    if not ((1 <= day <= 31) or (41 <= day <= 71)):
        return False, f"Tanggal tidak valid: {day}"
    
    # Validate month
    if not (1 <= month <= 12):
        return False, f"Bulan tidak valid: {month}"
    
    # Validate sequence
    if not (1 <= sequence <= 9999):
        return False, f"Nomor urut tidak valid: {sequence}"
    
    return True, "NIK valid"


def parse_nik(nik: str) -> dict:
    """
    Parse NIK and extract information
    
    Args:
        nik: 16-digit NIK string
        
    Returns:
        Dictionary with parsed NIK components
    """
    is_valid, message = validate_nik(nik)
    if not is_valid:
        return {'valid': False, 'error': message}
    
    day = int(nik[6:8])
    gender = 'L' if day <= 31 else 'P'
    actual_day = day if day <= 31 else day - 40
    
    month = int(nik[8:10])
    year_2d = int(nik[10:12])
    
    # Determine full year (assume 1900s if > current year's last 2 digits)
    current_year_2d = datetime.now().year % 100
    if year_2d > current_year_2d:
        full_year = 1900 + year_2d
    else:
        full_year = 2000 + year_2d
    
    return {
        'valid': True,
        'province_code': nik[0:2],
        'regency_code': nik[2:4],
        'district_code': nik[4:6],
        'wilayah_code': nik[0:6],
        'birth_day': actual_day,
        'birth_month': month,
        'birth_year': full_year,
        'birth_date': f"{actual_day:02d}-{month:02d}-{full_year}",
        'gender': gender,
        'gender_name': 'Laki-laki' if gender == 'L' else 'Perempuan',
        'sequence': int(nik[12:16])
    }


# Singleton instance
_generator_instance = None

def get_generator() -> IDGenerator:
    """Get or create IDGenerator singleton instance"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = IDGenerator()
    return _generator_instance
