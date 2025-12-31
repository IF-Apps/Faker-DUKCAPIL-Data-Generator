"""
Family Generator Module
Generate Indonesian family data with consistent relationships
"""

import random
import logging
from datetime import date, timedelta
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
from tqdm import tqdm

# Setup module logger
logger = logging.getLogger(__name__)

from .wilayah_loader import WilayahLoader, get_loader
from .id_generator import IDGenerator, get_generator
from .reference_data import (
    get_random_agama, get_random_pendidikan, get_random_pekerjaan,
    get_random_golongan_darah, get_random_nama, get_random_nama_ayah,
    get_random_nama_ibu, get_random_alamat, get_random_rt, get_random_rw,
    get_random_status_perkawinan
)
from .tempat_lahir import get_random_tempat_lahir, build_tempat_lahir_pools


class FamilyGenerator:
    """Generate Indonesian family data with DUKCAPIL format"""
    
    # Age constraints
    MIN_HEAD_AGE = 20
    MAX_HEAD_AGE = 65
    MIN_MARRIAGE_AGE_MALE = 19
    MIN_MARRIAGE_AGE_FEMALE = 17
    MIN_PARENT_CHILD_AGE_GAP = 17
    MAX_PARENT_CHILD_AGE_GAP = 45
    MIN_CHILDREN = 0
    MAX_CHILDREN = 5
    
    def __init__(self, wilayah_loader: WilayahLoader = None, id_generator: IDGenerator = None):
        """
        Initialize FamilyGenerator
        
        Args:
            wilayah_loader: WilayahLoader instance
            id_generator: IDGenerator instance
        """
        self.wilayah = wilayah_loader or get_loader()
        self.id_gen = id_generator or get_generator()
        
        # Build tempat lahir pools for varied birth places
        self.tempat_lahir_pools, self.all_tempat_lahir = build_tempat_lahir_pools(
            self.wilayah.regencies, self.wilayah.districts
        )
        
        # Statistics tracking
        self.stats = {
            'total_families': 0,
            'total_people': 0,
            'gender': {'L': 0, 'P': 0},
            'status_hubungan': {},
            'agama': {},
            'villages': {}
        }
    
    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            'total_families': 0,
            'total_people': 0,
            'gender': {'L': 0, 'P': 0},
            'status_hubungan': {},
            'agama': {},
            'villages': {}
        }
        self.id_gen.reset()
    
    def distribute_families(
        self,
        villages: List[dict],
        num_families: int,
        mode: int,
        simulation_data: Dict[str, int] = None,
        correction_percent: int = 0
    ) -> Dict[str, int]:
        """
        Distribute families across villages
        
        Args:
            villages: List of village info dicts
            num_families: Total number of families to generate (ignored for mode 4)
            mode: Distribution mode (1=even, 2=even with random count, 3=random, 4=simulation)
            simulation_data: Dict mapping village_code to NKK count (for mode 4)
            correction_percent: Percentage correction for simulation mode (-100 to 1000)
            
        Returns:
            Dict mapping village_code to family count
        """
        distribution = {}
        
        if mode == 1:
            # Mode 1: Even distribution
            base_count = num_families // len(villages)
            remainder = num_families % len(villages)
            
            for i, village in enumerate(villages):
                count = base_count + (1 if i < remainder else 0)
                if count > 0:
                    distribution[village['village_code']] = count
        
        elif mode == 2:
            # Mode 2: All villages get families, but random count
            # Ensure every village gets at least 1 family if possible
            if num_families >= len(villages):
                # First, give each village 1 family
                remaining = num_families - len(villages)
                for village in villages:
                    distribution[village['village_code']] = 1
                
                # Distribute remaining randomly
                if remaining > 0:
                    for _ in range(remaining):
                        village = random.choice(villages)
                        distribution[village['village_code']] += 1
            else:
                # Fewer families than villages - distribute randomly
                selected = random.sample(villages, num_families)
                for village in selected:
                    distribution[village['village_code']] = distribution.get(village['village_code'], 0) + 1
        
        elif mode == 4 and simulation_data:
            # Mode 4: Simulation-based distribution
            # Only include villages that exist in simulation data
            for village in villages:
                village_code = village['village_code']
                if village_code in simulation_data:
                    base_count = simulation_data[village_code]
                    # Apply correction: count = base * (1 + correction/100)
                    corrected_count = int(base_count * (1 + correction_percent / 100))
                    if corrected_count > 0:
                        distribution[village_code] = corrected_count
        
        else:
            # Mode 3: Random distribution (some villages may get 0)
            for _ in range(num_families):
                village = random.choice(villages)
                code = village['village_code']
                distribution[code] = distribution.get(code, 0) + 1
        
        return distribution
    
    def generate_families(
        self,
        region_code: str,
        num_families: int,
        distribution_mode: int = 1,
        show_progress: bool = True,
        simulation_data: Dict[str, int] = None,
        correction_percent: int = 0
    ) -> List[dict]:
        """
        Generate multiple families for a region
        
        Args:
            region_code: Regional code (province/regency/district)
            num_families: Number of families to generate
            distribution_mode: 1=even, 2=even random, 3=random, 4=simulation
            show_progress: Show progress bar
            simulation_data: Dict mapping village_code to NKK count (for mode 4)
            correction_percent: Percentage correction for simulation mode
            
        Returns:
            List of person records (all family members)
        """
        self.reset_stats()
        
        # Get all villages in region
        villages = self.wilayah.get_sub_regions(region_code)
        if not villages:
            raise ValueError(f"Tidak ada kelurahan ditemukan untuk kode {region_code}")
        
        # Distribute families across villages
        distribution = self.distribute_families(
            villages, num_families, distribution_mode,
            simulation_data=simulation_data, correction_percent=correction_percent
        )
        
        # Recalculate actual num_families for mode 4
        actual_num_families = sum(distribution.values())
        
        # Build village lookup
        village_lookup = {v['village_code']: v for v in villages}
        
        # Generate families
        all_people = []
        
        # Create progress bar
        family_items = list(distribution.items())
        
        if show_progress:
            pbar = tqdm(total=actual_num_families, desc="Generating families", unit="KK")
        
        for village_code, family_count in family_items:
            village_info = village_lookup[village_code]
            
            for _ in range(family_count):
                family = self._generate_single_family(village_info)
                all_people.extend(family)
                
                # Update stats
                self.stats['total_families'] += 1
                village_name = village_info['village_name']
                if village_name not in self.stats['villages']:
                    self.stats['villages'][village_name] = {'kk': 0, 'jiwa': 0}
                self.stats['villages'][village_name]['kk'] += 1
                self.stats['villages'][village_name]['jiwa'] += len(family)
                
                if show_progress:
                    pbar.update(1)
        
        if show_progress:
            pbar.close()
        
        # Post-validation: ensure 1 NKK = 1 Kepala Keluarga
        all_people, fixes = validate_and_fix_families(all_people)
        if fixes > 0:
            logger.info(f"Post-validation applied {fixes} auto-fixes to ensure 1 Kepala Keluarga per NKK")
        
        return all_people
    
    def _generate_single_family(self, village_info: dict) -> List[dict]:
        """Generate a single family with all members"""
        family_members = []
        
        # Get NIK codes from village
        prov_code, reg_code, dist_code = self.wilayah.get_nik_codes(village_info['village_code'])
        
        # Generate shared family data
        nkk = self.id_gen.generate_nkk(prov_code, reg_code, dist_code)
        family_agama = get_random_agama(weighted=True)
        
        # Try to get RT/RW data from koordinat_rt_rw.csv
        rt_rw_data = self.wilayah.get_rt_rw_data(village_info['village_code'])
        
        if rt_rw_data:
            # Use actual RT/RW data
            rt = rt_rw_data['rt']
            rw = rt_rw_data['rw']
            alamat = rt_rw_data['alamat'] if rt_rw_data['alamat'] else get_random_alamat()
            latitude = rt_rw_data['latitude']
            longitude = rt_rw_data['longitude']
        else:
            # Fallback to random values
            alamat = get_random_alamat()
            rt = get_random_rt()
            rw = get_random_rw()
            latitude = None
            longitude = None
        
        # Generate head of family (Kepala Keluarga) - always male
        head_age = random.randint(self.MIN_HEAD_AGE, self.MAX_HEAD_AGE)
        head_birth_date = self._generate_birth_date(head_age)
        head_gender = 'L'
        
        # Determine if head is married
        is_married = random.random() < 0.85  # 85% chance married
        
        head = self._create_person(
            nkk=nkk,
            gender=head_gender,
            birth_date=head_birth_date,
            agama=family_agama,
            status_hubungan='Kepala Keluarga',
            status_perkawinan='Kawin' if is_married else 'Belum Kawin',
            village_info=village_info,
            alamat=alamat,
            rt=rt,
            rw=rw,
            prov_code=prov_code,
            reg_code=reg_code,
            dist_code=dist_code,
            latitude=latitude,
            longitude=longitude
        )
        family_members.append(head)
        
        # Generate wife if married
        if is_married:
            # Wife age: usually younger or similar age
            wife_age_diff = random.randint(-3, 8)  # Wife can be 3 years older to 8 years younger
            wife_age = max(self.MIN_MARRIAGE_AGE_FEMALE, head_age - wife_age_diff)
            wife_birth_date = self._generate_birth_date(wife_age)
            
            wife = self._create_person(
                nkk=nkk,
                gender='P',
                birth_date=wife_birth_date,
                agama=family_agama,
                status_hubungan='Istri',
                status_perkawinan='Kawin',
                village_info=village_info,
                alamat=alamat,
                rt=rt,
                rw=rw,
                prov_code=prov_code,
                reg_code=reg_code,
                dist_code=dist_code,
                latitude=latitude,
                longitude=longitude
            )
            family_members.append(wife)
            
            # Generate children
            num_children = random.randint(self.MIN_CHILDREN, self.MAX_CHILDREN)
            youngest_parent_age = min(head_age, wife_age)
            
            for i in range(num_children):
                # Child age must be at least MIN_PARENT_CHILD_AGE_GAP less than youngest parent
                max_child_age = youngest_parent_age - self.MIN_PARENT_CHILD_AGE_GAP
                if max_child_age < 0:
                    continue
                
                child_age = random.randint(0, max(0, max_child_age))
                child_birth_date = self._generate_birth_date(child_age)
                child_gender = random.choice(['L', 'P'])
                
                # Child's marital status based on age and gender (realistic)
                # Anak yang sudah kawin biasanya pindah KK, jadi di sini mayoritas belum kawin
                if child_age < 17:
                    child_status_perkawinan = 'Belum Kawin'
                elif child_age < 21:
                    # 95% belum kawin, 5% sudah kawin tapi masih ikut ortu
                    child_status_perkawinan = random.choices(
                        ['Belum Kawin', 'Kawin'],
                        weights=[0.95, 0.05], k=1
                    )[0]
                elif child_age < 25:
                    # Makin banyak yang kawin tapi di KK ortu = yg belum pindah
                    child_status_perkawinan = random.choices(
                        ['Belum Kawin', 'Kawin'],
                        weights=[0.85, 0.15], k=1
                    )[0]
                else:
                    # Anak dewasa yang masih di KK ortu = biasanya belum kawin
                    child_status_perkawinan = random.choices(
                        ['Belum Kawin', 'Kawin'],
                        weights=[0.75, 0.25], k=1
                    )[0]
                
                child = self._create_person(
                    nkk=nkk,
                    gender=child_gender,
                    birth_date=child_birth_date,
                    agama=family_agama,
                    status_hubungan='Anak',
                    status_perkawinan=child_status_perkawinan,
                    village_info=village_info,
                    alamat=alamat,
                    rt=rt,
                    rw=rw,
                    prov_code=prov_code,
                    reg_code=reg_code,
                    dist_code=dist_code,
                    nama_ayah=head['NAMA'],
                    nama_ibu=wife['NAMA'],
                    latitude=latitude,
                    longitude=longitude
                )
                family_members.append(child)
        
        # Per-family assertion: ensure exactly 1 Kepala Keluarga
        family_members = self._validate_and_fix_single_family(family_members, nkk)
        
        return family_members
    
    def _validate_and_fix_single_family(self, family_members: List[dict], nkk: str) -> List[dict]:
        """
        Validate and auto-fix NKK consistency rules:
        1. Exactly 1 Kepala Keluarga per family
        2. All members have same AGAMA
        3. All members have same address (KODE_KELURAHAN, RT, RW, ALAMAT)
        
        Args:
            family_members: List of family member records
            nkk: NKK for logging purposes
            
        Returns:
            Fixed list of family members
        """
        if not family_members:
            return family_members
        
        # === 1. Validate Kepala Keluarga ===
        kepala_count = sum(1 for m in family_members if m['STATUS_HUBUNGAN'] == 'Kepala Keluarga')
        kepala = None
        
        if kepala_count == 0:
            # No Kepala Keluarga - set oldest male as Kepala Keluarga
            logger.warning(f"NKK {nkk}: No Kepala Keluarga found, auto-fixing...")
            
            males = [m for m in family_members if m['JENIS_KELAMIN'] == 'L']
            candidates = males if males else family_members
            
            if candidates:
                oldest = min(candidates, key=lambda m: m['TANGGAL_LAHIR'])
                oldest['STATUS_HUBUNGAN'] = 'Kepala Keluarga'
                kepala = oldest
                logger.warning(f"NKK {nkk}: Set {oldest['NAMA']} as Kepala Keluarga")
        
        elif kepala_count > 1:
            # Multiple Kepala Keluarga - keep first, change others to Famili Lain
            logger.warning(f"NKK {nkk}: Found {kepala_count} Kepala Keluarga, auto-fixing...")
            
            first_kepala_found = False
            for member in family_members:
                if member['STATUS_HUBUNGAN'] == 'Kepala Keluarga':
                    if first_kepala_found:
                        member['STATUS_HUBUNGAN'] = 'Famili Lain'
                        logger.warning(f"NKK {nkk}: Changed {member['NAMA']} from Kepala Keluarga to Famili Lain")
                    else:
                        first_kepala_found = True
                        kepala = member
        else:
            # Exactly 1 Kepala Keluarga - find it
            kepala = next((m for m in family_members if m['STATUS_HUBUNGAN'] == 'Kepala Keluarga'), None)
        
        # If still no kepala, use first member as reference
        if kepala is None:
            kepala = family_members[0]
        
        # === 2. Validate AGAMA consistency ===
        kepala_agama = kepala['AGAMA']
        for member in family_members:
            if member['AGAMA'] != kepala_agama:
                logger.warning(f"NKK {nkk}: {member['NAMA']} has different AGAMA ({member['AGAMA']}), fixing to {kepala_agama}")
                member['AGAMA'] = kepala_agama
        
        # === 3. Validate address consistency ===
        address_fields = ['KODE_KELURAHAN', 'KELURAHAN', 'KODE_KECAMATAN', 'KECAMATAN', 
                          'KODE_KABUPATEN', 'KABUPATEN', 'KODE_PROVINSI', 'PROVINSI',
                          'ALAMAT', 'RT', 'RW', 'LATITUDE', 'LONGITUDE']
        
        for member in family_members:
            for field in address_fields:
                if member.get(field) != kepala.get(field):
                    logger.warning(f"NKK {nkk}: {member['NAMA']} has different {field}, fixing to match Kepala Keluarga")
                    member[field] = kepala.get(field)
        
        return family_members
    
    def _create_person(
        self,
        nkk: str,
        gender: str,
        birth_date: date,
        agama: str,
        status_hubungan: str,
        status_perkawinan: str,
        village_info: dict,
        alamat: str,
        rt: str,
        rw: str,
        prov_code: str,
        reg_code: str,
        dist_code: str,
        nama_ayah: str = None,
        nama_ibu: str = None,
        latitude: float = None,
        longitude: float = None
    ) -> dict:
        """Create a single person record"""
        
        # Generate NIK
        nik = self.id_gen.generate_nik(
            province_code=prov_code,
            regency_code=reg_code,
            district_code=dist_code,
            birth_date=birth_date,
            gender=gender
        )
        
        # Calculate age
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Generate name based on religion
        nama = get_random_nama(gender, agama=agama)
        
        # Get education and occupation based on age
        pendidikan = get_random_pendidikan(weighted=True, min_age=age)
        pekerjaan = get_random_pekerjaan(age, gender, pendidikan)
        
        # Generate parent names if not provided (using same religion as family)
        if nama_ayah is None:
            nama_ayah = get_random_nama_ayah(agama=agama)
        if nama_ibu is None:
            nama_ibu = get_random_nama_ibu(agama=agama)
        
        # Generate varied TEMPAT_LAHIR
        # Anak: 100% domisili, Dewasa: 60% domisili, 20% same province, 15% neighbor, 5% other
        tempat_lahir = get_random_tempat_lahir(
            is_anak=(status_hubungan == 'Anak'),
            regency_name=village_info['regency_name'],
            district_name=village_info['district_name'],
            province_code=village_info['province_code'],
            tempat_lahir_pools=self.tempat_lahir_pools,
            all_tempat_lahir=self.all_tempat_lahir
        )
        
        # Build person record
        person = {
            'NKK': nkk,
            'NIK': nik,
            'NAMA': nama,
            'JENIS_KELAMIN': gender,
            'TEMPAT_LAHIR': tempat_lahir,
            'TANGGAL_LAHIR': birth_date.strftime('%d-%m-%Y'),
            'AGAMA': agama,
            'PENDIDIKAN': pendidikan,
            'PEKERJAAN': pekerjaan,
            'STATUS_PERKAWINAN': status_perkawinan,
            'STATUS_HUBUNGAN': status_hubungan,
            'GOLONGAN_DARAH': get_random_golongan_darah(),
            'KEWARGANEGARAAN': 'WNI',
            'NAMA_AYAH': nama_ayah,
            'NAMA_IBU': nama_ibu,
            'ALAMAT': alamat,
            'RT': rt,
            'RW': rw,
            'KODE_KELURAHAN': village_info['village_code'],
            'KELURAHAN': village_info['village_name'],
            'KODE_KECAMATAN': village_info['district_code'],
            'KECAMATAN': village_info['district_name'],
            'KODE_KABUPATEN': village_info['regency_code'],
            'KABUPATEN': village_info['regency_name'],
            'KODE_PROVINSI': village_info['province_code'],
            'PROVINSI': village_info['province_name'],
            'LATITUDE': latitude,
            'LONGITUDE': longitude
        }
        
        # Update statistics
        self.stats['total_people'] += 1
        self.stats['gender'][gender] += 1
        
        if status_hubungan not in self.stats['status_hubungan']:
            self.stats['status_hubungan'][status_hubungan] = 0
        self.stats['status_hubungan'][status_hubungan] += 1
        
        if agama not in self.stats['agama']:
            self.stats['agama'][agama] = 0
        self.stats['agama'][agama] += 1
        
        return person
    
    def _generate_birth_date(self, age: int) -> date:
        """Generate a random birth date for given age"""
        today = date.today()
        
        # Calculate approximate birth year
        birth_year = today.year - age
        
        # Random month and day
        birth_month = random.randint(1, 12)
        
        # Handle month day limits
        if birth_month in [1, 3, 5, 7, 8, 10, 12]:
            max_day = 31
        elif birth_month in [4, 6, 9, 11]:
            max_day = 30
        else:
            # February - check leap year
            if (birth_year % 4 == 0 and birth_year % 100 != 0) or (birth_year % 400 == 0):
                max_day = 29
            else:
                max_day = 28
        
        birth_day = random.randint(1, max_day)
        
        return date(birth_year, birth_month, birth_day)
    
    def get_statistics(self) -> dict:
        """Get generation statistics for recap"""
        stats = self.stats.copy()
        
        # Calculate additional stats
        if stats['total_families'] > 0:
            stats['avg_members_per_family'] = round(stats['total_people'] / stats['total_families'], 2)
        else:
            stats['avg_members_per_family'] = 0
        
        # Sort villages by KK count
        sorted_villages = sorted(
            stats['villages'].items(),
            key=lambda x: x[1]['kk'],
            reverse=True
        )
        stats['top_villages'] = sorted_villages[:5]
        
        return stats


