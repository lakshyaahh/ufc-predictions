import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load datasets
master_df = pd.read_csv("dataset/Ultimate ufc/ufc-master.csv")
upcoming_df = pd.read_csv("dataset/Ultimate ufc/upcoming.csv")

# Convert Date columns to datetime for comparison
master_df['Date'] = pd.to_datetime(master_df['Date'])
upcoming_df['Date'] = pd.to_datetime(upcoming_df['Date'])

print(f"Master dataset: {len(master_df)} fights")
print(f"Upcoming dataset before: {len(upcoming_df)} fights")
print(f"Fights with empty Winner in upcoming: {upcoming_df['Winner'].isna().sum() + (upcoming_df['Winner'] == '').sum()}")

# Function to normalize fighter names
def normalize_name(name):
    if pd.isna(name):
        return ""
    return str(name).strip().lower()

# Track how many we fill
filled_count = 0
not_found = []

for idx, upcoming_row in upcoming_df.iterrows():
    if pd.notna(upcoming_row['Winner']) and upcoming_row['Winner'] != '':
        continue  # Already has a winner
    
    red_fighter = normalize_name(upcoming_row['RedFighter'])
    blue_fighter = normalize_name(upcoming_row['BlueFighter'])
    fight_date = upcoming_row['Date']
    
    # Try to find matching fight in master dataset
    # Look for exact fighter name match and similar date (within 1 year)
    matches = master_df[
        ((master_df['RedFighter'].apply(normalize_name) == red_fighter) &
         (master_df['BlueFighter'].apply(normalize_name) == blue_fighter)) |
        ((master_df['RedFighter'].apply(normalize_name) == blue_fighter) &
         (master_df['BlueFighter'].apply(normalize_name) == red_fighter))
    ]
    
    if len(matches) > 0:
        # If multiple matches, take the closest one by date
        if len(matches) > 1:
            matches['date_diff'] = abs((matches['Date'] - fight_date).dt.days)
            best_match = matches.loc[matches['date_diff'].idxmin()]
        else:
            best_match = matches.iloc[0]
        
        # Determine if Red or Blue fighter won
        if normalize_name(best_match['RedFighter']) == red_fighter:
            winner = 'Red' if best_match['Winner'] == 'Red' else 'Blue'
        else:
            # Fight was reversed in master dataset
            winner = 'Red' if best_match['Winner'] == 'Blue' else 'Blue'
        
        # Map to RedFighter or BlueFighter format
        if winner == 'Red':
            upcoming_df.at[idx, 'Winner'] = 'RedFighter'
        else:
            upcoming_df.at[idx, 'Winner'] = 'BlueFighter'
        
        filled_count += 1
    else:
        not_found.append({
            'index': idx,
            'RedFighter': upcoming_row['RedFighter'],
            'BlueFighter': upcoming_row['BlueFighter'],
            'Date': fight_date
        })

print(f"\n✅ Filled {filled_count} fights with winners")
print(f"⚠️  Could not find {len(not_found)} fights in master dataset")

if not_found and len(not_found) <= 20:
    print("\nFights not found:")
    for fight in not_found:
        print(f"  {fight['RedFighter']} vs {fight['BlueFighter']} ({fight['Date'].date()})")

# Save updated dataset
upcoming_df.to_csv("dataset/Ultimate ufc/upcoming.csv", index=False)
print(f"\n✅ Updated upcoming.csv saved")
print(f"Total fights with Winner now: {(upcoming_df['Winner'].notna() & (upcoming_df['Winner'] != '')).sum()}")
