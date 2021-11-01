"""
'Restaurant' class is the Parent, trying to contribute feel free to edit/delete accordingly

getter and setter method for all Account attributes
"""


class Restaurant:
    def __init__(self, capacity, opening_hours, isClosed, kitchen_status, status, review_dict):
        self.capacity = capacity
        self.opening_hours = opening_hours
        self.isClosed = isClosed
        self.kitchen_status = kitchen_status
        self.status = status
        self.review_dict = review_dict

    def get_capacity(self):
        return self.capacity

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_opening_hours(self):
        return self.opening_hours

    def set_opening_hours(self, opening_hours):
        self.opening_hours = opening_hours

    def get_isClosed(self):
        return self.isClosed

    def set_isClosed(self, isClosed):
        self.isClosed = isClosed

    def get_kitchen_status(self):
        return self.kitchen_status

    def set_kitchen_status(self, kitchen_status):
        self.kitchen_status = kitchen_status

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_review_dict(self):
        return self.review_dict

    def set_review_dict(self, review_dict):
        self.review_dict = review_dict
