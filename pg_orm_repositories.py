from sqlalchemy import select
from sqlalchemy.orm import Session

from pg_models import Product

from decimal import Decimal


def get_products(session: Session) -> list[Product]:
    stmt = select(Product)
    products = list(session.scalars(stmt).all())

    return products


def get_product_by_id(
    session: Session,
    product_id: int
) -> Product | None:
    product = session.get(Product, ident=product_id)

    return product


def create_product(
    session: Session,
    name: str,
    price: Decimal,
    stock: int
) -> Product:
    product = Product(
        name=name,
        price=price,
        stock=stock)

    session.add(product)
    session.flush()

    return product