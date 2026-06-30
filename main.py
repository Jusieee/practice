while True:
    work_buying = input('Выберите команду (купить/выход): ')
    if work_buying == "выход":
        break
    name = input("Название товара: ")
    cost = float(input("Цена товара: "))
    number = int(input("Количество товара: "))
    summa = cost * number
    print(f"Добрый день, вы приобрели {name}, стоящий {cost} руб. в в количестве:{number}. Ваша стоимость будет {summa} р.")
    if summa >= 3000:
        summa *= 0.9
        print(f"К вам применяется скидка в 10%, теперь ваша цена составляет - {summa} руб.")
    else:
        print(f"Для скидки нужно набрать от 3000 рублей включительно!")

