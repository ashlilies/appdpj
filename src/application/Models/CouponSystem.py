# Coupon System
# Ashlee Tan
# Last modified: 11 Jan 2022 11:44
# Recommended use: Create one (1) CouponSystem object per Restaurant class,
#                  then attach it to a Restaurant class attribute.
import datetime
import logging
import shelve

from application.Models.Food2 import FoodIdNotExistsError, FoodDao


class CouponSystem:
    count_id = 0

    class Discount:
        FIXED_PRICE = 0
        PERCENTAGE_OFF = 1

        def __init__(self, discount_type: int, discount_amount: float):
            self.discount_type = discount_type
            self.discount_amount = discount_amount  # 7%: 0.07

        @property
        def multiplier(self):
            if self.discount_type == self.__class__.PERCENTAGE_OFF:
                return 1.00 - self.discount_amount
            return None  # not possible to have multiplier with fixed prices

        def discounted_price(self, original_price):
            if self.discount_type == self.__class__.FIXED_PRICE:
                return self.discount_amount
            elif self.discount_type == self.__class__.PERCENTAGE_OFF:
                return original_price * self.multiplier

    class Coupon:
        def __init__(self,
                     coupon_code: str,
                     food_items_ids: list,
                     discount_type,
                     discount_amount: float,
                     expiry: datetime.datetime):
            self.coupon_code = coupon_code
            self.food_items = food_items_ids
            self.discount = CouponSystem.Discount(discount_type,
                                                  discount_amount)
            self.expiry = expiry
            self.enabled = True

        def discounted_price(self, food_id: int, coupon_code: str):
            # Get food item
            food = FoodDao.query(food_id)

            if not self.enabled:  # artifically cancelled coupon
                return None
            if datetime.datetime.now() > self.expiry:  # expired already
                self.enabled = False  # disable it for convenience's sake
                return None

            if coupon_code == self.coupon_code:  # coupon code match?
                if food in self.food_items:  # does it apply to this item?
                    return self.discount.discounted_price(food.price)
            return None  # if doesn't apply, return None

    DISCOUNT_FIXED_PRICE = Discount.FIXED_PRICE
    DISCOUNT_PERCENTAGE_OFF = Discount.PERCENTAGE_OFF

    def __init__(self):
        with shelve.open("coupons", 'c') as db:
            if "id" in db:
                CouponSystem.count_id = db["id"]

        CouponSystem.count_id += 1
        self.id = CouponSystem.count_id
        self.coupons = {}

        with shelve.open("coupons", 'c') as db:
            db["id"] = CouponSystem.count_id
            coupon_systems_dict = {}
            if "coupon_systems_dict" in db:
                coupon_systems_dict = db["coupon_systems_dict"]

            # shelve databases don't accept int keys - only python dicts
            coupon_systems_dict[self.id] = self
            db["coupon_systems_dict"] = coupon_systems_dict

    def new_coupon(self, coupon_code: str, food_ids: list, discount_type,
                   discount_amount: float, expiry: datetime.datetime):
        self.coupons[coupon_code] = CouponSystem.Coupon(coupon_code, food_ids,
                                                        discount_type,
                                                        discount_amount, expiry)

        with shelve.open("coupons", 'c') as db:  # save back coupon system
            coupon_systems_dict = {}
            if "coupon_systems_dict" in db:
                coupon_systems_dict = db["coupon_systems_dict"]

            coupon_systems_dict[self.id] = self
            db["coupon_systems_dict"] = coupon_systems_dict

    # Get all applicable coupons for a food_id.
    # If food_id not supplied, get all coupons for this system.
    def get_coupons(self, food_id: int = None) -> list:
        coupon_list = []
        for coupon_code in self.coupons:
            coupon = self.coupons[coupon_code]
            if (food_id is None or food_id in coupon.food_items) and coupon.enabled:
                coupon_list.append(coupon)
        return coupon_list

    # Get one specific coupon object by supplying its code, None if not found
    def get_coupon(self, code) -> "Coupon" or None:
        coupon = self.coupons.get(code)
        if coupon is None or not coupon.enabled:
            return None
        return coupon

    def edit_coupon(self, old_coupon_code: str, new_coupon_code: str,
                    food_items: list, discount_type,
                    discount_amount: float, expiry: datetime.datetime):
        self.coupons.pop(old_coupon_code)
        self.coupons[new_coupon_code] = CouponSystem.Coupon(new_coupon_code, food_items,
                                                            discount_type,
                                                            discount_amount, expiry)
        coupon = self.coupons[new_coupon_code]
        coupon.coupon_code = new_coupon_code
        coupon.food_items = food_items
        coupon.discount = CouponSystem.Discount(discount_type, discount_amount)
        coupon.expiry = expiry
        coupon.enabled = True  # not yet implemented

        with shelve.open("coupons", 'c') as db:  # save back coupon system
            coupon_systems_dict = {}
            if "coupon_systems_dict" in db:
                coupon_systems_dict = db["coupon_systems_dict"]

            coupon_systems_dict[self.id] = self
            db["coupon_systems_dict"] = coupon_systems_dict

    # Soft-delete coupons; set enabled to False
    def delete_coupon(self, coupon_code: str):
        if coupon_code in self.coupons:
            coupon = self.coupons[coupon_code]
            coupon.enabled = False

        with shelve.open("coupons", 'c') as db:  # save back coupon system
            coupon_systems_dict = {}
            if "coupon_systems_dict" in db:
                coupon_systems_dict = db["coupon_systems_dict"]

            coupon_systems_dict[self.id] = self
            db["coupon_systems_dict"] = coupon_systems_dict

    def discounted_price(self, food_id: int, coupon_code: str):
        food = FoodDao.query(food_id)

        if food is None:
            logging.error("CS: Failed to get discounted price for food-id %s" % food_id)
            raise FoodIdNotExistsError

        if coupon_code in self.coupons:
            coupon = self.coupons[coupon_code]
            if not coupon.enabled:
                return food.price

            if food_id not in coupon.food_items:
                return food.price

            if datetime.date.today() > coupon.expiry:  # expired already
                coupon.enabled = False  # disable it for convenience's sake
                return food.price

            after_discount = coupon.discount.discounted_price(food.price)
            if after_discount is not None:
                return after_discount
        return food.price  # can't find matching discount return original price

    # Query database and return a CouponSystem, or None if not found
    @staticmethod
    def query(coupon_system_id: int) -> "CouponSystem" or None:
        with shelve.open("coupons", 'c') as db:
            if "coupon_systems_dict" in db:
                coupon_systems_dict = db["coupon_systems_dict"]
                return coupon_systems_dict.get(coupon_system_id, None)
        return None
