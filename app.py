import sqlite3

from fastapi import FastAPI, HTTPException, status, Path

from schemas import Product, CartItemCreate, ProductCreate, ProductUpdate

from database import get_connection

from repositories import delete_product_by_id, get_all_products, get_product_by_id, update_product_by_id


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Добро пожаловать в API нашего интернет-магазина!"}

@app.get("/products", response_model=list[Product])
def get_products():
    products = get_all_products()
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
def create_product(product: ProductCreate):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        product_name = product.name.strip()
        product_name_key = product_name.casefold()

        cursor.execute(
            """
            SELECT id
            from product
            WHERE name_key = ?
            """,
            (product_name_key,),
        )

        existing_product = cursor.fetchone()

        if existing_product is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такой товар уже есть",
            )

        cursor.execute(
            """
            INSERT INTO product (name, price, stock, name_key)
            VALUES (?, ?, ?, ?)
            """,
            (
                product_name,
                product.price,
                product.stock,
                product_name_key,
            ),
        )

        connection.commit()

        return {
            "id": cursor.lastrowid,
            "name": product_name,
            "price": product.price,
            "stock": product.stock,
        }
    except sqlite3.IntegrityError:
        connection.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой товар уже есть"
        )

    except sqlite3.Error:
        connection.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Товар не удалось создать"
        )

    finally:
        connection.close()

@app.post(
    "/cart/items",
    status_code=status.HTTP_201_CREATED,
)
def add_to_cart(item: CartItemCreate):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id, name, stock
            FROM product
            WHERE id = ?
            """,
            (item.product_id,)
        )
        product = cursor.fetchone()

        # Проверка на наличие товара
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден",
            )

        # Проверка наличие товара на складе
        if item.quantity > product["stock"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Доступно {product["stock"]} шт. товара',
            )

        # Добавление товара в корзину
        cursor.execute(
            """
            INSERT INTO cart_items (product_id, quantity)
            VALUES (?, ?)
            """,
            (item.product_id, item.quantity),
        )
        connection.commit()

        return {
            "message": "Товар добавлен",
            "cart_item": {
                "id": cursor.lastrowid,
                "product_id": item.product_id,
                "product_name": product["name"],
                "quantity": item.quantity,
            },
        }
    except sqlite3.Error:
        connection.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе в базе данных"
        )
    finally:
        connection.close()

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int = Path(gt=0)):
    product = get_product_by_id(product_id)

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
def delete_product(product_id: int = Path(gt=0)):
    try:
        deleted = delete_product_by_id(product_id)
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
):

    try:
        updated_product = update_product_by_id(
            product_id=product_id,
            name=product.name,
            price=product.float,
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
        raise  HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Серверная ошибка"
        )