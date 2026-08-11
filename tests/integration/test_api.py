from fastapi.testclient import TestClient

from api.app import app


def test_health():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "healthy"}


def test_customer_routes():
    with TestClient(app) as client:
        response = client.get("/api/v1/customers/demo-customer")
        assert response.status_code == 200
        assert response.json()["email"] == "demo@example.com"
        assert client.get("/api/v1/customers/missing").status_code == 404
