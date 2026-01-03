import pandas as pd
import numpy as np

print("=" * 80)
print("CREATING EXPANDED TRAINING DATASET FROM UFC-MASTER")
print("=" * 80)

# Load the master UFC dataset with all historical results
master = pd.read_csv("ufc-master.csv")
print(f"\nLoaded ufc-master.csv: {len(master)} total fights")

# Convert dates
master['Date'] = pd.to_datetime(master['Date'])

# We need the required features to be available
required_features = [
    "ReachDiff", "HeightDiff", "AgeDiff",
    "WinStreakDif", "WinStreakDif", "LoseStreakDif",
    "KODif", "SubDif", "WinDif", "LossDif",
    "Winner"
]

# Check what columns we have
print(f"\nAvailable columns: {master.columns.tolist()[:20]}")

# The ufc-master has different naming - let me check
print("\nLooking for feature columns...")

# Check if the feature columns exist
available_cols = master.columns.tolist()
feature_cols_present = []
feature_cols_missing = []

potential_features = {
    "ReachDiff": ["ReachDif", "ReachDiff"],
    "HeightDiff": ["HeightDif", "HeightDiff"],  
    "AgeDif": ["AgeDif", "AgeDiff"],
    "WinStreakDif": ["WinStreakDif", "WinStreakDiff"],
    "LoseStreakDif": ["LoseStreakDif", "LoseStreakDiff"],
    "KODif": ["KODif", "KODiff"],
    "SubDif": ["SubDif", "SubDiff"],
    "WinDif": ["WinDif", "WinDiff"],
    "LossDif": ["LossDif", "LossDiff"]
}

# Map the features
feature_mapping = {}
for target_name, possible_names in potential_features.items():
    for possible in possible_names:
        if possible in available_cols:
            feature_mapping[target_name] = possible
            print(f"  Found: {target_name} -> {possible}")
            break
    else:
        print(f"  MISSING: {target_name}")

print(f"\nFeature columns mapped: {len(feature_mapping)}/{len(potential_features)}")

# Get features that exist
features_to_use = list(feature_mapping.values())
print(f"\nFeatures available for training: {features_to_use}")

# Filter dataset
# 1. Remove rows with missing Winner or "Unknown" winner
df_clean = master[master['Winner'].notna()].copy()
df_clean = df_clean[df_clean['Winner'] != '']
df_clean = df_clean[~df_clean['Winner'].str.lower().str.contains('unknown', na=False)]

print(f"\nAfter filtering for valid winners: {len(df_clean)} fights")

# 2. Remove rows with missing features
for col in features_to_use:
    df_clean = df_clean[df_clean[col].notna()]

print(f"After filtering for valid features: {len(df_clean)} fights")

# 3. Convert Winner format from "Red"/"Blue" to "RedFighter"/"BlueFighter"
df_clean['Winner'] = df_clean['Winner'].apply(lambda x: 'RedFighter' if x == 'Red' else 'BlueFighter')

# 4. Select only needed columns
columns_needed = features_to_use + ['Winner']
df_final = df_clean[columns_needed].copy()

# Rename columns to match our standard format
rename_dict = {}
for target, source in feature_mapping.items():
    if source in df_final.columns:
        rename_dict[source] = target

df_final = df_final.rename(columns=rename_dict)

print(f"\nFinal dataset shape: {len(df_final)} fights x {len(df_final.columns)} columns")
print(f"Winner distribution:")
print(df_final['Winner'].value_counts())

# Save the expanded dataset
df_final.to_csv("master_dataset.csv", index=False)
print(f"\n✅ Saved {len(df_final)} fights to master_dataset.csv")

# Show sample
print(f"\nSample data (first 3 rows):")
print(df_final.head(3))
