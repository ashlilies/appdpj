# Ashlee
# Shopping cart system, to be used in Consumer accounts
import logging
import shelve

from application.Models.CountId import CountId
from application.Models.Food2 import FoodDao

CART_DB = "cart.db"


class Cart:
    count_id = 0

    def __init__(self):
        CountId.load(CART_DB, Cart)
        Cart.count_id += 1
        self.id = Cart.count_id
        CountId.save(CART_DB, Cart)

        self.__item_quantity_dict = {}  # key: item_id, value: quantity

    def add_item(self, item_id: int, quantity: int = 1):
        for i in range(quantity):
            if item_id in self.__item_quantity_dict:
                self.__item_quantity_dict[item_id] += 1
            else:
                self.__item_quantity_dict[item_id] = 1

        CartDao.save(self)

    def remove_item(self, item_id: int, quantity: int = 1):
        if item_id in self.__item_quantity_dict:
            if self.__item_quantity_dict[item_id] > 1:
                self.__item_quantity_dict[item_id] -= quantity
            else:
                self.__item_quantity_dict.pop(item_id)

        CartDao.save(self)

    def get_item_ids(self) -> list:
        item_ids = []
        for item_id in self.__item_quantity_dict:
            item_ids.append(item_id)
        return item_ids

    # Returns a list containing tuple pairs of (FoodObj, qty)
    def get_foods(self) -> list:
        foods = []
        for food_id in self.__item_quantity_dict:
            food = FoodDao.query(food_id)
            qty = self.__item_quantity_dict[food_id]
            if food is not None:
                food_t = (food, qty)
                foods.append(food_t)

        return foods

    def clear_cart(self):
        for item_id in self.__item_quantity_dict:
            self.__item_quantity_dict.pop(item_id)

        CartDao.save(self)


class CartDao:
    @staticmethod
    def create_cart() -> Cart:
        cart = Cart()
        CartDao.save(cart)
        return cart

    @staticmethod
    def get_cart(cart_id) -> Cart:
        cart_dict = {}
        with shelve.open(CART_DB, 'c') as db:
            if "cart" in db:
                cart_dict = db["cart"]

        return cart_dict.get(cart_id)

    @staticmethod
    def save(cart: Cart):
        try:
            with shelve.open(CART_DB, 'c') as db:
                cart_dict = {}
                if "cart" in db:
                    cart_dict = db["cart"]
                cart_dict[cart.id] = cart
                db["cart"] = cart_dict
        except KeyError:
            logging.error("FoodDao: failed to save food dict")
