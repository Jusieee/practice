from services import get_cart


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