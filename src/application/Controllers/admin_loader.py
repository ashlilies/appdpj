# Controller for the Admin side of things.
# Do NOT run directly. Run main.py in the appdpj/src/ directory instead.

# New routes go here, not in __init__.
from application import app, login_manager

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])

# Initialize all our separated controllers
from application.Controllers.admin.admin_ashlee import *
from application.Controllers.admin.admin_ruri import *
from application.Controllers.admin.admin_yonglin import *
from application.Controllers.admin.admin_clara import *
