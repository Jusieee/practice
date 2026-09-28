import pytest

import sqlite3

from fastapi.testclient import TestClient

import database


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
def db_connection():
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    yield connection
    connection.close()


@pytest.fixture
def product_in_db(db_connection):
    cursor = db_connection.execute(
        """
        INSERT INTO product(name, price, stock, name_key)
        VALUES (?, ?, ?, ?)
        """,
        ("Мышь", 1000, 5, "мышь")
    )
    return cursor.lastrowid


@pytest.fixture
def client(db_connection):
    app.dependency_overrides[get_db] = lambda: db_connection
    yield TestClient(app)