from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)
    is_premium = Column(Boolean, default=False)
    free_predictions_used = Column(Integer, default=0)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(String, index=True)
    red_fighter = Column(String, index=True)
    blue_fighter = Column(String, index=True)
    prob_RedFighter = Column(Float)
    prob_BlueFighter = Column(Float)
    ci_low_RedFighter = Column(Float, nullable=True)
    ci_high_RedFighter = Column(Float, nullable=True)
    ci_low_BlueFighter = Column(Float, nullable=True)
    ci_high_BlueFighter = Column(Float, nullable=True)
    predicted_winner = Column(String)
    actual_winner = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    event_name = Column(String)
    event_date = Column(DateTime, index=True)
    red_fighter = Column(String, index=True)
    blue_fighter = Column(String, index=True)
    weight_class = Column(String)
    red_stats = Column(String, nullable=True)  # JSON string
    blue_stats = Column(String, nullable=True)  # JSON string
    result_winner = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


