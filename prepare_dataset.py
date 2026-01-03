import pandas as pd

# === 1. Load CSVs ===
upcoming = pd.read_csv("dataset/Ultimate ufc/upcoming.csv")
events = pd.read_csv("dataset/Ultimate ufc/ufc-master.csv")  # or adjust if events file is elsewhere
# fights dataset is large, load only if needed
# fights = pd.read_csv("dataset/Ultimate ufc/ufc-master.csv")

# === 2. Inspect columns ===
print("Upcoming fights sample:")
print(upcoming.head())
print("\nEvents sample:")
print(events.head())

# === 3. Select relevant columns from upcoming ===
cols_to_keep = [
    "RedFighter", "BlueFighter", "Date", "Location", "Country",
    "WeightClass", "Gender", "NumberOfRounds",
    "RedAge", "BlueAge",
    "RedHeightCms", "BlueHeightCms",
    "RedReachCms", "BlueReachCms",
    "RedCurrentWinStreak", "BlueCurrentWinStreak",
    "RedCurrentLoseStreak", "BlueCurrentLoseStreak",
    "RedWinsByKO", "BlueWinsByKO",
    "RedWinsBySubmission", "BlueWinsBySubmission",
    "RedWins", "BlueWins",
    "RedLosses", "BlueLosses",
    "Winner"
]

df = upcoming[cols_to_keep].copy()

# === 4. Feature Engineering ===
df["ReachDiff"] = df["RedReachCms"] - df["BlueReachCms"]
df["HeightDiff"] = df["RedHeightCms"] - df["BlueHeightCms"]
df["AgeDiff"] = df["RedAge"] - df["BlueAge"]
df["WinStreakDiff"] = df["RedCurrentWinStreak"] - df["BlueCurrentWinStreak"]
df["LoseStreakDiff"] = df["RedCurrentLoseStreak"] - df["BlueCurrentLoseStreak"]
df["KODiff"] = df["RedWinsByKO"] - df["BlueWinsByKO"]
df["SubDiff"] = df["RedWinsBySubmission"] - df["BlueWinsBySubmission"]
df["WinDiff"] = df["RedWins"] - df["BlueWins"]
df["LossDiff"] = df["RedLosses"] - df["BlueLosses"]

# === 5. Save cleaned dataset ===
df.to_csv("dataset/Ultimate ufc/master_dataset.csv", index=False)

print("\n✅ Cleaned dataset saved as dataset/Ultimate ufc/master_dataset.csv")
print("Columns in master dataset:", df.columns.tolist())