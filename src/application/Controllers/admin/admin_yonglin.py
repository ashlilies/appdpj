from flask import render_template, request, redirect, url_for
import os.path

from flask_login import login_required, current_user

from application import app
from application.Controllers.admin.admin_ashlee import admin_side
from application.Models.Admin import *
from application.Models.Certification import Certification
from application.Models.Transaction import Transaction
from werkzeug.utils import secure_filename
import shelve, os


# <------------------------- YONG LIN ------------------------------>
# YL: for transactions -- creating of dummy data
@app.route("/admin/transaction/createExampleTransactions")
@admin_side
@login_required
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
@admin_side
@login_required
def admin_transaction():
    # read transactions from db
    with shelve.open('transaction', 'c') as db:
        if 'shop_transactions' in db:
            transaction_list = db['shop_transactions']
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
@admin_side
@login_required
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
@admin_side
@login_required
def test_upload():
    return render_template("admin/certification.html")


@app.route('/admin/uploader', methods=['GET', 'POST'])
@admin_side
@login_required
def uploader():
    certification_dict = {}
    nb = 'NIL'
    npnl = 'NIL'
    if request.method == 'POST':
        with shelve.open('certification', 'c') as handle:
            try:
                certification_dict = handle['certification']
            except Exception as e:
                logging.error("uploader: ""certification.db (%s)" % e)

            # create new class object
            cert = Certification()
            # cert.id = current_user.restaurant_id

            # get values in checkboxes
            certchecks = request.form.getlist('certCheck')
            print(certchecks)
            for i in certchecks:
                if i == 'NoPorkNoLard':
                    npnl = 'YES'
                elif i == 'NoBeef':
                    nb = 'YES'
                else:
                    print('something is wrong')
            cert.noPorknoLard = npnl
            cert.noBeef = nb

            # HYGIENE CERTIFICATE
            hygiene = request.files['hygieneDocument']  # getting the file from the form
            hygieneFile = secure_filename(hygiene.filename)
            app.config['UPLOADED_HYGIENE'] = f'application/static/uploads/restaurantCertification/hygiene/{cert.id}/'
            if hygieneFile != '':
                os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_HYGIENE'])), exist_ok=True)
                hygiene.save(os.path.join(os.getcwd(), app.config['UPLOADED_HYGIENE']) + hygieneFile)
                logging.info('Hygiene -- file uploaded successfully')
                cert.hygiene_cert = f"application/static/uploads/restaurantCertification/hygiene/{cert.id}/{hygieneFile}"

            # HALAL CERTIFICATE
            halal = request.files['halalDocument']
            halalFile = secure_filename(halal.filename)
            if halal.filename != "":
                app.config['UPLOADED_HALAL'] = f'application/static/uploads/restaurantCertification/halal/{cert.id}/'
                os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_HALAL'])), exist_ok=True)
                halal.save(os.path.join(os.getcwd(), app.config['UPLOADED_HALAL']) + halalFile)
                logging.info('Halal -- file uploaded successfully')
                cert.halal_cert = f"application/static/uploads/restaurantCertification/halal/{cert.id}/{halalFile}"
            else:
                cert.halal_cert = ''

            # VEGETARIAN CERTIFICATE
            vegetarian = request.files['vegetarianDocument']
            vegetarianFile = secure_filename(vegetarian.filename)
            if vegetarian.filename != "":
                app.config[
                    'UPLOADED_VEGETARIAN'] = f'application/static/uploads/restaurantCertification/vegetarian/{cert.id}/'
                os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_VEGETARIAN'])),
                            exist_ok=True)
                vegetarian.save(os.path.join(os.getcwd(), app.config['UPLOADED_VEGETARIAN']) + vegetarianFile)
                logging.info('Vegetarian -- file uploaded successfully')
                cert.vegetarian_cert = f"application/static/uploads/restaurantCertification/vegetarian/{cert.id}/{vegetarianFile}"
            else:
                cert.vegetarian_cert = ''

            # VEGAN CERTIFICATE
            vegan = request.files['veganDocument']
            veganFile = secure_filename(vegan.filename)
            if vegan.filename != "":
                app.config['UPLOADED_VEGAN'] = f'application/static/uploads/restaurantCertification/vegan/{cert.id}/'
                os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_VEGAN'])),
                            exist_ok=True)
                # save document in app.config['UPLOADED_HALAL']
                vegan.save(os.path.join(os.getcwd(), app.config['UPLOADED_VEGAN']) + veganFile)
                logging.info('Vegan -- file uploaded successfully')
                cert.vegan_cert = f"application/static/uploads/restaurantCertification/vegan/{cert.id}/{veganFile}"
            else:
                cert.vegan_cert = ''

            certification_dict[cert.id] = cert
            handle['certification'] = certification_dict

            for key in certification_dict:
                food = certification_dict.get(key)
                print(food)
                print(food.id)
                print(food.halal_cert)
                print(food.vegetarian_cert)
                print(food.vegan_cert)

        return redirect(url_for('read_cert'))


