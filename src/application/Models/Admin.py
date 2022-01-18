# Denotes a single restaurant's account

from application.Models.Account import *
from application.Models.Restaurant import Restaurant



class Admin(Account):
    def __init__(self, restaurant_name, email, password):
        super().__init__(email, password)  # comes first, so we can abort error
        self.restaurant_id = None  # set later
        self.name = restaurant_name

        logging.info(("Admin Class: Created new Admin account with "
                      "email=%s, Restaurant obj with restaurant_name=%s, "
                      "account_id=%s")
                     % (self.get_email(), self.name, self.account_id))

        with shelve.open("accounts", 'c') as db:
            accounts_dict = db["accounts"]
            accounts_dict[self.account_id] = self

    def set_name(self, new_name):
        self.name = new_name

        with shelve.open(ACCOUNT_DB, 'c') as db:
            accounts = db["accounts"]
            accounts[self.account_id] = self
