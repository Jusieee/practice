from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from pg_models import Product
from pg_orm_repositories import create_product
from pg_exceptions import DuplicateProductError


def create_product_service(
    session: Session,
    name: str,
    price: Decimal,
    stock: int
) -> Product:
    try:
        product = create_product(
            session,
            name=name,
            price=price,
            stock=stock
        )

        session.commit()

    except IntegrityError as exc:
        session.rollback()
        constraint_name = exc.orig.diag.constraint_name

        if constraint_name == "uq_product_name":
            raise DuplicateProductError(
                "Товар с таким названием уже существует"
            ) from exc
        else:
            raise IntegrityError

    session.refresh(product)

    return product
