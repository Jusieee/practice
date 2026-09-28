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


def test_create_and_get_product(db_connection):
    created_product = create_product(
        db_connection,
        name="Монитор",
        price=25000,
        stock=4
    )

    product = get_product_by_id(
        db_connection,
        created_product["id"]
    )

    assert product is not None
    assert product["id"] == created_product["id"]
    assert product["name"] == "Монитор"
    assert product["price"] == 25000
    assert product["stock"] == 4


def test_create_product_dublicate_name(db_connection):
    first_product = create_product(
        db_connection,
        name="Монитор",
        price=25000,
        stock=4
    )

    with pytest.raises(sqlite3.IntegrityError):
        create_product(
            db_connection,
            name=" МоНиТоР ",
            price=30000,
            stock=10
        )

    product = get_product_by_id(db_connection, first_product["id"])

    assert product is not None
    assert product["name"] == "Монитор"
    assert product["price"] == 25000
    assert product["stock"] == 4


def test_update_product_success(db_connection):
    created_product = create_product(
        db_connection,
        name="Монитор",
        price=25000,
        stock=4
    )

    updated_product = update_product_by_id(
        db_connection,
        product_id=created_product["id"],
        name="Игровой монитор",
        price=30000,
        stock=7
    )

    product_from_db = get_product_by_id(db_connection, created_product["id"])

    assert updated_product == {
        "id": updated_product["id"],
        "name": "Игровой монитор",
        "price": 30000,
        "stock": 7
    }

    assert product_from_db["name"] == "Игровой монитор"
    assert product_from_db["price"] == 30000
    assert product_from_db["stock"] == 7


def test_update_product_not_found(db_connection):
    result = update_product_by_id(
        db_connection,
        product_id=999,
        name="Монитор",
        price=25000,
        stock=4
    )

    assert result is None


def test_update_product_dublicate_name(db_connection):
    first_product = create_product(
        db_connection,
        name="Монитор",
        price=25000,
        stock=4
    )

    second_product = create_product(
        db_connection,
        name="Клавиатура",
        price=5000,
        stock=10
    )

    with pytest.raises(sqlite3.IntegrityError):
        update_product_by_id(
            db_connection,
            product_id=second_product["id"],
            name=" МоНиТор  ",
            price=7000,
            stock=15
        )

    product_from_db = get_product_by_id(db_connection, second_product["id"])

    assert product_from_db["name"] == "Клавиатура"
    assert product_from_db["price"] == 5000
    assert product_from_db["stock"] == 10


def test_create_and_get_cart_item(db_connection):
    product = create_product(
        db_connection,
        name="Мышь",
        price=1000,
        stock=10
    )

    cart_item_id = create_cart_item(
        db_connection,
        product_id=product["id"],
        quantity=3
    )

    cart_item = get_cart_item_by_product_id(db_connection, product["id"])

    assert cart_item is not None
    assert cart_item["id"] == cart_item_id
    assert cart_item["product_id"] == product["id"]
    assert cart_item["quantity"] == 3


def test_create_dublicate_cart_item(db_connection):
    product = create_product(
        db_connection,
        name="Мышь",
        price=1000,
        stock=10
    )

    create_cart_item(
        db_connection,
        product_id=product["id"],
        quantity=2
    )

    with pytest.raises(sqlite3.IntegrityError):
        create_cart_item(
            db_connection,
            product_id=product["id"],
            quantity=5
        )

    cart_item = get_cart_item_by_product_id(db_connection, product["id"])

    assert cart_item["quantity"] == 2


def test_update_cart_item_quantity(db_connection):
    product = create_product(
        db_connection,
        name="Мышь",
        price=1000,
        stock=10
    )

    cart_item_id = create_cart_item(
        db_connection,
        product_id=product["id"],
        quantity=2
    )

    result = update_cart_item_quantity(
        db_connection,
        cart_item_id=cart_item_id,
        quantity=7
    )

    cart_item = get_cart_item_by_product_id(
        db_connection,
        product["id"]
    )

    assert result is True

    assert cart_item["quantity"] == 7


def test_delete_cart_item_success(db_connection):
    product = create_product(
        db_connection,
        name="Мышь",
        price=1000,
        stock=10
    )

    create_cart_item(
        db_connection,
        product_id=product["id"],
        quantity=3
    )

    result = delete_cart_item_by_product_id(
        db_connection,
        product_id=product["id"]
    )

    cart_item = get_cart_item_by_product_id(
        db_connection,
        product_id=product["id"]
    )

    assert result is True
    assert cart_item is None


def test_delete_cart_item_not_found(db_connection):
    result = delete_cart_item_by_product_id(db_connection, 999)

    assert result is False


def test_get_cart_item_with_join(db_connection):
    first_product = create_product(
        db_connection,
        name="Мышь",
        price=1000,
        stock=10
    )

    second_product = create_product(
        db_connection,
        name="Клавиатура",
        price=5000,
        stock=7
    )

    create_cart_item(
        db_connection,
        product_id=first_product["id"],
        quantity=2
    )

    create_cart_item(
        db_connection,
        product_id=second_product["id"],
        quantity=3
    )

    cart_items = get_cart_items(db_connection)

    assert len(cart_items) == 2

    items_product_by_id = {
        item["product_id"]: item
        for item in cart_items
    }

    mouse = items_product_by_id[first_product["id"]]
    keyboard = items_product_by_id[second_product["id"]]

    assert mouse["name"] == "Мышь"
    assert mouse["price"] == 1000
    assert mouse["quantity"] == 2

    assert keyboard["name"] == "Клавиатура"
    assert keyboard["price"] == 5000
    assert keyboard["quantity"] == 3


def test_get_cart_items_empty(db_connection):
    cart_items = get_cart_items(db_connection)

    assert cart_items == []