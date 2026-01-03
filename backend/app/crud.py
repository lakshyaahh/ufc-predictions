from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import User, Prediction, Match
from .security import hash_password, verify_password
from datetime import datetime


def create_user(db: Session, username: str, email: str, password: str) -> User:
    """Create a new user with hashed password"""
    hashed_password = hash_password(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_premium=False,
        free_predictions_used=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str) -> User:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, username: str, password: str) -> User:
    """Authenticate user by username and password"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def increment_predictions_used(db: Session, user_id: int) -> User:
    """Increment free predictions used counter"""
    user = get_user_by_id(db, user_id)
    if user and not user.is_premium:
        user.free_predictions_used += 1
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user


def set_premium(db: Session, user_id: int, stripe_customer_id: str = None, stripe_subscription_id: str = None) -> User:
    """Set user to premium"""
    user = get_user_by_id(db, user_id)
    if user:
        user.is_premium = True
        if stripe_customer_id:
            user.stripe_customer_id = stripe_customer_id
        if stripe_subscription_id:
            user.stripe_subscription_id = stripe_subscription_id
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user


def get_predictions_left(db: Session, user_id: int) -> int:
    """Get remaining free predictions for user"""
    user = get_user_by_id(db, user_id)
    if not user:
        return 0
    if user.is_premium:
        return -1  # Unlimited
    return max(0, 3 - user.free_predictions_used)


def create_prediction(db: Session, user_id: int, red_fighter: str, blue_fighter: str,
                     red_prob: float, blue_prob: float, red_lower_ci: float, red_upper_ci: float,
                     blue_lower_ci: float, blue_upper_ci: float, predicted_winner: str) -> Prediction:
    """Create a prediction record"""
    prediction = Prediction(
        user_id=user_id,
        red_fighter=red_fighter,
        blue_fighter=blue_fighter,
        red_probability=red_prob,
        blue_probability=blue_prob,
        red_lower_ci=red_lower_ci,
        red_upper_ci=red_upper_ci,
        blue_lower_ci=blue_lower_ci,
        blue_upper_ci=blue_upper_ci,
        predicted_winner=predicted_winner,
        actual_winner=None,
        created_at=datetime.utcnow()
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def get_user_predictions(db: Session, user_id: int, limit: int = 10) -> list:
    """Get predictions for a user"""
    return db.query(Prediction).filter(Prediction.user_id == user_id).order_by(Prediction.created_at.desc()).limit(limit).all()


def create_match(db: Session, event_id: str, event_name: str, event_date: datetime,
                red_fighter: str, blue_fighter: str, weight_class: str,
                red_stats: dict = None, blue_stats: dict = None) -> Match:
    """Create an upcoming match record"""
    match = Match(
        event_id=event_id,
        event_name=event_name,
        event_date=event_date,
        red_fighter=red_fighter,
        blue_fighter=blue_fighter,
        weight_class=weight_class,
        red_stats=red_stats or {},
        blue_stats=blue_stats or {},
        result_winner=None
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_upcoming_matches(db: Session, limit: int = 3) -> list:
    """Get upcoming matches"""
    return db.query(Match).filter(Match.event_date > datetime.utcnow()).order_by(Match.event_date).limit(limit).all()


def delete_expired_matches(db: Session) -> int:
    """Delete matches that have already occurred"""
    expired_count = db.query(Match).filter(Match.event_date <= datetime.utcnow()).delete()
    db.commit()
    return expired_count


