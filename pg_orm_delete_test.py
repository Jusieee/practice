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
    product = session.get(Product, 9)

    if product is not None:
        session.delete(product)
        session.flush()

    session.rollback()

with Session(engine) as session:
    product = session.get(Product, 9)
    print("Товар остался -> ", product.name)