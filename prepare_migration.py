import sqlite3

from pathlib import Path


source_path = Path("online_shop.db")
backup_path = Path("online_shop_migration_test_2.db")

if not source_path.is_file():
    raise FileNotFoundError("Основная база не найдена")

if backup_path.exists():
    raise FileExistsError("Тестовая копия уже существует")

source = sqlite3.connect(
    f"file:{source_path.resolve().as_posix()}?mode=ro",
    uri=True
)
backup = sqlite3.connect(backup_path)

try:
    source.backup(backup)
finally:
    source.close()
    backup.close()

print("Резервная копия создана!")


connection = sqlite3.connect(backup_path)
connection.row_factory = sqlite3.Row

try:
    product_count = connection.execute(
        "SELECT COUNT(*) FROM product"
    ).fetchone()[0]

    cart_count = connection.execute(
        "SELECT COUNT(*) FROM cart_items"
    ).fetchone()[0]

    orphan_rows = connection.execute(
        """
        SELECT c.id, c.product_id, c.quantity
        FROM cart_items AS c
        LEFT JOIN product AS p
            ON c.product_id = p.id
        WHERE p.id IS NULL
        """
    ).fetchall()

    print("Всего товаров:", product_count)
    print("Записей в корзине:", cart_count)
    print("Некорректных записей:", len(orphan_rows))

    for row in orphan_rows:
        print(dict(row))

finally:
    connection.close()