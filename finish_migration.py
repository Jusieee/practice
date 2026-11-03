import sqlite3

from pathlib import Path


db_path = Path("online_shop_migration_test_2.db")

if not db_path.is_file():
    raise FileNotFoundError("Тестовая копия не найдена")

connection = sqlite3.connect(db_path)

try:
    connection.execute("PRAGMA foreign_keys = off")
    connection.execute("BEGIN")

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

    if old_rows != new_rows:
        raise ValueError("Данные таблиц различаются")

    foreign_keys = connection.execute(
        "PRAGMA foreign_key_list(cart_items_new)"
    ).fetchall()

    if not any(row[2] == "product" for row in foreign_keys):
        raise ValueError("Внешний ключ не найден")

    connection.execute("DROP TABLE cart_items")

    connection.execute(
        """
        ALTER TABLE cart_items_new
        RENAME TO cart_items
        """
    )

    connection.execute(
        """
        CREATE UNIQUE INDEX idx_cart_items_product_id
        ON cart_items(product_id)
        """
    )

    violations = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    if violations:
        raise ValueError("Нарушена ссылочная целостность")

    connection.commit()
    print("Миграция успешно завершена!")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()