# FoodyPulse base account class - to be used for Admin and Consumer
import logging

from werkzeug.security import generate_password_hash, check_password_hash
import shelve

from application.Models.Logger import Logger


class Account:
    count_id = 0  # ADVANTAGE: Can handle soft-deleted accounts better
    list_of_accounts = []

    # Returns a logger object of the appropriate msg-type.
    @staticmethod
    def get_logger(self):
        return Logger("Base Account")

    def __init__(self, email, password):
        logger = self.__class__.get_logger()
        logger.info("Initializing new account with email=%s" % email)
        load_db()

        # First, check if email already exists.
        if self.__class__.email_exists(email):
            logger.warn("Email=%s already exists; can't create account" % email)
            raise Exception("Account with email already exists")

        self.__class__.count_id += 1  # Update class count id
        self.account_id = self.__class__.count_id  # actually set account's ID

        self.__email = email  # protected b/c of db updates automatic

        self.__password_hash = None
        self.set_password_hash(password)
        self.__class__.list_of_accounts.append(self)

        logger.info("Success creating account with email=%s" % email)

        save_db()

    @classmethod
    def login_user(cls, email, password):
        load_db()
        logger = Logger("Base Account")
        logger.info("Attempting to log in email=%s" % email)
        # O^n array search for account and return account object
        for account in cls.list_of_accounts:
            if account.__email == email:  # found account inside :D
                if check_password_hash(account.__password_hash, password):
                    logger.info("Successfully logged in email=%s" % email)
                    return account  # return account obj if correct pw
        logger.warn("Failed to log in email=%s" % email)
        return None  # else if no user-pw match return None

    @classmethod
    def email_exists(cls, email) -> bool:
        for account in cls.list_of_accounts:
            if account.__email == email:
                return True
        return False

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email
        save_db()

    def set_password_hash(self, password):  # update the password
        logger = Logger("Base Account")
        logger.info("Updating password for account email=%s" % self.__email)
        self.__password_hash = generate_password_hash(password=password,
                                                      method='sha256')
        save_db()

    # Returns a pointer to an account, or None if not found
    @classmethod
    def get_account_by_id(cls, account_id):
        for account in cls.list_of_accounts:
            if account.account_id == account_id:
                return account
        return None


def load_db():
    logger = Account.get_logger()
    # todo: try-except for all db
    with shelve.open("accounts", 'c') as db:
        if "count_id" in db:  # has db been initialized?
            Account.count_id = db["count_id"]
            Account.list_of_accounts = db["list_of_accounts"]
            logger.info("Loading DB: count_id=%s, list of accounts has %s "
                        "elems"
                        % (db["count_id"], len(db["list_of_accounts"])))
        else:
            logger.info("Loading DB not found - creating new db")


def save_db():
    logger = Account.get_logger()
    logger.info("Saving DB: count_id=%s, list of accounts has %s elems"
                % (Account.count_id, len(Account.list_of_accounts)))
    with shelve.open("accounts", 'c') as db:
        db["count_id"] = Account.count_id
        db["list_of_accounts"] = Account.list_of_accounts
