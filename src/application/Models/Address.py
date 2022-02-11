# XU YONG LIN
# Address field - Consumer
class ConsumerAddress:
    def __init__(self, account_id, address):
        self.account_id = account_id
        self.address = address

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


# # Address Data Access Object
# class AddressDao:
#     @staticmethod
#     def create_address(account_id, address):
#         consumer = ConsumerAddress(account_id, address)
#         AddressDao.save(consumer)
#
#     @staticmethod
#     def update_address(account_id, address):
#         consumer = AddressDao.query(account_id)
#         if consumer is None:
#             raise AddressNotExistsError
#
#         consumer.address = address
#         consumer.edited = True
#
#         AddressDao.save(consumer)
#
#     @staticmethod
#     def get_user_addresss(account_id):
#         address_list = []
#         address_dict = {}
#
#         with shelve.open(ADDRESS_DB, 'c') as db:
#             if "address" in db:
#                 address_dict = db["address"]
#
#         for k in address_dict:
#             consumer = address_dict[k]
#             if consumer.account_id == account_id:
#                 address_list.append(consumer)
#
#         return address_list
#
#     @staticmethod
#     def save(consumer):
#         try:
#             with shelve.open(ADDRESS_DB, 'c') as db:
#                 address_dict = {}
#                 if "address" in db:
#                     address_dict = db["address"]
#                 address_dict[consumer.id] = consumer
#                 db["address"] = address_dict
#         except KeyError:
#             logging.error("AddressDao: failed to save address dict")
#
#     @staticmethod
#     def query(account_id):
#         try:
#             with shelve.open(ADDRESS_DB, 'c') as db:
#                 if "address" in db:
#                     address_dict = db["address"]
#                     return address_dict[account_id]
#
#         except KeyError:
#             logging.error("Address: tried to query account_id %s but not found" % account_id)
#
#
# class AddressNotExistsError(Exception):
#     pass