import getpass

import psycopg

from pg_repositories import get_product_by_id


product_id = 999
password = getpass.getpass("Пароль PostgreSQL:")
with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="online_shop_pg",
    user="postgres",
    password=password
) as connection:
    product = get_product_by_id(
        connection,
        product_id
    )
    if product is not None:
        print(product)
    else:
        print('Товар не найден!')