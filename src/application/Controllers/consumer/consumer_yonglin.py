import logging
import shelve

from flask import render_template, request, redirect, url_for
from flask_login import current_user
from geopy.geocoders import Nominatim

from application import app
from application.Models.Address import ConsumerAddress
from application.consumer_address_form import ConsumerAddressForm

# <------------------------- YONG LIN ------------------------------>
# ADDRESS FIELD (form field)
geolocator = Nominatim(user_agent="foodypulse")


@app.route("/myAddress", methods=["GET", "POST"])
def consumer_myaddress():
    consumer_address_form = ConsumerAddressForm(request.form)
    # controller will be the place where we do all the interaction
    # address_form = ConsumerAddressForm(request.form)

    # todo: change attributes to private attributes (for 'safety' reason)
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
                # todo: limit area to Singapore Region
                # todo: show the location on the map itself
                location = geolocator.geocode(consumer_address_form.consumer_address.data)
                print(location.address)
            except Exception as e:
                # todo: input showing of error as a pop out page at the top -- follow Ashlee's code
                print('Error in Address (%s)' %e)

            consumer = ConsumerAddress(current_user.account_id, location.address)
            address_dict[current_user.account_id] = consumer

            # current_user.checkout_address = consumer_address_form.consumer_address
            db['address'] = address_dict
        return redirect(url_for('consumer_cart'))  # todo: link to ruri's payment link
    else:
        address_dict = {}
        with shelve.open('address.db', 'c') as db:
            try:
                address_dict = db['address']
                consumer = address_dict.get(current_user.account_id)
                consumer_address_form.consumer_address.data = consumer.address
            except Exception as e:
                logging.error('address: unable to display address due to %s in db' % e)
        return render_template("consumer/address.html", form=consumer_address_form)
