from decimal import Decimal

import psycopg


def create_product(
    connection: psycopg.Connection,
    name: str,
    price: Decimal,
    stock: int
) -> tuple | None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO product (name, price, stock)
            VALUES (%s, %s, %s)
            RETURNING id, name, price, stock
            """,
            (name, price, stock)
        )
        product = cursor.fetchone()

    return product