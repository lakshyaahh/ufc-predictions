import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# === 1. Load cleaned dataset ===
df = pd.read_csv("master_dataset.csv")
print(f"Loaded dataset: {len(df)} total rows")

# === 2. Filter out rows with missing or unknown winners ===
df = df[df["Winner"].notna()]  # Remove NaN winners
df = df[df["Winner"].isin(["RedFighter", "BlueFighter"])]  # Keep only valid winners
print(f"After filtering: {len(df)} fights with valid winners")
print(f"Winner distribution:\n{df['Winner'].value_counts()}\n")

# === 3. Define features & target ===
# Note: The expanded dataset uses these column names
features = [
    "ReachDiff", "HeightDiff", "AgeDif",
    "WinStreakDif", "LoseStreakDif",
    "KODif", "SubDif", "WinDif", "LossDif"
]
X = df[features]
y = df["Winner"]

print(f"Training with {len(features)} features:")
print(f"  {features}\n")

# === 4. Split into train/test ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Training set: {len(X_train)} fights")
print(f"Test set: {len(X_test)} fights\n")

# === 5. Train Random Forest ===
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
print("Model trained successfully!")

# === 6. Evaluate ===
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n{'=' * 60}")
print(f"ACCURACY: {accuracy:.4f}")
print(f"{'=' * 60}\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# === 7. Save model ===
joblib.dump(model, "ufc_prediction_model.pkl")
print("\n✅ Model saved as ufc_prediction_model.pkl")