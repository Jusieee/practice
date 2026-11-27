import pytest

from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from pg_services import create_product_service


def test_session_recovery_after_integrity_error(test_session):
    with pytest.raises(IntegrityError):
        create_product_service(
            test_session,
            "Invalid Mouse",
            Decimal("-100.00"),
            5
        )

    product = create_product_service(
        test_session,
        "Valid Mouse",
        Decimal("999.90"),
        5
    )

    assert product.id is not None
    assert product.name == "Valid Mouse"
    assert product.price == Decimal("999.90")
    assert product.stock == 5