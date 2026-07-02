cart = []
total_sum = 0

while True:
    work_buying = input('Выберите команду (купить/выход): ')
    if work_buying == "выход":
        print(f"Вы приобрели {cart}, стоимость товаров вышла :{total_sum} руб.")
        break
    elif work_buying == "купить":
        name = input("Название товара: ")
        cost = float(input("Цена товара: "))
        number = int(input("Количество товара: "))
        cart.append(name)
        total_sum += cost * number
        if total_sum >= 3000:
            total_sum *= 0.9
            print(f"Товар {name}, добавлен в корзину, вам доступна скидка 10% Ваша итоговая цена сейчас составляет: "
                f"{total_sum}")
        else:
            print(f"Товар {name}, добавлен в корзину, Для получение скидки, наберите корзину на 3000 рублей! Ваша "
                    f"итоговая цена сейчас составляет: {total_sum}")
    else:
    print(f"Неизвестная команда, попробуйте еще раз!")