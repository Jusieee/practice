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
