"""
Parallel Family Generator Module
Generate Indonesian family data using multiprocessing for improved performance
"""

import os
import csv
import json
import random
import logging
from datetime import date, timedelta
from typing import List, Dict, Tuple, Optional, Generator
from multiprocessing import Pool, cpu_count, Manager
from functools import partial
import queue
import threading

from tqdm import tqdm

# Setup module logger
logger = logging.getLogger(__name__)

from .wilayah_loader import WilayahLoader, get_loader
from .reference_data import (
    get_random_agama, get_random_pendidikan, get_random_pekerjaan,
    get_random_golongan_darah, get_random_nama, get_random_nama_ayah,
    get_random_nama_ibu, get_random_alamat, get_random_rt, get_random_rw,
    get_random_status_perkawinan
)
from .tempat_lahir import get_random_tempat_lahir, build_tempat_lahir_pools


class ProcessLocalIDGenerator:
    """
    ID Generator for multiprocessing - uses worker_id to ensure unique sequences.
    Each worker generates sequences in format: WXXX where W=worker_id, XXX=local_seq
    This ensures no collision between workers.
    """
    
    def __init__(self, worker_id: int, total_workers: int):
        """
        Initialize process-local ID generator
        
        Args:
            worker_id: Unique ID for this worker (0 to total_workers-1)
            total_workers: Total number of workers
        """
        self.worker_id = worker_id
        self.total_workers = total_workers
        
        # Local sequence counters per base_key
        self._nik_sequences: Dict[str, int] = {}
        self._nkk_sequences: Dict[str, int] = {}
        
        # Track used NIKs and NKKs within this worker to avoid duplicates
        self._used_niks: set = set()
        self._used_nkks: set = set()
    
    def generate_nik(
        self,
        province_code: str,
        regency_code: str,
        district_code: str,
        birth_date: date,
        gender: str
    ) -> str:
        """Generate a valid unique NIK"""
        # Format date part
        day = birth_date.day
        if gender == 'P':  # Female: add 40 to day
            day += 40
        
        date_str = f"{day:02d}{birth_date.month:02d}{birth_date.year % 100:02d}"
        
        # Build base key for sequence tracking
        base_key = f"{province_code}{regency_code}{district_code}{date_str}"
        
        # Get next sequence number - start each worker at different offset
        if base_key not in self._nik_sequences:
            # Worker 0: 1-2499, Worker 1: 2500-4999, Worker 2: 5000-7499, Worker 3: 7500-9999
            sequences_per_worker = 9999 // max(self.total_workers, 1)
            self._nik_sequences[base_key] = self.worker_id * sequences_per_worker
        
        # Find next available unique sequence within worker's range
        max_seq = (self.worker_id + 1) * (9999 // max(self.total_workers, 1))
        
        while self._nik_sequences[base_key] < min(max_seq, 9999):
            self._nik_sequences[base_key] += 1
            sequence = self._nik_sequences[base_key]
            
            nik = f"{province_code}{regency_code}{district_code}{date_str}{sequence:04d}"
            
            if nik not in self._used_niks:
                self._used_niks.add(nik)
                return nik
        
        # If exhausted, try remaining sequences (may overlap with other workers, but track locally)
        for sequence in range(1, 10000):
            nik = f"{province_code}{regency_code}{district_code}{date_str}{sequence:04d}"
            if nik not in self._used_niks:
                self._used_niks.add(nik)
                return nik
        
        # Final fallback: use microsecond timestamp + worker_id for uniqueness
        import time
        timestamp_suffix = (int(time.time() * 1000000) + self.worker_id) % 10000
        nik = f"{province_code}{regency_code}{district_code}{date_str}{timestamp_suffix:04d}"
        self._used_niks.add(nik)
        return nik
    
    def generate_nkk(
        self,
        province_code: str,
        regency_code: str,
        district_code: str,
        issue_date: date = None
    ) -> str:
        """Generate a valid NKK with worker-specific sequence"""
        if issue_date is None:
            issue_date = date.today()
        
        # Try multiple dates if needed to avoid collision
        max_date_attempts = 365  # Try up to 1 year back
        
        for date_offset in range(max_date_attempts):
            current_date = issue_date - timedelta(days=date_offset)
            date_str = f"{current_date.day:02d}{current_date.month:02d}{current_date.year % 100:02d}"
            base_key = f"NKK_{province_code}{regency_code}{district_code}{date_str}"
            
            if base_key not in self._nkk_sequences:
                # Start each worker at different offset to avoid collision
                # Worker 0: 1-2499, Worker 1: 2500-4999, etc.
                sequences_per_worker = 9999 // max(self.total_workers, 1)
                self._nkk_sequences[base_key] = self.worker_id * sequences_per_worker
            
            # Find next available unique NKK
            start_seq = self._nkk_sequences[base_key]
            max_seq = (self.worker_id + 1) * (9999 // max(self.total_workers, 1))
            
            while self._nkk_sequences[base_key] < max_seq:
                self._nkk_sequences[base_key] += 1
                sequence = self._nkk_sequences[base_key]
                
                if sequence > 9999:
                    break  # Try next date
                
                nkk = f"{province_code}{regency_code}{district_code}{date_str}{sequence:04d}"
                
                if nkk not in self._used_nkks:
                    self._used_nkks.add(nkk)
                    return nkk
            
            # Exhausted this date's range for this worker, try previous date
            continue
        
        # Final fallback: use timestamp + worker_id for uniqueness
        import time
        timestamp_suffix = (int(time.time() * 1000000) + self.worker_id) % 10000
        nkk = f"{province_code}{regency_code}{district_code}{date_str}{timestamp_suffix:04d}"
        self._used_nkks.add(nkk)
        return nkk


# Age constraints (module-level for worker access)
MIN_HEAD_AGE = 20
MAX_HEAD_AGE = 65
MIN_MARRIAGE_AGE_MALE = 19
MIN_MARRIAGE_AGE_FEMALE = 17
MIN_PARENT_CHILD_AGE_GAP = 17
MIN_CHILDREN = 0
MAX_CHILDREN = 5


def _build_alamat_from_record(record: dict) -> str:
    """Build street address from RT/RW record with jalan_list and lorong_list"""
    parts = []
    
    # Pick one random jalan if available
    jalan_list = record.get('jalan_list', [])
    if jalan_list:
        jalan = random.choice(jalan_list).strip()
        if jalan:
            parts.append(jalan)
    
    # Pick one random lorong if available
    lorong_list = record.get('lorong_list', [])
    if lorong_list:
        lorong = random.choice(lorong_list).strip()
        if lorong:
            # Add "Lorong" prefix if not already present
            if not lorong.upper().startswith('LORONG') and not lorong.upper().startswith('LR'):
                lorong = f"Lorong {lorong}"
            parts.append(lorong)
    
    return ', '.join(parts) if parts else ''


def _generate_birth_date(age: int) -> date:
    """Generate a random birth date for given age"""
    today = date.today()
    birth_year = today.year - age
    birth_month = random.randint(1, 12)
    
    if birth_month in [1, 3, 5, 7, 8, 10, 12]:
        max_day = 31
    elif birth_month in [4, 6, 9, 11]:
        max_day = 30
    else:
        if (birth_year % 4 == 0 and birth_year % 100 != 0) or (birth_year % 400 == 0):
            max_day = 29
        else:
            max_day = 28
    
    birth_day = random.randint(1, max_day)
    return date(birth_year, birth_month, birth_day)


def _create_person(
    nkk: str,
    nik: str,
    gender: str,
    birth_date: date,
    agama: str,
    status_hubungan: str,
    status_perkawinan: str,
    village_info: dict,
    alamat: str,
    rt: str,
    rw: str,
    tempat_lahir_pools: Dict[str, List[str]],
    all_tempat_lahir: List[str],
    nama_ayah: str = None,
    nama_ibu: str = None,
    latitude: float = None,
    longitude: float = None
) -> dict:
    """Create a single person record (pure function for multiprocessing)"""
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    # Generate name based on religion
    nama = get_random_nama(gender, agama=agama)
    pendidikan = get_random_pendidikan(weighted=True, min_age=age)
    pekerjaan = get_random_pekerjaan(age, gender, pendidikan)
    
    # Generate parent names if not provided (using same religion as family)
    if nama_ayah is None:
        nama_ayah = get_random_nama_ayah(agama=agama)
    if nama_ibu is None:
        nama_ibu = get_random_nama_ibu(agama=agama)
    
    # Generate varied TEMPAT_LAHIR
    tempat_lahir = get_random_tempat_lahir(
        is_anak=(status_hubungan == 'Anak'),
        regency_name=village_info['regency_name'],
        district_name=village_info['district_name'],
        province_code=village_info['province_code'],
        tempat_lahir_pools=tempat_lahir_pools,
        all_tempat_lahir=all_tempat_lahir
    )
    
    return {
        'NKK': nkk,
        'NIK': nik,
        'NAMA': nama,
        'JENIS_KELAMIN': gender,
        'TEMPAT_LAHIR': tempat_lahir,
        'TANGGAL_LAHIR': birth_date.strftime('%d|%m|%Y'),
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


def _generate_single_family(
    village_info: dict,
    id_gen: ProcessLocalIDGenerator,
    prov_code: str,
    reg_code: str,
    dist_code: str,
    tempat_lahir_pools: Dict[str, List[str]],
    all_tempat_lahir: List[str],
    rt_rw_lookup: Dict[str, List[dict]] = None
) -> List[dict]:
    """Generate a single family (pure function for multiprocessing)"""
    family_members = []
    
    # Generate shared family data
    nkk = id_gen.generate_nkk(prov_code, reg_code, dist_code)
    family_agama = get_random_agama(weighted=True)
    
    # Try to get RT/RW data from lookup
    village_code = village_info['village_code']
    rt_rw_data = None
    if rt_rw_lookup and village_code in rt_rw_lookup:
        records = rt_rw_lookup[village_code]
        if records:
            rt_rw_data = random.choice(records)
    
    if rt_rw_data:
        # Use actual RT/RW data
        rt = rt_rw_data['rt']
        rw = rt_rw_data['rw']
        # Build alamat from jalan_list and lorong_list
        alamat = _build_alamat_from_record(rt_rw_data)
        if not alamat:
            alamat = get_random_alamat()
        latitude = rt_rw_data['latitude']
        longitude = rt_rw_data['longitude']
    else:
        # Fallback to random values
        alamat = get_random_alamat()
        rt = get_random_rt()
        rw = get_random_rw()
        latitude = None
        longitude = None
    
    # Generate head of family
    head_age = random.randint(MIN_HEAD_AGE, MAX_HEAD_AGE)
    head_birth_date = _generate_birth_date(head_age)
    head_gender = 'L'
    is_married = random.random() < 0.85
    
    head_nik = id_gen.generate_nik(prov_code, reg_code, dist_code, head_birth_date, head_gender)
    
    head = _create_person(
        nkk=nkk,
        nik=head_nik,
        gender=head_gender,
        birth_date=head_birth_date,
        agama=family_agama,
        status_hubungan='Kepala Keluarga',
        status_perkawinan='Kawin' if is_married else 'Belum Kawin',
        village_info=village_info,
        alamat=alamat,
        rt=rt,
        rw=rw,
        tempat_lahir_pools=tempat_lahir_pools,
        all_tempat_lahir=all_tempat_lahir,
        latitude=latitude,
        longitude=longitude
    )
    family_members.append(head)
    
    # Generate wife if married
    wife = None
    if is_married:
        wife_age_diff = random.randint(-3, 8)
        wife_age = max(MIN_MARRIAGE_AGE_FEMALE, head_age - wife_age_diff)
        wife_birth_date = _generate_birth_date(wife_age)
        
        wife_nik = id_gen.generate_nik(prov_code, reg_code, dist_code, wife_birth_date, 'P')
        
        wife = _create_person(
            nkk=nkk,
            nik=wife_nik,
            gender='P',
            birth_date=wife_birth_date,
            agama=family_agama,
            status_hubungan='Istri',
            status_perkawinan='Kawin',
            village_info=village_info,
            alamat=alamat,
            rt=rt,
            rw=rw,
            tempat_lahir_pools=tempat_lahir_pools,
            all_tempat_lahir=all_tempat_lahir,
            latitude=latitude,
            longitude=longitude
        )
        family_members.append(wife)
        
        # Generate children
        num_children = random.randint(MIN_CHILDREN, MAX_CHILDREN)
        youngest_parent_age = min(head_age, wife_age)
        
        for _ in range(num_children):
            max_child_age = youngest_parent_age - MIN_PARENT_CHILD_AGE_GAP
            if max_child_age < 0:
                continue
            
            child_age = random.randint(0, max(0, max_child_age))
            child_birth_date = _generate_birth_date(child_age)
            child_gender = random.choice(['L', 'P'])
            
            # Child's marital status
            if child_age < 17:
                child_status_perkawinan = 'Belum Kawin'
            elif child_age < 21:
                child_status_perkawinan = random.choices(
                    ['Belum Kawin', 'Kawin'], weights=[0.95, 0.05], k=1
                )[0]
            elif child_age < 25:
                child_status_perkawinan = random.choices(
                    ['Belum Kawin', 'Kawin'], weights=[0.85, 0.15], k=1
                )[0]
            else:
                child_status_perkawinan = random.choices(
                    ['Belum Kawin', 'Kawin'], weights=[0.75, 0.25], k=1
                )[0]
            
            child_nik = id_gen.generate_nik(prov_code, reg_code, dist_code, child_birth_date, child_gender)
            
            child = _create_person(
                nkk=nkk,
                nik=child_nik,
                gender=child_gender,
                birth_date=child_birth_date,
                agama=family_agama,
                status_hubungan='Anak',
                status_perkawinan=child_status_perkawinan,
                village_info=village_info,
                alamat=alamat,
                rt=rt,
                rw=rw,
                tempat_lahir_pools=tempat_lahir_pools,
                all_tempat_lahir=all_tempat_lahir,
                nama_ayah=head['NAMA'],
                nama_ibu=wife['NAMA'],
                latitude=latitude,
                longitude=longitude
            )
            family_members.append(child)
    
    # Per-family assertion: ensure exactly 1 Kepala Keluarga
    family_members = _validate_and_fix_single_family(family_members, nkk)
    
    return family_members


def _validate_and_fix_single_family(family_members: List[dict], nkk: str) -> List[dict]:
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
    from collections import defaultdict
    
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


def _worker_generate_batch(args: Tuple) -> Tuple[List[dict], dict]:
    """
    Worker function to generate a batch of families.
    Returns (list of people, batch statistics)
    """
    worker_id, total_workers, batch_items, village_lookup, nik_codes_lookup, tempat_lahir_pools, all_tempat_lahir, rt_rw_lookup = args
    
    # Create worker-local ID generator
    id_gen = ProcessLocalIDGenerator(worker_id, total_workers)
    
    all_people = []
    batch_stats = {
        'families': 0,
        'people': 0,
        'gender': {'L': 0, 'P': 0},
        'status_hubungan': {},
        'agama': {},
        'villages': {}
    }
    
    for village_code, family_count in batch_items:
        village_info = village_lookup[village_code]
        prov_code, reg_code, dist_code = nik_codes_lookup[village_code]
        
        for _ in range(family_count):
            family = _generate_single_family(
                village_info, id_gen, prov_code, reg_code, dist_code,
                tempat_lahir_pools, all_tempat_lahir, rt_rw_lookup
            )
            all_people.extend(family)
            
            # Update batch stats
            batch_stats['families'] += 1
            batch_stats['people'] += len(family)
            
            village_name = village_info['village_name']
            if village_name not in batch_stats['villages']:
                batch_stats['villages'][village_name] = {'kk': 0, 'jiwa': 0}
            batch_stats['villages'][village_name]['kk'] += 1
            batch_stats['villages'][village_name]['jiwa'] += len(family)
            
            for person in family:
                batch_stats['gender'][person['JENIS_KELAMIN']] += 1
                
                sh = person['STATUS_HUBUNGAN']
                batch_stats['status_hubungan'][sh] = batch_stats['status_hubungan'].get(sh, 0) + 1
                
                ag = person['AGAMA']
                batch_stats['agama'][ag] = batch_stats['agama'].get(ag, 0) + 1
    
    return all_people, batch_stats


def _worker_generate_batch_streaming(args: Tuple) -> Tuple[int, dict]:
    """
    Worker function that writes directly to temp files (streaming).
    Returns (families_generated, batch_statistics)
    """
    worker_id, total_workers, batch_items, village_lookup, nik_codes_lookup, temp_dir, fieldnames, tempat_lahir_pools, all_tempat_lahir, rt_rw_lookup = args
    
    id_gen = ProcessLocalIDGenerator(worker_id, total_workers)
    temp_file = os.path.join(temp_dir, f"worker_{worker_id}.csv")
    
    batch_stats = {
        'families': 0,
        'people': 0,
        'gender': {'L': 0, 'P': 0},
        'status_hubungan': {},
        'agama': {},
        'villages': {}
    }
    
    with open(temp_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        for village_code, family_count in batch_items:
            village_info = village_lookup[village_code]
            prov_code, reg_code, dist_code = nik_codes_lookup[village_code]
            
            for _ in range(family_count):
                family = _generate_single_family(
                    village_info, id_gen, prov_code, reg_code, dist_code,
                    tempat_lahir_pools, all_tempat_lahir, rt_rw_lookup
                )
                
                # Write immediately to disk
                for person in family:
                    writer.writerow(person)
                    
                    # Update stats
                    batch_stats['people'] += 1
                    batch_stats['gender'][person['JENIS_KELAMIN']] += 1
                    
                    sh = person['STATUS_HUBUNGAN']
                    batch_stats['status_hubungan'][sh] = batch_stats['status_hubungan'].get(sh, 0) + 1
                    
                    ag = person['AGAMA']
                    batch_stats['agama'][ag] = batch_stats['agama'].get(ag, 0) + 1
                
                batch_stats['families'] += 1
                
                village_name = village_info['village_name']
                if village_name not in batch_stats['villages']:
                    batch_stats['villages'][village_name] = {'kk': 0, 'jiwa': 0}
                batch_stats['villages'][village_name]['kk'] += 1
                batch_stats['villages'][village_name]['jiwa'] += len(family)
    
    return batch_stats['families'], batch_stats


class ParallelFamilyGenerator:
    """Generate Indonesian family data using parallel processing"""
    
    # CSV fieldnames for streaming
    FIELDNAMES = [
        'NKK', 'NIK', 'NAMA', 'JENIS_KELAMIN', 'TEMPAT_LAHIR', 'TANGGAL_LAHIR',
        'AGAMA', 'PENDIDIKAN', 'PEKERJAAN', 'STATUS_PERKAWINAN', 'STATUS_HUBUNGAN',
        'GOLONGAN_DARAH', 'KEWARGANEGARAAN', 'NAMA_AYAH', 'NAMA_IBU', 'ALAMAT',
        'RT', 'RW', 'KODE_KELURAHAN', 'KELURAHAN', 'KODE_KECAMATAN', 'KECAMATAN',
        'KODE_KABUPATEN', 'KABUPATEN', 'KODE_PROVINSI', 'PROVINSI', 'LATITUDE', 'LONGITUDE'
    ]
    
    def __init__(self, wilayah_loader: WilayahLoader = None, num_workers: int = None):
        """
        Initialize ParallelFamilyGenerator
        
        Args:
            wilayah_loader: WilayahLoader instance
            num_workers: Number of worker processes (default: cpu_count())
        """
        self.wilayah = wilayah_loader or get_loader()
        self.num_workers = num_workers or cpu_count()
        
        # Build tempat lahir pools for varied birth places
        self.tempat_lahir_pools, self.all_tempat_lahir = build_tempat_lahir_pools(
            self.wilayah.regencies, self.wilayah.districts
        )
        
        # Statistics
        self.stats = self._empty_stats()
    
    def _empty_stats(self) -> dict:
        return {
            'total_families': 0,
            'total_people': 0,
            'gender': {'L': 0, 'P': 0},
            'status_hubungan': {},
            'agama': {},
            'villages': {}
        }
    
    def reset_stats(self):
        self.stats = self._empty_stats()
    
    def _merge_stats(self, batch_stats: dict):
        """Merge batch statistics into main stats"""
        self.stats['total_families'] += batch_stats['families']
        self.stats['total_people'] += batch_stats['people']
        
        for g, c in batch_stats['gender'].items():
            self.stats['gender'][g] += c
        
        for sh, c in batch_stats['status_hubungan'].items():
            self.stats['status_hubungan'][sh] = self.stats['status_hubungan'].get(sh, 0) + c
        
        for ag, c in batch_stats['agama'].items():
            self.stats['agama'][ag] = self.stats['agama'].get(ag, 0) + c
        
        for vname, vdata in batch_stats['villages'].items():
            if vname not in self.stats['villages']:
                self.stats['villages'][vname] = {'kk': 0, 'jiwa': 0}
            self.stats['villages'][vname]['kk'] += vdata['kk']
            self.stats['villages'][vname]['jiwa'] += vdata['jiwa']
    
    def distribute_families(
        self,
        villages: List[dict],
        num_families: int,
        mode: int,
        simulation_data: Dict[str, int] = None,
        correction_percent: int = 0
    ) -> Dict[str, int]:
        """
        Distribute families across villages (same logic as FamilyGenerator)
        
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
            base_count = num_families // len(villages)
            remainder = num_families % len(villages)
            for i, village in enumerate(villages):
                count = base_count + (1 if i < remainder else 0)
                if count > 0:
                    distribution[village['village_code']] = count
        
        elif mode == 2:
            if num_families >= len(villages):
                remaining = num_families - len(villages)
                for village in villages:
                    distribution[village['village_code']] = 1
                if remaining > 0:
                    for _ in range(remaining):
                        village = random.choice(villages)
                        distribution[village['village_code']] += 1
            else:
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
            for _ in range(num_families):
                village = random.choice(villages)
                code = village['village_code']
                distribution[code] = distribution.get(code, 0) + 1
        
        return distribution
    
    def _prepare_batches(
        self,
        distribution: Dict[str, int]
    ) -> List[List[Tuple[str, int]]]:
        """Distribute work items across workers"""
        items = list(distribution.items())
        
        # Divide items among workers
        batches = [[] for _ in range(self.num_workers)]
        
        # Round-robin distribution for better load balancing
        for i, item in enumerate(items):
            batches[i % self.num_workers].append(item)
        
        return batches
    
    def generate_families_parallel(
        self,
        region_code: str,
        num_families: int,
        distribution_mode: int = 1,
        show_progress: bool = True,
        simulation_data: Dict[str, int] = None,
        correction_percent: int = 0
    ) -> List[dict]:
        """
        Generate families using parallel processing (in-memory mode).
        Good for < 500,000 records.
        
        Args:
            region_code: Regional code
            num_families: Number of families
            distribution_mode: 1=even, 2=even random, 3=random, 4=simulation
            show_progress: Show progress bar
            simulation_data: Dict mapping village_code to NKK count (for mode 4)
            correction_percent: Percentage correction for simulation mode
            
        Returns:
            List of all person records
        """
        self.reset_stats()
        
        # Get villages
        villages = self.wilayah.get_sub_regions(region_code)
        if not villages:
            raise ValueError(f"Tidak ada kelurahan untuk kode {region_code}")
        
        # Prepare distribution
        distribution = self.distribute_families(
            villages, num_families, distribution_mode,
            simulation_data=simulation_data, correction_percent=correction_percent
        )
        
        # Recalculate actual num_families for mode 4
        actual_num_families = sum(distribution.values())
        
        # Build lookups for workers (picklable data only)
        village_lookup = {v['village_code']: v for v in villages}
        nik_codes_lookup = {
            v['village_code']: self.wilayah.get_nik_codes(v['village_code'])
            for v in villages
        }
        
        # Prepare batches
        batches = self._prepare_batches(distribution)
        
        # Build worker arguments
        worker_args = [
            (i, self.num_workers, batches[i], village_lookup, nik_codes_lookup,
             self.tempat_lahir_pools, self.all_tempat_lahir, self.wilayah.rt_rw_data)
            for i in range(self.num_workers)
            if batches[i]  # Skip empty batches
        ]
        
        actual_workers = len(worker_args)
        
        if show_progress:
            print(f"🚀 Parallel processing dengan {actual_workers} workers...")
        
        # Process in parallel
        all_people = []
        
        with Pool(actual_workers) as pool:
            if show_progress:
                results = []
                with tqdm(total=actual_num_families, desc="Generating", unit="KK") as pbar:
                    for result, batch_stats in pool.imap_unordered(_worker_generate_batch, worker_args):
                        all_people.extend(result)
                        self._merge_stats(batch_stats)
                        pbar.update(batch_stats['families'])
            else:
                for result, batch_stats in pool.map(_worker_generate_batch, worker_args):
                    all_people.extend(result)
                    self._merge_stats(batch_stats)
        
        # Post-validation: ensure 1 NKK = 1 Kepala Keluarga
        all_people, fixes = validate_and_fix_families(all_people)
        if fixes > 0:
            logger.info(f"Post-validation applied {fixes} auto-fixes to ensure 1 Kepala Keluarga per NKK")
        
        return all_people
    
    def generate_families_streaming(
        self,
        region_code: str,
        num_families: int,
        output_path: str,
        distribution_mode: int = 1,
        show_progress: bool = True,
        simulation_data: Dict[str, int] = None,
        correction_percent: int = 0
    ) -> str:
        """
        Generate families with streaming write to CSV.
        Memory efficient for millions of records.
        
        Args:
            region_code: Regional code
            num_families: Number of families
            output_path: Path for output CSV file
            distribution_mode: 1=even, 2=even random, 3=random, 4=simulation
            show_progress: Show progress bar
            simulation_data: Dict mapping village_code to NKK count (for mode 4)
            correction_percent: Percentage correction for simulation mode
            
        Returns:
            Path to output CSV file
        """
        import tempfile
        import shutil
        
        self.reset_stats()
        
        # Get villages
        villages = self.wilayah.get_sub_regions(region_code)
        if not villages:
            raise ValueError(f"Tidak ada kelurahan untuk kode {region_code}")
        
        # Prepare distribution
        distribution = self.distribute_families(
            villages, num_families, distribution_mode,
            simulation_data=simulation_data, correction_percent=correction_percent
        )
        
        # Recalculate actual num_families for mode 4
        actual_num_families = sum(distribution.values())
        
        # Build lookups
        village_lookup = {v['village_code']: v for v in villages}
        nik_codes_lookup = {
            v['village_code']: self.wilayah.get_nik_codes(v['village_code'])
            for v in villages
        }
        
        # Prepare batches
        batches = self._prepare_batches(distribution)
        
        # Create temp directory for worker outputs
        temp_dir = tempfile.mkdtemp(prefix="dukcapil_gen_")
        
        try:
            # Build worker arguments
            worker_args = [
                (i, self.num_workers, batches[i], village_lookup, nik_codes_lookup, 
                 temp_dir, self.FIELDNAMES, self.tempat_lahir_pools, self.all_tempat_lahir,
                 self.wilayah.rt_rw_data)
                for i in range(self.num_workers)
                if batches[i]
            ]
            
            actual_workers = len(worker_args)
            
            if show_progress:
                print(f"🚀 Streaming parallel dengan {actual_workers} workers...")
            
            # Process in parallel
            with Pool(actual_workers) as pool:
                if show_progress:
                    with tqdm(total=actual_num_families, desc="Generating", unit="KK") as pbar:
                        for families_done, batch_stats in pool.imap_unordered(
                            _worker_generate_batch_streaming, worker_args
                        ):
                            self._merge_stats(batch_stats)
                            pbar.update(families_done)
                else:
                    for families_done, batch_stats in pool.map(
                        _worker_generate_batch_streaming, worker_args
                    ):
                        self._merge_stats(batch_stats)
            
            # Merge temp files into final output
            if show_progress:
                print("📝 Menggabungkan hasil...")
            
            with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                
                # Append each worker's temp file
                for i in range(self.num_workers):
                    temp_file = os.path.join(temp_dir, f"worker_{i}.csv")
                    if os.path.exists(temp_file):
                        with open(temp_file, 'r', encoding='utf-8') as infile:
                            reader = csv.DictReader(infile, fieldnames=self.FIELDNAMES)
                            for row in reader:
                                writer.writerow(row)
            
            return output_path
        
        finally:
            # Cleanup temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def get_statistics(self) -> dict:
        """Get generation statistics"""
        stats = self.stats.copy()
        
        if stats['total_families'] > 0:
            stats['avg_members_per_family'] = round(
                stats['total_people'] / stats['total_families'], 2
            )
        else:
            stats['avg_members_per_family'] = 0
        
        sorted_villages = sorted(
            stats['villages'].items(),
            key=lambda x: x[1]['kk'],
            reverse=True
        )
        stats['top_villages'] = sorted_villages[:5]
        
        return stats


def get_optimal_workers() -> int:
    """Get optimal number of workers based on system"""
    cores = cpu_count()
    # Leave 1-2 cores free for system
    if cores > 4:
        return cores - 2
    elif cores > 2:
        return cores - 1
    else:
        return cores
