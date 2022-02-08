# Ashlee
from application.Models.Account import *
from application.Models.Cart import Cart, CartDao


class Consumer(Account):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(email, password)
        self.type = "consumer"
        self.first_name = first_name
        self.last_name = last_name
        # self.age = int(age)  # To be implemented later, not for MVP
        self.cart = CartDao.create_cart().id
        self.save()

        logging.info("Consumer: created new account with email %s" % email)

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

