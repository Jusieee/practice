from repositories import (
    create_product,
    get_product_by_id
)

def test_create_and_get_product(test_db):
    created_product = create_product(
        name="Монитор",
        price=25000,
        stock=4
    )

    product = get_product_by_id(
        created_product["id"]
    )

    assert product is not None
    assert product["id"] == created_product["id"]
    assert product["name"] == "Монитор"
    assert product["price"] == 25000
    assert product["stock"] == 4