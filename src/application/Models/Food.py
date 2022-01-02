# Clara
from application.Models.Account import save_db


class Food:
    def __init__(self, image, name, description, price, allergy,
                 specification=None, topping=None):
        self.__image = image
        self.name = name
        self.description = description
        self.price = price
        self.allergy = allergy
        self.specification = specification
        self.topping = topping

        save_db()

    # Get the image as a file?
    def get_image(self):
        return self.__image

    # Set the image as a file?
    def set_image(self, image):
        self.__image = image
