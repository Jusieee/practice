import pytest

from services import (
    InsufficientStockError,
    ProductNotFoundError,
    add_product_to_cart,
    get_cart,
)


def test_get_cart_calculates_total(monkeypatch):
    fake_cart_items = [
        {
            "id": 1,
            "product_id": 10,
            "name": "Мышь",
            "price": 1000,
            "quantity": 2
        },
        {
            "id": 2,
            "product_id": 20,
            "name": "Клавиатура",
            "price": 3000,
            "quantity": 1
        }
    ]

    monkeypatch.setattr(
        "services.get_cart_items",
        lambda: fake_cart_items
    )

    result = get_cart()

    assert result["total"] == 5000
    assert result["items"][0]["total_price"] == 2000
    assert result["items"][1]["total_price"] == 3000


def test_add_product_to_cart_not_enough_stock(monkeypatch):
    fake_product = {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 5
    }

    fake_cart_item = {
        "id": 10,
        "product_id": 1,
        "quantity": 3
    }

    monkeypatch.setattr(
        "services.get_product_by_id",
        lambda product_id: fake_product
    )

    monkeypatch.setattr(
        "services.get_cart_item_by_product_id",
        lambda product_id: fake_cart_item
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "Функция изменения корзины не должна вызываться"
        )

    monkeypatch.setattr(
        "services.create_cart_item",
        fail_if_called
    )

    monkeypatch.setattr(
        "services.update_cart_item_quantity",
        fail_if_called
    )

    with pytest.raises(InsufficientStockError) as error:
        add_product_to_cart(
            product_id=1,
            quantity=4
        )

    assert error.value.available == 5


def test_add_product_to_cart_creates_new_item(monkeypatch):
    fake_product = {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 10
    }

    monkeypatch.setattr(
        "services.get_product_by_id",
        lambda product_id: fake_product
    )

    monkeypatch.setattr(
        "services.get_cart_item_by_product_id",
        lambda product_id: None
    )

    created_data = {}

    def fake_create_cart_item(product_id, quantity):
        created_data["product_id"] = product_id
        created_data["quantity"] = quantity

        return 15

    monkeypatch.setattr(
        "services.create_cart_item",
        fake_create_cart_item,
    )

    result = add_product_to_cart(
        product_id=1,
        quantity=3
    )

    assert created_data["product_id"] == 1
    assert created_data["quantity"] == 3

    assert result["id"] == 15
    assert result["product_id"] == 1
    assert result["product_name"] == "Мышь"
    assert result["quantity"] == 3


def test_add_product_to_cart_updates_existing_item(monkeypatch):
    fake_product = {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 10
    }

    fake_cart_item = {
        "id": 15,
        "product_id": 1,
        "quantity": 3
    }

    monkeypatch.setattr(
        "services.get_product_by_id",
        lambda product_id: fake_product
    )

    monkeypatch.setattr(
        "services.get_cart_item_by_product_id",
        lambda product_id: fake_cart_item
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "cart_item уже есть, создаться не должен"
        )

    monkeypatch.setattr(
        "services.create_cart_item",
        fail_if_called
    )

    updated_data = {}

    def fake_update_cart_item_quantity(cart_item_id, quantity):
        updated_data["cart_item_id"] = cart_item_id
        updated_data["quantity"] = quantity

    monkeypatch.setattr(
        "services.update_cart_item_quantity",
        fake_update_cart_item_quantity
    )

    result = add_product_to_cart(
        product_id=1,
        quantity=2
    )

    assert updated_data["cart_item_id"] == 15
    assert updated_data["quantity"] == 5

    assert result["id"] == 15
    assert result["product_id"] == 1
    assert result["product_name"] == "Мышь"
    assert result["quantity"] == 5


def test_add_product_to_cart_not_found_item(monkeypatch):
    monkeypatch.setattr(
        "services.get_product_by_id",
        lambda product_id: None
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "Товара такого нету"
        )

    monkeypatch.setattr(
        "services.get_cart_item_by_product_id",
        fail_if_called
    )

    with pytest.raises(ProductNotFoundError):
        add_product_to_cart(
            product_id=999,
            quantity=1
        )