import pytest


@pytest.fixture
def fake_product():
    return {
        "id": 1,
        "name": "Мышь",
        "price": 1000,
        "stock": 10
    }