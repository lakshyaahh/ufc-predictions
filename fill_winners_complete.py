import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 70)
print("UFC FIGHT RESULTS - FILLING WINNER COLUMN")
print("=" * 70)

# Load the master UFC dataset with all historical results
master_fights = pd.read_csv("dataset/Ultimate ufc/ufc-master.csv")
print(f"\n[OK] Loaded ufc-master.csv: {len(master_fights)} historical fights")

# Convert date columns to datetime
master_fights['Date'] = pd.to_datetime(master_fights['Date'])

# Function to normalize fighter names for matching
def normalize_name(name):
    if pd.isna(name):
        return ""
    return str(name).strip().lower()

# Create a lookup dictionary for quick access
# Key: (red_fighter_normalized, blue_fighter_normalized), Value: winner
fight_results = {}
reverse_results = {}

for _, row in master_fights.iterrows():
    red_norm = normalize_name(row['RedFighter'])
    blue_norm = normalize_name(row['BlueFighter'])
    winner = row['Winner']  # 'Red' or 'Blue'
    
    # Store both orientations
    fight_results[(red_norm, blue_norm)] = winner
    reverse_results[(blue_norm, red_norm)] = 'Red' if winner == 'Blue' else 'Blue'

print(f"[OK] Built fight results lookup: {len(fight_results)} unique matchups")

# Process each CSV file in the workspace
import os
from pathlib import Path

csv_files_to_process = [
    "master_dataset.csv",
    "dataset/Ultimate ufc/upcoming.csv"
]

for csv_file in csv_files_to_process:
    filepath = csv_file
    if not os.path.exists(filepath):
        print(f"\n[WARNING] File not found: {filepath}")
        continue
    
    # Load the dataset
    df = pd.read_csv(filepath)
    print(f"\n{'=' * 70}")
    print(f"Processing: {filepath}")
    print(f"{'=' * 70}")
    print(f"Total fights: {len(df)}")
    
    if 'Winner' not in df.columns:
        print("[WARNING] No Winner column found. Skipping.")
        continue
    
    # Count current status
    empty_count = (df['Winner'].isna().sum()) + (df['Winner'] == '').sum()
    filled_count = len(df) - empty_count
    print(f"Already filled: {filled_count}")
    print(f"Empty/Unknown: {empty_count}")
    
    if empty_count == 0 and filled_count == len(df):
        print("[OK] All fights already have winner results!")
        continue
    
    # Fill empty winners
    updated = 0
    not_found_list = []
    
    for idx, row in df.iterrows():
        # Check if already has a winner
        if pd.notna(row['Winner']) and str(row['Winner']).strip() != '':
            continue
        
        red_fighter = normalize_name(row['RedFighter'])
        blue_fighter = normalize_name(row['BlueFighter'])
        
        if not red_fighter or not blue_fighter:
            continue
        
        # Look up the fight result
        if (red_fighter, blue_fighter) in fight_results:
            winner = fight_results[(red_fighter, blue_fighter)]
            df.at[idx, 'Winner'] = 'RedFighter' if winner == 'Red' else 'BlueFighter'
            updated += 1
        elif (blue_fighter, red_fighter) in reverse_results:
            winner = reverse_results[(blue_fighter, red_fighter)]
            df.at[idx, 'Winner'] = 'RedFighter' if winner == 'Red' else 'BlueFighter'
            updated += 1
        else:
            not_found_list.append({
                'Red': row['RedFighter'],
                'Blue': row['BlueFighter'],
                'Date': row.get('Date', 'N/A')
            })
    
    # Save the updated file
    if updated > 0:
        df.to_csv(filepath, index=False)
        print(f"\n[SUCCESS] Updated: {updated} fights")
        print(f"   Saved to: {filepath}")
    
    if not_found_list:
        print(f"\n[WARNING] Could not find in historical data: {len(not_found_list)} fights")
        if len(not_found_list) <= 15:
            for fight in not_found_list[:10]:
                print(f"   • {fight['Red']} vs {fight['Blue']} ({fight['Date']})")
            if len(not_found_list) > 10:
                print(f"   ... and {len(not_found_list) - 10} more")

print("\n" + "=" * 70)
print("[SUCCESS] WINNER COLUMN FILL COMPLETE")
print("=" * 70)
