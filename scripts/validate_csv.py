#!/usr/bin/env python3
"""
DUKCAPIL CSV Validator
Validate NKK consistency rules in generated CSV files

Usage:
    python scripts/validate_csv.py <csv_file>
    python scripts/validate_csv.py output/dukcapil_7371_20251228_142646.csv
"""

import sys
import os
import pandas as pd
from collections import defaultdict

def validate_nkk_consistency(csv_path: str, show_samples: bool = True, sample_limit: int = 3):
    """
    Validate NKK consistency rules:
    1. Each NKK has exactly 1 Kepala Keluarga
    2. All members in same NKK have same AGAMA
    3. All members in same NKK have same address
    
    Args:
        csv_path: Path to CSV file
        show_samples: Show sample invalid NKKs
        sample_limit: Number of samples to show
    """
    print(f"\n{'='*60}")
    print(f"DUKCAPIL CSV VALIDATOR")
    print(f"{'='*60}")
    print(f"File: {csv_path}")
    
    # Load CSV
    print("\nLoading CSV...")
    df = pd.read_csv(csv_path, low_memory=False)
    
    total_records = len(df)
    total_nkk = df['NKK'].nunique()
    
    print(f"Total records: {total_records:,}")
    print(f"Total unique NKK: {total_nkk:,}")
    print(f"Average members per NKK: {total_records / total_nkk:.2f}")
    
    issues = {
        'no_kepala': [],
        'multiple_kepala': [],
        'different_agama': [],
        'different_address': []
    }
    
    # Group by NKK for validation
    print("\nValidating NKK consistency...")
    
    for nkk, group in df.groupby('NKK'):
        # 1. Check Kepala Keluarga count
        kepala_count = (group['STATUS_HUBUNGAN'] == 'Kepala Keluarga').sum()
        if kepala_count == 0:
            issues['no_kepala'].append(nkk)
        elif kepala_count > 1:
            issues['multiple_kepala'].append(nkk)
        
        # 2. Check AGAMA consistency
        if group['AGAMA'].nunique() > 1:
            issues['different_agama'].append(nkk)
        
        # 3. Check address consistency (KODE_KELURAHAN)
        if group['KODE_KELURAHAN'].nunique() > 1:
            issues['different_address'].append(nkk)
    
    # Print results
    print(f"\n{'='*60}")
    print("VALIDATION RESULTS")
    print(f"{'='*60}")
    
    print("\n--- 1. Kepala Keluarga Validation ---")
    valid_kepala = total_nkk - len(issues['no_kepala']) - len(issues['multiple_kepala'])
    print(f"  ✅ Valid (exactly 1): {valid_kepala:,}")
    print(f"  ❌ No Kepala Keluarga: {len(issues['no_kepala']):,}")
    print(f"  ❌ Multiple Kepala Keluarga: {len(issues['multiple_kepala']):,}")
    
    print("\n--- 2. AGAMA Validation ---")
    valid_agama = total_nkk - len(issues['different_agama'])
    print(f"  ✅ Consistent: {valid_agama:,}")
    print(f"  ❌ Different AGAMA in NKK: {len(issues['different_agama']):,}")
    
    print("\n--- 3. Address Validation ---")
    valid_address = total_nkk - len(issues['different_address'])
    print(f"  ✅ Consistent: {valid_address:,}")
    print(f"  ❌ Different address in NKK: {len(issues['different_address']):,}")
    
    # Show samples
    if show_samples:
        print(f"\n{'='*60}")
        print("SAMPLE INVALID NKKs")
        print(f"{'='*60}")
        
        if issues['multiple_kepala']:
            print(f"\n--- Sample NKK with Multiple Kepala Keluarga ---")
            for nkk in issues['multiple_kepala'][:sample_limit]:
                sample = df[df['NKK'] == nkk][['NKK', 'NAMA', 'STATUS_HUBUNGAN', 'AGAMA']]
                print(f"\nNKK: {nkk}")
                print(sample.to_string(index=False))
        
        if issues['different_agama']:
            print(f"\n--- Sample NKK with Different AGAMA ---")
            for nkk in issues['different_agama'][:sample_limit]:
                sample = df[df['NKK'] == nkk][['NKK', 'NAMA', 'STATUS_HUBUNGAN', 'AGAMA']]
                print(f"\nNKK: {nkk}")
                print(sample.to_string(index=False))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    total_issues = (len(issues['no_kepala']) + len(issues['multiple_kepala']) + 
                    len(issues['different_agama']) + len(issues['different_address']))
    
    if total_issues == 0:
        print("\n✅ ALL VALID: All NKK meet consistency rules")
        return True
    else:
        print(f"\n❌ INVALID: {total_issues:,} total issues found")
        print("\nIssue breakdown:")
        print(f"  - No Kepala Keluarga: {len(issues['no_kepala']):,}")
        print(f"  - Multiple Kepala Keluarga: {len(issues['multiple_kepala']):,}")
        print(f"  - Different AGAMA: {len(issues['different_agama']):,}")
        print(f"  - Different Address: {len(issues['different_address']):,}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_csv.py <csv_file>")
        print("Example: python scripts/validate_csv.py output/dukcapil_7371_20251228_142646.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)
    
    is_valid = validate_nkk_consistency(csv_path)
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
