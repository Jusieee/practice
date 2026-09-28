import sqlite3

from fastapi import Depends, FastAPI, HTTPException, status, Path

from schemas import (
    Product,
    CartItemActionResponse,
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
    ProductCreate,
    ProductUpdate,
)

from repositories import (
    create_product,
    delete_product_by_id,
    get_all_products,
    get_product_by_id,
    update_product_by_id
)

from services import (
    add_product_to_cart,
    CartItemNotFoundError,
    get_cart,
    InsufficientStockError,
    ProductNotFoundError,
    remove_product_from_cart,
    set_cart_item_quantity
)

from database import get_db


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Добро пожаловать в API нашего интернет-магазина!"}


@app.get("/products", response_model=list[Product])
def get_products(
        connection: sqlite3.Connection = Depends(get_db)
):
    products = get_all_products(connection)
    return [
        {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "stock": product["stock"]
        }
        for product in products
    ]


@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED
)
def create_product_endpoint(product: ProductCreate, connection: sqlite3.Connection = Depends(get_db)):
    try:
        with connection:
            return create_product(
                connection,
                product.name,
                product.price,
                product.stock
            )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой товар уже есть"
        )

    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Товар не удалось создать"
        )


@app.post(
    "/cart/items",
    status_code=status.HTTP_201_CREATED,
    response_model=CartItemActionResponse
)
def add_to_cart(
    item: CartItemCreate,
    connection: sqlite3.Connection = Depends(get_db)
):
    try:
        return add_product_to_cart(connection, item.product_id, item.quantity)
    except ProductNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    except InsufficientStockError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Недостаточно товаров, доступно {error.available}"
        )

    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе в базе данных"
        )


@app.get("/products/{product_id}", response_model=Product)
def get_product(
    product_id: int = Path(gt=0),
    connection: sqlite3.Connection = Depends(get_db)
):
    product = get_product_by_id(connection, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )

    return {
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "stock": product["stock"],
    }


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int = Path(gt=0),
    connection: sqlite3.Connection = Depends(get_db)
):
    try:
        with connection:
            deleted = delete_product_by_id(connection, product_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Такого товара нету"
                )
    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Серверная ошибка"
        )


@app.put("/products/{product_id}",
         response_model=Product)
def update_product(
    product: ProductUpdate,
    product_id: int = Path(gt=0),
    connection: sqlite3.Connection = Depends(get_db)
):
    try:
        with connection:
            updated_product = update_product_by_id(
                connection,
                product_id=product_id,
                name=product.name,
                price=product.price,
                stock=product.stock
            )
            if updated_product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Такого товара нету"
                )
            return updated_product
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Товар с такой информацией уже есть"
        )

    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Серверная ошибка"
        )


@app.get("/cart",
         response_model=CartResponse)
def get_cart_endpoint(connection: sqlite3.Connection = Depends(get_db)):
    try:
        return get_cart(connection)
    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Серверная ошибка"
        )


@app.delete("/cart/items/{product_id}",
            status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_items_endpoint(
    product_id: int = Path(gt=0),
    connection: sqlite3.Connection = Depends(get_db)
):
    try:
        remove_product_from_cart(connection, product_id)
    except CartItemNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Серверная ошибка"
        )


@app.patch("/cart/items/{product_id}",
           response_model=CartItemActionResponse
           )
def update_cart_item(
        item: CartItemUpdate,
        product_id: int = Path(gt=0),
        connection: sqlite3.Connection = Depends(get_db)
):
    try:
        return set_cart_item_quantity(
            connection,
            product_id=product_id,
            quantity=item.quantity
        )
    except ProductNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    except CartItemNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товара в корзине нету"
        )

    except InsufficientStockError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Доступно только: {error.available} шт."
        )

    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Серверная ошибка"
        )
