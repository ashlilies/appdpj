# Denotes a single restaurant's account

from application.Models.Account import *


class Admin(Account):
    def __init__(self, restaurant_name, email, password):
        self.restaurant_name = restaurant_name
        self.list_of_transactions = []
        super().__init__(email, password)

    # Add a transaction to a shop's list
    def add_transaction(self, transaction: Transaction):
        self.list_of_transactions.append(transaction)
