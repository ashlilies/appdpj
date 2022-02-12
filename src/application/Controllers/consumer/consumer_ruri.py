from flask import render_template
from flask_login import login_required

from application import app
from application.Controllers.consumer.consumer_ashlee import consumer_side

# <------------------------- RURI ------------------------------>

# Moved by Ashlee


@app.route("/delordine")
@consumer_side
@login_required
def delordine():  # ruri
    return render_template('consumer/delOrDine.html')

