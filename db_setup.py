import sqlite3

connection = sqlite3.connect("online_shop.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS product(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
price REAL NOT NULL,
stock INTEGER DEFAULT 0
)
""")

cursor.execute('''
CREATE TABLE IF NOT EXISTS cart_items(
id INTEGER PRIMARY KEY AUTOINCREMENT,
product_id INTEGER,
quantity INTEGER DEFAULT 0
)
''')

connection.commit()
connection.close()

print("База данных и таблица успешно настроены!")