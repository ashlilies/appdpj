# FoodyPulse base account class - to be used for Admin and Consumer
# By Ashlee
# Fulfils: Create, Read, Update, Delete (?)
import logging
import re   # regex

from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
import shelve

DB_NAME = "foodypulse"
# from application import DB_NAME


class Account:
    count_id = 0  # ADVANTAGE: Can handle soft-deleted accounts better
    list_of_accounts = []

    EMAIL_ALREADY_EXISTS = "Account with email already exists"

    # Writes generic logs for BaseAccount stuff. Only INFO level for now.
    # Meant to be used outside Account class only for convenience's sake.
    # Possibly removed in a future edit.
    @staticmethod
    def log(msg: str):
        logging.info("BaseAccount: %s" % msg)

    def __init__(self, email, password):
        load_db()

        logging.info("BaseAccount: Attempting to create account with email %s"
                     % email)

        # First, check if email already exists.
        if self.__class__.email_exists(email):
            logging.warning("BaseAccount: Account with email %s already exists"
                            % email)
            raise Exception(Account.EMAIL_ALREADY_EXISTS)

        Account.count_id += 1  # Update Account class count id
        self.account_id = Account.count_id  # actually set account's ID

        self.__email = email  # protected b/c of db updates automatic

        self.__password_hash = None
        self.set_password_hash(password)

        self.disabled = False  # Disabled or soft-deleted accounts

        Account.list_of_accounts.append(self)

        logging.info("BaseAccount: Successfully created account, email=%s"
                     % email)
        save_db()
        login_user(self)

    # Str: returns email of any account easily.
    def __str__(self):
        return self.__email

    @classmethod
    def login_user(cls, email, password):
        logging.info("BaseAccount: Attempting to log in email=%s" % email)
        load_db()

        # O^n array search for account and return account object
        for account in cls.list_of_accounts:
            if account.__email == email:  # found account inside :D
                logging.info("BaseAccount: Found matching account inside db, "
                             "checking pw...")
                if check_password_hash(account.__password_hash, password):
                    logging.info("BaseAccount: Correct email and pw!")
                    login_user(account, remember=False)
                    # TODO: Support flask-login everywhere.
                    # return account  # return account obj if correct pw
                logging.warning("BaseAccount: Email exists, wrong pw")

        logging.warning("BaseAccount: No email-pw match found in db")
        return None  # else if no user-pw match return None

    @classmethod
    def email_exists(cls, email) -> bool:
        for account in cls.list_of_accounts:
            if account.__email == email:
                return True
        return False

    # Check_active: check if account exists AND not disabled/deleted
    @classmethod
    def check_active(cls, account):
        if account in cls.list_of_accounts:
            if not account.disabled:
                logging.info("BaseAccount: %s is active" % account.get_email())
                return account
            logging.info("BaseAccount: %s exists but disabled" % account.get_email())
        logging.info("BaseAccount: %s does NOT exist in list of accounts" % account)
        return None

    def get_email(self):
        return self.__email

    EMAIL_CHANGE_SUCCESS = 0
    EMAIL_CHANGE_ALREADY_EXISTS = 1
    EMAIL_CHANGE_INVALID = 2

    # 0 indicates success, 1 indicates email exists already,
    # 2 indicates invalid email
    def set_email(self, email) -> int:
        load_db()

        # Hacky way to prevent Python from duplicating object??? check repr
        account = Account.get_account_by_id(self.account_id)

        # First, check if email is even valid
        if not check_email(email):
            # TODO: Handle validation at signup as well
            return self.__class__.EMAIL_CHANGE_INVALID

        # Check if the email already exists
        if self.__class__.email_exists(email):
            return self.__class__.EMAIL_CHANGE_ALREADY_EXISTS

        account.__email = email
        save_db()
        return self.__class__.EMAIL_CHANGE_SUCCESS

    def set_password_hash(self, password):  # update the password
        logging.info("BaseAccount: Updating pw hash for %s" % self.__email)
        self.__password_hash = generate_password_hash(password=password,
                                                      method='sha256')
        save_db()

    def check_password_hash(self, password) -> bool:
        logging.info("BaseAccount: Checking pw hash for %s" % self.__email)
        return check_password_hash(self.__password_hash, password)

    # Returns a pointer to an account, or None if not found
    @classmethod
    def get_account_by_id(cls, account_id):
        for account in cls.list_of_accounts:
            if account.account_id == account_id:
                return account
        return None


# TODO: Please change to foodypulse .db?
#       Since is a generic db that caches everything, including cascading.
def load_db():
    Account.log("Attempting to load DB")
    with shelve.open(DB_NAME, 'c') as db:
        if "count_id" in db:  # has db been initialized?
            Account.log("Found count_id in db, hence db exists")
            Account.count_id = db["count_id"]
            Account.list_of_accounts = db["list_of_accounts"]
            Account.log("Loaded count_id=%s, list_of_accounts has %s elems"
                        % (db["count_id"], len(db["list_of_accounts"])))


def save_db():
    Account.log("Attempting to save db (count_id=%s, len(list_of_accs)=%s)..."
                % (Account.count_id, len(Account.list_of_accounts)))
    with shelve.open(DB_NAME, 'c') as db:
        db["count_id"] = Account.count_id
        db["list_of_accounts"] = Account.list_of_accounts


# Some useful functions used here.
regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


def check_email(email):  # check email using re(gex)
    return re.search(regex, email)
