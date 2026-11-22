from sqlalchemy import select

from pg_models import Product

from decimal import Decimal

from pg_database import SessionLocal


with SessionLocal() as session:
    stmt = select(Product)
    products = session.scalars(stmt).all()

    print("Все товары: ")
    for product in products:
        print(product.name, product.price, product.stock)

    stmt = (
        select(Product)
        .where(Product.price > Decimal("2000"))
        .where(Product.stock > 0)
    )
    products = session.scalars(stmt).all()

    print("Имеющиеся товары больше 2000: ")
    for product in products:
        print(product.name, product.price, product.stock)

    stmt = (
        select(Product)
        .limit(2)
        .order_by(Product.price.desc())
    )
    products = session.scalars(stmt).all()

    print("2 самых дорогих товара: ")
    for product in products:
        print(product.name, product.price, product.stock)