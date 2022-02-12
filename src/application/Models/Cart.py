# Ashlee
# Shopping cart system, to be used in Consumer accounts
import logging
import shelve

from application.Models.CountId import CountId
from application.Models.CouponSystem import CouponSystem
from application.Models.Food2 import FoodDao
from application.Models.RestaurantSystem import RestaurantSystem

CART_DB = "cart.db"


# LIMITATION: Only 1 coupon code can be applied at the same time.
class CartItem:
    def __init__(self, item_id, qty):
        self.item_id = item_id
        self.qty = qty
        self.coupon_code = None

    def is_discounted(self) -> bool:
        if self.food.price * self.qty == self.price:
            return False
        return True

    @property
    def price(self):
        food = FoodDao.query(self.item_id)

        if self.coupon_code is None:
            return food.price * self.qty

        # get parent restaurant to get coupon system
        cs = CouponSystem.query(RestaurantSystem.find_restaurant_by_id(
            FoodDao.query(self.item_id).parent_restaurant_id).coupon_system_id)
        return cs.discounted_price(self.item_id, self.coupon_code) * self.qty

    @property
    def food(self):  # Returns a food object. DO NOT USE PRICE FROM HERE
        return FoodDao.query(self.item_id)


class Cart:
    count_id = 0

    NOT_SET = 0
    DINE_IN = 1
    DELIVERY = 2

    def __init__(self):
        CountId.load(CART_DB, Cart)
        Cart.count_id += 1
        self.id = Cart.count_id
        CountId.save(CART_DB, Cart)
        self.coupon_code = ""
        self.__mode = Cart.NOT_SET

        self.__item_dict = {}  # key: item_id, value: quantity

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, new_mode):
        self.__mode = new_mode
        CartDao.save(self)

    def add_item(self, item_id: int, quantity: int = 1):
        for i in range(quantity):
            if item_id in self.__item_dict:
                self.__item_dict[item_id].qty += 1
            else:
                self.__item_dict[item_id] = CartItem(item_id, quantity)

        CartDao.save(self)

    def remove_item(self, item_id: int, quantity: int = 1):
        if item_id in self.__item_dict:
            if self.__item_dict[item_id].qty > 1:
                self.__item_dict[item_id].qty -= quantity
            else:
                self.__item_dict.pop(item_id)

        CartDao.save(self)

    def get_item_ids(self) -> list:
        item_ids = []
        for item_id in self.__item_dict:
            item_ids.append(item_id)
        return item_ids

    # Returns a list containing CartItems
    def get_cart_items(self) -> list:
        cart_items = []
        for food_id in self.__item_dict:
            cart_items.append(self.__item_dict[food_id])

        return cart_items

    def clear_cart(self):
        for item_id in self.__item_dict:
            self.__item_dict.pop(item_id)

        CartDao.save(self)

    def apply_coupon(self, coupon_code):
        for item_id in self.__item_dict:
            cart_item = self.__item_dict[item_id]
            cart_item.coupon_code = coupon_code
        self.coupon_code = coupon_code

        CartDao.save(self)

    # For our controller
    def get_total_before_discount(self):
        price = 0.0
        for item_id in self.__item_dict:
            item = self.__item_dict[item_id]
            price += item.food.price * item.qty
        return price

    def get_total_discount(self):
        orig_total = self.get_total_before_discount()
        discount_total = self.get_subtotal()
        return orig_total - discount_total

    def get_subtotal(self):
        price = 0.0
        for item_id in self.__item_dict:
            item = self.__item_dict[item_id]
            price += item.price
        return price

    def is_empty(self):
        if self.get_cart_items() == []:
            return True
        return False


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
