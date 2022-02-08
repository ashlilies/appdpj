# Ruri
import uuid
import shelve


RESTAURANT_DB = 'restaurant_db'
import pickle
# from application.Models.Admin import Admin


class Restaurant():
    def __init__(self, name, logo, contact, open, close, add1, add2, postc, desc, bank, del1, del2, del3, del4, del5):
        # super().__init__(restaurant_name)  #using the restaurant name created @ account level
        # self.user_object = user_object
        restaurant_id = uuid.uuid4().hex
        self.id = restaurant_id
        self.name = name
        self.logo = logo
        self.contact = contact
        self.open = open
        self.close = close
        self.add1 = add1
        self.add2 = add2
        self.postc = postc
        self.bank = bank
        self.desc = desc
        self.del1 = del1
        self.del2 = del2
        self.del3 = del3
        self.del4 = del4
        self.del5 = del5

        # save_db()

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_logo(self, logo):
        self.logo = logo

    def get_logo(self):
        return self.logo

    def set_contact(self, contact):
        self.contact = contact

    def get_contact(self):
        return self.contact

    def set_open(self, open):
        self.open = open

    def get_open(self):
        return self.open

    def set_close(self, close):
        self.close = close

    def get_close(self):
        return self.close

    def set_add1(self, add1):
        self.add1 = add1

    def get_add1(self):
        return self.add1

    def set_add2(self, add2):
        self.add2 = add2

    def get_add2(self):
        return self.add2

    def set_postc(self, postc):
        self.postc = postc

    def get_postc(self):
        return self.postc

    def set_bank(self, bank):
        self.bank = bank

    def get_bank(self):
        return self.bank

    def set_desc(self, desc):
        self.desc = desc

    def get_desc(self):
        return self.desc

    def set_del1(self, del1):
        self.del1 = del1

    def get_del1(self):
        return self.del1

    def set_del2(self, del2):
        self.del2 = del2

    def get_del2(self):
        return self.del2

    def set_del3(self, del3):
        self.del3 = del3

    def get_del3(self):
        return self.del3

    def set_del4(self, del4):
        self.del4 = del4

    def get_del4(self):
        return self.del4

    def set_del5(self, del5):
        self.del5 = del5

    def get_del5(self):
        return self.del5

    @property
    def stars_int(self):
        from application.Models.Review import ReviewDao
        return int(ReviewDao.get_average_rating(self.id))



