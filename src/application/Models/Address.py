# Address field - Consumer
import logging
import shelve

from application.Models.Account import Account
from application.Models.CountId import CountId
from application.Models.FileUpload import delete_file
from application.Models.RestaurantSystem import RestaurantSystem

ADDRESS_DB = "address.db"


class ConsumerAddress:

    def __init__(self, consumer_id, homeAddress, workAddress, otherAddress):
        CountId.load(ADDRESS_DB, ConsumerAddress)
        self.id = consumer_id
        CountId.save(ADDRESS_DB, ConsumerAddress)

        self.consumer_id = consumer_id
        self.homeAddress = homeAddress
        self.workAddress = workAddress
        self.otherAddress = otherAddress

        # self.parent_restaurant_id = parent_restaurant_id
        self.edited = False

    # @property
    # def consumer_name(self):
    #     consumer = Account.query(self.consumer_id)
    #     name = "%s" % (consumer)
    #     return name

    # # For easy retrieval on consumer address on restaurant side ?
    # @property
    # def restaurant_name(self):
    #     restaurant = RestaurantSystem.find_restaurant_by_id(self.parent_restaurant_id)
    #     return restaurant.name


# Address Data Access Object
class AddressDao:
    @staticmethod
    def create_address(consumer_id, homeAddress, workAddress, otherAddress):
        consumer = ConsumerAddress(consumer_id, homeAddress, workAddress, otherAddress)
        AddressDao.save(consumer)

    @staticmethod
    def update_address(consumer_id,homeAddress, workAddress, otherAddress):
        consumer = AddressDao.query(consumer_id)
        if consumer is None:
            raise ReviewIdNotExistsError

        consumer.homeAddress = homeAddress
        consumer.workAddress = workAddress
        consumer.otherAddress = otherAddress
        consumer.edited = True

        AddressDao.save(consumer)

    @staticmethod
    def get_user_addresss(user_id):
        # Linear search and retun a list of consumer objects with matching user ID
        address_list = []
        address_dict = {}

        with shelve.open(ADDRESS_DB, 'c') as db:
            if "address" in db:
                address_dict = db["address"]

        for k in address_dict:
            consumer = address_dict[k]
            if consumer.consumer_id == user_id:
                address_list.append(consumer)

        return address_list

    @staticmethod
    def save(consumer):
        try:
            with shelve.open(ADDRESS_DB, 'c') as db:
                address_dict = {}
                if "address" in db:
                    address_dict = db["address"]
                address_dict[consumer.id] = consumer
                db["address"] = address_dict
        except KeyError:
            logging.error("AddressDao: failed to save address dict")

    @staticmethod
    def query(consumer_id):
        try:
            with shelve.open(ADDRESS_DB, 'c') as db:
                if "address" in db:
                    address_dict = db["address"]
                    return address_dict[consumer_id]

        except KeyError:
            logging.error("Food: tried to query consumer_id %s but not found" % consumer_id)


class ReviewIdNotExistsError(Exception):
    pass
