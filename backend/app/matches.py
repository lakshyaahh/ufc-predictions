import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import crud
import json


async def fetch_upcoming_fights_from_espn() -> list:
    """
    Fetch upcoming UFC fights from ESPN API
    Returns list of fight dicts with: event_id, event_name, event_date, red_fighter, blue_fighter, weight_class
    """
    try:
        # This is a placeholder - ESPN doesn't have a public UFC API
        # In production, you'd use:
        # 1. UFC Stats official API (ufcstats.com)
        # 2. Web scraping from ESPN/UFC.com
        # 3. Third-party UFC API service
        
        # For now, return sample data
        sample_fights = [
            {
                "event_id": "ufc_302",
                "event_name": "UFC 302: Marquardt vs. Aspinall",
                "event_date": datetime.utcnow() + timedelta(days=7),
                "red_fighter": "Sean Strickland",
                "blue_fighter": "Dricus du Plessis",
                "weight_class": "Middleweight",
                "red_stats": {
                    "record": "31-5-0",
                    "reach": 74.0,
                    "height": 6.0,
                    "age": 32,
                    "KO_ratio": 0.32,
                    "wins": 31,
                    "losses": 5
                },
                "blue_stats": {
                    "record": "21-2-0",
                    "reach": 72.0,
                    "height": 6.1,
                    "age": 30,
                    "KO_ratio": 0.48,
                    "wins": 21,
                    "losses": 2
                }
            },
            {
                "event_id": "ufc_303",
                "event_name": "UFC 303: Pereira vs. Prochazka",
                "event_date": datetime.utcnow() + timedelta(days=14),
                "red_fighter": "Alex Pereira",
                "blue_fighter": "Jiri Prochazka",
                "weight_class": "Light Heavyweight",
                "red_stats": {
                    "record": "11-2-0",
                    "reach": 75.5,
                    "height": 6.3,
                    "age": 36,
                    "KO_ratio": 0.73,
                    "wins": 11,
                    "losses": 2
                },
                "blue_stats": {
                    "record": "29-3-1",
                    "reach": 74.0,
                    "height": 6.3,
                    "age": 31,
                    "KO_ratio": 0.28,
                    "wins": 29,
                    "losses": 3
                }
            },
            {
                "event_id": "ufc_304",
                "event_name": "UFC 304: Belal vs. Edwards 2",
                "event_date": datetime.utcnow() + timedelta(days=21),
                "red_fighter": "Muhammad Belal",
                "blue_fighter": "Leon Edwards",
                "weight_class": "Welterweight",
                "red_stats": {
                    "record": "20-5-0",
                    "reach": 72.5,
                    "height": 5.10,
                    "age": 35,
                    "KO_ratio": 0.25,
                    "wins": 20,
                    "losses": 5
                },
                "blue_stats": {
                    "record": "21-3-0",
                    "reach": 74.0,
                    "height": 6.0,
                    "age": 32,
                    "KO_ratio": 0.29,
                    "wins": 21,
                    "losses": 3
                }
            }
        ]
        return sample_fights
    except Exception as e:
        print(f"Error fetching fights from ESPN: {e}")
        return []


async def populate_upcoming_matches(db: Session) -> int:
    """
    Fetch upcoming fights and populate Match table
    Returns count of matches created
    """
    # Delete expired matches first
    crud.delete_expired_matches(db)
    
    # Fetch new upcoming fights
    fights = await fetch_upcoming_fights_from_espn()
    
    created_count = 0
    for fight in fights:
        # Check if match already exists
        existing = db.query(crud.Match).filter(
            crud.Match.event_id == fight["event_id"]
        ).first()
        
        if not existing:
            crud.create_match(
                db,
                event_id=fight["event_id"],
                event_name=fight["event_name"],
                event_date=fight["event_date"],
                red_fighter=fight["red_fighter"],
                blue_fighter=fight["blue_fighter"],
                weight_class=fight["weight_class"],
                red_stats=fight.get("red_stats", {}),
                blue_stats=fight.get("blue_stats", {})
            )
            created_count += 1
    
    return created_count


async def get_match_details(db: Session, match_id: int) -> dict:
    """Get detailed information about a match"""
    match = db.query(crud.Match).filter(crud.Match.id == match_id).first()
    if not match:
        return None
    
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
        "time_until_event": (match.event_date - datetime.utcnow()).total_seconds()
    }
