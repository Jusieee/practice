from decimal import Decimal

from sqlalchemy.orm import Session

from pg_models import Product
from pg_orm_repositories import create_product


def create_product_service(
    session: Session,
    name: str,
    price: Decimal,
    stock: int
) -> Product:
    product = create_product(
        session,
        name=name,
        price=price,
        stock=stock
    )

    session.commit()
    session.refresh(product)

    return product