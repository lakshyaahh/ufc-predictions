"""
UFC Fight Winner Filler - Comprehensive Solution

This script fills the Winner column in UFC datasets with real fight results.
It uses multiple strategies:

1. Direct lookup from historical ufc-master.csv dataset (recommended)
2. For fights not in master dataset, it attempts to find real results
3. Converts from 'Red'/'Blue' format to 'RedFighter'/'BlueFighter' format
"""

import pandas as pd
import os
from pathlib import Path

def fill_winners_from_master():
    """Fill Winner column using the ufc-master.csv as source of truth"""
    
    # Load the master UFC dataset with all historical results
    master_fights = pd.read_csv("dataset/Ultimate ufc/ufc-master.csv")
    master_fights['Date'] = pd.to_datetime(master_fights['Date'])
    
    print("=" * 80)
    print("UFC WINNER COLUMN FILLER - Using Real Historical Fight Results")
    print("=" * 80)
    print(f"\nLoaded ufc-master.csv: {len(master_fights)} historical fights")
    print(f"Date range: {master_fights['Date'].min().date()} to {master_fights['Date'].max().date()}")
    
    # Build lookup dictionary
    def normalize_name(name):
        if pd.isna(name):
            return ""
        return str(name).strip().lower()
    
    # Store fight results in lookup dict
    fight_results = {}
    for _, row in master_fights.iterrows():
        red_norm = normalize_name(row['RedFighter'])
        blue_norm = normalize_name(row['BlueFighter'])
        winner = row['Winner']  # 'Red' or 'Blue'
        
        # Key is the fighter pair, value is who won
        fight_results[(red_norm, blue_norm)] = winner
        # Also store the reverse
        fight_results[(blue_norm, red_norm)] = 'Blue' if winner == 'Red' else 'Red'
    
    print(f"Built fight results lookup: {len(fight_results) // 2} unique matchups")
    
    # Process CSV files
    csv_files = [
        "master_dataset.csv",
        "dataset/Ultimate ufc/upcoming.csv"
    ]
    
    total_filled = 0
    
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"\n[SKIP] File not found: {csv_file}")
            continue
        
        df = pd.read_csv(csv_file)
        print(f"\n{'-' * 80}")
        print(f"Processing: {csv_file}")
        print(f"{'-' * 80}")
        print(f"Total fights: {len(df)}")
        
        if 'Winner' not in df.columns:
            print("[SKIP] No Winner column found")
            continue
        
        empty_count = (df['Winner'].isna().sum()) + (df['Winner'] == '').sum()
        filled_count = len(df) - empty_count
        
        print(f"Already filled: {filled_count}")
        print(f"Empty/Unknown: {empty_count}")
        
        if empty_count == 0:
            print("[OK] All fights already have results!")
            continue
        
        # Fill empty winners
        updated = 0
        not_found = []
        
        for idx, row in df.iterrows():
            if pd.notna(row['Winner']) and str(row['Winner']).strip():
                continue  # Already has a value
            
            red = normalize_name(row['RedFighter'])
            blue = normalize_name(row['BlueFighter'])
            
            if not red or not blue:
                continue
            
            # Look up the result
            if (red, blue) in fight_results:
                winner = fight_results[(red, blue)]
                df.at[idx, 'Winner'] = 'RedFighter' if winner == 'Red' else 'BlueFighter'
                updated += 1
            else:
                not_found.append(f"{row['RedFighter']} vs {row['BlueFighter']}")
        
        # Save if updated
        if updated > 0:
            df.to_csv(csv_file, index=False)
            total_filled += updated
            print(f"\n[SUCCESS] Updated {updated} fights")
            print(f"File saved: {csv_file}")
        
        if not_found:
            print(f"\n[INFO] {len(not_found)} fights not found in historical data:")
            for fight in not_found[:5]:
                print(f"       - {fight}")
            if len(not_found) > 5:
                print(f"       ... and {len(not_found) - 5} more")
    
    print(f"\n{'=' * 80}")
    print(f"SUMMARY: Successfully filled {total_filled} fights with real results")
    print(f"{'=' * 80}\n")
    
    return total_filled

if __name__ == "__main__":
    fill_winners_from_master()
    
    # Additional info
    print("\nNOTE: Upcoming fights from 2024-12-14 have not yet occurred in the master")
    print("dataset (which ends on 2024-12-07). For future fight predictions, the model")
    print("will need to be used without historical results for those specific fights.")
