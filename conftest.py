import pytest


@pytest.fixture
def fake_product():
    return {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 10
    }

@pytest.fixture
def fake_cart_item():
    return {
        "id": 15,
        "product_id": 1,
        "quantity": 3
    }