import sqlite3

connection = sqlite3.connect("online_shop.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM product")
product = cursor.fetchall()

for item in product:
    print(item)

connection.close()