from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from datetime import datetime
from .model import load_model, predict_df
from .database import SessionLocal, engine
from .auth import create_access_token, verify_token
from .utils import calibrate_probabilities, compute_confidence_interval
from . import models, crud, payments, matches
import os

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UFC Predictions API", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "ufc_prediction_model.pkl")
try:
    model = load_model(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"Warning: Model not loaded - {e}")
    model = None


# Pydantic models
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class PredictRequest(BaseModel):
    match_id: int
    red_fighter: str
    blue_fighter: str
    red_stats: dict
    blue_stats: dict


class CheckoutRequest(BaseModel):
    success_url: str
    cancel_url: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============= AUTH ENDPOINTS =============

@app.post("/auth/register")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Register new user with email and password"""
    # Check if user exists
    if crud.get_user_by_username(db, req.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if crud.get_user_by_email(db, req.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user
    user = crud.create_user(db, req.username, req.email, req.password)
    
    # Create token
    token = create_access_token(user.id, user.username)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "is_premium": user.is_premium
    }


@app.post("/auth/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Login user with username and password"""
    user = crud.authenticate_user(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token(user.id, user.username)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "is_premium": user.is_premium,
        "free_predictions_left": crud.get_predictions_left(db, user.id)
    }


# ============= PREDICTION ENDPOINTS =============

