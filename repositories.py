from database import get_connection


def get_product_by_id(product_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, name, price, stock
            FROM product
            WHERE id = ?
            """,
            (product_id,),
        )

        return cursor.fetchone()

    finally:
        connection.close()