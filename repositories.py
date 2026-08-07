import sqlite3

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


def get_all_products():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, name, price, stock
            FROM product
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def delete_product_by_id(product_id: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM product
            WHERE id = ?
            """,
            (product_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def update_product_by_id(
        product_id: int,
        name: str,
        price: float,
        stock: int
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id
            FROM product
            WHERE id = ?
            """,
            (product_id,)
        )

        existing_product = cursor.fetchone()

        if existing_product is None:
            return None

        product_name = name.strip()
        product_name_key = product_name.casefold()

        cursor.execute(
            """
            UPDATE product
            SET name = ?,
                price = ?,
                stock = ?,
                name_key = ?
            WHERE id = ?
            """,
            (
                product_name,
                price,
                stock,
                product_name_key,
                product_id,
            ),
        )

        connection.commit()

        return {
            "id": product_id,
            "name": product_name,
            "price": price,
            "stock": stock
        }

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def create_product(
        name: str,
        price: float,
        stock: int
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        product_name = name.strip()
        product_name_key = product_name.casefold()

        cursor.execute(
            """
            INSERT INTO product (
                name,
                price,
                stock,
                name_key
            )
            VALUES (?, ?, ?, ?)
            """,
            (product_name, price, stock, product_name_key)
        )

        connection.commit()

        return {
            "id": cursor.lastrowid,
            "name": product_name,
            "price": price,
            "stock": stock
        }

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def create_cart_item(
        product_id: int,
        quantity: int
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO cart_item (product_id, quantity)
            VALUES (?, ?)
            """,
            (product_id, quantity)
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()