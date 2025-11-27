from pydantic import BaseModel
from typing import Optional

class TransactionFeatures(BaseModel):
    timestamp: str
    hour_of_day: int
    day_of_week: int
    is_weekend: bool
    time_since_last_txn_minutes: Optional[float]
    distance_from_last_txn_km: Optional[float]
    velocity_kmh: Optional[float]
    amount_zscore: Optional[float]
    amount_to_user_avg_ratio: Optional[float]
    is_new_merchant: bool
    is_new_city: bool
    transactions_last_10min: int
    transactions_last_60min: int
    sum_amount_last_60min: float
    merchant_category_encoded: Optional[float]
    is_night_time: bool
