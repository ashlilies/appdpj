# Controller for the Consumer side of things.
# Do NOT run directly. Run main.py in the appdpj/src/ directory instead.


from flask import render_template, redirect, url_for

from application import app


# Initialize all our separated controllers
from application.Controllers.consumer.consumer_ashlee import *
from application.Controllers.consumer.consumer_ruri import *
from application.Controllers.consumer.consumer_yonglin import *
from application.Controllers.consumer.consumer_clara import *
