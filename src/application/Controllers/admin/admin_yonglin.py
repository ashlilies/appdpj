import datetime
import traceback

import flask
from flask import render_template, request, redirect, url_for, session, flash, Flask
import os
import os.path

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from application import app
from application.Controllers.admin.admin_ashlee import admin_side
from application.Models.Admin import *
from application.Models.Certification import *
from application.Models.Transaction import *
from application.Controllers.admin.admin_ruri import *
from werkzeug.utils import secure_filename
import shelve, os


# <------------------------- YONG LIN ------------------------------>
# YL: for transactions -- creating of dummy data

# old creating of transaction
@app.route("/admin/transaction/createExampleTransactions")
# @login_required
# @admin_side
def create_example_transactions():
    # WARNING - Overrides ALL transactions in the db!
    transaction_list = []

    # creating a shelve file with dummy data
    # 1: <account id> ; <user_id> ; <option> ; <price> ; <coupons> , <rating>
    # t1 = Transaction()
    # t1.account_name = 'Yong Lin'
    # t1.set_option('Delivery')
    # t1.set_price(50.30)
    # t1.set_used_coupons('SPAGETIT')
    # t1.set_ratings(2)
    # transaction_list.append(t1)
    #
    # t2 = Transaction()  # t2
    # t2.account_name = 'Ching Chong'
    # t2.set_option('Dine-in')
    # t2.set_price(80.90)
    # t2.set_used_coupons('50PASTA')
    # t2.set_ratings(5)
    # transaction_list.append(t2)
    #
    # t3 = Transaction()  # t3
    # t3.account_name = 'Hosea'
    # t3.set_option('Delivery')
    # t3.set_price(20.10)
    # t3.set_used_coupons('50PASTA')
    # t3.set_ratings(1)
    # transaction_list.append(t3)
    #
    # t4 = Transaction()  # t4
    # t4.account_name = 'Clara'
    # t4.set_option('Delivery')
    # t4.set_price(58.30)
    # t4.set_used_coupons('SPAGETIT')
    # t4.set_ratings(2)
    # transaction_list.append(t4)
    #
    # t5 = Transaction()  # t5
    # t5.account_name = 'Ruri'
    # t5.set_option('Dine-in')
    # t5.set_price(80.90)
    # t5.set_used_coupons('50PASTA')
    # t5.set_ratings(3)
    # transaction_list.append(t5)
    #
    # t6 = Transaction()  # t6
    # t6.account_name = 'Ashlee'
    # t6.set_option('Delivery')
    # t6.set_price(100.10)
    # t6.set_used_coupons('50PASTA')
    # t6.set_ratings(2)
    # transaction_list.append(t6)
    #
    # t7 = Transaction()
    # t7.account_name = 'Hello'
    # t7.set_option('Dine-in')
    # t7.set_price(10.90)
    # t7.set_used_coupons('50PASTA')
    # t7.set_ratings(4)
    # transaction_list.append(t7)
    #
    # t8 = Transaction()
    # t8.account_name = 'Lolita'
    # t8.set_option('Delivery')
    # t8.set_price(50.30)
    # t8.set_used_coupons('SPAGETIT')
    # t8.set_ratings(2)
    # transaction_list.append(t8)
    #
    # t9 = Transaction()  # t2
    # t9.account_name = 'Cheryln'
    # t9.set_option('Dine-in')
    # t9.set_price(80.90)
    # t9.set_used_coupons('50PASTA')
    # t9.set_ratings(5)
    # transaction_list.append(t9)
    #
    # t10 = Transaction()  # t4
    # t10.account_name = 'Swee Koon'
    # t10.set_option('Delivery')
    # t10.set_price(58.30)
    # t10.set_used_coupons('SPAGETIT')
    # t10.set_ratings(2)
    # transaction_list.append(t10)
    #
    # t11 = Transaction()  # t5
    # t11.account_name = 'Adrian'
    # t11.set_option('Dine-in')
    # t11.set_price(80.90)
    # t11.set_used_coupons('50PASTA')
    # t11.set_ratings(3)
    # transaction_list.append(t11)
    #
    # t12 = Transaction()  # t6
    # t12.account_name = 'Ryan'
    # t12.set_option('Delivery')
    # t12.set_price(100.10)
    # t12.set_used_coupons('50PASTA')
    # t12.set_ratings(2)
    # transaction_list.append(t12)
    #
    # t13 = Transaction()
    # t13.account_name = 'Sammi'
    # t13.set_option('Dine-in')
    # t13.set_price(10.90)
    # t13.set_used_coupons('50PASTA')
    # t13.set_ratings(4)
    # transaction_list.append(t13)
    #
    # t14 = Transaction()  # t4
    # t14.account_name = 'Vianna'
    # t14.set_option('Delivery')
    # t14.set_price(58.30)
    # t14.set_used_coupons('SPAGETIT')
    # t14.set_ratings(2)
    # transaction_list.append(t14)
    #
    # t15 = Transaction()  # t5
    # t15.account_name = 'Dylan'
    # t15.set_option('Dine-in')
    # t15.set_price(80.90)
    # t15.set_used_coupons('50PASTA')
    # t15.set_ratings(3)
    # transaction_list.append(t15)
    #
    # t16 = Transaction()  # t6
    # t16.account_name = 'Chit Boon'
    # t16.set_option('Delivery')
    # t16.set_price(100.10)
    # t16.set_used_coupons('50PASTA')
    # t16.set_ratings(2)
    # transaction_list.append(t16)
    #
    # t17 = Transaction()
    # t17.account_name = 'Kit Fan'
    # t17.set_option('Dine-in')
    # t17.set_price(10.90)
    # t17.set_used_coupons('50PASTA')
    # t17.set_ratings(4)
    # transaction_list.append(t17)
    #
    # t18 = Transaction()
    # t18.account_name = 'Gabriel Choo'
    # t18.set_option('Delivery')
    # t18.set_price(50.30)
    # t18.set_used_coupons('SPAGETIT')
    # t18.set_ratings(2)
    # transaction_list.append(t18)
    #
    t19 = Transaction()  # t2
    name19 = 'Yuen Loong'
    option19 = 'Delivery'
    price19 = 20.10
    coupon19 = '50PASTA'
    rating19 = 1
    t19.new_transaction(name19, option19, price19, coupon19, rating19)

    t20 = Transaction()
    name20 = 'Yuen Loong'
    option20 = 'Delivery'
    price20 = 20.10
    coupon20 = '50PASTA'
    rating20 = 1
    t20.new_transaction(name20, option20, price20, coupon20, rating20)

    return redirect(url_for("admin_transaction"))


