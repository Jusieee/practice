from fastapi.testclient import TestClient

from app import app

import sqlite3

from services import CartItemNotFoundError, InsufficientStockError ,ProductNotFoundError


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


def test_create_product_duplicate(monkeypatch):
    def fake_create_product(name, price, stock):
        raise sqlite3.IntegrityError

    monkeypatch.setattr(
        "app.create_product",
        fake_create_product
    )

    response = client.post(
        "/products",
        json={
            "name": "Монитор",
            "price": 25000,
            "stock": 4
        }
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "Такой товар уже есть"
    }


def test_create_product_invalid_price(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "created_product не должен вызываться при ошибке валидации"
        )

    monkeypatch.setattr(
        "app.create_product",
        fail_if_called
    )

    response = client.post(
        "/products",
        json={
            "name": "Монитор",
            "price": -100,
            "stock": 4
        }
    )

    assert response.status_code == 422


def test_add_product_to_cart_success(monkeypatch):
    fake_cart_item = {
        "id": 10,
        "product_id": 1,
        "product_name": "Мышь",
        "quantity": 3
    }

    monkeypatch.setattr(
        "app.add_product_to_cart",
        lambda product_id, quantity: fake_cart_item
    )

    response = client.post(
        "/cart/items",
        json={
            "product_id": 1,
            "quantity": 3
        }
    )

    assert response.status_code == 201

    assert response.json() == {
        "id": 10,
        "product_id": 1,
        "product_name": "Мышь",
        "quantity": 3
    }


def test_add_product_to_cart_product_not_found(monkeypatch):
    def fake_add_product_to_cart(product_id, quantity):
        raise ProductNotFoundError

    monkeypatch.setattr(
        "app.add_product_to_cart",
        fake_add_product_to_cart
    )

    response = client.post(
        "/cart/items",
        json={
            "product_id": 999,
            "quantity": 1
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Товар не найден"
    }


def test_add_product_to_cart_not_enough_stock(monkeypatch):
    def fake_add_product_to_cart(product_id, quantity):
        raise InsufficientStockError(5)

    monkeypatch.setattr(
        "app.add_product_to_cart",
        fake_add_product_to_cart
    )

    response = client.post(
        "/cart/items",
        json={
            "product_id": 1,
            "quantity": 10
        }
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "Недостаточно товаров, доступно 5"
    }


def test_add_product_to_cart_invalid_quantity(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "add_product_to_cart не должен вызываться, при ошибке валидации"
        )

    monkeypatch.setattr(
        "app.add_product_to_cart",
        fail_if_called
    )

    response = client.post(
        "/cart/items",
        json={
            "product_id": 1,
            "quantity": 0
        }
    )

    assert response.status_code == 422


def test_set_cart_item_quantity_success(monkeypatch):
    fake_cart_item = {
        "id": 15,
        "product_id": 1,
        "product_name": "Мышь",
        "quantity": 4
    }

    monkeypatch.setattr(
        "app.set_cart_item_quantity",
        lambda product_id, quantity: fake_cart_item
    )

    response = client.patch(
        "/cart/items/1",
        json={
            "quantity": 4
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": 15,
        "product_id": 1,
        "product_name": "Мышь",
        "quantity": 4
    }


def test_set_cart_item_quantity_product_not_found(monkeypatch):
    def fake_set_cart_item_quantity(product_id, quantity):
        raise ProductNotFoundError

    monkeypatch.setattr(
        "app.set_cart_item_quantity",
        fake_set_cart_item_quantity
    )

    response = client.patch(
        "/cart/items/999",
        json={
            "quantity": 3
        }
    )

    assert response.status_code == 404


def test_set_cart_item_quantity_cart_item_not_found(monkeypatch):
    def fake_set_cart_item_quantity(product_id, quantity):
        raise CartItemNotFoundError

    monkeypatch.setattr(
        "app.set_cart_item_quantity",
        fake_set_cart_item_quantity
    )

    response = client.patch(
        "/cart/items/1",
        json={
            "quantity": 3
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Товара в корзине нету"
    }


def test_set_cart_item_quantity_not_enough_stock(monkeypatch):
    def fake_cart_item_quantity(product_id,quantity):
        raise InsufficientStockError(5)

    monkeypatch.setattr(
        "app.set_cart_item_quantity",
        fake_cart_item_quantity
    )

    response = client.patch(
        "/cart/items/1",
        json={
            "quantity": 10
        }
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "Доступно только: 5 шт."
    }


def test_set_cart_item_quantity_invalid_quantity(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "Функция не должна запускаться"
        )

    monkeypatch.setattr(
        "app.set_cart_item_quantity",
        fail_if_called
    )

    response = client.patch(
        "/cart/items/1",
        json={
            "quantity": 0
        }
    )

    assert response.status_code == 422


def test_delete_cart_item_success(monkeypatch):
    monkeypatch.setattr(
        "app.remove_product_from_cart",
        lambda product_id: None
    )

    response = client.delete("/cart/items/1")

    assert response.status_code == 204

    assert response.content == b""