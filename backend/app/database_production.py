"""
Production Database Configuration
Supports both SQLite (dev) and PostgreSQL (production)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment
# In production: postgresql://user:pass@host:5432/db
# In development: sqlite:///predictions.db
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to SQLite for local development
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "predictions.db")
    DATABASE_URL = f"sqlite:///{os.path.abspath(DB_PATH)}"

# SQLAlchemy engine
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL production
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
else:
    # SQLite development
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
