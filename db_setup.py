import sqlite3

connection = sqlite3.connect("online_shop.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS product(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
price REAL NOT NULL,
stock INTEGER DEFAULT 0,
name_key TEXT NOT NULL UNIQUE
)
""")

cursor.execute('''
CREATE TABLE IF NOT EXISTS cart_items(
id INTEGER PRIMARY KEY AUTOINCREMENT,
product_id INTEGER,
quantity INTEGER DEFAULT 0
)
''')

cursor.execute(
    """
    SELECT product_id, COUNT(*)
    FROM cart_items
    GROUP BY product_id
    HAVING COUNT(*) > 1
    """
)

dublicates = cursor.fetchall()
# print(dublicates)

cursor.execute(
    """
    DELETE FROM cart_items
    """
)

cursor.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_cart_items_product_id
    ON cart_items(product_id)
    """
)

connection.commit()
connection.close()

print("База данных и таблица успешно настроены!")