import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from haversine import haversine
from collections import defaultdict
from typing import List, Dict

def prepare_features(transactions: pd.DataFrame) -> pd.DataFrame:
        # Check for required columns
    df = transactions.copy()
    # Map possible frontend field names to expected backend names (case-insensitive)
    if 'merchant' in df.columns and 'merchant_name' not in df.columns:
        df['merchant_name'] = df['merchant']
    if 'Merchant' in df.columns and 'merchant_name' not in df.columns:
        df['merchant_name'] = df['Merchant']
    if 'category' in df.columns and 'merchant_category' not in df.columns:
        df['merchant_category'] = df['category']
    if 'Category' in df.columns and 'merchant_category' not in df.columns:
        df['merchant_category'] = df['Category']
    # Check for required columns after mapping
    required_cols = ['merchant_name', 'merchant_category', 'city', 'country', 'amount', 'date', 'time']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Columns present: {list(df.columns)}")
    required_cols = ['merchant_name', 'merchant_category', 'city', 'country', 'amount', 'date', 'time']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Columns present: {list(df.columns)}")
    # Parse timestamp robustly
    # If 'date' already contains time (ISO format), parse directly
    sample_date = str(df['date'].iloc[0])
    # Defensive: fill missing/invalid time with 00:00
    if 'time' in df.columns:
        df['time'] = df['time'].astype(str).replace(['', 'nan', 'NaT', 'None'], '00:00').fillna('00:00')
    else:
        df['time'] = '00:00'
    if 'T' in sample_date:
        df['timestamp'] = pd.to_datetime(df['date'], errors='coerce')
    else:
        # Try parsing with date and time, fallback to just date if needed
        try:
            df['timestamp'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str), errors='coerce')
            # If all NaT, fallback to just date
            if df['timestamp'].isna().all():
                df['timestamp'] = pd.to_datetime(df['date'], errors='coerce')
        except Exception:
            df['timestamp'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values('timestamp').reset_index(drop=True)
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.weekday
    df['is_weekend'] = df['day_of_week'] >= 5
    # Time since last txn
    df['time_since_last_txn_minutes'] = df['timestamp'].diff().dt.total_seconds().div(60).fillna(0)
    # Distance and velocity
    # Basic lookup for common US cities (city, country) -> (lat, lon)
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
    city_coords = {}
    def get_city_coords(city, country):
        key = (str(city).strip(), str(country).strip())
        if key in US_CITY_COORDS:
            return US_CITY_COORDS[key]
        # fallback to dummy if not found
        if key not in city_coords:
            city_coords[key] = (hash(city)%90, hash(country)%180)
        return city_coords[key]
    df['latlon'] = df.apply(lambda row: get_city_coords(row['city'], row['country']), axis=1)
    # Compute pairwise distances and time differences for all transactions
    n = len(df)
    distance_matrix = np.zeros((n, n))
    time_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i, j] = haversine(df.at[i, 'latlon'], df.at[j, 'latlon'])
                time_matrix[i, j] = abs((df.at[i, 'timestamp'] - df.at[j, 'timestamp']).total_seconds()) / 60.0
    # For each transaction, store max and min distance/time to any other transaction
    df['max_distance_km'] = [distance_matrix[i].max() for i in range(n)]
    df['min_distance_km'] = [distance_matrix[i][distance_matrix[i]>0].min() if np.any(distance_matrix[i]>0) else 0 for i in range(n)]
    df['max_time_delta_minutes'] = [time_matrix[i].max() for i in range(n)]
    df['min_time_delta_minutes'] = [time_matrix[i][time_matrix[i]>0].min() if np.any(time_matrix[i]>0) else 0 for i in range(n)]
    # Keep original sequential features for compatibility
    df['distance_from_last_txn_km'] = np.nan
    df.loc[0, 'distance_from_last_txn_km'] = 0
    for i in range(1, len(df)):
        df.loc[i, 'distance_from_last_txn_km'] = haversine(df.at[i-1, 'latlon'], df.at[i, 'latlon'])
    df['velocity_kmh'] = df['distance_from_last_txn_km'] / (df['time_since_last_txn_minutes'] / 60).replace(0, np.nan)
    # Amount features: ensure numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['amount_zscore'] = (df['amount'] - df['amount'].mean()) / (df['amount'].std() + 1e-6)
    df['amount_to_user_avg_ratio'] = df['amount'] / (df['amount'].mean() + 1e-6)
    # Rolling window features
    df['transactions_last_10min'] = [df.iloc[max(0,i-10):i]['timestamp'].apply(lambda t: (df.at[i,'timestamp']-t).total_seconds()/60 < 10).count() for i in range(len(df))]
    df['transactions_last_60min'] = [df.iloc[max(0,i-60):i]['timestamp'].apply(lambda t: (df.at[i,'timestamp']-t).total_seconds()/60 < 60).count() for i in range(len(df))]
    df['sum_amount_last_60min'] = [df.iloc[max(0,i-60):i][df['timestamp'] >= df.at[i,'timestamp']-timedelta(minutes=60)]['amount'].sum() for i in range(len(df))]
    # New merchant/city flags
    seen_merchants = set()
    seen_cities = set()
    is_new_merchant = []
    is_new_city = []
    for idx, row in df.iterrows():
        merchant = row['merchant_name']
        city = row['city']
        is_new_merchant.append(merchant not in seen_merchants)
        is_new_city.append(city not in seen_cities)
        seen_merchants.add(merchant)
        seen_cities.add(city)
    df['is_new_merchant'] = is_new_merchant
    df['is_new_city'] = is_new_city
    # Merchant category encoding (simple target encoding)
    cat_map = {cat: i for i, cat in enumerate(df['merchant_category'].unique())}
    df['merchant_category_encoded'] = df['merchant_category'].map(cat_map)
    # Night time flag
    df['is_night_time'] = df['hour_of_day'].apply(lambda h: 0 <= h < 5)
    # Drop helper columns
    df = df.drop(columns=['latlon'])
    return df
