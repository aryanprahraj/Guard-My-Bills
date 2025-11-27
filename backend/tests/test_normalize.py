import pandas as pd
from backend.core.normalize import normalize_columns

def test_normalize_columns():
    df = pd.DataFrame({
        'Transaction Date': ['2025-01-01'],
        'Transaction Amount': [100],
        'Description': ['Test Merchant']
    })
    norm = normalize_columns(df)
    assert 'date' in norm.columns
    assert 'amount' in norm.columns
    assert 'merchant' in norm.columns
    assert norm['amount'].iloc[0] == 100
