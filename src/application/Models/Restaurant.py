# ruri flora newman
from application.Models.Food import Food

class Restaurant:
    def __init__(self, name, contact, open_hour, close_hour, address, tags,
                 bank, desc, deli_fee12, deli_fee24,
                 deli_fee46, deli_fee68, table_plan):
        self.name = name
        self.contact = contact
        self.open_hour = open_hour
        self.close_hour = close_hour
        self.address = address
        self.tags = tags
        self.bank = bank
        self.desc = desc
        self.__list_of_food = []  # a list of food objects by the restaurant

        # how many KM away? 1-2 2-4 4-6 6-8 and 9+
        self.deli_fee12 = deli_fee12
        self.deli_fee24 = deli_fee24
        self.deli_fee46 = deli_fee46
        self.deli_fee68 = deli_fee68
        self.table_plan = table_plan

    # Add food from restaurant menu
    def add_food(self, food: Food):
        self.__list_of_food.append(food)

    # Remove food from restaurant menu
    def remove_food(self, name_of_food_to_remove: str):
        # add logic to remove a specific food item (maybe by name?) here
        for food in self.__list_of_food:
            if food.name == name_of_food_to_remove:
                self.__list_of_food.remove(food)
                del food
