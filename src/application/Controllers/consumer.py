# Controller for the Consumer side of things.
# New ones go here, not in __init__.

# Fill your @app.routes below here...
from flask import render_template

from application import app

@app.route("/testing")
def testing_route():
    return "testing"