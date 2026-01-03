import pandas as pd
import numpy as np
from scipy import stats
import requests
from datetime import datetime, timedelta


def calibrate_probabilities(probs):
    """
    Apply Platt scaling calibration to predicted probabilities.
    For production, train calibrator on validation set first.
    For demo, use simple smoothing.
    """
    # Simple smoothing towards 0.5 for uncalibrated models
    return 0.7 * probs + 0.3 * 0.5


def compute_confidence_interval(prob, n_samples=1000):
    """
    Compute 95% confidence interval for a binomial proportion.
    Uses Wilson score interval (more stable than normal approximation).
    """
    if n_samples < 30:
        return (prob - 0.1, prob + 0.1)  # fallback
    
    from scipy.stats import binom
    # Wilson score interval
    z = 1.96  # 95% CI
    denominator = 1 + z**2 / n_samples
    p_hat = prob
    center = (p_hat + z**2 / (2 * n_samples)) / denominator
    margin = z * np.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n_samples)) / n_samples) / denominator
    return (max(0, center - margin), min(1, center + margin))


def fetch_upcoming_fights_espn():
    """
    Fetch upcoming UFC fights from ESPN API.
    Returns list of fight dictionaries with fighter names.
    """
    try:
        # UFC is typically event ID 401271938 or similar for upcoming events
        # This is a mock example; real implementation would parse ESPN XML/JSON
        url = "https://site.api.espn.com/apis/site/v2/sports/mma/ufc/events"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            fights = []
            # Parse ESPN response (structure varies)
            return fights
        return []
    except Exception as e:
        print(f"Error fetching UFC fights: {e}")
        return []


def fetch_upcoming_fights_ufcstats():
    """
    Alternative: fetch from UFC Stats or other MMA source.
    """
    try:
        # Mock example - would need actual API key/scraping
        return []
    except Exception as e:
        print(f"Error fetching UFC fights: {e}")
        return []
