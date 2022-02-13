import logging
import shelve

import overpy as overpy
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from flask_googlemaps import GoogleMaps

from geopy.geocoders import Nominatim

from application import app
from application.Controllers.consumer.consumer_ashlee import consumer_side
from application.Models.Address import ConsumerAddress
from application.consumer_address_form import ConsumerAddressForm

# <------------------------- YONG LIN ------------------------------>
# ADDRESS FIELD (form field)
geolocator = Nominatim(user_agent="foodypulse")
GoogleMaps(app)


@app.route("/myAddress", methods=["GET", "POST"])
@login_required
@consumer_side
def consumer_myaddress():
    consumer_address_form = ConsumerAddressForm(request.form)
    # controller will be the place where we do all the interaction
    # address_form = ConsumerAddressForm(request.form)
    longitude = None
    latitude = None

    if request.method == 'POST' and consumer_address_form.validate():
        # saving / updating the user's address
        address_dict = {}
        with shelve.open('address.db', 'c') as db:
            try:
                address_dict = db['address']
            except Exception as e:
                print('Error in retrieving address from address.db (%s)' % e)

            # implementation of api
            try:
                location = geolocator.geocode(consumer_address_form.consumer_address.data)
                print(location.address)
                longitude = location.longitude
                latitude = location.latitude
                flash("Successfully Saved your delivery address!")

                consumer = ConsumerAddress(current_user.account_id, location.address, latitude, longitude)
                address_dict[current_user.account_id] = consumer
                print(consumer.get_latitude(), consumer.get_longitude())

            except Exception as e:
                # todo: input showing of error as a pop out page at the top -- follow Ashlee's code
                logging.error('Error in Address (%s)' % e)
                flash("Could not find your address, please try again")

            db['address'] = address_dict
        return render_template("consumer/address.html", form=consumer_address_form, latitude=latitude, longitude=longitude)
    else:
        address_dict = {}
        with shelve.open('address.db', 'c') as db:
            try:
                address_dict = db['address']
                consumer = address_dict.get(current_user.account_id)
                consumer_address_form.consumer_address.data = consumer.address
                print(consumer.address)
            except Exception as e:
                logging.error('address: unable to display address due to %s in db' % e)

        return render_template("consumer/address.html", form=consumer_address_form)