def generate_recap(stats: dict, region_name: str, region_code: str) -> str:
    """Generate recap text from statistics"""
    lines = [
        "",
        "=" * 50,
        "                    REKAP DATA",
        "=" * 50,
        f"Wilayah         : {region_name} ({region_code})",
        f"Total Keluarga  : {stats['total_families']} KK",
        f"Total Penduduk  : {stats['total_people']} jiwa",
        "",
        "--- Sebaran Jenis Kelamin ---"
    ]
    
    total = stats['total_people']
    for gender, count in stats['gender'].items():
        pct = (count / total * 100) if total > 0 else 0
        label = "Laki-laki" if gender == 'L' else "Perempuan"
        lines.append(f"{label:15} : {count} ({pct:.1f}%)")
    
    lines.append("")
    lines.append("--- Sebaran Status Hubungan ---")
    for status, count in sorted(stats['status_hubungan'].items(), key=lambda x: -x[1]):
        pct = (count / total * 100) if total > 0 else 0
        lines.append(f"{status:15} : {count} ({pct:.1f}%)")
    
    lines.append("")
    lines.append("--- Sebaran Agama ---")
    for agama, count in sorted(stats['agama'].items(), key=lambda x: -x[1]):
        pct = (count / total * 100) if total > 0 else 0
        lines.append(f"{agama:15} : {count} ({pct:.1f}%)")
    
    lines.append("")
    lines.append("--- Sebaran Kelurahan (Top 5) ---")
    for village_name, data in stats.get('top_villages', []):
        lines.append(f"{village_name[:20]:20} : {data['kk']} KK ({data['jiwa']} jiwa)")
    
    if len(stats.get('villages', {})) > 5:
        remaining = len(stats['villages']) - 5
        lines.append(f"... dan {remaining} kelurahan lainnya")
    
    lines.append("")
    lines.append("--- Statistik Keluarga ---")
    lines.append(f"Rata-rata anggota/KK  : {stats.get('avg_members_per_family', 0)} jiwa")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)


