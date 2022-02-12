import logging
import shelve

from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask_googlemaps import GoogleMaps, get_address, get_coordinates
from geopy.geocoders import Nominatim

from application import app
from application.Controllers.consumer.consumer_ashlee import consumer_side
from application.Models.Address import ConsumerAddress
from application.consumer_address_form import ConsumerAddressForm

# <------------------------- YONG LIN ------------------------------>
# ADDRESS FIELD (form field)
GOOGLEMAPS_KEY = '8JZ7i18MjFuM35dJHq70n3Hx4'
GoogleMaps(app)  # initialize the extension


def testAPI():
    # geolocator = Nominatim(user_agent="foodypulse")
    #
    # location = geolocator.geocode("Nanyang Polytechnic")
    # print(location.address)
    from flask_googlemaps import get_address, get_coordinates
    API_KEY = 'YOUR API KEY'

    # Reverse Geocoding: getting detailed address from coordinates of a location
    print(get_address(API_KEY, 22.4761596, 88.4149326))
    # output: {'zip': '700150', 'country': 'India', 'state': 'West Bengal', 'city': 'Kolkata', 'locality': 'Kolkata', 'road': 'Techno City', 'formatted_address': 'Sirin Rd, Mauza Ranabhutia, Techno City, Kolkata, West Bengal 700150, India'}

    # Geocoding: getting coordinates from address text
    print(get_coordinates(API_KEY, 'Netaji Subhash Engineering College Kolkata'))
    # output: {'lat': 22.4761596, 'lng': 88.4149326}


testAPI()


@app.route("/myAddress", methods=["GET", "POST"])
@consumer_side
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
                print('Error in retrieving address from address.db (%s)' % e)

            consumer = ConsumerAddress(current_user.account_id, consumer_address_form.consumer_address.data)
            address_dict[current_user.account_id] = consumer
            current_user.checkout_address = consumer_address_form.consumer_address
            db['address'] = address_dict
        return redirect(url_for('consumer_cart'))  # todo: link to ruri's payment link
    else:
        address_dict = {}
        with shelve.open('address.db', 'c') as db:
            try:
                address_dict = db['address']
                consumer = address_dict.get(current_user.account_id)
                consumer_address_form.consumer_address.data = consumer.consumer_address
            except Exception as e:
                logging.error('address: unable to display address due to %s in db' % e)
        return render_template("consumer/address.html", form=consumer_address_form)
