from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app

# <------------------------- YONG LIN ------------------------------>
# shopping cart
# displaying of the available food
# todo: find bootstrap examples of shopping cart, and then make the css look good before getting the data etc.
# urgent but can only do after integration of everything

# ADDRESS FIELD (form field)
# todo: something similar to ruri's restaurant details, create, and update tgt
# todo: dropdown box for each individual address? or smt like clara's adding of toppings
from application.Models.Address import ConsumerAddress, AddressDao
from application.consumer_address_form import ConsumerAddressForm


@app.route("/myAddress", methods=["GET", "POST"])
def consumer_myaddress():
    consumer_address_form = ConsumerAddressForm(request.form)
    # controller will be the place where we do all the interaction
    create_address_form = ConsumerAddressForm(request.form)

    if request.method == 'POST' and consumer_address_form.validate():
        AddressDao.create_address(1, create_address_form.consumer_homeAddress.data,
                                  create_address_form.consumer_workAddress.data,
                                  create_address_form.consumer_otherAddress.data)

        return redirect(url_for("consumer_home"))
    else:
        print('i hate appdev')

    return render_template("consumer/address.html", form=create_address_form)

# ADDRESS UPDATE FIELD (form field)
# @app.route("/updateAddress")
# def consumer_retrieve_reviews():
#     return render_template("consumer/reviews/myReviews.html")
