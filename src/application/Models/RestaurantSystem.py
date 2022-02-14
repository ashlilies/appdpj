from application.Models.Restaurant import Restaurant
import uuid
import shelve
import pickle

RESTAURANT_DB = 'restaurant_db'


class RestaurantSystem():
    @staticmethod
    def find_restaurant_by_id(restaurant_id):
        with shelve.open(RESTAURANT_DB, 'c') as db:
            return db.get(restaurant_id)

    # Return a list of all restaurants - Ashlee
    @staticmethod
    def get_restaurants():
        restaurant_list = []
        with shelve.open(RESTAURANT_DB, 'c') as db:
            for k in db:
                restaurant_list.append(db.get(k))

        return restaurant_list

    @staticmethod
    def create_restaurant(name, logo, contact, open, close, add1,
                          postc,latitude, longitude, desc, bank, del1, del2, del3, del4,
                          del5):
        restaurant = Restaurant(name, logo, contact, open, close, add1,
                                postc, latitude, longitude, desc, bank, del1, del2, del3, del4,
                                del5)
        RestaurantSystem.save_to_shelve(restaurant)
        return restaurant

    @staticmethod
    def edit_restaurant(restaurant: Restaurant,
                        name, logo, contact, open, close, add1,
                        postc, latitude, longitude,desc, bank, del1, del2, del3, del4, del5):
        restaurant.set_name(name)
        restaurant.set_logo(logo)
        restaurant.set_contact(contact)
        restaurant.set_open(open)
        restaurant.set_close(close)
        restaurant.set_add1(add1)
        # restaurant.set_add2(add2)
        restaurant.set_postc(postc)
        restaurant.latitude = latitude
        restaurant.longitude = longitude
        restaurant.set_desc(desc)
        restaurant.set_bank(bank)
        restaurant.set_del1(del1)
        restaurant.set_del2(del2)
        restaurant.set_del3(del3)
        restaurant.set_del4(del4)
        restaurant.set_del5(del5)
        RestaurantSystem.save_to_shelve(restaurant)

    @staticmethod
    def save_to_shelve(restaurant: Restaurant):
        with shelve.open(RESTAURANT_DB, 'c') as db:
            db[restaurant.get_id()] = restaurant


def all_restaurant():
    all_restaurant_array = []
    open_shelve = shelve.open(RESTAURANT_DB)
    try:
        for restaurant in open_shelve:
            all_restaurant_array.append(open_shelve[restaurant])
    except:
        print("Error")
    finally:
        open_shelve.close()
    return all_restaurant_array
