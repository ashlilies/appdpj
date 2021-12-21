from application.Models.Account import *


class Admin(Account):
    def __init__(self, restaurant_name, email, password):
        self.restaurant_name = restaurant_name
        super().__init__(email, password)