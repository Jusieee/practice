import sqlite3

from services import CartItemNotFoundError, InsufficientStockError ,ProductNotFoundError

import pytest


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Добро пожаловать в API нашего интернет-магазина!"
    }


def test_get_product_invalid_id(client):
    response = client.get("/products/0")

    assert response.status_code == 422


def test_get_product_invalid_string_id(client):
    response = client.get("/products/hello")

    assert response.status_code == 422


def test_get_product_success(monkeypatch, client):
    fake_product = {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 5
    }

    monkeypatch.setattr(
        "app.get_product_by_id",
        lambda connection, product_id: fake_product
    )

    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 5
    }


def test_get_product_not_found(monkeypatch, client):
    monkeypatch.setattr(
        "app.get_product_by_id",
        lambda connection, product_id: None
    )

    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Товар не найден"
    }


def test_create_product_success(monkeypatch, client):
    fake_created_product = {
        "id": 10,
        "name": "Монитор",
        "price": 25000,
        "stock": 4
    }

    monkeypatch.setattr(
        "app.create_product",
        lambda connection, name, price, stock: fake_created_product
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


def test_create_product_duplicate(monkeypatch, client):
    def fake_create_product(connection, name, price, stock):
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


def test_add_product_to_cart_success(monkeypatch, client):
    fake_cart_item = {
        "id": 10,
        "product_id": 1,
        "product_name": "Мышь",
        "quantity": 3
    }

    monkeypatch.setattr(
        "app.add_product_to_cart",
        lambda connection, product_id, quantity: fake_cart_item
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


def test_add_product_to_cart_product_not_found(monkeypatch, client):
    def fake_add_product_to_cart(connection, product_id, quantity):
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


def test_add_product_to_cart_not_enough_stock(monkeypatch, client):
    def fake_add_product_to_cart(connection, product_id, quantity):
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


def test_set_cart_item_quantity_success(monkeypatch, client):
    fake_cart_item = {
        "id": 15,
        "product_id": 1,
        "product_name": "Мышь",
        "quantity": 4
    }

    monkeypatch.setattr(
        "app.set_cart_item_quantity",
        lambda connection, product_id, quantity: fake_cart_item
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


def test_set_cart_item_quantity_product_not_found(monkeypatch, client):
    def fake_set_cart_item_quantity(connection, product_id, quantity):
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


def test_set_cart_item_quantity_cart_item_not_found(monkeypatch, client):
    def fake_set_cart_item_quantity(connection, product_id, quantity):
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


def test_set_cart_item_quantity_not_enough_stock(monkeypatch, client):
    def fake_cart_item_quantity(connection, product_id,quantity):
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


def test_set_cart_item_quantity_invalid_quantity(monkeypatch, client):
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


def test_delete_cart_item_success(monkeypatch, client):
    monkeypatch.setattr(
        "app.remove_product_from_cart",
        lambda connection, product_id: None
    )

    response = client.delete("/cart/items/1")

    assert response.status_code == 204

    assert response.content == b""


def test_delete_cart_item_not_found(monkeypatch, client):
    def fake_remove_product_from_cart(*args, **kwargs):
        raise CartItemNotFoundError

    monkeypatch.setattr(
        "app.remove_product_from_cart",
        fake_remove_product_from_cart
    )

    response = client.delete("/cart/items/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Товар не найден"
    }


@pytest.mark.parametrize(
    "quantity",
    [0, -1, -10]
)
def test_add_product_to_cart_invalid_quantity(
        monkeypatch,
        quantity,
        client
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "add_product не должен запускаться"
        )

    monkeypatch.setattr(
        "app.add_product_to_cart",
        fail_if_called
    )

    response = client.post(
        "/cart/items",
        json={
            "product_id": 1,
            "quantity": quantity
        }
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "price, stock",
    [
        (0, 4),
        (-1, 4),
        (1000, -1),
        (-100, 5)
    ]
)
def test_create_product_invalid_data(
    monkeypatch,
    price,
    stock,
    client
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "Create_product не должен запускаться"
        )

    monkeypatch.setattr(
        "app.create_product",
        fail_if_called
    )

    response = client.post(
        "/products",
        json={
            "name": "Монитор",
            "price": price,
            "stock": stock
        }
    )

    assert response.status_code == 422


def test_created_product_is_saved(client):
    created = client.post(
        "/products",
        json={
            "name": "Мышь",
            "price": 1000,
            "stock": 5
        }
    )
    assert created.status_code == 201

    response = client.get(f"/products/{created.json()['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Мышь"


def test_cart_flow(client):
    created = client.post(
        "/products",
        json={
            "name": "Мышь",
            "price": 1000,
            "stock": 5
        }
    )
    product_id = created.json()["id"]

    response = client.post(
        "/cart/items",
        json={
            "product_id": product_id,
            "quantity": 2
        }
    )
    assert response.status_code == 201
    cart = client.get("/cart")
    assert cart.json()["total"] == 2000


def test_updated_product_is_saved(client):
    created = client.post(
        "/products",
        json={
            "name": "Мышь",
            "price": 1000,
            "stock": 5
        }
    )
    product_id = created.json()["id"]

    updated = client.put(
        f"/products/{product_id}",
        json={
            "name": "Мышь",
            "price": 500,
            "stock": 10
        }
    )
    assert updated.status_code == 200

    response = client.get(f"/products/{updated.json()['id']}")
    assert response.json()["price"] == 500
    assert response.json()["stock"] == 10


def test_deleted_product_is_gone(client):
    created = client.post(
        "/products",
        json={
            "name": "Мышь",
            "price": 1000,
            "stock": 5
        }
    )
    product_id = created.json()["id"]

    deleted = client.delete(
        f"/products/{product_id}"
    )
    assert deleted.status_code == 204
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404