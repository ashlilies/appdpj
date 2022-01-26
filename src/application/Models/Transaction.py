# xu yong lin
# consists of: create(to be done more on consumer side), read, delete(soft delete) of transactions
import logging
import shelve
import uuid

TRANSACTION_DB = 'transaction_db'


class Transaction:
    transaction_id = 1
    food_coupons = ['SPAGETIT', '50PASTA']

    def __init__(self, account_name=None, option=None, price=0, used_coupons=None,
                 ratings=0):
        with shelve.open(TRANSACTION_DB, 'c') as db:
            try:
                Transaction.transaction_id = db['transaction_id_count']
            except Exception as e:
                logging.info("line 18: transaction_id_count: error reading from db (%s)" % e)
        self.transaction_id = Transaction.transaction_id
        self.account_name = account_name
        self.__option = option
        self.__price = price
        self.__used_coupons = used_coupons
        self.__ratings = ratings
        self.deleted = False
        self.transactions = {}

        Transaction.transaction_id += 1
        #  database access in Models not Controller -- saving, for first time creating
        # maybe can create a function for this
        with shelve.open(TRANSACTION_DB, 'c') as handle:
            handle['transaction_id_count'] = Transaction.transaction_id

    def set_option(self, option):
        self.__option = option

    def get_option(self):
        return self.__option

    def set_price(self, price):
        try:
            if price == float(price):
                self.__price = price
        except:
            self.deleted = True

    def get_price(self):
        return self.__price

    def set_used_coupons(self, used_coupons):
        if used_coupons in Transaction.food_coupons:
            self.__used_coupons = used_coupons
        else:
            self.__used_coupons = 'NIL'

    def get_used_coupons(self):
        return self.__used_coupons

    # ratings must be in 2 dp, can only accept numbers
    def set_ratings(self, ratings):
        try:
            if ratings == int(ratings):
                self.__ratings = ratings
        except:
            self.deleted = True

    def get_ratings(self):
        return self.__ratings

    # query handle for a transaction by passing in the id
    # only for r -- retrieval
    def query(self, id):
        try:
            with shelve.open(TRANSACTION_DB, 'c') as db:
                transaction = db['shop_transactions']
                return transaction[str(id)]
        except Exception as e:
            print(e)
            logging.error('Transaction: tried to query id %s but not found' % id)
            return None

    # create new transaction
    def new_transaction(self, name, option, price, coupon, rating):
        transaction_id = Transaction.transaction_id
        self.transactions[transaction_id] = Transaction(name, option, price, coupon, rating)
        print(self.transactions)
        with shelve.open(TRANSACTION_DB, 'c') as db:
            transaction_system_dict = {}
            if "transaction_system_dict" in db:
                transaction_system_dict = db["transaction_system_dict"]
            transaction_system_dict[self.transaction_id] = self
            db["transaction_system_dict"] = transaction_system_dict

    # get all transactions
    def get_all_transaction(self):
        with shelve.open(TRANSACTION_DB, 'c') as db:
            if "transaction_system_dict" in db:
                transaction_system_list = db["transaction_system_dict"]
                logging.info('get_all_transaction: reading from shelve')
            else:
                logging.info("get_all_transaction: nothing found in db, starting empty")
                transaction_system_list = []

        def get_transaction_by_id(transaction_id):
            for transaction in transaction_system_list:
                if transaction_id == transaction.count_id:
                    return transaction

    # soft delete transaction
    def soft_delete_transaction(self, id):
        transaction_id = int(id)

        transaction_list = []
        with shelve.open(TRANSACTION_DB, 'c') as db:
            for transaction in db["transaction_system_dict"]:
                transaction_list.append(transaction)

        def get_transaction_by_id(t_id): # debug
            for t in transaction_list:
                if t_id == t.count_id:
                    return t
        logging.info("soft_delete_transaction: deleted transaction with id %d " %transaction_id)

        # set instance attribute self.deleted to True
        get_transaction_by_id(transaction_id).deleted = True

        with shelve.open(TRANSACTION_DB, 'c') as db:
            db["transaction_system_dict"] = transaction_list


# # create transaction
# def create_t(name, option, price, coupon, rating):
#     id = str(uuid.uuid4())
#     t = Transaction(id)
#     t.account_name(name)
#     t.set_option(option)
#     t.set_price(price)
#     t.set_used_coupons(coupon)
#     t.set_price(price)
#     t.set_ratings()
#     t_db[id] = t


# soft delete transaction

# # opening and closing of shelve
# def all_transactions():
#     transaction_list = []
#     with shelve.open(TRANSACTION_DB, 'c') as handle:
#         try:
#             for transaction in handle:
#                 t = handle['transaction']
#                 transaction_list.append(t)
#         except Exception as e:
#             logging.error("error: opening TRANSACTION_DB %s" % e)
#     return transaction_list
