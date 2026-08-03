import sqlite3

# Подключаемся к нашей созданной базе
connection = sqlite3.connect("online_shop.db")
cursor = connection.cursor()

# Подготавливаем список товаров (кортежи внутри списка)
products = [
    ("Куртка", 4500.0, 10),
    ("Носки", 300.0, 50),
    ("Смартфон", 25000.0, 5)
]

initial_products = [
    (
        name,
        price,
        stock,
        name.strip().casefold(),
    )
    for name, price, stock in products
]

# executemany — это крутой метод, который позволяет вставить сразу много строк за один раз
cursor.executemany(
    """
    INSERT INTO product (name, price, stock, name_key) 
    VALUES (?, ?, ?, ?)
    """,
    initial_products)

# Обязательно сохраняем изменения!
connection.commit()
connection.close()

print("Витрина магазина успешно заполнена товарами!")

