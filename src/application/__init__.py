# IF YOU'RE HERE: New routes go in Controllers > admin or consumer!

import atexit
import logging

import flask_mail
from flask import Flask
from flask_login import LoginManager
import os

from flask_mail import Mail
from flask_recaptcha import ReCaptcha

app = Flask(__name__)

app.secret_key = "doofypulseEngineers"  # used for secure stuff

# Handling Flask uploads.
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.FileHandler("fp-log.txt"),
                        logging.StreamHandler()
                    ])
logging.info("Logger configured!")


# after the app quits, we can run anything e.g. save all databases -ashlee
def exit_handler():
    logging.info("Exit Handler: Stopping Flask!")


atexit.register(exit_handler)

# Initialize our login manager.
login_manager = LoginManager()
login_manager.init_app(app)  # app is a Flask object


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
       or None if it doesn't exist
       Runs every single time. Hence, it is safe to update account db directly.
    """
    return Account.query(int(user_id))


# TODO: We should have 1 common place for login.
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please log in to continue.")
    return redirect(url_for("consumer_login"))


email_user = ""
if os.environ.get('EMAIL_USER'):
    email_user = os.environ['EMAIL_USER']
email_pw = ""
if os.environ.get('EMAIL_PASSWORD'):
    email_pw = os.environ['EMAIL_PASSWORD']

mail_settings = {
    "MAIL_SERVER": 'smtp-mail.outlook.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": email_user,
    "MAIL_PASSWORD": email_pw
}

app.config.update(mail_settings)
mail = Mail(app)

app.config['RECAPTCHA_SITE_KEY'] = '6Lc6xnoeAAAAAIL1QJbYG7g6H4Uh98viYp2v8OJa' # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = '6Lc6xnoeAAAAAO8clUhP0zoX68LDR-lvdqJqe4wC' # <-- Add your secret key
recaptcha = ReCaptcha(app) # Create a ReCaptcha object by passing in 'app' as parameter


# Includes
from application.Forms import CreateUserForm, CreateCustomerForm
from application.Controllers.admin_loader import *
from application.Controllers.consumer_loader import *
