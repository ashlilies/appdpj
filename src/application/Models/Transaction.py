# xu yong lin

class Transaction:
    def __init__(self, accounts_ordered_from, option, price, used_coupons,
                 ratings):
        self.__accounts_ordered_from = accounts_ordered_from
        self.__option = option
        self.__price = float(price)
        self.__used_coupons = used_coupons
        self.__ratings = float(ratings)

    def set_accounts_ordered_from(self, accounts):
        self.__accounts_ordered_from = accounts

    def get_accounts_ordered_from(self):
        return self.__accounts_ordered_from

    def set_option(self, option):
        self.__option = option

    def get_option(self):
        return self.__option

    def set_price(self, price):
        self.__accounts_ordered_from = price

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
