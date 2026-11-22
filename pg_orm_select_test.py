import getpass

from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from pg_models import Product

from decimal import Decimal


password = getpass.getpass("Пароль PostgreSQL:")

database_url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password=password,
    host="localhost",
    port=5432,
    database="online_shop_pg"
)

engine = create_engine(database_url)

with (Session(engine) as session):
    stmt = select(Product)
    products = session.scalars(stmt).all()

    print("Все товары: ")
    for product in products:
        print(product.name, product.price, product.stock)

    stmt = (
        select(Product)
        .where(Product.price > Decimal("2000"))
        .where(Product.stock > 0)
    )
    products = session.scalars(stmt).all()

    print("Имеющиеся товары больше 2000: ")
    for product in products:
        print(product.name, product.price, product.stock)

    stmt = (
        select(Product)
        .limit(2)
        .order_by(Product.price.desc())
    )
    products = session.scalars(stmt).all()

    print("2 самых дорогих товара: ")
    for product in products:
        print(product.name, product.price, product.stock)