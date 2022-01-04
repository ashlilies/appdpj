# xu yong lin
# yet to include this part in python
class Transaction:

    def __init__(self, account_id=None, option=None, price=0, used_coupons=None,
                 ratings=0):
        self.account_id = account_id
        self.__option = option
        self.__price = float(price)
        self.__used_coupons = used_coupons
        self.__ratings = int(ratings)

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
        self.__ratings = ratings

    def get_ratings(self):
        return self.__ratings

