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
    address_form = ConsumerAddressForm(request.form)

    if request.method == 'POST' and consumer_address_form.validate():
        # checks if consumer address has already been inputted by consumer
        if not current_user.consumer_id:
            # todo: integrate customer_id into this '1' data
            consumer = AddressDao.create_address(1, address_form.consumer_homeAddress.data,
                                      address_form.consumer_workAddress.data,
                                      address_form.consumer_otherAddress.data
                                      )
            current_user.consumer_id = consumer.id
        else:
            consumer = AddressDao.get_user_addresss(current_user.consumer_id)
            AddressDao.update_address(1, address_form.consumer_homeAddress.data,
                                      address_form.consumer_workAddress.data,
                                      address_form.consumer_otherAddress.data
                                      )

        return redirect(url_for("consumer_home"))
    if current_user.consumer_id is not None:
        consumer = AddressDao.get_user_addresss(current_user.consumer_id)
        address_form.consumer_homeAddress.data = consumer.homeAddress
        address_form.consumer_workAddress.data = consumer.workAddress
        address_form.consumer_otherAddress.data = consumer.otherAddress

    return render_template("consumer/address.html", form=address_form)

# ADDRESS UPDATE FIELD (form field)
# @app.route("/updateAddress")
# def consumer_retrieve_reviews():
#     return render_template("consumer/reviews/myReviews.html")
