from repositories import (
    create_product,
    get_product_by_id
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