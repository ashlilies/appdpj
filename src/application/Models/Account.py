# FoodyPulse base account class - to be used for Admin and Consumer
# TODO: Use a dict instead of a list for more flexibility and speed
# By Ashlee
# Fulfils: Create, Read, Update, Delete (?)
import logging
import re  # regex
from werkzeug.security import generate_password_hash, check_password_hash
import shelve

ACCOUNT_DB = "account"


class Account:
    count_id = 0
    accounts_dict = {}

    EMAIL_ALREADY_EXISTS = "Account with email already exists"

    def __init__(self, email, password):
        with shelve.open(ACCOUNT_DB, 'c') as db:
            # Load current count id and dict of accounts from db
            if "count_id" in db:
                Account.count_id = db["count_id"]
                Account.accounts_dict = db["accounts"]

            # First, check if email already exists.
            if self.__class__.email_exists(email):
                raise Exception(Account.EMAIL_ALREADY_EXISTS)

            Account.count_id += 1
            self.account_id = Account.count_id
            self.__email = email
            self.__password_hash = None
            self.set_password_hash(password)
            self.disabled = False  # Suspended or soft-deleted accounts
            self.authenticated = True  # autologin on creation
            Account.accounts_dict[self.account_id] = self

            db["count_id"] = Account.count_id
            db["accounts"] = Account.accounts_dict

            logging.info("BaseAccount: Successfully created account, email=%s"
                         % email)

    # Str: returns email of any account easily.
    def __str__(self):
        return self.__email

    def is_authenticated(self):
        return self.authenticated

    # This property should return True if active user - not suspended etc
    def is_active(self):
        return not self.disabled

    # Anonymous users aren't supported by us. :)
    def is_anonymous(self):
        return False

    # Must return a unicode
    def get_id(self):
        return str(self.account_id)

    @classmethod
    def check_credentials(cls, email, password) -> "Account":
        with shelve.open(ACCOUNT_DB, 'c') as db:
            for account in db["accounts"]:
                if account.__email == email:
                    if account.check_password_hash(password):
                        return account
        return None

    # Queries db for account and returns an Account or None
    @staticmethod
    def query(account_id: int) -> "Account" or None:
        with shelve.open(ACCOUNT_DB) as db:
            if "accounts" in db:
                return db["accounts"].get(account_id)
        return None

    @classmethod
    def email_exists(cls, email) -> bool:
        with shelve.open(ACCOUNT_DB, 'c') as db:
            if "accounts" in db:
                for account in db["accounts"]:
                    if account.__email == email:
                        return True
        return False

    def get_email(self):
        return self.__email

    EMAIL_CHANGE_SUCCESS = 0
    EMAIL_CHANGE_ALREADY_EXISTS = 1
    EMAIL_CHANGE_INVALID = 2

    def set_email(self, email) -> int:
        with shelve.open(ACCOUNT_DB, 'c') as db:
            if "count_id" in db:
                Account.count_id = db["count_id"]
                Account.accounts_dict = db["accounts"]

            account = Account.accounts_dict[self.account_id]

            if not check_email(email):
                return self.__class__.EMAIL_CHANGE_INVALID

            if self.__class__.email_exists(email):
                return self.__class__.EMAIL_CHANGE_ALREADY_EXISTS

            account.__email = email
            db["acounts"] = Account.accounts_dict
            return self.__class__.EMAIL_CHANGE_SUCCESS

    def set_password_hash(self, password):  # update the password
        self.__password_hash = generate_password_hash(password=password,
                                                      method='sha256')
        logging.info("BaseAccount: Updating pw hash for %s" % self.__email)

    def check_password_hash(self, password) -> bool:
        with shelve.open(ACCOUNT_DB, 'c') as db:
            Account.accounts_dict = db["accounts"]
            account = Account.accounts_dict.get(self.account_id)
            return check_password_hash(account.__password_hash, password)

    def hard_delete_account(self):
        with shelve.open(ACCOUNT_DB, 'c') as db:
            Account.accounts_dict = db["accounts"]
            Account.accounts_dict.pop(self.account_id)
            db["accounts"] = Account.accounts_dict


# Some useful functions used here.
regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


def check_email(email):  # check email using re(gex)
    return re.search(regex, email)
