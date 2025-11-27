import io
import pandas as pd
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_upload_statement_csv():
    # Create a sample CSV in memory
    df = pd.DataFrame([
        {"date": "2025-11-01", "time": "10:00:00", "amount": 100, "merchant_name": "A", "merchant_category": "Food", "city": "X", "state": "S1", "country": "C1"},
        {"date": "2025-11-01", "time": "12:00:00", "amount": 200, "merchant_name": "B", "merchant_category": "Travel", "city": "Y", "state": "S2", "country": "C2"},
        {"date": "2025-11-01", "time": "13:00:00", "amount": 150, "merchant_name": "A", "merchant_category": "Food", "city": "X", "state": "S1", "country": "C1"}
    ])
    csv_bytes = io.BytesIO()
    df.to_csv(csv_bytes, index=False)
    csv_bytes.seek(0)
    files = {"file": ("test.csv", csv_bytes, "text/csv")}
    response = client.post("/upload-statement", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert "summary" in data
    assert "spending_analytics" in data
    for txn in data["transactions"]:
        assert "fraud_probability" in txn
        assert "anomaly_score" in txn
        assert "risk_level" in txn
        assert "reasons" in txn
    analytics = data["spending_analytics"]
    assert "total_per_category" in analytics
    assert "total_per_merchant" in analytics
    assert "monthly_spend" in analytics
