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
        logging.info("Food: food count id loaded: %d" % Food.count_id)

        Food.count_id += 1
        self.__food_id = Food.count_id
        self.__image = image
        self.name = name
        self.description = description
        self.price = price
        self.allergy = allergy
        self.specification = specification
        self.topping = topping

        # Done by Ashlee - database access in Models not Controller
        with shelve.open("food", 'c') as db:
            db["food_count_id"] = Food.count_id
            food_dict = {}
            if "food" in db:
                food_dict = db["food"]

            food_dict[str(self.__food_id)] = self
            db["food"] = food_dict



    def get_food_id(self):
        return self.__food_id

    def set_food_id(self, food_id):
        self.__food_id = food_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    def set_allergy(self, allergy):
        self.allergy = allergy

    def get_allergy(self):
        return self.allergy

    def get_specification(self):
        return self.specification

    def get_topping(self):
        return self.topping

    # Get the image as a file?
    def get_image(self):
        return self.__image

    # Set the image as a file?
    def set_image(self, image):
        self.__image = image

    # query db for a food item by passing in the id - added by ashlee
    @staticmethod
    def query(id: int) -> "Food" or None:
        try:
            with shelve.open("food", 'c') as db:
                foods = db["food"]
                return foods[str(id)]

        except KeyError:
            logging.error("Food: tried to query id %s but not found" % id)
            return None