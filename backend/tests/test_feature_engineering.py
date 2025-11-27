import pandas as pd
from backend.core.feature_engineering import prepare_features

def test_prepare_features_basic():
    data = [
        {"date": "2025-11-01", "time": "10:00:00", "amount": 100, "merchant_name": "A", "merchant_category": "Food", "city": "X", "state": "S1", "country": "C1"},
        {"date": "2025-11-01", "time": "12:00:00", "amount": 200, "merchant_name": "B", "merchant_category": "Travel", "city": "Y", "state": "S2", "country": "C2"},
        {"date": "2025-11-01", "time": "13:00:00", "amount": 150, "merchant_name": "A", "merchant_category": "Food", "city": "X", "state": "S1", "country": "C1"}
    ]
    df = pd.DataFrame(data)
    features = prepare_features(df)
    # Check columns
    required = [
        'timestamp', 'hour_of_day', 'day_of_week', 'is_weekend',
        'time_since_last_txn_minutes', 'distance_from_last_txn_km', 'velocity_kmh',
        'amount_zscore', 'amount_to_user_avg_ratio', 'is_new_merchant', 'is_new_city',
        'transactions_last_10min', 'transactions_last_60min', 'sum_amount_last_60min',
        'merchant_category_encoded', 'is_night_time'
    ]
    for col in required:
        assert col in features.columns
    # Check timestamp parsing
    assert pd.api.types.is_datetime64_any_dtype(features['timestamp'])
    # Check distance and velocity
    assert features['distance_from_last_txn_km'].iloc[0] == 0
    assert features['velocity_kmh'].iloc[0] == 0 or pd.isna(features['velocity_kmh'].iloc[0])
    # Check z-score
    assert abs(features['amount_zscore'].mean()) < 1e-6
    # Check new city/merchant
    assert features['is_new_city'].iloc[0] == True
    assert features['is_new_merchant'].iloc[0] == True
    # Check rolling window
    assert features['transactions_last_10min'].iloc[1] >= 0
