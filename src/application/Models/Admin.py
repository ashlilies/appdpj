# Denotes a single restaurant's account

from application.Models.Account import *
from application.Models.Certification import Certification
from application.Models.CouponSystem import CouponSystem
from application.Models.Restaurant import Restaurant


class Admin(Account):
    def __init__(self, restaurant_name, email, password):
        super().__init__(email, password)  # comes first, so we can abort error
        self.type = "admin"  # for easy rendering in Jinja2
        self.__restaurant_id = None  # set later
        self.__name = None
        self.coupon_system_id = CouponSystem().id
        self.__transaction_system_id = None
        # Certification(self.__restaurant_id)  # doesn't work
        self.set_name(restaurant_name)

        logging.info(("Admin Class: Created new Admin account with "
                      "email=%s, Restaurant obj with restaurant_name=%s, "
                      "account_id=%s")
                     % (self.get_email(), self.__name, self.account_id))

        with shelve.open("accounts", 'c') as db:
            # DO NOT SHORTCUT: db["accounts"][self.account_id] = self XXXXXXXX
            # IT JUST DOESN'T WORK FOR SOME REASON :(
            accounts = db["accounts"]
            accounts[self.account_id] = self
            db["accounts"] = accounts

    def get_name(self):
        with shelve.open("accounts", 'c') as db:
            accounts = db["accounts"]
            account = accounts[self.account_id]
            return account.__name

    def set_name(self, new_name):
        self.__name = new_name

        with shelve.open(ACCOUNT_DB, 'c') as db:
            accounts = db["accounts"]
            accounts[self.account_id] = self
            db["accounts"] = accounts

    @property
    def restaurant_id(self):
        return self.__restaurant_id

    @restaurant_id.setter
    def restaurant_id(self, new_id):
        self.__restaurant_id = new_id

        with shelve.open(ACCOUNT_DB, 'c') as db:
            accounts = db["accounts"]
            accounts[self.account_id] = self
            db["accounts"] = accounts

    @property
    def certification_system_id(self):  # as requested by yonglin
        return self.__restaurant_id

