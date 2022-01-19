# This isn't a controller :( this is a Model

from application.Models.Restaurant import *
import uuid
import shelve
import pickle
RESTAURANT_DB = 'restaurant_db'

class RestaurantSystem():
    def __init__(self):
        self.restaurant = all_restaurant()

    # def find_user_by_id(self, id):
    #     db = shelve.open(DB_NAME, 'r')
    #     for i in db:
    #         if i.account_id == id:
    #             return i

    def find_restaurant_by_id(self,id):
        for restaurant in self.restaurant:
            if restaurant.get_id() == id:
                return restaurant

    def create_restaurant(self,id, name, logo, contact, open, close, add1, add2, postc, desc, bank, del1, del2, del3, del4, del5):
        restaurant = Restaurant(id,name, logo, contact, open, close, add1, add2, postc, desc, bank, del1, del2, del3, del4, del5)
        if restaurant.save_to_shelve():
            self.restaurant.append(restaurant)
            return True
        return False


    def edit_restaurant(self,id, name, logo, contact, open, close, add1, add2, postc, desc, bank, del1, del2, del3, del4, del5):
        find_restaurant = self.find_restaurant_by_id(id)
        if find_restaurant:
            find_restaurant.set_name(name)
            find_restaurant.set_logo(logo)
            find_restaurant.set_contact(contact)
            find_restaurant.set_open(open)
            find_restaurant.set_close(close)
            find_restaurant.set_add1(add1)
            find_restaurant.set_add2(add2)
            find_restaurant.set_postc(postc)
            find_restaurant.set_desc(desc)
            find_restaurant.set_bank(bank)
            find_restaurant.set_del1(del1)
            find_restaurant.set_del2(del2)
            find_restaurant.set_del3(del3)
            find_restaurant.set_del4(del4)
            find_restaurant.set_del5(del5)
            find_restaurant.save_to_shelve()
            print("Correct")
            return True
        else:
            print("Wrong")
            return False


def all_restaurant():
    all_restaurant_array = []
    open_shelve = shelve.open(RESTAURANT_DB)
    try:
        for restaurant in open_shelve :
            all_restaurant_array.append(deserialize(open_shelve[restaurant]))
    except:
        print("Error")
    finally:
        open_shelve.close()
    return all_restaurant_array



def deserialize(object):
    try:
        return pickle.loads(object)
    except:
        return None
