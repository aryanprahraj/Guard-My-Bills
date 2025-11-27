import numpy as np

RISK_THRESHOLDS = {
    'HIGH': 0.8,
    'MEDIUM': 0.5,
    'LOW': 0.0
}

RULES = [
    ('impossible_travel', lambda row: row.get('velocity_kmh', 0) > 800, 'Impossible travel: velocity > 800 km/h'),
    ('suspicious_travel', lambda row: row.get('velocity_kmh', 0) > 300, 'Suspicious velocity > 300 km/h'),
    ('nighttime_anomaly', lambda row: row.get('is_night_time', False), 'Nighttime transaction (12AM-5AM)'),
    ('high_amount', lambda row: row.get('amount_zscore', 0) > 2.5, 'Unusually high amount (z-score > 2.5)'),
    ('first_time_city_high', lambda row: row.get('is_new_city', False) and row.get('amount_zscore', 0) > 1.5, 'First-time city with high spend'),
    ('first_time_merchant_high', lambda row: row.get('is_new_merchant', False) and row.get('amount_zscore', 0) > 1.5, 'First-time merchant with high spend'),
    ('burst_spending', lambda row: row.get('transactions_last_10min', 0) > 3, 'Rapid burst: >3 txns in 10min')
]

def explain_fraud(row, ml_score):
    reasons = []
    for rule_name, rule_fn, reason_str in RULES:
        try:
            if rule_fn(row):
                reasons.append(reason_str)
        except Exception:
            continue
    # Risk level
    if ml_score >= RISK_THRESHOLDS['HIGH'] or 'Impossible travel' in reasons:
        risk = 'HIGH'
    elif ml_score >= RISK_THRESHOLDS['MEDIUM'] or reasons:
        risk = 'MEDIUM'
    else:
        risk = 'LOW'
    return risk, reasons
