import datetime
import traceback

import flask
from flask import render_template, request, redirect, url_for, session, flash, Flask
from flask_login import logout_user, login_required, current_user
import os
import os.path

from application.CouponForms import CreateCouponForm
from application.Models.Admin import *
from application.Models.CouponSystem import CouponSystem
from application.Models.Certification import Certification
from application.Models.Food import Food
from application.Models.Restaurant import Restaurant
from application import app, login_manager
from application.Models.Transaction import Transaction
from application.adminAddFoodForm import CreateFoodForm
from werkzeug.utils import secure_filename
import shelve, os
import uuid
from application.rest_details_form import *

# Ruri's imported libraries
import urllib.request
import os
from werkzeug.utils import secure_filename

# <------------------------- YONG LIN ------------------------------>
# YL: for transactions -- creating of dummy data
@app.route("/admin/transaction/createExampleTransactions")
def create_example_transactions():
    # WARNING - Overrides ALL transactions in the db!
    transaction_list = []

    # creating a shelve file with dummy data
    # 1: <account id> ; <user_id> ; <option> ; <price> ; <coupons> , <rating>
    t1 = Transaction()
    t1.account_name = 'Yong Lin'
    t1.set_option('Delivery')
    t1.set_price(50.30)
    t1.set_used_coupons('SPAGETIT')
    t1.set_ratings(2)
    transaction_list.append(t1)

    t2 = Transaction()  # t2
    t2.account_name = 'Ching Chong'
    t2.set_option('Dine-in')
    t2.set_price(80.90)
    t2.set_used_coupons('50PASTA')
    t2.set_ratings(5)
    transaction_list.append(t2)

    t3 = Transaction()  # t3
    t3.account_name = 'Hosea'
    t3.set_option('Delivery')
    t3.set_price(20.10)
    t3.set_used_coupons('50PASTA')
    t3.set_ratings(1)
    transaction_list.append(t3)

    t4 = Transaction()  # t4
    t4.account_name = 'Clara'
    t4.set_option('Delivery')
    t4.set_price(58.30)
    t4.set_used_coupons('SPAGETIT')
    t4.set_ratings(2)
    transaction_list.append(t4)

    t5 = Transaction()  # t5
    t5.account_name = 'Ruri'
    t5.set_option('Dine-in')
    t5.set_price(80.90)
    t5.set_used_coupons('50PASTA')
    t5.set_ratings(3)
    transaction_list.append(t5)

    t6 = Transaction()  # t6
    t6.account_name = 'Ashlee'
    t6.set_option('Delivery')
    t6.set_price(100.10)
    t6.set_used_coupons('50PASTA')
    t6.set_ratings(2)
    transaction_list.append(t6)

    t7 = Transaction()
    t7.account_name = 'Hello'
    t7.set_option('Dine-in')
    t7.set_price(10.90)
    t7.set_used_coupons('50PASTA')
    t7.set_ratings(4)
    transaction_list.append(t7)

    t8 = Transaction()
    t8.account_name = 'Lolita'
    t8.set_option('Delivery')
    t8.set_price(50.30)
    t8.set_used_coupons('SPAGETIT')
    t8.set_ratings(2)
    transaction_list.append(t8)

    t9 = Transaction()  # t2
    t9.account_name = 'Cheryln'
    t9.set_option('Dine-in')
    t9.set_price(80.90)
    t9.set_used_coupons('50PASTA')
    t9.set_ratings(5)
    transaction_list.append(t9)

    t10 = Transaction()  # t4
    t10.account_name = 'Swee Koon'
    t10.set_option('Delivery')
    t10.set_price(58.30)
    t10.set_used_coupons('SPAGETIT')
    t10.set_ratings(2)
    transaction_list.append(t10)

    t11 = Transaction()  # t5
    t11.account_name = 'Adrian'
    t11.set_option('Dine-in')
    t11.set_price(80.90)
    t11.set_used_coupons('50PASTA')
    t11.set_ratings(3)
    transaction_list.append(t11)

    t12 = Transaction()  # t6
    t12.account_name = 'Ryan'
    t12.set_option('Delivery')
    t12.set_price(100.10)
    t12.set_used_coupons('50PASTA')
    t12.set_ratings(2)
    transaction_list.append(t12)

    t13 = Transaction()
    t13.account_name = 'Sammi'
    t13.set_option('Dine-in')
    t13.set_price(10.90)
    t13.set_used_coupons('50PASTA')
    t13.set_ratings(4)
    transaction_list.append(t13)

    t14 = Transaction()  # t4
    t14.account_name = 'Vianna'
    t14.set_option('Delivery')
    t14.set_price(58.30)
    t14.set_used_coupons('SPAGETIT')
    t14.set_ratings(2)
    transaction_list.append(t14)

    t15 = Transaction()  # t5
    t15.account_name = 'Dylan'
    t15.set_option('Dine-in')
    t15.set_price(80.90)
    t15.set_used_coupons('50PASTA')
    t15.set_ratings(3)
    transaction_list.append(t15)

    t16 = Transaction()  # t6
    t16.account_name = 'Chit Boon'
    t16.set_option('Delivery')
    t16.set_price(100.10)
    t16.set_used_coupons('50PASTA')
    t16.set_ratings(2)
    transaction_list.append(t16)

    t17 = Transaction()
    t17.account_name = 'Kit Fan'
    t17.set_option('Dine-in')
    t17.set_price(10.90)
    t17.set_used_coupons('50PASTA')
    t17.set_ratings(4)
    transaction_list.append(t17)

    t18 = Transaction()
    t18.account_name = 'Gabriel Choo'
    t18.set_option('Delivery')
    t18.set_price(50.30)
    t18.set_used_coupons('SPAGETIT')
    t18.set_ratings(2)
    transaction_list.append(t18)

    t19 = Transaction()  # t2
    t19.account_name = 'Bryan Hoo'
    t19.set_option('Dine-in')
    t19.set_price(80.90)
    t19.set_used_coupons('50PASTA')
    t19.set_ratings(5)
    transaction_list.append(t19)

    t20 = Transaction()  # t3
    t20.account_name = 'Yuen Loong'
    t20.set_option('Delivery')
    t20.set_price(20.10)
    t20.set_used_coupons('50PASTA')
    t20.set_ratings(1)
    transaction_list.append(t20)

    # writing to the database
    with shelve.open('transaction', "c") as db:
        try:
            db['shop_transactions'] = transaction_list
        except Exception as e:
            logging.error("create_example_transactions: error writing to db (%s)" % e)

    return redirect(url_for("admin_transaction"))


