# XU YONG LIN
# Address field - Consumer
class ConsumerAddress:
    def __init__(self, account_id, address, latitude, longitude):
        self.account_id = account_id
        self.address = address
        self.__latitude = latitude
        self.__longitude = longitude


    def set_longitude(self, longitude):
        self.__longitude = longitude

    def set_latitude(self, latitude):
        self.__latitude = latitude

    def get_longitude(self):
        return self.__longitude

    def get_latitude(self):
        return self.__latitude