@app.post("/predict")
async def predict(req: PredictRequest, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Make a UFC fight prediction (freemium: 3 free, then premium required)"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    user_id = token_data["user_id"]
    user = crud.get_user_by_id(db, user_id)
    
    # Check freemium limit
    predictions_left = crud.get_predictions_left(db, user_id)
    if predictions_left == 0 and not user.is_premium:
        raise HTTPException(status_code=403, detail="Free predictions exhausted. Upgrade to premium.")
    
    # Prepare fight data for model
    try:
        fight_data = {
            "RedFighter": req.red_fighter,
            "BlueFighter": req.blue_fighter,
            "reach_diff": req.red_stats.get("reach", 0) - req.blue_stats.get("reach", 0),
            "height_diff": req.red_stats.get("height", 0) - req.blue_stats.get("height", 0),
            "age_diff": req.red_stats.get("age", 30) - req.blue_stats.get("age", 30),
            "RedWinStreak": req.red_stats.get("wins", 0),
            "BlueWinStreak": req.blue_stats.get("wins", 0),
            "RedKODiff": (req.red_stats.get("KO_ratio", 0) - req.blue_stats.get("KO_ratio", 0)) * 100,
            "RedSubDiff": (req.red_stats.get("sub_ratio", 0) - req.blue_stats.get("sub_ratio", 0)) * 100,
            "RedTDDiff": (req.red_stats.get("td_defense", 0) - req.blue_stats.get("td_defense", 0)) * 100,
        }
        
        df = pd.DataFrame([fight_data])
        predictions = model.predict_proba(df)[0]
        
        # Apply calibration and confidence intervals
        red_prob = float(calibrate_probabilities(predictions[1]))
        blue_prob = float(calibrate_probabilities(predictions[0]))
        red_ci_low, red_ci_high = compute_confidence_interval(red_prob)
        blue_ci_low, blue_ci_high = compute_confidence_interval(blue_prob)
        
        predicted_winner = "Red Fighter" if red_prob > blue_prob else "Blue Fighter"
        
        # Store prediction
        pred = crud.create_prediction(
            db,
            user_id=user_id,
            red_fighter=req.red_fighter,
            blue_fighter=req.blue_fighter,
            red_prob=red_prob,
            blue_prob=blue_prob,
            red_lower_ci=float(red_ci_low),
            red_upper_ci=float(red_ci_high),
            blue_lower_ci=float(blue_ci_low),
            blue_upper_ci=float(blue_ci_high),
            predicted_winner=predicted_winner
        )
        
        # Increment prediction counter
        crud.increment_predictions_used(db, user_id)
        
        return {
            "id": pred.id,
            "red_fighter": pred.red_fighter,
            "blue_fighter": pred.blue_fighter,
            "red_probability": pred.red_probability,
            "blue_probability": pred.blue_probability,
            "red_confidence_interval": [pred.red_lower_ci, pred.red_upper_ci],
            "blue_confidence_interval": [pred.blue_lower_ci, pred.blue_upper_ci],
            "predicted_winner": pred.predicted_winner,
            "created_at": pred.created_at.isoformat(),
            "predictions_left": crud.get_predictions_left(db, user_id)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


# ============= USER ENDPOINTS =============

@app.get("/user/stats")
async def user_stats(token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Get user tier and prediction stats"""
    user_id = token_data["user_id"]
    user = crud.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "is_premium": user.is_premium,
        "free_predictions_used": user.free_predictions_used,
        "free_predictions_left": crud.get_predictions_left(db, user_id),
        "created_at": user.created_at.isoformat(),
        "stripe_customer_id": user.stripe_customer_id
    }


@app.get("/user/predictions")
async def user_predictions(limit: int = 10, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Get user's prediction history"""
    user_id = token_data["user_id"]
    predictions = crud.get_user_predictions(db, user_id, limit)
    
    return [
        {
            "id": p.id,
            "red_fighter": p.red_fighter,
            "blue_fighter": p.blue_fighter,
            "red_probability": p.red_probability,
            "blue_probability": p.blue_probability,
            "predicted_winner": p.predicted_winner,
            "actual_winner": p.actual_winner,
            "created_at": p.created_at.isoformat()
        }
        for p in predictions
    ]


# ============= MATCHES ENDPOINTS =============

@app.get("/matches/upcoming")
async def upcoming_matches(db: Session = Depends(get_db)):
    """Get 3 upcoming UFC fights"""
    await matches.populate_upcoming_matches(db)
    upcoming = crud.get_upcoming_matches(db, limit=3)
    
    return [
        {
            "id": m.id,
            "event_id": m.event_id,
            "event_name": m.event_name,
            "event_date": m.event_date.isoformat(),
            "red_fighter": m.red_fighter,
            "blue_fighter": m.blue_fighter,
            "weight_class": m.weight_class,
            "red_stats": m.red_stats,
            "blue_stats": m.blue_stats,
            "seconds_until_event": int((m.event_date - datetime.utcnow()).total_seconds())
        }
        for m in upcoming
    ]


@app.get("/matches/{match_id}")
async def match_details(match_id: int, db: Session = Depends(get_db)):
    """Get details for a specific match"""
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return {
        "id": match.id,
        "event_id": match.event_id,
        "event_name": match.event_name,
        "event_date": match.event_date.isoformat(),
        "red_fighter": match.red_fighter,
        "blue_fighter": match.blue_fighter,
        "weight_class": match.weight_class,
        "red_stats": match.red_stats,
        "blue_stats": match.blue_stats,
        "result_winner": match.result_winner,
        "seconds_until_event": int((match.event_date - datetime.utcnow()).total_seconds())
    }


# ============= PAYMENT ENDPOINTS =============

@app.post("/stripe/create-checkout")
async def create_stripe_checkout(req: CheckoutRequest, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Create Stripe checkout session for $25 premium upgrade"""
    user_id = token_data["user_id"]
    user = crud.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_premium:
        return {"message": "User is already premium"}
    
    result = await payments.create_checkout_session(db, user_id, req.success_url, req.cancel_url)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/stripe/verify-checkout")
async def verify_stripe_checkout(session_id: str = Body(...), token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Verify checkout was successful and upgrade user to premium"""
    user_id = token_data["user_id"]
    
    result = await payments.handle_checkout_success(db, session_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "status": "success",
        "is_premium": True,
        "free_predictions_left": -1  # Unlimited for premium
    }


@app.get("/stripe/status/{session_id}")
async def stripe_checkout_status(session_id: str):
    """Get status of a Stripe checkout session"""
    result = await payments.get_checkout_status(session_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


# ============= HEALTH CHECK =============

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "version": "2.0"
    }


