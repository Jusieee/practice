from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "massage": "Добро пожаловать в API нашего интернет-магазина!"
    }

def test_get_product_invalid_id():
    response = client.get("/products/0")

    assert response.status_code == 422

def test_get_product_invalid_string_id():
    response = client.get("/products/hello")

    assert response.status_code == 422