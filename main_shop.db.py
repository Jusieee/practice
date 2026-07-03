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
        print("\n=== ВАШ ЧЕК ===")
        cursor.execute("""
            SELECT product.name, product.price, cart_items.quantity
            FROM cart_items
            JOIN product ON cart_items.product_id = product.id
        """)
        cart_items = cursor.fetchall()
        total_sum = 0
        for item in cart_items:
            name = item[0]
            price = item[1]
            quantity = item[2]
            item_cost = price * quantity
            total_sum += item_cost
            print(f"{name} — {price} руб. х {quantity} шт. = {item_cost} руб.")
        final_price = total_sum
        if total_sum >= 3000:
            final_price = total_sum * 0.9
            print(f"\n🎉 Ура! Вам доступна скидка 10% за заказ от 3000 руб.")
        print(f"Итого к оплате: {final_price} руб.")
        print("=================")
        break
    else:
        print("Неизвестная команда!")