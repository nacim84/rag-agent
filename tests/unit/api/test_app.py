from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    # Security check: env should NOT be exposed
    assert "env" not in data
