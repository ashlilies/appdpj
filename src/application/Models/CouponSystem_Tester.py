from CouponSystem import CouponSystem
import datetime

from application.Models.Food import Food

food1 = Food("no_image", "name", "desc", 5.80, "None", ["spec1"], ["topping1"])
food2 = Food("no_image", "name", "desc", 9.80, "None", ["spec1"], ["topping1"])
cs = CouponSystem()
cs.new_coupon("ABC", [food1.get_food_id(), food2.get_food_id()],
              CouponSystem.Discount.PERCENTAGE_OFF,
              0.20, datetime.datetime.today() + datetime.timedelta(days=1))

cs.new_coupon("Coupon3", [food1.get_food_id(), food2.get_food_id()],
              CouponSystem.Discount.FIXED_PRICE,
              0.50, datetime.datetime.today() + datetime.timedelta(days=1))

food2.set_price(100)


coupon_code = input("Enter coupon code to apply: ")
print(cs.discounted_price(food2.get_food_id(), coupon_code))
