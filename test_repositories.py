from repositories import (
    create_product,
    create_cart_item,
    delete_cart_item_by_product_id,
    get_cart_item_by_product_id,
    get_cart_items,
    get_product_by_id,
    update_cart_item_quantity,
    update_product_by_id
)

import pytest

import sqlite3


def test_create_and_get_product(test_db):
    created_product = create_product(
        name="Монитор",
        price=25000,
        stock=4
    )

    product = get_product_by_id(
        created_product["id"]
    )

    assert product is not None
    assert product["id"] == created_product["id"]
    assert product["name"] == "Монитор"
    assert product["price"] == 25000
    assert product["stock"] == 4


def test_create_product_dublicate_name(test_db):
    first_product = create_product(
        name="Монитор",
        price=25000,
        stock=4
    )

    with pytest.raises(sqlite3.IntegrityError):
        create_product(
            name=" МоНиТоР ",
            price=30000,
            stock=10
        )

    product = get_product_by_id(first_product["id"])

    assert product is not None
    assert product["name"] == "Монитор"
    assert product["price"] == 25000
    assert product["stock"] == 4


def test_update_product_success(test_db):
    created_product = create_product(
        name="Монитор",
        price=25000,
        stock=4
    )

    updated_product = update_product_by_id(
        product_id=created_product["id"],
        name="Игровой монитор",
        price=30000,
        stock=7
    )

    product_from_db = get_product_by_id(created_product["id"])

    assert updated_product == {
        "id": updated_product["id"],
        "name": "Игровой монитор",
        "price": 30000,
        "stock": 7
    }

    assert product_from_db["name"] == "Игровой монитор"
    assert product_from_db["price"] == 30000
    assert product_from_db["stock"] == 7


def test_update_product_not_found(test_db):
    result = update_product_by_id(
        product_id=999,
        name="Монитор",
        price=25000,
        stock=4
    )

    assert result is None


def test_update_product_dublicate_name(test_db):
    first_product = create_product(
        name="Монитор",
        price=25000,
        stock=4
    )

    second_product = create_product(
        name="Клавиатура",
        price=5000,
        stock=10
    )

    with pytest.raises(sqlite3.IntegrityError):
        update_product_by_id(
            product_id=second_product["id"],
            name=" МоНиТор  ",
            price=7000,
            stock=15
        )

    product_from_db = get_product_by_id(second_product["id"])

    assert product_from_db["name"] == "Клавиатура"
    assert product_from_db["price"] == 5000
    assert product_from_db["stock"] == 10


def test_create_and_get_cart_item(test_db):
    product = create_product(
        name="Мышь",
        price=1000,
        stock=10
    )

    cart_item_id = create_cart_item(
        product_id=product["id"],
        quantity=3
    )

    cart_item = get_cart_item_by_product_id(product["id"])

    assert cart_item is not None
    assert cart_item["id"] == cart_item_id
    assert cart_item["product_id"] == product["id"]
    assert cart_item["quantity"] == 3


def test_create_dublicate_cart_item(test_db):
    product = create_product(
        name="Мышь",
        price=1000,
        stock=10
    )

    create_cart_item(
        product_id=product["id"],
        quantity=2
    )

    with pytest.raises(sqlite3.IntegrityError):
        create_cart_item(
            product_id=product["id"],
            quantity=5
        )

    cart_item = get_cart_item_by_product_id(product["id"])

    assert cart_item["quantity"] == 2


def test_update_cart_item_quantity(test_db):
    product = create_product(
        name="Мышь",
        price=1000,
        stock=10
    )

    cart_item_id = create_cart_item(
        product_id=product["id"],
        quantity=2
    )

    result = update_cart_item_quantity(
        cart_item_id=cart_item_id,
        quantity=7
    )

    cart_item = get_cart_item_by_product_id(
        product["id"]
    )

    assert result == cart_item_id

    assert cart_item["quantity"] == 7


def test_delete_cart_item_success(test_db):
    product = create_product(
        name="Мышь",
        price=1000,
        stock=10
    )

    create_cart_item(
        product_id=product["id"],
        quantity=3
    )

    result = delete_cart_item_by_product_id(
        product_id=product["id"]
    )

    cart_item = get_cart_item_by_product_id(
        product_id=product["id"]
    )

    assert result is True
    assert cart_item is None


def test_delete_cart_item_not_found(test_db):
    result = delete_cart_item_by_product_id(999)

    assert result is False


def test_get_cart_item_with_join(test_db):
    first_product = create_product(
        name="Мышь",
        price=1000,
        stock=10
    )

    second_product = create_product(
        name="Клавиатура",
        price=5000,
        stock=7
    )

    first_cart_item_id = create_cart_item(
        product_id=first_product["id"],
        quantity=2
    )

    second_cart_item_id = create_cart_item(
        product_id=second_product["id"],
        quantity=3
    )

    cart_items = get_cart_items()

    assert len(cart_items) == 2

    assert cart_items[0]["id"] == first_cart_item_id
    assert cart_items[0]["product_id"] == first_product["id"]
    assert cart_items[0]["name"] == "Мышь"
    assert cart_items[0]["price"] == 1000
    assert cart_items[0]["quantity"] == 2

    assert cart_items[1]["id"] == second_cart_item_id
    assert cart_items[1]["product_id"] == second_product["id"]
    assert cart_items[1]["name"] == "Клавиатура"
    assert cart_items[1]["price"] == 5000
    assert cart_items[1]["quantity"] == 3