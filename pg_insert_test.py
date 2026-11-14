import getpass

import psycopg

from decimal import Decimal

from pg_repositories import create_product


password = getpass.getpass("Пароль postgreSQL: ")
with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="online_shop_pg",
    user="postgres",
    password=password
) as connection:
    product = create_product(
        connection,
        "USB Hub",
        Decimal("1299.90"),
        4
    )
    print(product)