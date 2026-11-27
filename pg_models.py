from decimal import Decimal

from sqlalchemy import Identity, Integer, Numeric, String, text, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "product"

    __table_args__ = (
        CheckConstraint(
            "price > 0",
            name="check_product_price"
        ),
        CheckConstraint(
            "stock >= 0",
            name="check_product_stock"
        ),
        UniqueConstraint(
            "uq_product_name",
            name="Mouse"
        )
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0")
    )

if __name__ == "__main__":
    print(Product.__tablename__)

    for column in Product.__table__.columns:
        print(column.name, column.type)