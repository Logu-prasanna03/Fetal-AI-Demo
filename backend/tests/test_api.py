from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app

client = TestClient(app)


def test_health_reports_model_status():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_prediction_returns_safe_response():
    email = f"demo.patient.{uuid4()}@example.com"
    register = client.post("/api/v1/auth/register", json={"full_name": "Demo Patient", "email": email, "password": "test-password-123", "role": "patient"})
    token = register.json()["access_token"]
    response = client.post("/api/v1/analyses", headers={"Authorization": f"Bearer {token}"}, json={"patient_reference": "Demo-001", "measurements": {}})
    body = response.json()
    assert response.status_code == 200
    assert body["category"] in {"Normal", "Suspect", "Pathological"}
    assert body["is_demo_model"] is True
    assert "Not for diagnosis" in body["safety_notice"]
