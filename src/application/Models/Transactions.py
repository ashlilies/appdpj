# xu yong lin
class Transaction:
    def __init__(self, accounts_ordered_from, option, price, coupons, ratings):
        self.__accounts_ordered_from = accounts_ordered_from
        self.__option = option
        self.__price = float(price)
        self.__coupons = coupons
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

    def set_coupons(self, coupons):
        self.__coupons = coupons

    def get_coupons(self):
        return self.__coupons

    def set_ratings(self, ratings):
        self.__ratings = ratings

    def get_ratings(self):
        return self.__ratings


# account, option, price, coupons, ratings
s = Transaction("yuenloong", "delivery", 10.20, "SPAGETIT", 5)
# s.set_accounts_ordered_from("yuenlong")
# s.set_option("delivery")
# s.set_price(10.20)
# s.set_coupons("SPAGETIT")
# s.set_ratings(5)

k = Transaction("debby", "dinein", 20.20, "SPAGETIT", 1)

