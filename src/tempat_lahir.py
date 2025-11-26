"""
Tempat Lahir (Birth Place) Module
Generate varied birth places for Indonesian citizens
"""

import random
from typing import Dict, List


# ============================================================================
# PROVINSI TETANGGA (Neighboring Provinces)
# Based on geographical borders of Indonesian provinces
# ============================================================================
PROVINSI_TETANGGA: Dict[str, List[str]] = {
    # SUMATERA
    '11': ['12', '13'],  # Aceh -> Sumut, Sumbar
    '12': ['11', '13', '14', '21'],  # Sumut -> Aceh, Sumbar, Riau, Kepri
    '13': ['12', '14', '15', '16'],  # Sumbar -> Sumut, Riau, Jambi, Sumsel
    '14': ['12', '13', '15', '21'],  # Riau -> Sumut, Sumbar, Jambi, Kepri
    '15': ['13', '14', '16', '17'],  # Jambi -> Sumbar, Riau, Sumsel, Bengkulu
    '16': ['13', '15', '17', '18', '19'],  # Sumsel -> Sumbar, Jambi, Bengkulu, Lampung, Babel
    '17': ['15', '16', '18'],  # Bengkulu -> Jambi, Sumsel, Lampung
    '18': ['16', '17', '31', '36'],  # Lampung -> Sumsel, Bengkulu, DKI, Banten
    '19': ['16'],  # Babel -> Sumsel
    '21': ['12', '14'],  # Kepri -> Sumut, Riau
    
    # JAWA
    '31': ['32', '36'],  # DKI -> Jabar, Banten
    '32': ['31', '33', '36'],  # Jabar -> DKI, Jateng, Banten
    '33': ['32', '34', '35'],  # Jateng -> Jabar, DIY, Jatim
    '34': ['33'],  # DIY -> Jateng
    '35': ['33', '51'],  # Jatim -> Jateng, Bali
    '36': ['18', '31', '32'],  # Banten -> Lampung, DKI, Jabar
    
    # BALI & NUSA TENGGARA
    '51': ['35', '52'],  # Bali -> Jatim, NTB
    '52': ['51', '53'],  # NTB -> Bali, NTT
    '53': ['52'],  # NTT -> NTB
    
    # KALIMANTAN
    '61': ['62', '63'],  # Kalbar -> Kalteng, Kalsel
    '62': ['61', '63', '64', '65'],  # Kalteng -> Kalbar, Kalsel, Kaltim, Kaltara
    '63': ['61', '62', '64'],  # Kalsel -> Kalbar, Kalteng, Kaltim
    '64': ['62', '63', '65', '72', '75'],  # Kaltim -> Kalteng, Kalsel, Kaltara, Sulteng, Gorontalo
    '65': ['62', '64'],  # Kaltara -> Kalteng, Kaltim
    
    # SULAWESI
    '71': ['72', '75', '76'],  # Sulut -> Sulteng, Gorontalo, Sulbar
    '72': ['64', '71', '73', '74', '75', '76'],  # Sulteng -> Kaltim, Sulut, Sulsel, Sultra, Gorontalo, Sulbar
    '73': ['72', '74', '76'],  # Sulsel -> Sulteng, Sultra, Sulbar
    '74': ['72', '73'],  # Sultra -> Sulteng, Sulsel
    '75': ['64', '71', '72'],  # Gorontalo -> Kaltim, Sulut, Sulteng
    '76': ['71', '72', '73'],  # Sulbar -> Sulut, Sulteng, Sulsel
    
    # MALUKU
    '81': ['82'],  # Maluku -> Malut
    '82': ['81', '71'],  # Malut -> Maluku, Sulut
    
    # PAPUA
    '91': ['92', '93', '94', '95', '96'],  # Papua
    '92': ['91', '96'],  # Papua Barat
    '93': ['91', '94', '95'],  # Papua Selatan
    '94': ['91', '93', '95'],  # Papua Tengah
    '95': ['91', '93', '94'],  # Papua Pegunungan
    '96': ['91', '92'],  # Papua Barat Daya
}


def get_tempat_lahir_domisili(regency_name: str, district_name: str) -> str:
    """
    Get tempat lahir for domisili (current residence).
    KOTA -> city name, KABUPATEN -> district/kecamatan name
    
    Args:
        regency_name: e.g., "KOTA MAKASSAR" or "KAB. GOWA" or "KOTA ADM. JAKARTA SELATAN"
        district_name: e.g., "Ujung Pandang" or "Somba Opu"
        
    Returns:
        UPPERCASE tempat lahir name
    """
    # Handle special Jakarta format: "KOTA ADM. JAKARTA SELATAN" -> "JAKARTA SELATAN"
    if 'KOTA ADM.' in regency_name:
        return regency_name.replace('KOTA ADM. ', '').upper()
    elif regency_name.startswith('KOTA '):
        return regency_name.replace('KOTA ', '').upper()
    elif 'KAB. ADM.' in regency_name:
        # Handle "KAB. ADM. KEP. SERIBU" -> use district name
        return district_name.upper()
    else:
        # KABUPATEN: use district/kecamatan name
        return district_name.upper()