# YL: for transactions -- reading of data and displaying (R in CRUD)
@app.route("/admin/transaction")
def admin_transaction():
    # read transactions from db
    with shelve.open('transaction', 'c') as db:
        if 'shop_transactions' in db:
            transaction_list = db['shop_transactions']
            print(db['shop_transactions'])
            logging.info("admin_transaction: reading from db['shop_transactions']"
                         ", %d elems" % len(db["shop_transactions"]))
        else:
            logging.info("admin_transaction: nothing found in db, starting empty")
            transaction_list = []

    def get_transaction_by_id(transaction_id):  # debug
        for transaction in transaction_list:
            if transaction_id == transaction.count_id:
                return transaction

    return render_template("admin/transaction.html",
                           count=len(transaction_list),
                           transaction_list=transaction_list)


# YL: for transactions -- soft delete (D in CRUD)
# soft delete -> restaurant can soft delete transactions jic if the transaction is cancelled
@app.route('/admin/transaction/delete/<transaction_id>')
def delete_transaction(transaction_id):
    transaction_id = int(transaction_id)

    transaction_list = []
    with shelve.open('transaction', 'c') as db:
        for transaction in db['shop_transactions']:
            transaction_list.append(transaction)

    def get_transaction_by_id(t_id):  # debug
        for t in transaction_list:
            if t_id == t.count_id:
                return t

    logging.info("delete_transaction: deleted transaction with id %d"
                 % transaction_id)

    # set instance attribute 'deleted' of Transaction.py = False
    get_transaction_by_id(transaction_id).deleted = True

    # writeback to shelve
    with shelve.open('transaction', 'c') as db:
        db["shop_transactions"] = transaction_list

    return redirect(url_for('admin_transaction'))


# certification -- xu yong lin
# YL: for certification -- form (C in CRUD)
@app.route("/admin/uploadCertification")
def test_upload():
    return render_template("admin/certification.html")

