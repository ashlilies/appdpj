import Account

"""
'Driver' class inherits 'Account' class

getter and setter method for all Driver attributes
"""


class Driver(Account):

    def __init__(self, is_accepting, capacity, curr_location, status, commission_status):
        self.is_accepting = is_accepting
        self.capacity = capacity
        self.curr_location = curr_location
        self.status = status
        self.commission_status = commission_status

    def get_is_accepting(self):
        return self.is_accepting

    def set_is_accepting(self, is_accepting):
        self.is_accepting = is_accepting

    def get_capacity(self):
        return self.capacity

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_curr_location(self):
        return self.curr_location

    def set_curr_location(self, curr_location):
        self.curr_location = curr_location

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