# YL: for transactions -- reading of data and displaying (R in CRUD)
@app.route("/admin/transaction")
# @login_required
# @admin_side
def admin_transaction():
    # read transactions from db
    # with shelve.open('transaction_db', 'c') as db:
    #     if 'shop_transactions' in db:
    #         transaction_list = db['shop_transactions']
    #         logging.info("admin_transaction: reading from db['shop_transactions']"
    #                      ", %d elems" % len(db["shop_transactions"]))
    #     else:
    #         logging.info("admin_transaction: nothing found in db, starting empty")
    #         transaction_list = []
    #
    # def get_transaction_by_id(transaction_id):  # debug
    #     for transaction in transaction_list:
    #         if transaction_id == transaction.count_id:
    #             return transaction
    transaction_system_id = current_user.transaction_system_id
    # either current_user = None OR
    # transaction_system _id  has some spelling error
    transaction_system = Transaction.query(transaction_system_id)
    transaction_list = transaction_system.get_all_transaction()
    count = len(transaction_list)

    # return render_template("admin/transaction.html",
    #                        count=len(transaction_list),
    #                        transaction_list=transaction_list)
    return render_template("admin/transaction.html",
                           transaction_list=transaction_list,
                           count=count)



# YL: for transactions -- soft delete (D in CRUD)
# soft delete -> restaurant can soft delete transactions jic if the transaction is cancelled
@app.route('/admin/transaction/delete/<transaction_id>')
def delete_transaction(transaction_id):
    # todo: replace with flask-login
    # if not logged in, nd to log in first
    transaction_id = int(transaction_id)

    #
    # transaction_list = []
    # with shelve.open('transaction', 'c') as db:
    #     for transaction in db['shop_transactions']:
    #         transaction_list.append(transaction)
    #
    # def get_transaction_by_id(t_id):  # debug
    #     for t in transaction_list:
    #         if t_id == t.count_id:
    #             return t
    #
    # logging.info("delete_transaction: deleted transaction with id %d"
    #              % transaction_id)
    #
    # # set instance attribute 'deleted' of Transaction.py = False
    # get_transaction_by_id(transaction_id).deleted = True
    #
    # # writeback to shelve
    # with shelve.open('transaction', 'c') as db:
    #     db["shop_transactions"] = transaction_list

    return redirect(url_for('admin_transaction'))


