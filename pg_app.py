from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from pg_database import get_db
from pg_orm_repositories import get_products
from pg_shemas import ProductRead


app = FastAPI(title="Online_shop_PostgreSQL")


@app.get("/products", response_model=list[ProductRead])
def read_products(session: Session = Depends(get_db)):
    products = get_products(session)

    return products