# xu yong lin
import logging
import shelve

# from application import DB_NAME
from application.Models.Account import Account
from application.Models.CountId import CountId

TRANSACTION_DB = "transaction.db"


class Transaction:
    count_id = 1
    STATUS_UNKNOWN = -1
    STATUS_PREPARING = 0
    STATUS_ON_THE_WAY = 1
    STATUS_DELIVERED = 2

    def __init__(self, restaurant_id, account_id, price, used_coupon=None):
        CountId.load(TRANSACTION_DB, Transaction)
        self.id = Transaction.count_id
        Transaction.count_id += 1
        CountId.save(TRANSACTION_DB, Transaction)

        self.restaurant_id = restaurant_id
        self.account_id = account_id
        self.price = price
        self.used_coupon = used_coupon
        self.deleted = False
        self.__status = Transaction.STATUS_PREPARING

    def text_status(self):
        if self.status == Transaction.STATUS_PREPARING:
            return "Preparing"
        elif self.status == Transaction.STATUS_ON_THE_WAY:
            return "On the Way"
        elif self.status == Transaction.STATUS_DELIVERED:
            return "Delivered"
        else:
            return "Unknown"

    @property
    def acccount_name(self):
        account = Account.query(self.account_id)
        return account.name

    @property
    def status(self):
        if self.__status not in [Transaction.STATUS_PREPARING,
                                 Transaction.STATUS_ON_THE_WAY,
                                 Transaction.STATUS_DELIVERED]:
            return Transaction.STATUS_UNKNOWN
        return self.__status

    @status.setter
    def status(self, new_status: int):
        self.__status = new_status
        TransactionDao.save(self)


class TransactionDao:
    @staticmethod
    def create_transaction(restaurant_id, account_name, price, used_coupon=None,
                           rating=0) -> Transaction:
        transaction = Transaction(restaurant_id, account_name, price,
                                  used_coupon)
        TransactionDao.save(transaction)
        return transaction

    @staticmethod
    def get_transaction(transaction_id) -> Transaction:
        transaction_dict = {}
        with shelve.open(TRANSACTION_DB, 'c') as db:
            if "transaction" in db:
                transaction_dict = db["transaction"]

        return transaction_dict.get(transaction_id)

    # Returns a list of transaction objects
    @staticmethod
    def get_transactions(restaurant_id) -> list:
        transaction_list = []
        transaction_dict = {}
        with shelve.open(TRANSACTION_DB, 'c') as db:
            if "transaction" in db:
                transaction_dict = db["transaction"]

        for transaction_id in transaction_dict:
            transaction = transaction_dict.get(transaction_id)
            if transaction.restaurant_id == restaurant_id:
                transaction_list.append(transaction)

        return transaction_list

    # Returns a list of transaction objects
    @staticmethod
    def get_user_transactions(account_id) -> list:
        transaction_list = []
        transaction_dict = {}
        with shelve.open(TRANSACTION_DB, 'c') as db:
            if "transaction" in db:
                transaction_dict = db["transaction"]

        for transaction_id in transaction_dict:
            transaction = transaction_dict.get(transaction_id)
            if transaction.account_id == account_id:
                transaction_list.append(transaction)

        return transaction_list

    # Soft-delete transactions
    @staticmethod
    def delete_transaction(transaction_id):
        transaction = TransactionDao.get_transaction(transaction_id)
        if transaction:
            logging.info("delete_transaction: deleted transaction with id %d"
                         % transaction_id)
            transaction.deleted = True
            TransactionDao.save(transaction)

    @staticmethod
    def save(transaction: Transaction):
        try:
            with shelve.open(TRANSACTION_DB, 'c') as db:
                transaction_dict = {}
                if "transaction" in db:
                    transaction_dict = db["transaction"]
                transaction_dict[transaction.id] = transaction
                db["transaction"] = transaction_dict
        except KeyError:
            logging.error("Transaction: failed to save transaction dict")
