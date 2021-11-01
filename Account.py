"""
'Account' class is the Parent, trying to contribute feel free to edit/delete accordingly

getter and setter method for all Account attributes
"""


class Account:
    def __init__(self, name, contactNo, password, email):
        self.name = name
        self.contactNo = contactNo
        self.password = password
        self.email = email

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getContactNo(self):
        return self.contactNo

    def setContactNo(self, contactNo):
        self.contactNo = contactNo

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email
