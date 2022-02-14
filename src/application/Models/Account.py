# FoodyPulse base account class - to be used for Admin and Consumer
# TODO: Use a dict instead of a list for more flexibility and speed
# By Ashlee
# Fulfils: Create, Read, Update, Delete (?)
import logging
import re  # regex
import uuid

import flask_mail
import pyotp
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
import shelve

from application import app, mail

ACCOUNT_DB = "accounts"


class Account:
    count_id = 0

    EMAIL_ALREADY_EXISTS = "Account with email already exists"

    def __init__(self, email: str, password: str):
        with shelve.open(ACCOUNT_DB, 'c') as db:
            # Load current count id and dict of accounts from db
            accounts_dict = {}
            if "count_id" in db:
                Account.count_id = db["count_id"]
                accounts_dict = db["accounts"]

            # First, check if email already exists.
            if Account.email_exists(email):
                raise EmailAlreadyExistsException

            Account.count_id += 1
            self.account_id = Account.count_id
            self.__email = email
            self.__password_hash = None
            self.password_reset_key = None
            self.totp_secret = pyotp.random_base32()[:10]
            self.set_password_hash(password)
            self.disabled = False  # Suspended or soft-deleted accounts
            self.authenticated = False  # autologin on creation
            accounts_dict[self.account_id] = self

            db["count_id"] = Account.count_id
            db["accounts"] = accounts_dict

            logging.info("BaseAccount: Successfully created account, email=%s"
                         % email)

    # Str: returns email of any account easily. Useful for logging.
    def __str__(self):
        return self.__email

    # Set authenticated status and save to database
    def authenticate(self):
        self.authenticated = True

        with shelve.open("accounts", 'c') as db:
            if "accounts" in db:  # first run?
                accounts = db["accounts"]
                accounts[self.account_id] = self
                db["accounts"] = accounts

    def deauthenticate(self):
        self.authenticated = False

        with shelve.open("accounts", 'c') as db:
            if "accounts" in db:  # first run?
                accounts = db["accounts"]
                accounts[self.account_id] = self
                db["accounts"] = accounts

    # 4 functions below for flask-login
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

    # Generates a new OTP secret and sets it
    def generate_otp_secret(self):
        self.totp_secret = pyotp.random_base32()[:10]
        self.save()

    @classmethod
    def check_credentials(cls, email, password) -> "Account" or None:
        with shelve.open(ACCOUNT_DB, 'c') as db:
            if "accounts" in db:
                for account_id in db["accounts"]:
                    account = db["accounts"][account_id]
                    if account.__email == email and not account.disabled:
                        if account.check_password_hash(password):
                            return account
        return None

    # Useful for password resets
    @classmethod
    def get_account_by_email(cls, email) -> "Account" or None:
        with shelve.open(ACCOUNT_DB, 'c') as db:
            if "accounts" in db:
                for account_id in db["accounts"]:
                    account = db["accounts"][account_id]
                    if account.__email == email and not account.disabled:
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
                for account_id in db["accounts"]:
                    account = db["accounts"][account_id]
                    if account.__email == email and not account.disabled:
                        return True
        return False

    def get_email(self):
        return self.__email

    EMAIL_CHANGE_SUCCESS = 0
    EMAIL_CHANGE_ALREADY_EXISTS = 1
    EMAIL_CHANGE_INVALID = 2

    def set_email(self, email) -> int:
        if not check_email(email):
            return self.__class__.EMAIL_CHANGE_INVALID

        if self.__class__.email_exists(email):
            return self.__class__.EMAIL_CHANGE_ALREADY_EXISTS

        self.__email = email

        with shelve.open("accounts", 'c') as db:
            if "accounts" in db:  # first run?
                accounts = db["accounts"]
                accounts[self.account_id] = self
                db["accounts"] = accounts

        return self.__class__.EMAIL_CHANGE_SUCCESS

    def set_password_hash(self, password):  # update the password
        self.__password_hash = generate_password_hash(password=password,
                                                      method='sha256')
        logging.info("BaseAccount: Updating pw hash for %s" % self.__email)

        with shelve.open("accounts", 'c') as db:
            if "accounts" in db:  # first run?
                accounts = db["accounts"]
                accounts[self.account_id] = self
                db["accounts"] = accounts

    def check_password_hash(self, password) -> bool:
        return check_password_hash(self.__password_hash, password)

    def check_otp(self, otp: str):
        totp = pyotp.TOTP(self.totp_secret)
        return totp.verify(otp)

    def reset_password(self):
        if not self.disabled:
            self.password_reset_key = pyotp.random_base32()[:10]
            totp_reset = pyotp.TOTP(self.password_reset_key, interval=300)
            tok = totp_reset.now()
            with app.app_context():
                msg = flask_mail.Message(subject="Password Reset Attempt",
                                         sender=app.config.get("MAIL_USERNAME"),
                                         recipients=[self.__email],
                                         body=("Your password reset key is %s\n"
                                               "Alternatively, you may copy "
                                               "and paste this link into your "
                                               "browser: %s%s\n"
                                               "The key and link is valid for "
                                               "the next 5 minutes."
                                               % (tok,
                                                  "http://127.0.0.1:5000",
                                                  url_for("password_auto_reset",
                                                          account_id=self.account_id,
                                                          pw_reset_token=tok))))
                mail.send(msg)
            self.save()

    def reset_pw_verify(self, pw_reset_token):
        totp_reset = pyotp.TOTP(self.password_reset_key, interval=300)
        if totp_reset.verify(pw_reset_token):
            self.password_reset_key = None

            with app.app_context():
                pw = str(uuid.uuid4())[:8]
                self.set_password_hash(pw)

                with app.app_context():
                    msg = flask_mail.Message(
                        subject="Password Reset Successfully",
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=[self.__email],
                        body="Your new password is %s. Please change it after "
                             "logging in.\n"
                             "For reference, your secret key is %s." % (pw, self.totp_secret))
                    mail.send(msg)

            self.save()
            return True
        return False

    def hard_delete_account(self):
        with shelve.open(ACCOUNT_DB, 'c', writeback=True) as db:
            if "accounts" in db:
                db["accounts"].pop(self.account_id)

    def save(self):  # Save an account to the db
        with shelve.open(ACCOUNT_DB, 'c') as db:
            accounts = db["accounts"]
            accounts[self.account_id] = self
            db["accounts"] = accounts


# Some useful functions used here.
regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


def check_email(email):  # check email using re(gex)
    return re.search(regex, email)


class EmailAlreadyExistsException(Exception):
    pass
