cart = []
item = {}
total_sum = 0

while True:
    work_buying = input('Выберите команду (купить/выход): ')
    if work_buying == "выход":
        print(f"Ваш чек:")
        for item in cart:
            print(f"{item["name"]} - {item["cost"]} руб. х {item["number"]} шт")
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
        if total_sum >= 3000:
            display_cost = total_sum * 0.9
            print(f"Товар {item["name"]}, добавлен в корзину, вам доступна скидка 10% Ваша итоговая цена сейчас "
                  f"составляет:{display_cost}")
        else:
            display_cost = total_sum
            print(f"Товар {item["name"]}, добавлен в корзину, Для получение скидки, наберите корзину на 3000 рублей! "
                  f"Ваша итоговая цена сейчас составляет: {display_cost}")
    else:
        print(f"Неизвестная команда, попробуйте еще раз!")