# certification -- xu yong lin
# YL: for certification -- form (C in CRUD)
@app.route("/admin/uploadCertification")
@login_required
@admin_side
def test_upload():
    return render_template("admin/certification.html")


@app.route('/admin/uploader', methods=['GET', 'POST'])
@login_required
@admin_side
def uploader():
    nb = 'NIL'
    npnl = 'NIL'
    if request.method == 'POST':
        # restaurant_id = str(current_user.restaurant_id)
        # print('restaurant_id: ',restaurant_id) # error: restaurant_id = None??
        # add_cert = Certification.query(restaurant_id) # just for the id only
        cert = Restaurant()
        # should be like this...


        cert_id = cert.id
        # current_user.certification_system_id = cert_id
        print('current.cert_id: ', cert_id)
        # ERROR OCCURS HERE: WHY IS ADD_CERT RETURNING NONE
        add_cert = Certification.query(cert_id)
        print('add_cert: ',add_cert)

        certchecks = request.form.getlist('certCheck')
        for i in certchecks:
            if i == 'NoPorkNoLard':
                npnl = 'YES'
            elif i == 'NoBeef':
                nb = 'YES'
        print('line 296; nb', nb)
        print('line 297; npnl', npnl)

        app.config['UPLOADED_PDF'] = f'application/static/restaurantCertification/{cert_id}/'

        # file saving -- for hygiene, halal, vegetarian, vegan
        hygiene = request.files['hygieneDocument']
        hygieneFile = secure_filename(hygiene.filename)
        os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])), exist_ok=True)
        hygiene.save(os.path.join(os.getcwd(), app.config[
            'UPLOADED_PDF']) + hygieneFile)
        logging.info('Hygiene -- file uploaded successfully')
        save_hygiene = f"application/static/restaurantCertification/{cert_id}/{hygieneFile}"

        halal = request.files['halalDocument']
        halalFile = secure_filename(halal.filename)
        if halal.filename != "":
            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])), exist_ok=True)
            halal.save(os.path.join(os.getcwd(), app.config['UPLOADED_PDF']) + halalFile)
            logging.info('Halal -- file uploaded successfully')
            save_halal = f"application/static/restaurantCertification/{cert_id}/{halalFile}"
        else:
            save_halal = ''

        vegetarian = request.files['vegetarianDocument']
        vegetarianFile = secure_filename(vegetarian.filename)
        if vegetarian.filename != "":
            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])),
                        exist_ok=True)
            vegetarian.save(os.path.join(os.getcwd(), app.config['UPLOADED_PDF']) + vegetarianFile)
            logging.info('Vegetarian -- file uploaded successfully')
            save_vegetarian = f"application/static/restaurantCertification/{cert_id}/{vegetarianFile}"
        else:
            save_vegetarian = ''

        vegan = request.files['veganDocument']
        veganFile = secure_filename(vegan.filename)
        if vegan.filename != "":
            # TODO: Add logic to save the file to filesystem and the Certification object here
            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])),
                        exist_ok=True)
            vegan.save(os.path.join(os.getcwd(), app.config['UPLOADED_PDF']) + veganFile)
            logging.info('Vegan -- file uploaded successfully')
            save_vegan = f"application/static/restaurantCertification/{cert_id}/{veganFile}"
        else:
            save_vegan = ''

        # 'NoneType' object has no attribute 'create_res_cert'
        add_cert.create_res_cert(cert_id, save_hygiene, save_halal, save_vegetarian, save_vegan, npnl, nb)

        return redirect(url_for('admin_certificate_management'))


