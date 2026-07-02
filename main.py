class Product:
# __init__ — это специальный метод (конструктор).
# Он вызывается автоматически, когда мы создаем новый товар.
    def __init__(self, name, price, quantity):
        self.name = name # Свойство объекта (атрибут)
        self.price = price # Свойство объекта
        self.quantity = quantity # Свойство объекта

    # Мы можем встроить функцию (метод) прямо внутрь класса!
    def get_total_cost(self):
        return self.price * self.quantity

def get_display_price(price):
    if price >= 3000:
        price *= 0.9
        return price
    return price

cart = []
total_sum = 0

while True:
    work_buying = input('Выберите команду (купить/выход): ')
    if work_buying == "выход":
        print(f"Ваш чек:")
        for item in cart:
            print(f"{item.name} - {item.price} руб. х {item.quantity} шт")
        final_price = get_display_price(total_sum)
        print(f"Ваша общая цена: {final_price} руб")
        break
    elif work_buying == "купить":
        name = input("Название товара: ")
        cost = float(input("Цена товара: "))
        number = int(input("Количество товара: "))
        new_item = Product(name, cost, number)
        cart.append(new_item)
        total_sum += new_item.get_total_cost()
        display_price = get_display_price(total_sum)
        print(f"Добавлен товар {name}, сейчас в корзине набрано на {display_price} руб.")
    else:
        print(f"Неизвестная команда, попробуйте еще раз!")