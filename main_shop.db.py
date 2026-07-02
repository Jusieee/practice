import sqlite3

connection = sqlite3.connect("online_shop.db")
cursor = connection.cursor()

print("--- Добро пожаловать в наш цифровой магазин! ---")

while True:
    work_buying = input("\nВведите команду (купить/выход): ")
    if work_buying == "купить":
        print("\nДоступные товары:")
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        for p in products:
            print(f"ID: {p[0]} | {p[1]} — {p[2]} руб. (Остаток: {p[3]} шт.)")
        prod_id = int(input("\nВведите ID товара, который хотите купить: "))
        count = int(input("Количество: "))
        cursor.execute("INSERT INTO cart_items (product_id, quantity) VALUES (?, ?)", (prod_id, count))
        connection.commit()
        print("Товар успешно добавлен в вашу корзину!")
    elif work_buying == "выход":
        print("\nВаш чек: ")
        cursor.execute("SELECT * FROM cart_items")
        cart_item = cursor.fetchall()
        for cart in cart_item:
            print(cart)
        break
    else:
        print("Неизвестная команда!")