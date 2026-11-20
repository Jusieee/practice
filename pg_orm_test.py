import getpass

from sqlalchemy import create_engine

from sqlalchemy.engine import URL

from sqlalchemy.orm import Session

from pg_models import Product

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

with Session(engine) as session:
    product_1 = session.get(Product, 4)
    product_2 = session.get(Product, 999)
    products = (product_1, product_2)
    for product in products:
        if product is not None:
            print("Название: ", product.name)
            print("Цена: ", product.price)
            print("Остаток: ", product.stock)
        else:
            print("Товар не найден")
    pass

engine.dispose()