import logging
import shelve

from flask import render_template, request, redirect, url_for
from flask_login import current_user
from geopy import Nominatim

from application import app
from application.Models.Address import ConsumerAddress
from application.consumer_address_form import ConsumerAddressForm

# <------------------------- YONG LIN ------------------------------>
# ADDRESS FIELD (form field)
GOOGLE_MAPS_KEY = 'AIzaSyDgjG08WClpktEbJtz3LbejzyG98Vm-_OA'
geolocator = Nominatim(user_agent="geoapiExercises")


@app.route("/myAddress", methods=["GET", "POST"])
def consumer_myaddress():
    consumer_address_form = ConsumerAddressForm(request.form)
    # controller will be the place where we do all the interaction
    # address_form = ConsumerAddressForm(request.form)

    if request.method == 'POST' and consumer_address_form.validate():
        # if the address does not exist
        address_dict = {}
        with shelve.open('address.db', 'c') as db:
            try:
                address_dict = db['address']
            except Exception as e:
                print('Error in retrieving address from address.db (%s)' %e)

            consumer = ConsumerAddress(current_user.account_id, consumer_address_form.consumer_address.data)
            address_dict[current_user.account_id] = consumer
            current_user.checkout_address = consumer_address_form.consumer_address
            db['address'] = address_dict
        return redirect(url_for('consumer_cart')) # todo: link to ruri's payment link
    else:
        address_dict = {}
        with shelve.open('address.db', 'c') as db:
            try:
                address_dict = db['address']
                consumer = address_dict.get(current_user.account_id)
                consumer_address_form.consumer_address.data = consumer.consumer_address
            except Exception as e:
                logging.error('address: unable to display address due to %s in db' %e)
        return render_template("consumer/address.html", form=consumer_address_form)

