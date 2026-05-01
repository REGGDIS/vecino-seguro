"""Prueba básica del endpoint de salud del backend."""

from fastapi.testclient import TestClient

from app.main.main import app


def test_health_check_returns_ok() -> None:
    """Comprueba que `/health` responda correctamente."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

