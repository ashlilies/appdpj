import Food

"""
'Drink' class inherits 'Food' class
"""


class Drink(Food):
    def __init__(self, temperature, sugar_level, extra_toppings_list, size):
        self.temperature = temperature
        self.sugar_level = sugar_level
        self.extra_toppings_list = extra_toppings_list
        self.size = size