def validate_and_fix_families(data: List[dict]) -> Tuple[List[dict], int]:
    """
    Post-validation: Validate all generated data and auto-fix NKK consistency:
    1. Exactly 1 Kepala Keluarga per NKK
    2. All members have same AGAMA per NKK
    3. All members have same address per NKK
    
    Args:
        data: List of all person records
        
    Returns:
        Tuple of (fixed data, number of fixes applied)
    """
    # Group records by NKK
    nkk_groups = defaultdict(list)
    for person in data:
        nkk_groups[person['NKK']].append(person)
    
    total_fixes = 0
    
    for nkk, members in nkk_groups.items():
        # === 1. Validate Kepala Keluarga ===
        kepala_members = [m for m in members if m['STATUS_HUBUNGAN'] == 'Kepala Keluarga']
        kepala_count = len(kepala_members)
        kepala = None
        
        if kepala_count == 0:
            logger.warning(f"Post-validation NKK {nkk}: No Kepala Keluarga found, auto-fixing...")
            
            males = [m for m in members if m['JENIS_KELAMIN'] == 'L']
            candidates = males if males else members
            
            if candidates:
                oldest = min(candidates, key=lambda m: m['TANGGAL_LAHIR'])
                oldest['STATUS_HUBUNGAN'] = 'Kepala Keluarga'
                kepala = oldest
                logger.warning(f"Post-validation NKK {nkk}: Set {oldest['NAMA']} as Kepala Keluarga")
                total_fixes += 1
        
        elif kepala_count > 1:
            logger.warning(f"Post-validation NKK {nkk}: Found {kepala_count} Kepala Keluarga, auto-fixing...")
            
            first_kepala_found = False
            for member in members:
                if member['STATUS_HUBUNGAN'] == 'Kepala Keluarga':
                    if first_kepala_found:
                        member['STATUS_HUBUNGAN'] = 'Famili Lain'
                        logger.warning(f"Post-validation NKK {nkk}: Changed {member['NAMA']} from Kepala Keluarga to Famili Lain")
                        total_fixes += 1
                    else:
                        first_kepala_found = True
                        kepala = member
        else:
            kepala = kepala_members[0]
        
        # If still no kepala, use first member as reference
        if kepala is None:
            kepala = members[0]
        
        # === 2. Validate AGAMA consistency ===
        kepala_agama = kepala['AGAMA']
        for member in members:
            if member['AGAMA'] != kepala_agama:
                logger.warning(f"Post-validation NKK {nkk}: {member['NAMA']} has different AGAMA ({member['AGAMA']}), fixing to {kepala_agama}")
                member['AGAMA'] = kepala_agama
                total_fixes += 1
        
        # === 3. Validate address consistency ===
        address_fields = ['KODE_KELURAHAN', 'KELURAHAN', 'KODE_KECAMATAN', 'KECAMATAN', 
                          'KODE_KABUPATEN', 'KABUPATEN', 'KODE_PROVINSI', 'PROVINSI',
                          'ALAMAT', 'RT', 'RW', 'LATITUDE', 'LONGITUDE']
        
        for member in members:
            for field in address_fields:
                if member.get(field) != kepala.get(field):
                    logger.warning(f"Post-validation NKK {nkk}: {member['NAMA']} has different {field}, fixing to match Kepala Keluarga")
                    member[field] = kepala.get(field)
                    total_fixes += 1
    
    if total_fixes > 0:
        logger.info(f"Post-validation completed: {total_fixes} fixes applied")
    
    return data, total_fixes
