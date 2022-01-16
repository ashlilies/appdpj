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
                     food_items: list,
                     discount_type,
                     discount_amount: float,
                     expiry: datetime.datetime):
            with shelve.open("coupon", 'c') as db:
                if "coupon_count_id" in db:
                    CouponSystem.Coupon.count_id = db["coupon_count_id"]

            logging.info("CouponSystem.Coupon: current count id: %d"
                         % CouponSystem.Coupon.count_id)
            self.id = CouponSystem.Coupon.count_id
            self.coupon_code = coupon_code
            self.food_items = food_items
            self.discount = CouponSystem.Discount(discount_type,
                                                  discount_amount)
            self.expiry = expiry
            self.enabled = True

            CouponSystem.Coupon.count_id += 1
            with shelve.open("coupon", 'c') as db:
                db["coupon_count_id"] = CouponSystem.Coupon.count_id

        def discounted_price(self, food: Food, coupon_code: str):
            if not self.enabled:  # artifically cancelled coupon
                return None
            if datetime.datetime.now() > self.expiry:  # expired already
                return None

            if coupon_code == self.coupon_code:  # coupon code match?
                if food in self.food_items:  # does it apply to this item?
                    return self.discount.discounted_price(food.price)
            return None  # if doesn't apply, return None

    def __init__(self):
        self.list_of_coupons = []

    def new_coupon(self,
                   coupon_code: str,
                   food_items: list,
                   discount_type,
                   discount_amount: float,
                   expiry: datetime.datetime):
        self.list_of_coupons.append(CouponSystem.Coupon(coupon_code,
                                                        food_items,
                                                        discount_type,
                                                        discount_amount,
                                                        expiry))

    def discounted_price(self, food: Food, coupon_code: str):
        for coupon in self.list_of_coupons:
            after_discount = coupon.discount.discounted_price(food, coupon_code)
            if after_discount is not None:
                return after_discount
        return food.price  # can't find matching discount return original price
