import getpass

import psycopg

from decimal import Decimal

name = "Mechanical keyboard"
price = Decimal("3499.90")
stock = 5
password = getpass.getpass("Пароль postgreSQL: ")
with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="online_shop_pg",
    user="postgres",
    password=password
) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database()")
        result = cursor.fetchone()
        print("Текущая база: ", result[0])

        cursor.execute(
            """
            INSERT INTO product (name, price, stock)
            VALUES (%s, %s, %s)
            RETURNING id, name, price, stock
            """,
            (name, price, stock)
        )
        product = cursor.fetchone()
        print(product)