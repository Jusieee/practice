import sqlite3


connection = sqlite3.connect(
    "file:online_shop.db?mode=ro",
    uri=True
)

try:
    foreign_keys = connection.execute(
        "PRAGMA foreign_key_list(cart_items)",
    ).fetchall()

    print("Внешние ключи таблиицы cart_items:")
    print(foreign_keys)

finally:
    connection.close()