def get_random_tempat_lahir(
    is_anak: bool,
    regency_name: str,
    district_name: str,
    province_code: str,
    tempat_lahir_pools: Dict[str, List[str]],
    all_tempat_lahir: List[str] = None
) -> str:
    """
    Generate random TEMPAT_LAHIR based on distribution rules.
    
    For children (anak): 100% domisili
    For adults (kepala keluarga, istri): 
        - 60% domisili
        - 20% same province (other regency)
        - 15% neighboring province
        - 5% other province
    
    Args:
        is_anak: True if person is a child
        regency_name: Current regency name (e.g., "KOTA MAKASSAR" or "KAB. GOWA")
        district_name: Current district name (e.g., "Ujung Pandang")
        province_code: Current province code (e.g., "73")
        tempat_lahir_pools: Dict of {province_code: [list of tempat lahir names]}
        all_tempat_lahir: Flat list of all tempat lahir (for random other province)
        
    Returns:
        TEMPAT_LAHIR in UPPERCASE format
    """
    # Determine domisili tempat lahir
    domisili = get_tempat_lahir_domisili(regency_name, district_name)
    
    # For children, always use domisili
    if is_anak:
        return domisili
    
    # For adults, apply distribution
    roll = random.random()
    
    if roll < 0.60:
        # 60% - domisili
        return domisili
    
    elif roll < 0.80:
        # 20% - same province, different regency
        if province_code in tempat_lahir_pools:
            pool = tempat_lahir_pools[province_code]
            if pool:
                selected = random.choice(pool)
                # Avoid returning same as domisili if possible
                if len(pool) > 1:
                    attempts = 0
                    while selected == domisili and attempts < 5:
                        selected = random.choice(pool)
                        attempts += 1
                return selected
        return domisili
    
    elif roll < 0.95:
        # 15% - neighboring province
        neighbors = PROVINSI_TETANGGA.get(province_code, [])
        if neighbors:
            neighbor_prov = random.choice(neighbors)
            if neighbor_prov in tempat_lahir_pools:
                pool = tempat_lahir_pools[neighbor_prov]
                if pool:
                    return random.choice(pool)
        # Fallback to same province
        if province_code in tempat_lahir_pools:
            pool = tempat_lahir_pools[province_code]
            if pool:
                return random.choice(pool)
        return domisili
    
    else:
        # 5% - random other province
        if all_tempat_lahir:
            return random.choice(all_tempat_lahir)
        # Fallback
        return domisili


def build_tempat_lahir_pools(
    regencies: Dict[str, dict],
    districts: Dict[str, dict]
) -> tuple:
    """
    Build tempat lahir pools from regencies and districts data.
    
    For KOTA: use city name as tempat lahir
    For KABUPATEN: use all district/kecamatan names as tempat lahir
    
    Args:
        regencies: Dict of {regency_code: {'name': str, 'province_id': str}}
        districts: Dict of {district_code: {'name': str, 'regency_id': str}}
        
    Returns:
        Tuple of (pools_by_province, all_tempat_lahir)
        - pools_by_province: {province_code: [list of tempat lahir names]}
        - all_tempat_lahir: flat list of all unique tempat lahir names
    """
    pools_by_province: Dict[str, List[str]] = {}
    all_tempat_lahir_set = set()
    
    # First, process all regencies
    for reg_code, reg_data in regencies.items():
        province_code = reg_data['province_id']
        regency_name = reg_data['name']
        
        if province_code not in pools_by_province:
            pools_by_province[province_code] = []
        
        if regency_name.startswith('KOTA ADM.'):
            # Special format like "KOTA ADM. JAKARTA SELATAN" -> "JAKARTA SELATAN"
            city_name = regency_name.replace('KOTA ADM. ', '').upper()
            if city_name not in pools_by_province[province_code]:
                pools_by_province[province_code].append(city_name)
            all_tempat_lahir_set.add(city_name)
        elif regency_name.startswith('KOTA '):
            # KOTA: add city name
            city_name = regency_name.replace('KOTA ', '').upper()
            if city_name not in pools_by_province[province_code]:
                pools_by_province[province_code].append(city_name)
            all_tempat_lahir_set.add(city_name)
        else:
            # KABUPATEN: add all district names in this regency
            for dist_code, dist_data in districts.items():
                if dist_data['regency_id'] == reg_code:
                    district_name = dist_data['name'].upper()
                    if district_name not in pools_by_province[province_code]:
                        pools_by_province[province_code].append(district_name)
                    all_tempat_lahir_set.add(district_name)
    
    all_tempat_lahir = list(all_tempat_lahir_set)
    
    return pools_by_province, all_tempat_lahir
