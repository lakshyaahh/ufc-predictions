import joblib
import pandas as pd
import os


def load_model(path: str):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}. Place your ufc_prediction_model.pkl there.")
    return joblib.load(path)


def _ensure_features(df: pd.DataFrame):
    # Minimal renames/normalization used in training
    rename_map = {
        "ReachDif": "ReachDiff",
        "HeightDif": "HeightDiff",
        "ReachDiff": "ReachDiff",
        "HeightDiff": "HeightDiff",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    return df


def predict_df(model, df: pd.DataFrame):
    df = _ensure_features(df.copy())
    # Expected features used during training
    features = [
        "ReachDiff",
        "HeightDiff",
        "AgeDif",
        "WinStreakDif",
        "LoseStreakDif",
        "KODif",
        "SubDif",
        "WinDif",
        "LossDif",
    ]
    missing = [f for f in features if f not in df.columns]
    if missing:
        raise ValueError(f"Missing features for prediction: {missing}")
    X = df[features].fillna(0)
    probs = model.predict_proba(X)
    classes = list(model.classes_)
    # assume classes ["BlueFighter","RedFighter"] or similar
    results = df.copy().reset_index(drop=True)
    for i, cls in enumerate(classes):
        results[f"prob_{cls}"] = probs[:, i]
    # predicted winner label
    results["predicted_winner"] = [classes[i] for i in model.predict(X)]
    return results
