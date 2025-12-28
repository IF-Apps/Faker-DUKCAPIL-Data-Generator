#!/usr/bin/env python3
"""
Test script to validate generator consistency
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parallel_generator import ParallelFamilyGenerator
from collections import defaultdict
import time

def test_parallel_generator(num_families=100000, num_workers=4):
    print(f'=== TEST: {num_families:,} families with {num_workers} workers ===')
    start = time.time()
    gen = ParallelFamilyGenerator(num_workers=num_workers)
    people = gen.generate_families_parallel('7371', num_families, show_progress=True)
    elapsed = time.time() - start

    # Validate
    nkk_groups = defaultdict(list)
    nik_set = set()
    for p in people:
        nkk_groups[p['NKK']].append(p)
        nik_set.add(p['NIK'])

    total_nkk = len(nkk_groups)
    total_nik = len(nik_set)

    print(f'\nTime: {elapsed:.2f}s')
    print(f'Total people: {len(people):,}')
    print(f'Total unique NKK: {total_nkk:,} (expected: {num_families:,})')
    print(f'Total unique NIK: {total_nik:,} (expected: {len(people):,})')

    # Check all rules
    nkk_multi_kepala = sum(1 for members in nkk_groups.values() 
                           if sum(1 for m in members if m['STATUS_HUBUNGAN'] == 'Kepala Keluarga') > 1)
    nkk_no_kepala = sum(1 for members in nkk_groups.values() 
                        if sum(1 for m in members if m['STATUS_HUBUNGAN'] == 'Kepala Keluarga') == 0)
    nkk_diff_agama = sum(1 for members in nkk_groups.values() 
                         if len(set(m['AGAMA'] for m in members)) > 1)
    nkk_diff_addr = sum(1 for members in nkk_groups.values() 
                        if len(set(m['KODE_KELURAHAN'] for m in members)) > 1)

    print('')
    print('=== Validation Results ===')
    print(f'NKK collision: {num_families - total_nkk}')
    print(f'NIK collision: {len(people) - total_nik}')
    print(f'NKK with 0 Kepala Keluarga: {nkk_no_kepala}')
    print(f'NKK with >1 Kepala Keluarga: {nkk_multi_kepala}')
    print(f'NKK with different AGAMA: {nkk_diff_agama}')
    print(f'NKK with different address: {nkk_diff_addr}')

    all_valid = (total_nkk == num_families and 
                 total_nik == len(people) and
                 nkk_multi_kepala == 0 and 
                 nkk_no_kepala == 0 and
                 nkk_diff_agama == 0 and 
                 nkk_diff_addr == 0)

    print('')
    if all_valid:
        print('=== RESULT: ALL VALID! ===')
        return 0
    else:
        print('=== RESULT: INVALID ===')
        return 1


if __name__ == '__main__':
    num_families = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    sys.exit(test_parallel_generator(num_families, num_workers))
