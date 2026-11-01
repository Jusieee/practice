import sqlite3

from pathlib import Path


db_path = Path("online_shop_migration_test_2.db")

if not db_path.is_file():
    raise FileNotFoundError("Копия базы не найдена")

connection = sqlite3.connect(db_path)

try:
    connection.execute("PRAGMA foreign_keys = ON")

    old_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM cart_items
        """
    ).fetchone()[0]

    new_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM cart_items_new
        """
    ).fetchone()[0]

    print("Старая таблица:", old_count)
    print("Новая таблица до переноса", new_count)

    if new_count != 0:
        raise ValueError("Новая таблица уже содержит данные")

    connection.execute("BEGIN")

    connection.execute(
        """
        INSERT INTO cart_items_new (id, product_id, quantity)
        SELECT id, product_id, quantity
        FROM cart_items
        """
    )

    copied_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM cart_items_new
        """
    ).fetchone()[0]

    if copied_count != old_count:
        raise ValueError("Количество записей не совпадает")

    connection.commit()

    print("Новая таблица после переноса:", copied_count)
    print("Перенос успешно завершен")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()