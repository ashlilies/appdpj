# OLD Customer - for Library Loan System, not FoodyPulse
from application.Models.User import User


class Customer(User):
    count_id = 0

    def __init__(self, first_name, last_name, gender, membership, remarks, email, date_joined, address):
        # User.__init__(self, first_name, last_name, gender, membership, remarks)
        super().__init__(first_name, last_name, gender, membership, remarks)
        Customer.count_id += 1
        self.__customer_id = Customer.count_id
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address

    def get_customer_id(self):
        return self.__customer_id

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_date_joined(self):
        return self.__date_joined

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address
