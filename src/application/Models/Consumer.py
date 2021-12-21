from application.Models.Account import *


class Consumer(Account):
    def __init__(self, first_name, last_name, age: int, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.age = int(age)
        super().__init__(email, password)
