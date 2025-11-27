import io
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_generate_report_pdf():
    payload = {
        "summary": {"total_transactions": 3, "high_risk": 1, "medium_risk": 1, "low_risk": 1},
        "transactions": [
            {"date": "2025-11-01", "time": "10:00:00", "amount": 100, "merchant_name": "A", "merchant_category": "Food", "city": "X", "state": "S1", "country": "C1", "fraud_probability": 0.9, "anomaly_score": 2.1, "risk_level": "HIGH", "reasons": ["Impossible travel"]},
            {"date": "2025-11-01", "time": "12:00:00", "amount": 200, "merchant_name": "B", "merchant_category": "Travel", "city": "Y", "state": "S2", "country": "C2", "fraud_probability": 0.5, "anomaly_score": 1.1, "risk_level": "MEDIUM", "reasons": ["Nighttime transaction"]},
            {"date": "2025-11-01", "time": "13:00:00", "amount": 150, "merchant_name": "A", "merchant_category": "Food", "city": "X", "state": "S1", "country": "C1", "fraud_probability": 0.1, "anomaly_score": 0.2, "risk_level": "LOW", "reasons": []}
        ],
        "spending_analytics": {"total_per_category": {"Food": 250, "Travel": 200}, "total_per_merchant": {"A": 250, "B": 200}, "monthly_spend": {"2025-11": 450}}
    }
    response = client.post("/generate-report", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert int(response.headers.get("content-length", 0)) > 0
    assert response.content[:4] == b"%PDF"
