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

class ShoppingCart:
    def __init__(self):
        self.items = [] # Теперь список товаров живет ВНУТРИ корзины

    def add_product(self, product):
        self.items.append(product) # Метод для добавления товара в корзину

    def get_total_sum(self):
    # Метод, который пробегается по всем товарам в корзине
    # и считает их общую «чистую» стоимость
        total = 0
        for item in self.items:
            total += item.get_total_cost()
        return total

def get_display_price(price):
    if price >= 3000:
        price *= 0.9
        return price
    return price

my_cart = ShoppingCart()

while True:
    work_buying = input('Выберите команду (купить/выход): ')
    if work_buying == "выход":
        print(f"Ваш чек:")
        for item in my_cart.items:
            print(f"{item.name} - {item.price} руб. х {item.quantity} шт")
        final_price = my_cart.get_total_sum()
        display_price = get_display_price(final_price)
        print(f"Ваша общая цена: {display_price} руб")
        break
    elif work_buying == "купить":
        name = input("Название товара: ")
        cost = float(input("Цена товара: "))
        number = int(input("Количество товара: "))
        new_item = Product(name, cost, number)
        my_cart.add_product(new_item)
        current_total = my_cart.get_total_sum()
        display_price = get_display_price(current_total)
        print(f"Добавлен товар {name}, сейчас в корзине набрано на {display_price} руб.")
    else:
        print(f"Неизвестная команда, попробуйте еще раз!")