import pytest

from services import (
    InsufficientStockError,
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