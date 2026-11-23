from sqlalchemy import select
from sqlalchemy.orm import Session

from pg_models import Product


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
