from repositories import create_cart_item, get_product_by_id


class ProductNotFoundError(Exception):
    pass

class InsufficientStockError(Exception):
    def __init__(self, available: int):
        self.available = available


def add_product_to_cart(
        product_id: int,
        quantity: int
):
    product = get_product_by_id(product_id)

    if product is None:
        raise ProductNotFoundError

    if quantity > product["stock"]:
        raise InsufficientStockError(product["stock"])

    cart_item_id = create_cart_item(
        product_id=product_id,
        quantity=quantity
    )

    return {
        "id": cart_item_id,
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity
    }