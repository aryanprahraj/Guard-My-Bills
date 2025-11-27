import pandas as pd
from typing import Dict, Any
from core.feature_engineering import prepare_features
from core.ml_model import get_fraud_scores
from core.rules_engine import explain_fraud

def compare_transaction(suspect: dict, references: list) -> Dict[str, Any]:

    from haversine import haversine
    from datetime import datetime
    def parse_datetime(date_str, time_str):
        from dateutil import parser
        try:
            # Try ISO format first
            return datetime.fromisoformat(date_str + 'T' + time_str)
        except Exception:
            pass
        try:
            # Try parsing with dateutil (handles 12-hour and 24-hour)
            return parser.parse(f"{date_str} {time_str}")
        except Exception:
            return None


    # 1. If timestamp matches any reference, return fraud
    suspect_date = str(suspect.get('date', ''))
    suspect_time = str(suspect.get('time', ''))
    suspect_dt = parse_datetime(suspect_date, suspect_time)
    suspect_city = str(suspect.get('city', '')).strip().lower()
    suspect_country = str(suspect.get('country', '')).strip()
    for ref in references:
        ref_date = str(ref.get('date', ''))
        ref_time = str(ref.get('time', ''))
        ref_dt = parse_datetime(ref_date, ref_time)
        if suspect_dt and ref_dt and suspect_dt == ref_dt:
            return {'verdict': 'Fraud'}

    # 2. Distance threshold: 100 km/h
    from haversine import haversine
    US_CITY_COORDS = {
        ("New York", "United States of America"): (40.7128, -74.0060),
        ("Jersey City", "United States of America"): (40.7282, -74.0776),
        ("Los Angeles", "United States of America"): (34.0522, -118.2437),
        ("San Francisco", "United States of America"): (37.7749, -122.4194),
        ("Chicago", "United States of America"): (41.8781, -87.6298),
        ("Boston", "United States of America"): (42.3601, -71.0589),
        ("Houston", "United States of America"): (29.7604, -95.3698),
        ("Dallas", "United States of America"): (32.7767, -96.7970),
        ("Miami", "United States of America"): (25.7617, -80.1918),
        ("Seattle", "United States of America"): (47.6062, -122.3321),
        ("Philadelphia", "United States of America"): (39.9526, -75.1652),
        ("Washington", "United States of America"): (38.9072, -77.0369),
        ("Atlanta", "United States of America"): (33.7490, -84.3880),
        ("Austin", "United States of America"): (30.2672, -97.7431),
        ("Denver", "United States of America"): (39.7392, -104.9903),
        ("San Diego", "United States of America"): (32.7157, -117.1611),
        ("Phoenix", "United States of America"): (33.4484, -112.0740),
        ("Orlando", "United States of America"): (28.5383, -81.3792),
        ("Las Vegas", "United States of America"): (36.1699, -115.1398),
    }
    key1 = (str(suspect.get('city', '')).strip(), str(suspect.get('country', '')).strip())
    for ref in references:
        key2 = (str(ref.get('city', '')).strip(), str(ref.get('country', '')).strip())
        ref_date = str(ref.get('date', ''))
        ref_time = str(ref.get('time', ''))
        ref_dt = parse_datetime(ref_date, ref_time)
        if key1 in US_CITY_COORDS and key2 in US_CITY_COORDS and suspect_dt and ref_dt:
            dist_km = haversine(US_CITY_COORDS[key1], US_CITY_COORDS[key2])
            time_min = abs((suspect_dt - ref_dt).total_seconds()) / 60.0
            if time_min > 0:
                speed = dist_km / (time_min / 60.0)
                if speed > 100:
                    return {'verdict': 'Fraud'}

    # 3. If city is different from both references and time diff > 20 min, fraud
    cities_ref = [str(ref.get('city', '')).strip().lower() for ref in references]
    if suspect_city not in cities_ref:
        for ref in references:
            ref_date = str(ref.get('date', ''))
            ref_time = str(ref.get('time', ''))
            ref_dt = parse_datetime(ref_date, ref_time)
            if suspect_dt and ref_dt:
                time_diff = abs((suspect_dt - ref_dt).total_seconds()) / 60.0
                if time_diff > 20:
                    return {'verdict': 'Fraud'}

    # Default: Not Fraud
    return {'verdict': 'Not Fraud'}
