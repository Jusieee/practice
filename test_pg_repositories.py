import os

import pytest

from dotenv import load_dotenv

from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from pg_models import Product
from pg_orm_repositories import create_product


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


def test_create_product(test_session):
    product = create_product(
        test_session,
        name="Test Mouse",
        price=Decimal("999.90"),
        stock=5
    )

    assert product.id is not None
    assert product.name == "Test Mouse"
    assert product.price == Decimal("999.90")
    assert product.stock == 5
    test_session.commit()
