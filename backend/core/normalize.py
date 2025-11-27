import pandas as pd
import re

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Map common variants to standard schema
    col_map = {
        'date': ['date', 'transaction date', 'posting date'],
        'time': ['time', 'transaction time'],
        'amount': ['amount', 'amt', 'transaction amount', 'value'],
        'merchant': ['merchant', 'description', 'payee', 'merchant name'],
        'city': ['city', 'location'],
        'country': ['country'],
        'merchant_category': ['category', 'merchant category', 'type'],
    }
    std_cols = {}
    for std, variants in col_map.items():
        for v in variants:
            for c in df.columns:
                if re.sub(r'[^a-z]', '', c.lower()) == re.sub(r'[^a-z]', '', v.lower()):
                    std_cols[std] = c
    for std, orig in std_cols.items():
        df[std] = df[orig]
    # Fill missing columns with empty/defaults
    for std in col_map:
        if std not in df.columns:
            df[std] = '' if std != 'amount' else 0.0
    # Ensure amount is float
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
    # Always create merchant_name from merchant if present
    if 'merchant' in df.columns:
        df['merchant_name'] = df['merchant']
    elif 'merchant_name' not in df.columns:
        df['merchant_name'] = ''
    # Always create merchant_category from category if present
    if 'category' in df.columns:
        df['merchant_category'] = df['category']
    elif 'merchant_category' not in df.columns:
        df['merchant_category'] = ''
    # Ensure 'time' column is string and fill missing/empty with '00:00'
    if 'time' in df.columns:
        df['time'] = df['time'].astype(str).replace(['', 'nan', 'NaT', 'None'], '00:00').fillna('00:00')
    else:
        df['time'] = '00:00'
    return df