@app.route("/admin/certification")
def admin_certificate_management(restaurant_id, cert_list):
    # cert = Certification.query(restaurant_id)
    # print(cert)
    # cert = Certification()
    cert_system_id = current_user.restaurant_id

    cert_system = Certification.query(cert_system_id)
    cert_list = cert_system.get_cert()
    count = len(cert_list)
    return render_template('admin/certification2.html', cert_list=cert_list,
                           count=count)


# def read_cert():
#     # todo: include session id and insert the id in order to read the ind restaurant cert
#     certification_dict = {}
#     with shelve.open('certification', 'c') as handle:
#         try:
#             if 'certification' in handle:
#                 certification_dict = handle['certification']
#                 print('existing ', certification_dict)
#             else:
#                 handle['certification'] = certification_dict
#                 logging.info("read_cert: nothing found in database, starting empty")
#         except Exception as e:
#             logging.error("read_cert: error opening db (%s)" % e)
#
#         certificate_list = []
#         for key in certification_dict:
#             food = certification_dict.get(key)
#             certificate_list.append(food)
#
#     return render_template('admin/certification2.html', id=id, certificate_list=certificate_list)


# YL: for certification -- Update certification [if it expires/needs to be updated] (U in CRUD)
@app.route('/admin/updateCertification/<int:id>', methods=['GET', 'POST'])
# @login_required
# @admin_side
def update_cert(id):
    npnl = 'NIL'
    nb = 'NIL'
    if request.method == 'POST':
        # implement shelve logic from Models
        # todo: get id for restaurant here

        certchecks = request.form.getlist('certCheck')
        for i in certchecks:
            if i == 'NoPorkNoLard':
                npnl = 'YES'
            elif i == 'NoBeef':
                nb = 'YES'
        print('line 296; nb', nb)
        print('line 297; npnl', npnl)

        app.config['UPLOADED_PDF'] = f'application/static/restaurantCertification/{restaurant_id}/'

        # file saving -- for hygiene, halal, vegetarian, vegan
        hygiene = request.files['hygieneDocument']
        hygieneFile = secure_filename(hygiene.filename)
        os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])), exist_ok=True)
        hygiene.save(os.path.join(os.getcwd(), app.config[
            'UPLOADED_PDF']) + hygieneFile)
        logging.info('Hygiene -- file uploaded successfully')
        update_hygiene = f"application/static/restaurantCertification/{restaurant_id}/{hygieneFile}"

        halal = request.files['halalDocument']
        halalFile = secure_filename(halal.filename)
        if halal.filename != "":
            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])), exist_ok=True)
            halal.save(os.path.join(os.getcwd(), app.config['UPLOADED_PDF']) + halalFile)
            logging.info('Halal -- file uploaded successfully')
            update_halal = f"application/static/restaurantCertification/{restaurant_id}/{halalFile}"
        else:
            update_halal = ''

        vegetarian = request.files['vegetarianDocument']
        vegetarianFile = secure_filename(vegetarian.filename)
        if vegetarian.filename != "":
            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])),
                        exist_ok=True)
            vegetarian.save(os.path.join(os.getcwd(), app.config['UPLOADED_PDF']) + vegetarianFile)
            logging.info('Vegetarian -- file uploaded successfully')
            update_vegetarian = f"application/static/restaurantCertification/{restaurant_id}/{vegetarianFile}"
        else:
            update_vegetarian = ''

        vegan = request.files['veganDocument']
        veganFile = secure_filename(vegan.filename)
        if vegan.filename != "":
            # TODO: Add logic to save the file to filesystem and the Certification object here
            app.config['UPLOADED_VEGAN'] = f'application/static/restaurantCertification/{restaurant_id}/'
            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])),
                        exist_ok=True)
            vegan.save(os.path.join(os.getcwd(), app.config['UPLOADED_PDF']) + veganFile)
            logging.info('Vegan -- file uploaded successfully')
            update_vegan = f"application/static/restaurantCertification/{restaurant_id}/{veganFile}"
        else:
            update_vegan = ''

        # updating information into the update_res_cert
        cert = update_res_cert(restaurant_id, update_hygiene, update_halal, update_vegetarian, update_vegan, npnl, nb)

        return redirect(url_for('admin_certificate_management'))
    else:
        # implement viewing of restaurant cert details here
        return render_template('admin/updateCertification.html', id_list=id_list)

