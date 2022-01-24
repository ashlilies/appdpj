# Clara
import logging
import shelve


class Food:
    count_id = 0

    def __init__(self, image, name, description, price, allergy,
                 specification=None, topping=None):
        with shelve.open("food", 'c') as db:
            if "food_count_id" in db:
                Food.count_id = db["food_count_id"]
        logging.info("Food: food count food_id loaded: %d" % Food.count_id)

        Food.count_id += 1

        self.__food_id = Food.count_id
        self.__image = image
        self.__name = name
        self.__description = description
        self.__price = price
        self.__allergy = allergy
        self.__specification = specification
        self.__topping = topping

        # Done by Ashlee - database access in Models not Controller
        with shelve.open("food", 'c') as db:
            db["food_count_id"] = Food.count_id
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]

            food_dict[self.__food_id] = self
            db["food"] = food_dict

    def get_food_id(self):
        return self.__food_id

    def set_food_id(self, food_id):  # why do you need this though? -ash
        with shelve.open("food", 'c') as db:
            if "food" in db:
                food_dict = db["food"]
                food_dict.pop(self.__food_id)

        self.__food_id = food_id

        with shelve.open("food", 'c') as db:
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]
            food_dict[self.__food_id] = self
            db["food"] = food_dict

    def set_name(self, name):
        self.__name = name

        with shelve.open("food", 'c') as db:
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]
            food_dict[self.__food_id] = self
            db["food"] = food_dict

    def get_name(self):
        return self.__name

    def set_description(self, description):
        self.__description = description

        with shelve.open("food", 'c') as db:
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]
            food_dict[self.__food_id] = self
            db["food"] = food_dict

    def get_description(self):
        return self.__description

    def set_price(self, price):
        self.__price = price
        with shelve.open("food", 'c') as db:
            food_dict = db["food"]
            food_dict[self.get_food_id()] = self
            db["food"] = food_dict

    def get_price(self):
        return self.__price

    def set_allergy(self, allergy):
        self.__allergy = allergy
        with shelve.open("food", 'c') as db:
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]
            food_dict[self.__food_id] = self
            db["food"] = food_dict

    def get_allergy(self):
        return self.__allergy

    def get_specification(self):
        return self.__specification

    def set_specification(self, specification):
        self.__specification = specification
        with shelve.open("food", 'c') as db:
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]
            food_dict[self.__food_id] = self
            db["food"] = food_dict

    def get_topping(self):
        return self.__topping

    def set_topping(self, topping):
        self.__topping = topping
        with shelve.open("food", 'c') as db:
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]
            food_dict[self.__food_id] = self
            db["food"] = food_dict

    # Get the image as a file?
    def get_image(self):
        return self.__image

    # Set the image as a file?
    def set_image(self, image):
        self.__image = image
        with shelve.open("food", 'c') as db:
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]
            food_dict[self.__food_id] = self
            db["food"] = food_dict

    # query db for a food item by passing in the food_id - added by ashlee
    @staticmethod
    def query(food_id: int) -> "Food" or None:
        try:
            with shelve.open("food", 'c') as db:
                foods = db["food"]
                return foods[food_id]

        except KeyError:
            logging.error("Food: tried to query food_id %s but not found" % food_id)
            return None
