import pandas as pd
import numpy as np
from typing import Dict, Any

def analyze_spending(df: pd.DataFrame) -> Dict[str, Any]:
    # High-Level Overview
    total_inflow = df[df['amount'] > 0]['amount'].sum()
    total_outflow = df[df['amount'] < 0]['amount'].sum()
    net_cashflow = total_inflow + total_outflow
    
    # Month-over-month changes
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    monthly_spend = df.groupby('month')['amount'].sum().to_dict()
    # Convert Period keys to strings for JSON serialization
    monthly_spend = {str(k): float(v) for k, v in monthly_spend.items()}
    
    # Category-wise breakdown
    if 'category' not in df.columns:
        if 'merchant_category' in df.columns:
            df['category'] = df['merchant_category']
        else:
            df['category'] = 'Miscellaneous'
    df['category'] = df['category'].astype(str)
    if 'merchant_name' not in df.columns and 'merchant' in df.columns:
        df['merchant_name'] = df['merchant']
    if 'merchant_name' not in df.columns:
        df['merchant_name'] = ''
    df['merchant_name'] = df['merchant_name'].astype(str)
    cat_totals = {str(k): float(v) for k, v in df.groupby('category')['amount'].sum().to_dict().items()}
    cat_percent = {str(k): float(v) / abs(total_outflow) * 100 if total_outflow else 0 for k, v in cat_totals.items()}

    # Merchant-level insights
    merchant_totals = {str(k): float(v) for k, v in df.groupby('merchant_name')['amount'].sum().to_dict().items()}
    top_merchants = sorted(merchant_totals.items(), key=lambda x: abs(x[1]), reverse=True)[:5]

    # Recurring payments (simple: same merchant, same amount, >2 times)
    recurring = df.groupby(['merchant_name', 'amount']).size().reset_index(name='count')
    recurring = recurring[recurring['count'] >= 3][['merchant_name', 'amount', 'count']].to_dict('records')
    
    # Anomaly detection (z-score on amount)
    df['zscore'] = (df['amount'] - df['amount'].mean()) / (df['amount'].std() if df['amount'].std() else 1)
    anomalies = df[np.abs(df['zscore']) > 2].to_dict('records')
    
    # Day of week/time of day
    df['weekday'] = pd.to_datetime(df['date']).dt.day_name()
    df['hour'] = pd.to_datetime(df['time'], errors='coerce').dt.hour if 'time' in df.columns else 0
    weekday_spend = {str(k): float(v) for k, v in df.groupby('weekday')['amount'].sum().to_dict().items()}
    hour_spend = {str(k): float(v) for k, v in df.groupby('hour')['amount'].sum().to_dict().items()} if 'hour' in df.columns else {}
    
    # Budgeting (simple average)
    avg_monthly_spend = np.mean(list(monthly_spend.values())) if monthly_spend else 0
    
    # Recommendations (simple)
    recs = []
    if cat_percent:
        top_cat = max(cat_percent, key=cat_percent.get)
        recs.append(f"Consider reducing spend in {top_cat}.")
    if recurring:
        recs.append("Review recurring payments for possible savings.")
    if anomalies:
        recs.append("Some transactions are unusually large or small.")
    
    return {
        "overview": {
            "total_inflow": float(total_inflow),
            "total_outflow": float(total_outflow),
            "net_cashflow": float(net_cashflow),
            "avg_monthly_spend": float(avg_monthly_spend),
        },
        "monthly_spend": monthly_spend,
        "category_breakdown": cat_totals,
        "category_percent": cat_percent,
        "top_merchants": top_merchants,
        "recurring_payments": recurring,
        "anomalies": anomalies,
        "weekday_spend": weekday_spend,
        "hour_spend": hour_spend,
        "recommendations": recs
    }