# def upload_cert():
#     certification_dict = {}
#     nb = 'NIL'
#     npnl = 'NIL'
#     if request.method == 'POST':
#
#         with shelve.open(DB_NAME, 'c') as db:
#             try:
#                 certification_dict = db['certification']
#                 print(certification_dict)
#             except Exception as e:
#                 logging.error("Error in retrieving certificate from ""certification.db (%s)" % e)
#             # create a new Certification Object
#             certchecks = request.form.getlist('certCheck')
#             print(certchecks)
#             for i in certchecks:
#                 if 'NoBeef' in certchecks:
#                     nb = 'YES'
#                 elif 'NoPorkNoLard' in certchecks:
#                     npnl = 'Yes'
#                 else:
#                     print('something is wrong ')
#             print(npnl)
#             print(nb)
#
#             certification = Certification(request.form["hygieneDocument"], request.form["halalDocument"],
#                                           request.form["vegetarianDocument"], request.form["veganDocument"],
#                                           npnl, nb)
#             certification_dict[certification.id] = certification
#             db['certification'] = certification_dict
#
#             return redirect(url_for('read_cert'))
#         # update: cert dict => get the correct cert by id
#
#     return render_template("admin/certification.html")


# YL: for certification -- reading of data and displaying it to myRestaurant (C in CRUD)

@app.route('/admin/uploader', methods=['GET', 'POST'])
def uploader():
    certification_dict = {}
    # nb = 'NIL'
    # npnl = 'NIL'
    if request.method == 'POST':
        # todo: add different routes for hygiene, halal, vegetarian, vegan
        # todo: add other file's file saving
        with shelve.open('certification', 'c') as handle:
            try:
                certification_dict = handle['certification']
                print(certification_dict)
            except Exception as e:
                logging.error("uploader: ""certification.db (%s)" % e)

            cert = Certification()
            app.config['UPLOADED_PDF'] = f'application/static/restaurantCertification/hygiene/{cert.id}/'
            # print("931: %s" % halal)
            f = request.files['hygieneDocument'] # getting the file from the form
            filename = secure_filename(f.filename)

            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])), exist_ok=True)

            # save document in app.config['UPLOAD_PDF']
            f.save(os.path.join(os.getcwd(), app.config['UPLOADED_PDF']) + filename)

            logging.info('file uploaded successfully')

            # create new object
            cert.hygiene_cert = f"application/static/restaurantCertification/hygiene/{cert.id}/{filename}"

            # HALAL CERTIFICATE
            halal = request.files['halalDocument']
            if halal.filename != "":
                # TODO: Add logic to save the file to filesystem and the Certification object here
                pass

            # cert = Certification(f)
            certification_dict[cert.id] = cert
            handle['certification'] = certification_dict

        return redirect(url_for('read_cert'))

@app.route("/admin/certification")
def read_cert():
    # todo: include session id and insert the id in order to read the ind restaurant cert
    certification_dict = {}
    with shelve.open('certification', 'c') as handle:
        try:
            if 'certification' in handle:
                certification_dict = handle['certification']
                print('existing ',certification_dict)
                error = 'line 976 nothing wrong here'
                print(error)
                for key in certification_dict:
                    cert = certification_dict.get(key)
                    print('cert: ',cert)
                error2 = 'line 980 nothing wrong here'
                print(error2)
                # cert.hygiene_cert = f"application/static/restaurantCertification/hygiene/{cert.id}/"
            else:
                handle['certification'] = certification_dict
                print(certification_dict)
                logging.info("read_cert: nothing found in database, starting empty")
        except Exception as e:
            logging.error("read_cert: error opening db (%s)" % e)

        certificate_list = []
        for key in certification_dict:
            food = certification_dict.get(key)
            certificate_list.append(food)

    return render_template('admin/certification2.html', id=id, certificate_list=certificate_list)


# @app.route("/admin/certification")
# def read_cert():
#     # todo: display the pdf file via url_for
#     certification_dict = {}
#     with shelve.open('certification', "c") as db:
#         try:
#             if 'certification' in db:
#                 certification_dict = db['certification']
#
#             else:
#                 db['certification'] = certification_dict
#                 print(certification_dict)
#                 logging.info("read_cert: nothing found in db, starting empty")
#         except Exception as e:
#             logging.error("read_cert: error opening db (%s)" % e)
#
#         certificate_list = []
#         for key in certification_dict:
#             food = certification_dict.get(key)
#             certificate_list.append(food)
#
#     return render_template("admin/certification2.html", certificate_list=certificate_list)


