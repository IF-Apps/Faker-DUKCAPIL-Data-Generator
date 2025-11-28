"""
Parallel Family Generator Module
Generate Indonesian family data using multiprocessing for improved performance
"""

import os
import csv
import json
import random
from datetime import date
from typing import List, Dict, Tuple, Optional, Generator
from multiprocessing import Pool, cpu_count, Manager
from functools import partial
import queue
import threading

from tqdm import tqdm

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
        
        # Track used NIKs within this worker to avoid duplicates
        self._used_niks: set = set()
    
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
        
        # Get next sequence number
        if base_key not in self._nik_sequences:
            self._nik_sequences[base_key] = 0
        
        # Find next available unique sequence
        max_attempts = 10000
        for _ in range(max_attempts):
            self._nik_sequences[base_key] += 1
            local_seq = self._nik_sequences[base_key]
            
            # Create unique sequence: combine worker_id with local sequence
            # Format: worker_id (1 digit) + local_seq (3 digits) = 4 digits
            # This gives each worker up to 999 sequences per base_key
            # For more workers, use modulo to create unique combinations
            if self.total_workers <= 10:
                # Worker 0-9: sequence = W000-W999
                sequence = (self.worker_id * 1000) + (local_seq % 1000)
            else:
                # More workers: interleave sequences
                sequence = (local_seq * self.total_workers + self.worker_id) % 10000
            
            if sequence == 0:
                sequence = 1  # Avoid 0000
            
            nik = f"{province_code}{regency_code}{district_code}{date_str}{sequence:04d}"
            
            if nik not in self._used_niks:
                self._used_niks.add(nik)
                return nik
        
        # Fallback: use timestamp-based unique suffix
        import time
        timestamp_suffix = int(time.time() * 1000) % 10000
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
        
        date_str = f"{issue_date.day:02d}{issue_date.month:02d}{issue_date.year % 100:02d}"
        base_key = f"NKK_{province_code}{regency_code}{district_code}{date_str}"
        
        if base_key not in self._nkk_sequences:
            self._nkk_sequences[base_key] = 0
        
        self._nkk_sequences[base_key] += 1
        local_seq = self._nkk_sequences[base_key]
        
        # Create unique sequence combining worker_id with local sequence
        if self.total_workers <= 10:
            sequence = (self.worker_id * 1000) + (local_seq % 1000)
        else:
            sequence = (local_seq * self.total_workers + self.worker_id) % 10000
        
        if sequence == 0:
            sequence = 1
        
        return f"{province_code}{regency_code}{district_code}{date_str}{sequence:04d}"


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
    
    return family_members


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
        mode: int
    ) -> Dict[str, int]:
        """Distribute families across villages (same logic as FamilyGenerator)"""
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
        show_progress: bool = True
    ) -> List[dict]:
        """
        Generate families using parallel processing (in-memory mode).
        Good for < 500,000 records.
        
        Args:
            region_code: Regional code
            num_families: Number of families
            distribution_mode: 1=even, 2=even random, 3=random
            show_progress: Show progress bar
            
        Returns:
            List of all person records
        """
        self.reset_stats()
        
        # Get villages
        villages = self.wilayah.get_sub_regions(region_code)
        if not villages:
            raise ValueError(f"Tidak ada kelurahan untuk kode {region_code}")
        
        # Prepare distribution
        distribution = self.distribute_families(villages, num_families, distribution_mode)
        
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
                with tqdm(total=num_families, desc="Generating", unit="KK") as pbar:
                    for result, batch_stats in pool.imap_unordered(_worker_generate_batch, worker_args):
                        all_people.extend(result)
                        self._merge_stats(batch_stats)
                        pbar.update(batch_stats['families'])
            else:
                for result, batch_stats in pool.map(_worker_generate_batch, worker_args):
                    all_people.extend(result)
                    self._merge_stats(batch_stats)
        
        return all_people
    
    def generate_families_streaming(
        self,
        region_code: str,
        num_families: int,
        output_path: str,
        distribution_mode: int = 1,
        show_progress: bool = True
    ) -> str:
        """
        Generate families with streaming write to CSV.
        Memory efficient for millions of records.
        
        Args:
            region_code: Regional code
            num_families: Number of families
            output_path: Path for output CSV file
            distribution_mode: 1=even, 2=even random, 3=random
            show_progress: Show progress bar
            
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
        distribution = self.distribute_families(villages, num_families, distribution_mode)
        
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
                    with tqdm(total=num_families, desc="Generating", unit="KK") as pbar:
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
