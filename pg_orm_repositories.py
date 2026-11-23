from sqlalchemy import select
from sqlalchemy.orm import Session

from pg_models import Product


def get_products(session: Session) -> list[Product]:
    with session as sessions:
        stmt = select(Product)
        products = list(sessions.scalars(stmt).all())
    return products
