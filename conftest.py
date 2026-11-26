import pytest

import sqlite3

import os

from fastapi.testclient import TestClient

from app import app
from pg_app import app as pg_app

from database import get_db
from pg_database import get_db as pg_get_db

from dotenv import  load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session


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
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 0,
    FOREIGN KEY (product_id)
        REFERENCES product(id)
        ON DELETE CASCADE
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
    path = tmp_path / "test_online_shop.db"
    connection = sqlite3.connect(path)
    connection.executescript(SCHEMA)
    connection.close()
    return path


@pytest.fixture
def db_connection(db_path):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    yield connection
    connection.close()


@pytest.fixture
def client(db_path):
    def override_get_db():
        connection = sqlite3.connect(db_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
        finally:
            connection.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_session():
    load_dotenv()

    test_db_name = os.environ["DB_TEST_NAME"]

    if test_db_name != "online_shop_test":
        raise RuntimeError("Неверная тестовая база!")

    database_url = URL.create(
        "postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=test_db_name
    )

    test_engine = create_engine(database_url)

    try:
        with test_engine.connect() as connection:
            transaction = connection.begin()

            try:
                actual_db = connection.exec_driver_sql(
                    "SELECT current_database()"
                ).scalar_one()

                if actual_db != "online_shop_test":
                    raise RuntimeError("Подключение не к той базе!")

                with Session(
                    bind=connection,
                    join_transaction_mode="create_savepoint"
                ) as session:
                    yield session
            finally:
                transaction.rollback()

    finally:
        test_engine.dispose()


@pytest.fixture
def pg_client(test_session):
    def override_get_db():
        yield test_session

    pg_app.dependency_overrides[pg_get_db] = override_get_db

    try:
        with TestClient(pg_app) as client:
            yield client
    finally:
        pg_app.dependency_overrides.pop(pg_get_db, None)
