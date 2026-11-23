from fastapi.testclient import TestClient

from pg_app import app
from pg_database import get_db


def overrides_get_db():
    yield None


def test_create_product_invalid_price():
    app.dependency_overrides[get_db] = overrides_get_db

    try:
        with TestClient(app) as client:
            response = client.post(
                "/products",
                json={
                    "name": "Invalid Product",
                    "price": -100,
                    "stock": 5
                }
            )

        assert response.status_code == 422

        errors = response.json()["detail"]
        assert errors[0]["loc"] == ["body", "price"]
        assert errors[0]["type"] == "greater_than"

    finally:
        app.dependency_overrides.pop(get_db, None)