import getpass
import psycopg


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

        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        for product in products:
            print(product)