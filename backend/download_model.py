#!/usr/bin/env python3
"""
Heroku/Render startup script to download and place the trained model.
Add this path to Procfile if needed: release: python download_model.py
"""
import os
import requests

MODEL_URL = os.getenv("MODEL_URL", "")
MODEL_PATH = "./models/ufc_prediction_model.pkl"

if MODEL_URL:
    os.makedirs("./models", exist_ok=True)
    print(f"Downloading model from {MODEL_URL}...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)
    print(f"Model saved to {MODEL_PATH}")
else:
    print("MODEL_URL not set - using local model or container-packed model")
