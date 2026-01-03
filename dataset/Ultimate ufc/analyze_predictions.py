import pandas as pd

print("\n" + "="*80)
print("UFC FIGHT PREDICTION ANALYSIS")
print("="*80)

# Load predictions
predictions = pd.read_csv("predictions.csv")

print(f"\nEvent: December 14, 2024 UFC Card")
print(f"Total Fights Analyzed: {len(predictions)}")

red_wins = (predictions['Predicted_Winner'] == 'RedFighter').sum()
blue_wins = (predictions['Predicted_Winner'] == 'BlueFighter').sum()

print(f"Red Corner Predicted Wins: {red_wins} ({red_wins/len(predictions)*100:.1f}%)")
print(f"Blue Corner Predicted Wins: {blue_wins} ({blue_wins/len(predictions)*100:.1f}%)")

avg_conf = predictions[['RedFighter_Win_Probability', 'BlueFighter_Win_Probability']].max(axis=1).mean()
print(f"Average Confidence: {avg_conf:.1f}%")

print("\n" + "="*80)
print("DETAILED PREDICTIONS")
print("="*80 + "\n")

for idx, row in predictions.iterrows():
    red = row['RedFighter']
    blue = row['BlueFighter']
    pred = row['Predicted_Winner']
    red_prob = row['RedFighter_Win_Probability']
    blue_prob = row['BlueFighter_Win_Probability']
    
    marker = "[R]" if pred == "RedFighter" else "[B]"
    print(f"{idx+1:2d}. {marker} {red:30s} {red_prob:5.1f}%")
    print(f"        {blue:30s} {blue_prob:5.1f}%\n")

print("="*80)
print("HIGHEST CONFIDENCE PREDICTIONS")
print("="*80 + "\n")

# Find fights with highest confidence
max_probs = predictions[['RedFighter_Win_Probability', 'BlueFighter_Win_Probability']].max(axis=1)
top_confident = predictions.copy()
top_confident['max_prob'] = max_probs
top_confident = top_confident.nlargest(5, 'max_prob')

for idx, row in top_confident.iterrows():
    pred = row['Predicted_Winner']
    prob = row['max_prob']
    if pred == "RedFighter":
        print(f"  {row['RedFighter']:30s} vs {row['BlueFighter']:30s}")
        print(f"  Prediction: {row['RedFighter']:30s} ({prob:.1f}%)\n")
    else:
        print(f"  {row['RedFighter']:30s} vs {row['BlueFighter']:30s}")
        print(f"  Prediction: {row['BlueFighter']:30s} ({prob:.1f}%)\n")

print("="*80)
print("MOST UNCERTAIN PREDICTIONS (Closest Calls)")
print("="*80 + "\n")

# Find fights with lowest confidence (closest margins)
predictions['margin'] = abs(predictions['RedFighter_Win_Probability'] - predictions['BlueFighter_Win_Probability'])
closest = predictions.nsmallest(5, 'margin')

for idx, row in closest.iterrows():
    red = row['RedFighter']
    blue = row['BlueFighter']
    red_prob = row['RedFighter_Win_Probability']
    blue_prob = row['BlueFighter_Win_Probability']
    margin = row['margin']
    
    print(f"  {red:30s} {red_prob:5.1f}%")
    print(f"  {blue:30s} {blue_prob:5.1f}%")
    print(f"  Margin: {margin:.1f}%\n")

print("="*80)
print("MODEL INFORMATION")
print("="*80)
print("""
Training Data: 6,528 historical UFC fights (2010-2024)
Test Accuracy: 56.89%
Model: RandomForestClassifier (200 trees)

Class Performance:
  RedFighter:  Precision 61% | Recall 72% | F1 0.66
  BlueFighter: Precision 48% | Recall 36% | F1 0.41

Features Used (9 total):
  1. Reach Difference (cm)
  2. Height Difference (cm)
  3. Age Difference (years)
  4. Win Streak Difference
  5. Lose Streak Difference
  6. KO Wins Difference
  7. Submission Wins Difference
  8. Total Wins Difference
  9. Total Losses Difference
""")

print("="*80)
print("FILES GENERATED")
print("="*80)
print("\n  predictions.csv - All fight predictions with win probabilities")
print("\nNext: Monitor actual fight results to validate predictions!")
print("="*80 + "\n")
