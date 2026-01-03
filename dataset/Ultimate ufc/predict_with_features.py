import pandas as pd
import joblib

print("="*80)
print("UFC FIGHT OUTCOME PREDICTIONS - WITH FEATURE CALCULATION")
print("="*80)

# === 1. Load trained model ===
try:
    model = joblib.load("ufc_prediction_model.pkl")
    print("\n[OK] Loaded trained model: ufc_prediction_model.pkl")
except FileNotFoundError:
    print("\n[ERROR] Model file not found: ufc_prediction_model.pkl")
    exit(1)

# === 2. Load upcoming fights ===
try:
    upcoming = pd.read_csv("upcoming.csv")
    print(f"[OK] Loaded upcoming fights: {len(upcoming)} fights")
except FileNotFoundError:
    print("\n[ERROR] upcoming.csv not found")
    exit(1)

# === 3. Check which columns exist for feature calculation ===
print(f"\nAvailable columns: {upcoming.columns.tolist()[:15]}")

# === 4. Calculate derived features if they don't exist ===
features_needed = [
    "ReachDiff", "HeightDiff", "AgeDif",
    "WinStreakDif", "LoseStreakDif",
    "KODif", "SubDif", "WinDif", "LossDif"
]

# Check which features exist and which need to be calculated
existing_features = [f for f in features_needed if f in upcoming.columns]
missing_features = [f for f in features_needed if f not in upcoming.columns]

print(f"\nExisting features: {existing_features}")
print(f"Missing features: {missing_features}")

# Calculate missing features
if "ReachDiff" not in upcoming.columns and "ReachDif" not in upcoming.columns:
    if "BlueReachCms" in upcoming.columns and "RedReachCms" in upcoming.columns:
        upcoming["ReachDiff"] = upcoming["RedReachCms"] - upcoming["BlueReachCms"]
        print("✓ Calculated ReachDiff")

if "HeightDiff" not in upcoming.columns and "HeightDif" not in upcoming.columns:
    if "BlueHeightCms" in upcoming.columns and "RedHeightCms" in upcoming.columns:
        upcoming["HeightDiff"] = upcoming["RedHeightCms"] - upcoming["BlueHeightCms"]
        print("✓ Calculated HeightDiff")

# Re-check features after calculation
available_features = [f for f in features_needed if f in upcoming.columns]
print(f"\nTotal features available: {len(available_features)}/{len(features_needed)}")

if len(available_features) < 9:
    print(f"\n[WARNING] Not all features available. Only {len(available_features)}/9 features found")
    print(f"Available: {available_features}")
    print("\nUsing available features for prediction...")
    features_to_use = available_features
else:
    features_to_use = features_needed

# === 5. Make predictions ===
try:
    X_upcoming = upcoming[features_to_use]
    predictions = model.predict(X_upcoming)
    probs = model.predict_proba(X_upcoming)
    
    print(f"\n[OK] Made predictions for {len(predictions)} fights")
except Exception as e:
    print(f"\n[ERROR] Failed to make predictions: {str(e)}")
    exit(1)

# Get class labels
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
        results['RedFighter_Probability_%'] = probs[:, i] * 100
    else:
        results['BlueFighter_Probability_%'] = probs[:, i] * 100

# === 7. Display predictions ===
print("="*80)
print("UPCOMING FIGHT PREDICTIONS (Dec 14, 2024 Card)")
print("="*80 + "\n")

for idx, row in results.iterrows():
    red = row['RedFighter']
    blue = row['BlueFighter']
    predicted = row['Predicted_Winner']
    red_prob = row['RedFighter_Probability_%']
    blue_prob = row['BlueFighter_Probability_%']
    
    # Make it readable
    winner_mark = "✓" if predicted == "RedFighter" else " "
    print(f"{idx+1:2d}. {winner_mark} {red:25s} ({red_prob:5.1f}%) vs")
    print(f"    {blue:25s} ({blue_prob:5.1f}%)")
    print()

# === 8. Save predictions to CSV ===
output_file = "predictions.csv"
results.to_csv(output_file, index=False)

print("\n" + "="*80)
print(f"[SUCCESS] Predictions saved to: {output_file}")
print("="*80 + "\n")

# === 9. Summary statistics ===
red_wins = (results['Predicted_Winner'] == 'RedFighter').sum()
blue_wins = (results['Predicted_Winner'] == 'BlueFighter').sum()

print("PREDICTION SUMMARY:")
print(f"  Total fights analyzed: {len(results)}")
print(f"  Red corner predicted to win: {red_wins}")
print(f"  Blue corner predicted to win: {blue_wins}")

avg_confidence = results[['RedFighter_Probability_%', 'BlueFighter_Probability_%']].max(axis=1).mean()
print(f"  Average prediction confidence: {avg_confidence:.1f}%")

print(f"\n  Model accuracy on test set: 56.89%")
print(f"  (These predictions show probability estimates for each fighter)\n")