@app.route("/admin/certification")
@admin_side
@login_required
def read_cert():
    certification_dict = {}
    with shelve.open('certification', 'c') as handle:
        try:
            if 'certification' in handle:
                certification_dict = handle['certification']
            else:
                handle['certification'] = certification_dict
                print(certification_dict)
                logging.info("read_cert: nothing found in database, starting empty")
        except Exception as e:
            logging.error("read_cert: error opening db (%s)" % e)

        certificate_list = []
        for key in certification_dict:
            restaurant = certification_dict.get(current_user.restaurant_id)
            if key == current_user.restaurant_id:
                certificate_list = []
                certificate_list.append(restaurant)
                print(certificate_list)

        # certificate_list = []
        # for key in certification_dict:
        #     food = certification_dict.get(key)
        #     certificate_list.append(food)

    return render_template('admin/certification2.html', id=id, certificate_list=certificate_list)


# YL: for certification -- Update certification [if it expires/needs to be updated] (U in CRUD)
# TODO: CHECK IF THE FILES ARE THE SAME AND UPDATE THE DETAILS
@app.route('/admin/updateCertification/<int:id>', methods=['GET', 'POST'])
@admin_side
@login_required
def update_cert(id):
    nb = 'NIL'
    npnl = 'NIL'
    print(id)
    if request.method == 'POST':
        certification_dict = {}
        try:
            with shelve.open('certification', "c") as db:
                certification_dict = db['certification']

                cert = certification_dict.get(id)

                # get values from checkboxes
                certchecks = request.form.getlist('certCheck')
                print(certchecks)
                for i in certchecks:
                    if i == 'NoPorkNoLard':
                        npnl = 'YES'
                    elif i == 'NoBeef':
                        nb = 'YES'

                cert.noPorknoLard = npnl
                cert.noBeef = nb

                # HYGIENE DOCUMENT
                hygiene = request.files['hygieneDocument']
                hygieneFile = secure_filename(hygiene.filename)
                app.config[
                    'UPLOADED_HYGIENE'] = f'application/static/uploads/restaurantCertification/hygiene/{cert.id}/'
                os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_HYGIENE'])), exist_ok=True)
                hygiene.save(os.path.join(os.path.join(os.getcwd(), app.config['UPLOADED_HYGIENE']) + hygieneFile))
                if cert.hygiene_cert != '':
                    # unlinking existing hygiene doc file
                    if os.path.exists(cert.hygiene_cert):
                        os.remove(cert.hygiene_cert)
                        logging.info('Successfully removed existing hygiene document')
                    cert.hygiene_cert = f"application/static/uploads/restaurantCertification/hygiene/{cert.id}/{hygieneFile}"
                else:
                    cert.hygiene_cert = ''

                # HALAL DOCUMENT
                halal = request.files['halalDocument']
                halalFile = secure_filename(halal.filename)
                if halal.filename != '':
                    # saving of new file
                    app.config[
                        'UPLOADED_HALAL'] = f'application/static/uploads/restaurantCertification/halal/{cert.id}/'
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_HALAL'])),
                                exist_ok=True)
                    halal.save(os.path.join(os.path.join(os.getcwd(), app.config['UPLOADED_HALAL']) + halalFile))
                    # deleting of existing file
                    if os.path.exists(cert.halal_cert):
                        os.remove(cert.halal_cert)
                        logging.info('Successfully removed existing halal document')
                    cert.halal_cert = f"application/static/uploads/restaurantCertification/halal/{cert.id}/{halalFile}"

                # VEGETARIAN DOCUMENT
                vegetarian = request.files['vegetarianDocument']
                vegetarianFile = secure_filename(vegetarian.filename)
                if vegetarian.filename != '':
                    app.config[
                        'UPLOADED_VEGETARIAN'] = f'application/static/uploads/restaurantCertification/vegetarian/{cert.id}/'
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_VEGETARIAN'])),
                                exist_ok=True)
                    vegetarian.save(
                        os.path.join(os.path.join(os.getcwd(), app.config['UPLOADED_VEGETARIAN']) + vegetarianFile))
                    # deleting of existing file
                    if os.path.exists(cert.vegetarian_cert):
                        os.remove(cert.vegetarian_cert)
                        logging.info('Successfully removed existing vegetarian document')
                    cert.vegetarian_cert = f"application/static/uploads/restaurantCertification/vegetarian/{cert.id}/{vegetarianFile}"
                else:
                    cert.vegetarian_cert = ''

                # VEGAN DOCUMENT
                vegan = request.files['veganDocument']
                veganFile = secure_filename(vegan.filename)
                if vegan.filename != '':
                    # saving of new file
                    app.config[
                        'UPLOADED_VEGAN'] = f'application/static/uploads/restaurantCertification/vegan/{cert.id}/'
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_VEGAN'])),
                                exist_ok=True)
                    vegan.save(os.path.join(os.path.join(os.getcwd(), app.config['UPLOADED_VEGAN']) + veganFile))
                    # deleting of existing file
                    if os.path.exists(cert.vegan_cert):
                        os.remove(cert.vegan_cert)
                        logging.info('Successfully removed existing vegan document')
                    cert.vegan_cert = f"application/static/uploads/restaurantCertification/vegan/{cert.id}/{veganFile}"
                else:
                    cert.vegan_cert = ''

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
@admin_side
@login_required
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
