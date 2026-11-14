import getpass
import psycopg


product_id = 2
password = getpass.getpass("Пароль PostgreSQL: ")

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="online_shop_pg",
    user="postgres",
    password=password
) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database()")
        result = cursor.fetchone()
        print("Текущая база: ", result[0])

        cursor.execute(
            """
            SELECT *
            FROM product
            WHERE id = %s
            """,
            (product_id,)
        )
        product = cursor.fetchone()

        if product is None:
            print("Товар не найден")
        else:
            print("Найден товар: ", product)