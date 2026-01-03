import pandas as pd
import joblib

print("="*80)
print("UFC FIGHT OUTCOME PREDICTIONS")
print("="*80)

# === 1. Load trained model ===
try:
    model = joblib.load("ufc_prediction_model.pkl")
    print("\n[OK] Loaded trained model: ufc_prediction_model.pkl")
except FileNotFoundError:
    print("\n[ERROR] Model file not found: ufc_prediction_model.pkl")
    print("Please run train_model.py first to train the model")
    exit(1)

# === 2. Load upcoming fights dataset ===
try:
    # Try the upcoming.csv file (has 13 fights for Dec 14, 2024)
    upcoming = pd.read_csv("upcoming.csv")
    print(f"[OK] Loaded upcoming fights: {len(upcoming)} fights")
except FileNotFoundError:
    print("\n[ERROR] upcoming.csv not found")
    try:
        upcoming = pd.read_csv("upcoming_fights.csv")
        print(f"[OK] Loaded from upcoming_fights.csv: {len(upcoming)} fights")
    except FileNotFoundError:
        print("[ERROR] Neither upcoming.csv nor upcoming_fights.csv found")
        exit(1)

# === 3. Define the same features used in training ===
# Note: Model trained with ReachDiff/HeightDiff, but upcoming.csv has ReachDif/HeightDif
# Need to rename columns to match training data
column_mapping = {
    'ReachDif': 'ReachDiff',
    'HeightDif': 'HeightDiff'
}

for old_name, new_name in column_mapping.items():
    if old_name in upcoming.columns and new_name not in upcoming.columns:
        upcoming = upcoming.rename(columns={old_name: new_name})

features = [
    "ReachDiff", "HeightDiff", "AgeDif",
    "WinStreakDif", "LoseStreakDif",
    "KODif", "SubDif", "WinDif", "LossDif"
]

# === 4. Check if all features exist ===
missing_features = [f for f in features if f not in upcoming.columns]
if missing_features:
    print(f"\n[ERROR] Missing features in upcoming.csv: {missing_features}")
    print(f"Available columns: {upcoming.columns.tolist()[:20]}")
    exit(1)

print(f"[OK] All {len(features)} features available")

# === 5. Extract features and make predictions ===
X_upcoming = upcoming[features]
predictions = model.predict(X_upcoming)
probs = model.predict_proba(X_upcoming)

# Get class labels to map probabilities correctly
class_labels = model.classes_
print(f"Model classes: {list(class_labels)}\n")

# === 6. Create results dataframe ===
results = pd.DataFrame({
    'RedFighter': upcoming['RedFighter'],
    'BlueFighter': upcoming['BlueFighter'],
    'Date': upcoming.get('Date', 'N/A'),
    'Predicted_Winner': predictions,
})

# Map probabilities to correct fighter
for i, class_label in enumerate(class_labels):
    if class_label == 'RedFighter':
        results['RedFighter_Win_Probability'] = probs[:, i] * 100
    else:
        results['BlueFighter_Win_Probability'] = probs[:, i] * 100

# === 7. Display predictions ===
print("="*80)
print("FIGHT PREDICTIONS (13 Fights - Dec 14, 2024)")
print("="*80 + "\n")

for idx, row in results.iterrows():
    red = row['RedFighter']
    blue = row['BlueFighter']
    predicted = row['Predicted_Winner']
    red_prob = row['RedFighter_Win_Probability']
    blue_prob = row['BlueFighter_Win_Probability']
    
    print(f"{idx+1:2d}. {red:25s} vs {blue:25s}")
    print(f"    Prediction: {predicted:15s} | {red}: {red_prob:5.1f}%  |  {blue}: {blue_prob:5.1f}%")

# === 8. Save predictions to CSV ===
output_file = "predictions.csv"
results.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print(f"[SUCCESS] Predictions saved to: {output_file}")
print(f"{'='*80}\n")

# === 9. Summary statistics ===
red_predicted_wins = (results['Predicted_Winner'] == 'RedFighter').sum()
blue_predicted_wins = (results['Predicted_Winner'] == 'BlueFighter').sum()

print("SUMMARY:")
print(f"  Total fights predicted: {len(results)}")
print(f"  RedFighter predicted wins: {red_predicted_wins}")
print(f"  BlueFighter predicted wins: {blue_predicted_wins}")
avg_confidence = results[['RedFighter_Win_Probability', 'BlueFighter_Win_Probability']].max(axis=1).mean()
print(f"  Average prediction confidence: {avg_confidence:.1f}%")
print(f"\nNext: Check predictions.csv for detailed probabilities")