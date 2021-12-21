# xu yong lin
class Transaction:
    def __init__(self, accounts_ordered_from, option, price, coupons, ratings):
        self.accounts_ordered_from = accounts_ordered_from
        self.option = option
        self.price = float(price)
        self.coupons = coupons
        self.ratings = float(ratings)
