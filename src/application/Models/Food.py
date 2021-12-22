# Clara

class Food:
    def __init__(self, image, item_name, description, price, allergy,
                 specification):
        self.__image = image
        self.__item_name = item_name
        self.__description = description
        self.__price = price
        self.__allergy = allergy
        self.__specification = specification

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_item_name(self):
        return self.__item_name

    def set_item_name(self, item_name):
        self.__item_name = item_name

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_allergy(self):
        return self.__allergy

    def set_allergy(self, allergy):
        self.__allergy = allergy

    def get_specification(self):
        return self.__specification

    def set_specification(self, specification):
        self.__specification = specification
