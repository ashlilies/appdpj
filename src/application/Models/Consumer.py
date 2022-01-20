# Ashlee
from application.Models.Account import *
from application.Models.Cart import Cart


class Consumer(Account):
    def __init__(self, first_name, last_name, age: int, email, password):
        super().__init__(email, password)
        self.first_name = first_name
        self.last_name = last_name
        self.age = int(age)
        self.cart = Cart()
