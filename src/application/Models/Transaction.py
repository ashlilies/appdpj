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
        self.transaction = all_transactions()
        self.account_name = account_name
        self.__option = option
        self.__price = price
        self.__used_coupons = used_coupons
        self.__ratings = ratings
        self.deleted = False

        Transaction.transaction_id += 1
        #  database access in Models not Controller -- saving, for first time creating
        # maybe can create a function for this
        with shelve.open(TRANSACTION_DB, 'c') as handle:
            handle['transaction_id_count'] = Transaction.transaction_id

    def set_option(self, option):
        self.__option = option

    def get_option(self):
        return self.__option

    # price must be in 2 dp, can only accept numbers
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
            with shelve.open(TRANSACTION_DB, 'c') as handle:
                transaction = handle['shop_transactions']
                return transaction[str(id)]
        except Exception as e:
            print(e)
            logging.error('Transaction: tried to query id %s but not found' % id)
            return None


# opening of shelve
t_db = shelve.open('transaction_db')

# create transaction
def create_t(name, option, price, coupon, rating):
    id = str(uuid.uuid4())
    t = Transaction(id)
    t.account_name = name
    t.set_option = option
    t.set_price = price
    t.set_used_coupons = coupon
    t.set_price = price
    t_db[id] = t

# soft delete transaction

# opening and closing of shelve
def all_transactions():
    transaction_list = []
    with shelve.open(TRANSACTION_DB, 'c') as handle:
        try:
            for transaction in handle:
                t = handle['transaction']
                transaction_list.append(t)
        except Exception as e:
            logging.error("error: opening TRANSACTION_DB %s" % e)
    return transaction_list
