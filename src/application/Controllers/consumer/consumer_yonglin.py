import logging
import shelve

import apply as apply
import geopy.distance
import overpy as overpy
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from flask_googlemaps import GoogleMaps

from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
from geopy.distance import geodesic

from application import app
from application.Controllers.consumer.consumer_ashlee import consumer_side
from application.Models.Address import ConsumerAddress, calculate_distance
from application.Models.Cart import CartDao, Cart
from application.Models.RestaurantSystem import RestaurantSystem
from application.consumer_address_form import ConsumerAddressForm

# <------------------------- YONG LIN ------------------------------>
# ADDRESS FIELD (form field)
# create/update, reading of address
geolocator = Nominatim(user_agent="foodypulse")
GoogleMaps(app)


@app.route("/myAddress/<string:restaurant_id>", methods=["GET", "POST"])
@login_required
@consumer_side
def consumer_myaddress(restaurant_id):
    restaurant = RestaurantSystem.find_restaurant_by_id(restaurant_id)
    consumer_address_form = ConsumerAddressForm(request.form)
    longitude = None
    latitude = None
    location = None

    if request.method == 'POST' and consumer_address_form.validate():
        address_dict = {}
        with shelve.open('address.db', 'c') as db:
            try:
                address_dict = db['address']
            except Exception as e:
                logging.error('Error in retrieving address from address.db (%s)' % e)

            # implementation of api
            try:
                location = geolocator.geocode(consumer_address_form.consumer_address.data)
                print(location.address)
                longitude = location.longitude
                latitude = location.latitude
                flash("Successfully Saved your delivery address!")

                consumer = ConsumerAddress(current_user.account_id, location.address, latitude, longitude)
                address_dict[current_user.account_id] = consumer
                latitude = consumer.get_latitude()
                longitude = consumer.get_longitude()
                location = consumer.address
                calculate_distance(latitude, longitude, restaurant)

            except Exception as e:
                logging.error('Error in Address (%s)' % e)
                flash("Invalid address, please try again")
            # writeback
            db['address'] = address_dict

        cart = CartDao.get_cart(current_user.cart)
        cart_items = cart.get_cart_items()

        return render_template("consumer/address.html", form=consumer_address_form, location=location,
                               latitude=latitude,
                               longitude=longitude, cart=cart, cart_items=cart_items, restaurant=restaurant)
    else:
        address_dict = {}
        with shelve.open('address.db', 'c') as db:
            try:
                address_dict = db['address']
                consumer = address_dict.get(current_user.account_id)
                location = consumer.address
                consumer_address_form.consumer_address.data = location
            except Exception as e:
                logging.error('address: unable to display address due to %s in db' % e)

        cart = CartDao.get_cart(current_user.cart)
        cart_items = cart.get_cart_items()

        return render_template("consumer/address.html", cart=cart, cart_items=cart_items,
                               count=len(cart_items), form=consumer_address_form, location=location, latitude=latitude,
                               longitude=longitude, restaurant=restaurant)


# @app.route("/myAddress", methods=["GET", "POST"])
# @login_required
# @consumer_side
# def consumer_myaddress():
#     consumer_address_form = ConsumerAddressForm(request.form)
#     longitude = None
#     latitude = None
#
#     if request.method == 'POST' and consumer_address_form.validate():
#         # saving / updating the user's address
#         address_dict = {}
#         with shelve.open('address.db', 'c') as db:
#             try:
#                 address_dict = db['address']
#             except Exception as e:
#                 print('Error in retrieving address from address.db (%s)' % e)
#
#             # implementation of api
#             try:
#                 location = geolocator.geocode(consumer_address_form.consumer_address.data)
#                 print(location.address)
#                 longitude = location.longitude
#                 latitude = location.latitude
#                 flash("Successfully Saved your delivery address!")
#
#                 consumer = ConsumerAddress(current_user.account_id, location.address, latitude, longitude)
#                 address_dict[current_user.account_id] = consumer
#                 print(consumer.get_latitude(), consumer.get_longitude())
#
#             except Exception as e:
#                 logging.error('Error in Address (%s)' % e)
#                 flash("Could not find your address, please try again")
#             # writeback
#             db['address'] = address_dict
#         # cart = CartDao.get_cart(current_user.cart)
#         # cart_items = cart.get_cart_items()
#
#         return render_template("consumer/address.html", form=consumer_address_form, latitude=latitude,
#                                longitude=longitude)
#     else:
#         address_dict = {}
#         with shelve.open('address.db', 'c') as db:
#             try:
#                 address_dict = db['address']
#                 consumer = address_dict.get(current_user.account_id)
#                 consumer_address_form.consumer_address.data = consumer.address
#                 latitude = consumer.get_latitude()
#                 longitude = consumer.get_longitude()
#                 print(consumer.address)
#             except Exception as e:
#                 logging.error('address: unable to display address due to %s in db' % e)
#
#         cart = CartDao.get_cart(current_user.cart)
#         cart_items = cart.get_cart_items()
#
#         for item in cart_items:
#             print(item.food.name)
#             print(item.qty)
#         return render_template("consumer/address.html", cart=cart, cart_items=cart_items,
#                                count=len(cart_items), form=consumer_address_form, latitude=latitude, longitude=longitude)
#
#
