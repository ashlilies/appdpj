# Clara
from application.Models.Account import save_account_db


class Food:
    count_id = 0

    def __init__(self, image, name, description, price, allergy,
                 specification=None, topping=None):
        Food.count_id += 1
        self.__food_id = Food.count_id
        self.__image = image
        self.name = name
        self.description = description
        self.price = price
        self.allergy = allergy
        self.specification = specification
        self.topping = topping

        save_account_db()

    def get_food_id(self):
        return self.__food_id

    def set_food_id(self, food_id):
        self.__food_id = food_id

    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name

    def set_description(self,description):
        self.description = description

    def get_description(self):
        return self.description

    def set_price(self,price):
        self.price = price

    def get_price(self):
        return self.price

    def set_allergy(self,allergy):
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
