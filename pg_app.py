from fastapi import FastAPI, Depends, HTTPException, status

from sqlalchemy.orm import Session

from pg_database import get_db
from pg_orm_repositories import get_products, get_product_by_id
from pg_sсhemas import ProductRead


app = FastAPI(title="Online_shop_PostgreSQL")


@app.get("/products", response_model=list[ProductRead])
def read_products(session: Session = Depends(get_db)):
    products = get_products(session)

    return products

@app.get("/product/{product_id}", response_model=ProductRead)
def read_product(
    product_id: int,
    session: Session = Depends(get_db)
):
    product = get_product_by_id(session, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такого товара нету"
        )
    else:
        return product