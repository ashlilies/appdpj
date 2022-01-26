# IF YOU'RE HERE: New routes go in Controllers > admin or consumer!

import atexit
import logging
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "doofypulseEngineers"  # used for secure stuff

# Handling Flask uploads.
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    return redirect(url_for("admin_login"))


# Includes
from application.Forms import CreateUserForm, CreateCustomerForm
from application.Controllers.admin_loader import *
from application.Controllers.consumer_loader import *
