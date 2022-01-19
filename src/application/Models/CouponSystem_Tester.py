from CouponSystem import CouponSystem
import datetime

from application.Models.Food import Food

food1 = Food("no_image", "name", "desc", 5.80, "None", ["spec1"], ["topping1"])
food2 = Food("no_image", "name", "desc", 9.80, "None", ["spec1"], ["topping1"])
cs = CouponSystem()
cs.new_coupon("ABC", [food1.get_food_id(), food2.get_food_id()],
              CouponSystem.Discount.PERCENTAGE_OFF,
              0.20, datetime.datetime.today() + datetime.timedelta(days=1))

print(cs.discounted_price(food2.get_food_id(), "ABC"))
