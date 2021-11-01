"""
'Food' class is the Parent, trying to contribute feel free to edit/delete accordingly

getter and setter method for all Food attributes
"""


class Food:
    def __init__(self, is_halal, is_vegetarian, allergy_triggers_list, spiciness, is_available, cuisine_type,
                 description, photo_url):
        self.is_halal = is_halal
        self.is_vegetarian = is_vegetarian
        self.allergy_triggers_list = allergy_triggers_list
        self.spiciness = spiciness
        self.is_available = is_available
        self.cuisine_type = cuisine_type
        self.description = description
        self.photo_url = photo_url

    def get_is_halal(self):
        return self.is_halal

    def set_is_halal(self, is_halal):
        self.is_halal = is_halal

    def get_is_vegetarian(self):
        return self.is_vegetarian

    def set_is_vegetarian(self, is_vegetarian):
        self.is_vegetarian = is_vegetarian

    def get_allergy_triggers_list(self):
        return self.allergy_triggers_list

    def set_allergy_triggers_list(self, allergy_triggers_list):
        self.allergy_triggers_list = allergy_triggers_list

    def get_spiciness(self):
        return self.spiciness

    def set_spiciness(self, spiciness):
        self.spiciness = spiciness

    def get_is_available(self):
        return self.is_available

    def set_is_available(self, is_available):
        self.is_available = is_available

    def get_cuisine_type(self):
        return self.cuisine_type

    def set_cuisine_type(self, cuisine_type):
        self.cuisine_type = cuisine_type

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_photo_url(self):
        return self.photo_url

    def set_photo_url(self, photo_url):
        self.photo_url = photo_url
