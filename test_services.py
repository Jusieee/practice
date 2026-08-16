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

    with pytest.raises(InsufficientStockError) as error:
        add_product_to_cart(
            product_id=1,
            quantity=4
        )

    assert error.value.available == 5