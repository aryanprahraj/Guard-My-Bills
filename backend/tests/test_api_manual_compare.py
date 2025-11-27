from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_manual_compare_impossible_travel():
    txn1 = {"date": "2025-11-01", "time": "10:00:00", "amount": 100, "merchant_name": "A", "merchant_category": "Food", "city": "X", "state": "S1", "country": "C1"}
    txn2 = {"date": "2025-11-01", "time": "10:30:00", "amount": 200, "merchant_name": "B", "merchant_category": "Travel", "city": "Y", "state": "S2", "country": "C2"}
    payload = {"txn1": txn1, "txn2": txn2}
    response = client.post("/manual-compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "comparison" in data
    assert "fraud_verdict" in data
    for comp in data["comparison"]:
        assert "distance_km" in comp
        assert "time_delta_minutes" in comp
        assert "velocity_kmh" in comp
        assert "fraud_probability" in comp
        assert "risk_level" in comp
        assert "explanation_labels" in comp
    assert data["fraud_verdict"] in ("likely fraud", "possible", "unlikely")
