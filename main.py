def get_display_price(price):
    if price >= 3000:
        price *= 0.9
        return price
    return price

cart = []
item = {}
total_sum = 0

while True:
    work_buying = input('Выберите команду (купить/выход): ')
    if work_buying == "выход":
        print(f"Ваш чек:")
        for item in cart:
            print(f"{item['name']} - {item['cost']} руб. х {item['number']} шт")
        if total_sum >= 3000:
            total_sum *= 0.9
            print(f"Ваша общая цена: {total_sum}(скидка 10%)")
        else:
            print(f"Ваша общая цена: {total_sum}")
        break
    elif work_buying == "купить":
        item = {}
        item["name"] = input("Название товара: ")
        item["cost"] = float(input("Цена товара: "))
        item["number"] = int(input("Количество товара: "))
        cart.append(item)
        summa = item["cost"] * item["number"]
        total_sum += summa
        display_price = get_display_price(total_sum)
        print(f"Добавлен товар {item['name']}, сейчас в корзине набрано на {display_price} руб.")
    else:
        print(f"Неизвестная команда, попробуйте еще раз!")