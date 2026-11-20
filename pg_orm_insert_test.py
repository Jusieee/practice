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

engine = create_engine(database_url)

with Session(engine) as session:
    product = Product(
        name="Webcam",
        price=Decimal("2499.90"),
        stock=3
    )
    print("ID после создание обьекта: ", product.id)

    session.add(product)
    print("ID после add", product.id)

    session.flush()
    print("ID после flush: ", product.id)

    product_id = product.id

    session.commit()
    print("Транзакция сохранена")

with Session(engine) as session:
    product = session.get(Product, product_id)

    if product is None:
        print("Товар отсутствует в базе")
    else:
        print("Товар найден: ", product.name)

engine.dispose()