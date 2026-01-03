import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./predictions.db")

# JWT/Auth
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = int(os.getenv("TOKEN_EXPIRE_DAYS", 30))

# Model
MODEL_PATH = os.getenv("MODEL_PATH", "./models/ufc_prediction_model.pkl")

# Feature names
REQUIRED_FEATURES = [
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
