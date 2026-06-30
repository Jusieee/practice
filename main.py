name = input("Название товара: ")
cost = bool(input("Цена товара: "))
number = int(input("Количество товара: "))
summa = cost * number
print(f"Добрый день, вы приобрели {name}, стоящий {cost} руб. в в количестве:{number}. Ваша стоимость будет {summa} р.")

