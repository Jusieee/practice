import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
class CartItemCreate(BaseModel):
    product_id: int = Field(
        gt = 0,
        description = "ID товара",
    )
    quantity: int = Field(
        gt = 0,
        description = "Количество товара",
    )

@app.get("/")
def home():
    return {"message": "Добро пожаловать в API нашего интернет-магазина!"}

@app.get("/products")
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