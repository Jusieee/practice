import sqlite3


def get_product_by_id(connection: sqlite3.Connection, product_id: int):
    cursor = connection.execute(
        """
        SELECT id, name, price, stock
        FROM product
        WHERE id = ?
        """,
        (product_id,),
    )
    return cursor.fetchone()


def get_all_products(connection: sqlite3.Connection):
    cursor = connection.execute(
        """
        SELECT id, name, price, stock
        FROM product
        """
    )
    return cursor.fetchall()


def delete_product_by_id(connection: sqlite3.Connection, product_id: int) -> bool:
    cursor = connection.execute(
        """
        DELETE FROM product
        WHERE id = ?
        """,
        (product_id,)
    )
    return cursor.rowcount > 0


def update_product_by_id(
        connection: sqlite3.Connection,
        product_id: int,
        name: str,
        price: float,
        stock: int
):
    cursor = connection.execute(
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
    return {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }


def create_product(
        connection: sqlite3.Connection,
        name: str,
        price: float,
        stock: int
):
    product_name = name.strip()
    product_name_key = product_name.casefold()
    cursor = connection.execute(
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
    return {
        "id": cursor.lastrowid,
        "name": product_name,
        "price": price,
        "stock": stock
    }


def create_cart_item(
        connection: sqlite3.Connection,
        product_id: int,
        quantity: int
):
    cursor = connection.execute(
        """
        INSERT INTO cart_items (product_id, quantity)
        VALUES (?, ?)
        """,
        (product_id, quantity)
    )
    return cursor.lastrowid


def get_cart_item_by_product_id(connection: sqlite3.Connection, product_id: int):
    cursor = connection.execute(
        """
        SELECT id, product_id, quantity
        FROM cart_items
        WHERE product_id = ?
        """,
        (product_id,)
    )
    return cursor.fetchone()


def update_cart_item_quantity(
        connection: sqlite3.Connection,
        cart_item_id: int,
        quantity: int
):
    cursor = connection.execute(
        """
        UPDATE cart_items
        SET quantity = ?
        WHERE id = ?
        """,
        (quantity, cart_item_id)
    )
    return cursor.rowcount > 0


def get_cart_items(connection: sqlite3.Connection):
    cursor = connection.execute(
        """
        SELECT 
            cart_items.id,
            cart_items.product_id,
            product.name,
            product.price,
            cart_items.quantity
        FROM cart_items
        JOIN product
            ON cart_items.product_id = product.id
        """
    )
    return cursor.fetchall()


def delete_cart_item_by_product_id(connection: sqlite3.Connection, product_id: int) -> bool:
    cursor = connection.execute(
        """
        DELETE FROM cart_items
        WHERE product_id = ?
        """,
        (product_id,)
    )
    return cursor.rowcount > 0