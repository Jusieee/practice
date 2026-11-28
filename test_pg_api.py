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


def test_create_product_success(pg_client):
    response = pg_client.post(
        "/products",
        json={
            "name": "Test Keyboard",
            "price": "1990.90",
            "stock": 5
        }
    )

    assert response.status_code == 201

    product = response.json()
    assert product["id"] is not None
    assert product["name"] == "Test Keyboard"
    assert product["price"] == "1990.90"
    assert product["stock"] == 5

    get_response = pg_client.get(f"/products/{response.json()['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Keyboard"
    assert get_response.json()["price"] == "1990.90"
    assert get_response.json()["stock"] == 5


def test_create_duplicate_product(pg_client):
    data = {
        "name": "Test Keyboard",
        "price": "1990.90",
        "stock": 5
    }

    first_response = pg_client.post(
        "/products",
        json=data
    )
    assert first_response.status_code == 201

    second_response = pg_client.post(
        "/products",
        json=data
    )
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Товар с таким названием уже существует"
    }

    product = pg_client.get(f"/products/{first_response.json()['id']}")
    assert product is not None