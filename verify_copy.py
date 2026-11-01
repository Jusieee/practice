import sqlite3

from pathlib import Path


db_path = Path("online_shop_migration_test_2.db")

if not db_path.is_file():
    raise FileNotFoundError("База не найдена")

connection = sqlite3.connect(
    f"file:{db_path.resolve().as_posix()}?mede=ro",
    uri=True
)

try:
    old_rows = connection.execute(
        """
        SELECT id, product_id, quantity
        FROM cart_items
        ORDER BY id
        """
    ).fetchall()

    new_rows = connection.execute(
        """
        SELECT id, product_id, quantity
        FROM cart_items_new
        ORDER BY id
        """
    ).fetchall()

    print("Старые записи:", old_rows)
    print("Новые записи:", new_rows)

    if old_rows != new_rows:
        raise ValueError("Данные таблиц не совпадают")

    print("Проверка успешна! Данные совпадают")

finally:
    connection.close()