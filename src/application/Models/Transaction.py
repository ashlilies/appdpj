# xu yong lin
import logging

from application.Models.Account import Account


# yet to include this part in python
class Transaction:
    transaction_no = 0  # counts the number of transactions in the restaurant per month

    def __init__(self, transaction_no=0, option=None, price=0, used_coupons=None,
                 ratings=0):
        self.transaction_no = transaction_no
        self.__account_id = Account.count_id
        self.__option = option
        self.__price = float(price)
        self.__used_coupons = used_coupons
        self.__ratings = int(ratings)

    def set_account_id(self, accounts):
        self.__account_id = str(accounts)

    def get_account_id(self):
        return self.__account_id

    def set_option(self, option):
        self.__option = option

    def get_option(self):
        return self.__option

    def set_price(self, price):
        self.__price = price

    def get_price(self):
        return self.__price

    def set_used_coupons(self, used_coupons):
        self.__used_coupons = used_coupons

    def get_used_coupons(self):
        return self.__used_coupons

    def set_ratings(self, ratings):
        if ratings >= 5:
            print("rating is above 5! Please double check with customer")
        else:
            self.__ratings = ratings

    def get_ratings(self):
        return self.__ratings

