from fastapi.testclient import TestClient
from backend.main import app

def test_metrics():
    client = TestClient(app)
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "guardmybills_requests_total" in resp.text

def test_logs():
    client = TestClient(app)
    resp = client.get("/logs")
    assert resp.status_code == 200
