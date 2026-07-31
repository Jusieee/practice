import sqlite3

from fastapi import FastAPI, HTTPException, status, Path

from schemas import Product, CartItemCreate, ProductCreate


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Добро пожаловать в API нашего интернет-магазина!"}

@app.get("/products", response_model=list[Product])
def get_products():
    connection = sqlite3.connect("online_shop.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    connection.close()
    result = []
    for p in products:
        result.append({
            "id": p[0],
            "name": p[1],
            "price": p[2],
            "stock": p[3]
        })
    return result

@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductCreate):
    connection = sqlite3.connect("online_shop.db")
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id
            from product
            WHERE name = ?
            """,
            (product.name,),
        )

        existing_product = cursor.fetchone()

        if existing_product is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такой товар уже есть",
            )

        cursor.execute(
            """
            INSERT INTO product (name, price, stock)
            VALUES (?, ?, ?)
            """,
            (
                product.name,
                product.price,
                product.stock,
            ),
        )

        connection.commit()

        return {
            "id": cursor.lastrowid,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        }
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
    connection = sqlite3.connect("online_shop.db")
    connection.row_factory = sqlite3.Row
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
    connection = sqlite3.connect("online_shop.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, name, price, stock
        FROM product
        WHERE id = ?
        """,
        (product_id,),
    )
    product = cursor.fetchone()
    connection.close()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )

    return {
        "id": product[0],
        "name": product[1],
        "price": product[2],
        "stock": product[3],
    }