# YL: for certification -- Update certification [if it expires/needs to be updated] (U in CRUD)
# TODO: REDIRECT BACK TO FORM IN 'C IN CRUD'
# TODO: CHECK IF THE FILES ARE THE SAME AND UPDATE THE DETAILS
@app.route('/admin/updateCertification/<int:id>', methods=['GET', 'POST'])
def update_cert(id):
    nb = 'NIL'
    npnl = 'NIL'

    if request.method == 'POST':
        certification_dict = {}
        try:
            with shelve.open('certification', "c") as db:
                certification_dict = db['certification']

                # updating the information
                certchecks = request.form.getlist('certCheck')
                for i in certchecks:
                    if 'NoBeef' in certchecks:
                        nb = 'YES'
                    elif 'No Pork No Lard' in certchecks:
                        npnl = 'YES'
                    else:
                        print('something is wrong ')

                certification = certification_dict.get(id)
                # inset values of the updated thing inside
                certification.hygiene_cert = request.form["hygieneDocument"]
                certification.halal_cert = request.form["halalDocument"]
                certification.vegetarian_cert = request.form["vegetarianDocument"]
                certification.vegan_cert = request.form["veganDocument"]
                certification.noPorknoLard = npnl
                certification.noBeef = nb
                print(certification)

                # writeback
                db['certification'] = certification_dict
        except Exception as e:
            logging.error("Error in retrieving certificate from ""certification.db (%s)" % e)

        return redirect(url_for('read_cert'))
    else:
        certification_dict = {}
        id_list = []
        print('I am reading from shelve')
        try:
            # reading to display the pre-existing inputs
            with shelve.open('certification', "c") as db:
                certification_dict = db['certification']
        except Exception as e:
            logging.error("Error in retrieving certificate from ""certification.db (%s)" % e)

        c = certification_dict.get(id)
        id_list.append(c)
        print(c.hygiene_cert)
        return render_template('admin/updateCertification.html', id_list=id_list)


# YL: for certification -- Delete (D in CRUD)
@app.route('/deleteCertification/<int:id>', methods=['POST'])
def delete_cert(id):
    with shelve.open('certification', 'w') as db:
        try:
            certification_dict = db['certification']
            if id in certification_dict:
                certification_dict.pop(id)
            db['certification'] = certification_dict
        except Exception as e:
            logging.error("delete_food: error opening db (%s)" % e)

    return redirect(url_for('read_cert'))


# def upload_cert():
#     i = 1
#     certification_form = DocumentUploadForm(request.form)
#     certifications_dict = {}
#     if request.method == 'POST' and certification_form.validate():
#         db = shelve.open(DB_NAME, 'c')
#         try:
#             certifications_dict = db['certification']
#         except Exception as e:
#             logging.error("Error in retrieving Certification from "
#                           "certification.db (%s)" % e)
#
#         certifications_dict[i] = i
#         db['certification'] = certifications_dict
#
#         db.close()
#
#     certification = Certification(request.form["hygieneDocument"])
#
#     # if certification_form.validate_on_submit():
#     #     # file path to save files to:
#     #     assets_dir = os.path.join(os.path.dirname(app.instance_path), 'restaurantCertification')
#     #     # assests_dir ==> C:\Users\yongl\appdpj\src\restaurantCertification
#     #     hygiene = certification_form.hygiene_doc.data
#     #
#     #     # saving
#     #     hygiene.save(os.path.join(assets_dir, 'hygiene', hygiene.filename))
#     #
#     #     logging.info('Document uploaded successfully.')
#     #     return redirect(url_for('admin_home'))
#
#     return render_template("admin/certification2.html")


# @app.route("/admin/certification", methods=['GET', 'POST'])
# def admin_certification():
#     # TODO: FILE UPLOAD, FILE SAVING, SHELVE UPDATE
#     # set upload directory path
#     certification_form = RestaurantCertification()
#     if certification_form.validate_on_submit():
#         assets_dir = os.path.join(os.path.dirname('./static/restaurantCertification'))
#
#         hygiene = certification_form.hygiene_cert.data
#         halal = certification_form.halal_cert.data
#         vegetarian = certification_form.vegetarian_cert.data
#         vegan = certification_form.vegan_cert.data
#
#         # document save
#         # halal.save(os.path.join(app.config['UPLOAD_FOLDER'], halaldoc_name))
#         hygiene.save(os.path.join(assets_dir, '<userid>', hygiene))
#         halal.save(os.path.join(assets_dir, '<userid>', halal))
#         vegetarian.save(os.path.join(assets_dir, '<userid>', vegetarian))
#         vegan.save(os.path.join(assets_dir, '<userid>', vegan))
#
#         # halal.save(os.path.join('/application/static/restaurantCertification', halaldoc_name))
#         # vegetarian.save(
#         #     os.path.join('/application/static/restaurantCertification', vegetariandoc_name))
#         # vegan.save(os.path.join('/application/static/restaurantCertification', vegandoc_name))
#
#         flash('Document uploaded successfully')
#
#         return redirect(url_for('admin_transaction'))
#
#     return render_template("admin/certification.html",
#                            certification_form=certification_form)


