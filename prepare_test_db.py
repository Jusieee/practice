import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from pg_models import Base


load_dotenv()

test_db_name = os.environ["DB_TEST_NAME"]

if test_db_name != "online_shop_test":
    raise ValueError("Неверное имя тестовой базы")

database_url = URL.create(
    "postgresql+psycopg",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=test_db_name
)

test_engine = create_engine(database_url)

with test_engine.connect() as connection:
    db_name = connection.exec_driver_sql(
        "SELECT current_database()"
    ).scalar_one()

if db_name != "online_shop_test":
    raise RuntimeError("Подключение не к тестовой базе!")

Base.metadata.create_all(test_engine)

test_engine.dispose()