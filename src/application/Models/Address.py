# XU YONG LIN
# Address field - Consumer
class ConsumerAddress:
    def __init__(self, account_id, address, latitude, longitude):
        self.account_id = account_id
        self.address = address
        self.__latitude = latitude
        self.__longitude = longitude

    def set_latitude(self, latitude):
        self.__latitude = latitude

    def set_longitude(self, longitude):
        self.__longitude = longitude

    def get_latitude(self):
        return self.__latitude

    def get_longitude(self):
        return self.__longitude

    # def set_accound_id(self, account_id):
    #     self.__account_id = account_id
    #
    # def set_address(self, address):
    #     self.__address = address
    #
    # def get_account_id(self):
    #     return self.__account_id
    #
    # def get_address(self):
    #     return self.__address
