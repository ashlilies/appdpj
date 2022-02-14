# XU YONG LIN
# Address field - Consumer
from math import radians

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


def calculate_distance(conLatitude, conLongitude, restaurant):
    restaurant = restaurant
    resLatitude = restaurant.latitude
    resLongitude = restaurant.longitude

    consumer_latitude = radians(conLatitude)
    consumer_longitude = radians(conLongitude)
    consumer_latlon = (consumer_latitude, consumer_longitude)

    restaurant_latitude = radians(resLatitude)
    restaurant_longitude = radians(resLongitude)
    restaurant_latlon = (restaurant_latitude, restaurant_longitude)

    res_con_dist = (geopy.distance.distance(consumer_latlon, restaurant_latlon) * 100)
    res_con_dist = float(str(res_con_dist)[:-3])

    # print('distance',res_con_dist)
    # calculate_deltime_bydist(res_con_dist)
    # delivery_fee(res_con_dist, restaurant)
    return res_con_dist


def calculate_deltime_bydist(res_con_dist):
    prep_time = 15
    est_del_time = 5  # estimate per 2km
    duration = res_con_dist / 2
    total_time = (est_del_time * duration) + prep_time

    # print('total time',total_time)
    return total_time


def delivery_fee(res_con_dist, restaurant):
    del_fee = 0
    # 1-2, 2-4, 4-6, 6-8, more than 9
    if res_con_dist > 0 and res_con_dist <= 2:
        del_fee = restaurant.del1
    elif res_con_dist > 2 and res_con_dist <= 4:
        del_fee = restaurant.del2
    elif res_con_dist > 4 and res_con_dist <= 6:
        del_fee = restaurant.del3
    elif res_con_dist > 6 and res_con_dist <= 8:
        del_fee = restaurant.del4
    else:
        del_fee = restaurant.del5

    # print('del_fee',del_fee)
    return del_fee
