import pytest

from sqlalchemy.exc import IntegrityError

from decimal import Decimal

from pg_orm_repositories import create_product


def test_create_product(test_session):
    product = create_product(
        test_session,
        name="Test Mouse",
        price=Decimal("999.90"),
        stock=5
    )

    assert product.id is not None
    assert product.name == "Test Mouse"
    assert product.price == Decimal("999.90")
    assert product.stock == 5
    test_session.commit()


def test_create_product_invalid_price(test_session):
    with pytest.raises(IntegrityError) as exc_info:
        create_product(
            test_session,
            "Invalid Mouse",
            Decimal("-100.00"),
            5
        )

    assert (
        exc_info.value.orig.diag.constraint_name
        == "check_product_price"
    )