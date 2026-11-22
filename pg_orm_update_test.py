import getpass

from sqlalchemy import create_engine
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

engine = create_engine(database_url, echo=True)

with Session(engine) as session:
    product = session.get(Product, 9)
    if product is None:
        print("Товара не найден")
    else:
        print("Старая цена: ", product.price)
        print("Старый остаток: ", product.stock)

    product.price = Decimal("2799.90")
    product.stock = 10

    print(session.dirty)
    session.commit()