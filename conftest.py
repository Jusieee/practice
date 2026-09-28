import pytest

import sqlite3


SCHEMA = """
CREATE TABLE product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    name_key TEXT NOT NULL UNIQUE
);
CREATE TABLE cart_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER DEFAULT 0
);
CREATE UNIQUE INDEX idx_cart_items_product_id ON cart_items(product_id);
"""


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


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "test_online_shop.py"
    connection = sqlite3.connect(path)
    connection.executescript(SCHEMA)
    connection.close()
    return path

@pytest.fixture
def db_connection(db_path):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    yield connection
    connection.close()