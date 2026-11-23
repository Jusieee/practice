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
        assert response.json() ==  {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": [
                        "body",
                        "price"
                    ],
                    "msg": "Input should be greater than 0",
                    "input": -100,
                    "ctx": {
                        "gt": 0
                    }
                }
            ]
        }

    finally:
        app.dependency_overrides.pop(get_db, None)