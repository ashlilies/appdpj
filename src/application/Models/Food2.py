# Ashlee
import logging
import shelve

FOOD_DB = "food.db"


class Food:
    count_id = 0

    def __init__(self, restaurant_id, name, image, description, price, allergy,
                 specification=None, topping=None):
        with shelve.open(FOOD_DB, 'c') as db:
            if "count_id" in db:
                Food.count_id = db["count_id"]
                logging.info("Food: food count food_id loaded: %d" % Food.count_id)

        Food.count_id += 1
        self.id = Food.count_id
        self.name = name
        self.image = image  # stores the static path
        self.description = description
        self.price = price
        self.allergy = allergy
        self.specifications = specification
        self.toppings = topping
        self.parent_restaurant_id = restaurant_id

        with shelve.open(FOOD_DB, 'c') as db:
            db["count_id"] = Food.count_id


class FoodDao:
    @staticmethod
    def create_food(restaurant_id: str, name: str, image: str, description: str, price: float, allergy: str,
                    specifications: list, toppings: list):
        food = Food(restaurant_id, name, image, description, price, allergy, specifications, toppings)
        FoodDao.save(food)

    @staticmethod
    def update_food(food_id, name, image_path, description, price, allergy, specification, topping):
        food = FoodDao.query(food_id)
        if food is None:
            raise FoodIdNotExistsError

        food.name = name
        food.image_path = image_path
        food.description = description
        food.price = price
        food.allergy = allergy
        food.specification = specification
        food.topping = topping
        FoodDao.save(food)

    # Hard delete food items
    @staticmethod
    def delete_food(food_id):
        try:
            with shelve.open(FOOD_DB, 'c') as db:
                food_dict = db["food"]
                food_dict.pop(food_id)
                db["food"] = food_dict
        except KeyError:
            logging.error("FoodDao: Failed to delete food item")

    @staticmethod
    def get_foods(restaurant_id):
        # Linear search and retun a list of food objects with matching restaurant ID
        food_list = []

        food_dict = {}
        with shelve.open(FOOD_DB, 'c') as db:
            if "food" in db:
                food_dict = db["food"]

        for k in food_dict:
            food = food_dict[k]
            if food.parent_restaurant_id == restaurant_id:
                food_list.append(food)

        return food_list

    @staticmethod
    def save(food: Food):
        try:
            with shelve.open(FOOD_DB, 'c') as db:
                food_dict = {}
                if "food" in db:
                    food_dict = db["food"]
                food_dict[food.id] = food
                db["food"] = food_dict
        except KeyError:
            logging.error("FoodDao: failed to save food dict")

    @staticmethod
    def query(food_id: int) -> "Food" or None:
        try:
            with shelve.open(FOOD_DB, 'c') as db:
                if "food" in db:
                    food_dict = db["food"]
                    return food_dict[food_id]

        except KeyError:
            logging.error("Food: tried to query food_id %s but not found" % food_id)

        return None


class FoodIdNotExistsError(Exception):
    pass