# def update_cert(id):
#     nb = 'NIL'
#     npnl = 'NIL'
#
#     if request.method == 'POST':
#         certification_dict = {}
#         try:
#             with shelve.open('certification', "c") as db:
#                 certification_dict = db['certification']
#
#                 # create new class object
#                 cert = certification_dict.get(id)
#
#                 # get values from checkboxes
#                 certchecks = request.form.getlist('certChecks')
#                 print(certchecks)
#                 for i in certchecks:
#                     if 'NoPorkNoLard' in certchecks:
#                         npnl = 'YES'
#                     if 'NoBeef' in certchecks:
#                         nb = 'YES'
#                     else:
#                         print('update_cert(line401): something wrong with certchecks')
#                 cert.noPorknoLard = npnl
#                 cert.noBeef = nb
#
#                 # HYGIENE DOCUMENT
#                 hygiene = request.files.get('hygieneDocument')
#                 # saving of new file
#                 hygieneFile = secure_filename(hygiene.filename)
#                 app.config['UPLOADED_HYGIENE'] = f'application/static/restaurantCertification/hygiene/{cert.id}/'
#                 os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_HYGIENE'])), exist_ok=True)
#                 hygiene.save(os.path.join(os.path.join(os.getcwd(), app.config['UPLOADED_HYGIENE']) + hygieneFile))
#                 if cert.hygiene_cert is not None:
#                     # unlinking existing hygiene doc file
#                     if os.path.exists(
#                             f'application/static/restaurantCertification/hygiene/{cert.id}/{cert.hygiene_cert}'):
#                         os.remove(f'application/static/restaurantCertification/hygiene/{cert.id}/{cert.hygiene_cert}')
#                     logging.info('Successfully removed existing hygiene document')
#                 cert.hygiene_cert = f"application/static/restaurantCertification/hygiene/{cert.id}/{hygieneFile}"
#
#                 # HALAL DOCUMENT
#                 halal = request.files.get('halalDocument')
#                 # saving of new file
#                 halalFile = secure_filename(halal.filename)
#                 if halal.filename != '':
#                     # saving of new file
#                     app.config['UPLOADED_HALAL'] = f'application/static/restaurantCertification/halal/{cert.id}/'
#                     os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_HALAL'])),
#                                 exist_ok=True)
#                     halal.save(os.path.join(os.path.join(os.getcwd(), app.config['UPLOADED_HALAL']) + halalFile))
#                     # deleting of existing file
#                     if os.path.exists(f'application/static/restaurantCertification/halal/{cert.id}/{cert.halal_cert}'):
#                         os.remove(f'application/static/restaurantCertification/halal/{cert.id}/{cert.halal_cert}')
#                         logging.info('Successfully removed existing halal document')
#                 cert.halal_cert = f"application/static/restaurantCertification/halal/{cert.id}/{halalFile}"
#
#                 # VEGETARIAN DOCUMENT
#                 vegetarian = request.files.get('vegetarianDocument')
#                 # saving of new file
#                 vegetarianFile = secure_filename(vegetarian.filename)
#                 if vegetarian.filename != '':
#                     # saving of new file
#                     app.config[
#                         'UPLOADED_VEGETARIAN'] = f'application/static/restaurantCertification/vegetarian/{cert.id}/'
#                     os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_VEGETARIAN'])),
#                                 exist_ok=True)
#                     vegetarian.save(
#                         os.path.join(os.path.join(os.getcwd(), app.config['UPLOADED_VEGETARIAN']) + vegetarianFile))
#                     # deleting of existing file
#                     if os.path.exists(
#                             f'application/static/restaurantCertification/vegetarian/{cert.id}/{cert.vegetarian_cert}'):
#                         os.remove(
#                             f'application/static/restaurantCertification/vegetarian/{cert.id}/{cert.vegetarian_cert}')
#                         logging.info('Successfully removed existing vegetarian document')
#                 cert.vegetarian_cert = f"application/static/restaurantCertification/vegetarian/{cert.id}/{vegetarianFile}"
#
#                 # VEGAN DOCUMENT
#                 vegan = request.files.get('veganDocument')
#                 # saving of new file
#                 veganFile = secure_filename(vegan.filename)
#                 if vegan.filename != '':
#                     # saving of new file
#                     app.config['UPLOADED_VEGAN'] = f'application/static/restaurantCertification/vegan/{cert.id}/'
#                     os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_VEGAN'])),
#                                 exist_ok=True)
#                     vegan.save(os.path.join(os.path.join(os.getcwd(), app.config['UPLOADED_VEGAN']) + halalFile))
#                     # deleting of existing file
#                     if os.path.exists(f'application/static/restaurantCertification/vegan/{cert.id}//{cert.vegan_cert}'):
#                         os.remove(f'application/static/restaurantCertification/vegan/{cert.id}//{cert.vegan_cert}')
#                         logging.info('Successfully removed existing vegan document')
#                 cert.vegan_cert = f"application/static/restaurantCertification/vegan/{cert.id}/{veganFile}"
#
#                 # writeback
#                 db['certification'] = certification_dict
#         except Exception as e:
#             logging.error("Error in retrieving certificate from ""certification.db (%s)" % e)
#
#         return redirect(url_for('admin_certificate_management'))
#     else:
#         certification_dict = {}
#         id_list = []
#         print('I am reading from shelve')
#         try:
#             # reading to display the pre-existing inputs
#             with shelve.open('certification', "c") as db:
#                 certification_dict = db['certification']
#         except Exception as e:
#             logging.error("Error in retrieving certificate from ""certification.db (%s)" % e)
#
#         c = certification_dict.get(id)
#         id_list.append(c)
#         print(c.hygiene_cert)
#         return render_template('admin/updateCertification.html', id_list=id_list)


# YL: for certification -- Delete (D in CRUD)
@app.route('/deleteCertification/<int:id>', methods=['POST'])
# @login_required
# @admin_side
def delete_cert(id):
    del_cert = delete_certificate(id)
    return redirect(url_for('admin_certificate_management'))

# def delete_cert(id):
#     with shelve.open('certification', 'w') as db:
#         try:
#             certification_dict = db['certification']
#             if id in certification_dict:
#                 certification_dict.pop(id)
#             db['certification'] = certification_dict
#         except Exception as e:
#             logging.error("delete_food: error opening db (%s)" % e)
#
#     return redirect(url_for('admin_certificate_management'))
