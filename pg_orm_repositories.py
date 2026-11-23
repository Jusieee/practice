from sqlalchemy import select
from sqlalchemy.orm import Session

from pg_models import Product


def get_products(session: Session) -> list[Product]:
    stmt = select(Product)
    products = list(session.scalars(stmt).all())

    return products
