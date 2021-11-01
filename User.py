import Account

"""
'User' class inherits 'Account' class

getter and setter method for all User attributes
"""


class User(Account):

    def __init__(self, address, previous_purchases, favourites_list, coupon_list, shopping_cart):
        self.address = address
        self.previous_purchases = previous_purchases
        self.favourites_list = favourites_list
        self.coupon_list = coupon_list
        self.shopping_cart = shopping_cart

    def getAddress(self):
        return self.address

    def setAddress(self, address):
        self.address = address

    def get_previous_purchases(self):
        return self.previous_purchases

    def set_previous_purchases(self, previous_purchases):
        self.previous_purchases = previous_purchases

    def get_favourites_list(self):
        return self.favourites_list

    def set_favourites_list(self, favourites_list):
        self.favourites_list = favourites_list

    def get_coupon_list(self):
        return self.coupon_list

    def set_coupon_list(self, coupon_list):
        self.coupon_list = coupon_list

    def get_shopping_cart(self):
        return self.shopping_cart

    def set_shopping_cart(self, shopping_cart):
        self.shopping_cart = shopping_cart
