from repositories import (
    create_product,
    get_product_by_id,
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


def test_update_product_bot_found(test_db):
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