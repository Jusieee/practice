from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Добро пожаловать в API нашего интернет-магазина!"
    }


def test_get_product_invalid_id():
    response = client.get("/products/0")

    assert response.status_code == 422


def test_get_product_invalid_string_id():
    response = client.get("/products/hello")

    assert response.status_code == 422


def test_get_product_success(monkeypatch):
    fake_product = {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 5
    }

    monkeypatch.setattr(
        "app.get_product_by_id",
        lambda product_id: fake_product
    )

    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 5
    }


def test_get_product_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.get_product_by_id",
        lambda product_id: None
    )

    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Товар не найден"
    }


def test_create_product_success(monkeypatch):
    fake_created_product = {
        "id": 10,
        "name": "Монитор",
        "price": 25000,
        "stock": 4
    }

    monkeypatch.setattr(
        "app.create_product",
        lambda name, price, stock: fake_created_product
    )

    response = client.post(
        "/products",
        json={
            "name": "Монитор",
            "price": 25000,
            "stock": 4
        }
    )

    assert response.status_code == 201

    assert response.json() == {
        "id": 10,
        "name": "Монитор",
        "price": 25000,
        "stock": 4
    }