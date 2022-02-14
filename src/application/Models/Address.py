# XU YONG LIN
# Address field - Consumer
import geopy
from geopy.distance import geodesic

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


def calculate_distance(conLatitude, conLongitude, resLatitude, resLongitude):
    consumer_latitude = conLatitude
    consumer_longitude = conLongitude
    consumer_latlon = (consumer_latitude, consumer_longitude)

    restaurant_latitude = resLatitude
    restaurant_longitude = resLongitude
    restaurant_latlon = (restaurant_latitude, restaurant_longitude)

    res_con_dist = geopy.distance.geodisc(restaurant_latlon, consumer_latlon)

    print(res_con_dist)

def calculate_deltime_bydist(res_con_dist):
    est_del_time = 15 # estimate per 2km
    duration = res_con_dist/2
    delivery_time = est_del_time*duration

    return delivery_time
