import sqlite3

from pathlib import Path


db_path = Path("online_shop_migration_test.db")

if not db_path.is_file():
    raise FileNotFoundError("Копия базы не найдена")

connection = sqlite3.connect(db_path)

try:
    connection.execute("PRAGMA foreign_keys = ON")

    connection.execute("BEGIN")

    connection.execute(
        """
        CREATE TABLE cart_items_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 0,
            FOREIGN KEY (product_id)
                REFERENCES product(id)
                ON DELETE CASCADE
        )    
        """
    )

    connection.commit()
    print("Новая таблица создана!")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()
