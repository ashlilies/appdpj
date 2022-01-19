# Coupon System
# Ashlee Tan
# Last modified: 11 Jan 2022 11:44
# Recommended use: Create one (1) CouponSystem object per Restaurant class,
#                  then attach it to a Restaurant class attribute.
import datetime
import logging
import shelve

from application.Models.Food import Food


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
        count_id = 0

        def __init__(self,
                     coupon_code: str,
                     food_items_ids: list,
                     discount_type,
                     discount_amount: float,
                     expiry: datetime.datetime):
            with shelve.open("coupons", 'c') as db:
                if "coupon_count_id" in db:
                    CouponSystem.Coupon.count_id = db["coupon_count_id"]

            logging.info("CouponSystem.Coupon: current count id: %d"
                         % CouponSystem.Coupon.count_id)
            self.id = CouponSystem.Coupon.count_id
            self.coupon_code = coupon_code
            self.food_items = food_items_ids
            self.discount = CouponSystem.Discount(discount_type,
                                                  discount_amount)
            self.expiry = expiry
            self.enabled = True

            CouponSystem.Coupon.count_id += 1
            with shelve.open("coupons", 'c') as db:
                db["coupon_count_id"] = CouponSystem.Coupon.count_id

        def discounted_price(self, food_id: int, coupon_code: str):
            # Get food item
            food = Food.query(food_id)

            if not self.enabled:  # artifically cancelled coupon
                return None
            if datetime.datetime.now() > self.expiry:  # expired already
                self.enabled = False  # disable it for convenience's sake
                return None

            if coupon_code == self.coupon_code:  # coupon code match?
                if food in self.food_items:  # does it apply to this item?
                    return self.discount.discounted_price(food.get_price())
            return None  # if doesn't apply, return None

    def __init__(self):
        with shelve.open("coupons", 'c') as db:
            if "count_id" in db:
                CouponSystem.count_id = db["count_id"]

        CouponSystem.count_id += 1
        self.id = CouponSystem.count_id
        self.coupons = {}

        with shelve.open("coupons", 'c') as db:
            db["count_id"] = CouponSystem.count_id
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
    def get_coupons(self, food_id: int=None) -> list:
        coupon_list = []
        for coupon_code in self.coupons:
            coupon = self.coupons[coupon_code]
            if food_id is None or food_id in coupon.food_items:
                coupon_list.append(coupon)
        return coupon_list

    def edit_coupon(self, coupon_code: str, food_items: list, discount_type,
                    discount_amount: float, expiry: datetime.datetime,
                    enabled_status: bool):
        coupon = self.coupons[coupon_code]
        self.coupons[coupon_code] = CouponSystem.Coupon(coupon_code, food_items,
                                                        discount_type,
                                                        discount_amount, expiry)
        coupon.coupon_code = coupon_code
        coupon.food_items = food_items
        coupon.discount = CouponSystem.Discount(discount_type, discount_amount)
        coupon.expiry = expiry
        coupon.enabled = enabled_status

        with shelve.open("coupons", 'c') as db:  # save back coupon system
            coupon_systems_dict = {}
            if "coupon_systems_dict" in db:
                coupon_systems_dict = db["coupon_systems_dict"]

            coupon_systems_dict[self.id] = self
            db["coupon_systems_dict"] = coupon_systems_dict

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
        food = Food.query(food_id)
        if food is None:
            logging.error("CS: Failed to get discounted price for food-id %s" % food_id)
            return -1

        if coupon_code in self.coupons:
            coupon = self.coupons[coupon_code]
            if not coupon.enabled:
                return food.get_price()

            if not food_id in coupon.food_items:
                return food.get_price()

            after_discount = coupon.discount.discounted_price(food.get_price())
            if after_discount is not None:
                return after_discount
        return food.get_price()  # can't find matching discount return original price

    # Query database and return a CouponSystem, or None if not found
    @staticmethod
    def query(coupon_system_id: int) -> "CouponSystem" or None:
        with shelve.open("coupons", 'c') as db:
            if "coupon_systems_dict" in db:
                coupon_systems_dict = db["coupon_systems_dict"]
                return coupon_systems_dict.get(coupon_system_id, None)
        return None