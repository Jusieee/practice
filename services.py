from repositories import (
    create_cart_item,
    delete_cart_item_by_product_id,
    get_cart_items,
    get_cart_item_by_product_id,
    get_product_by_id,
    update_cart_item_quantity
)


class ProductNotFoundError(Exception):
    pass

class InsufficientStockError(Exception):
    def __init__(self, available: int):
        self.available = available

class CartItemNotFoundError(Exception):
    pass

def add_product_to_cart(
        connection,
        product_id: int,
        quantity: int
):
    with connection:
        product = get_product_by_id(connection, product_id)
        if product is None:
            raise ProductNotFoundError

        cart_item = get_cart_item_by_product_id(connection, product_id)
        current = cart_item["quantity"] if cart_item else 0
        total_quantity = current + quantity
        if total_quantity > product["stock"]:
            raise InsufficientStockError(product["stock"])

        if cart_item is None:
            cart_item_id = create_cart_item(connection, product_id, quantity)
        else:
            cart_item_id = cart_item["id"]
            update_cart_item_quantity(connection, cart_item_id, total_quantity)

    return {
        "id": cart_item_id,
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": total_quantity
    }


def get_cart(connection):
    with connection:
        cart_items = get_cart_items(connection)
        items = []
        total = 0
        for item in cart_items:
            item_total = item["price"] * item["quantity"]
            total += item_total
            items.append(
            {
                "id": item["id"],
                "product_id": item["product_id"],
                "product_name": item["name"],
                "price": item["price"],
                "quantity": item["quantity"],
                "total_price": item_total
            }
            )
    return {
        "items": items,
        "total": total
    }


def remove_product_from_cart(connection, product_id: int):
    with connection:
        removed = delete_cart_item_by_product_id(connection, product_id)
        if not removed:
            raise CartItemNotFoundError


def set_cart_item_quantity(
        connection,
        product_id: int,
        quantity: int
):
    with connection:
        product = get_product_by_id(connection, product_id)
        if product is None:
            raise ProductNotFoundError

        cart_item = get_cart_item_by_product_id(connection, product_id)
        if cart_item is None:
            raise CartItemNotFoundError
        if quantity > product["stock"]:
            raise InsufficientStockError(product["stock"])
        update_cart_item_quantity(connection, cart_item["id"], quantity)
    return {
        "id": cart_item["id"],
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity
    }