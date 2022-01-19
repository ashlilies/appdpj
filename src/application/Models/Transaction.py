# xu yong lin
import logging
import shelve

from application import DB_NAME


class Transaction:
    transaction_id = 1
    food_coupons = ['SPAGETIT', '50PASTA']

    def __init__(self, account_name=None, option=None, price=0, used_coupons=None,
                 ratings=0):

        with shelve.open('transaction', 'c') as db:
            try:
                Transaction.transaction_id = db['transaction_id_count']
            except Exception as e:
                logging.info("transaction_id_count: error reading from db (%s)" % e)
        self.count_id = Transaction.transaction_id
        self.account_name = account_name
        self.__option = option
        self.__price = price
        self.__used_coupons = used_coupons
        self.__ratings = ratings
        self.deleted = False
        Transaction.transaction_id += 1
        # writeback
        with shelve.open('transaction', 'c') as db:
            db['transaction_id_count'] = Transaction.transaction_id

    def set_option(self, option):
        self.__option = option

    def get_option(self):
        return self.__option

    # price must be in 2 dp, can only accept numbers
    def set_price(self, price):
        try:
            if price == float(price):
                self.__price = price
        except:
            self.deleted = True

    def get_price(self):
        return self.__price

    def set_used_coupons(self, used_coupons):
        if used_coupons in Transaction.food_coupons:
            self.__used_coupons = used_coupons
        else:
            self.__used_coupons = 'NIL'

    def get_used_coupons(self):
        return self.__used_coupons

    # ratings must be in 2 dp, can only accept numbers
    def set_ratings(self, ratings):
        try:
            if ratings == int(ratings):
                self.__ratings = ratings
        except:
            self.deleted = True

    def get_ratings(self):
        return self.__ratings
