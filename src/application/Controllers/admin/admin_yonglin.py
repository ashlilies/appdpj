from flask import render_template, request, redirect, url_for
import os.path

from flask_login import login_required, current_user

from application import app
from application.Controllers.admin.admin_ashlee import admin_side
from application.Models.Admin import *
from application.Models.Certification import Certification
from application.Models.Transaction import Transaction, TransactionDao
from werkzeug.utils import secure_filename
import shelve, os


# <------------------------- YONG LIN ------------------------------>

@app.route("/admin/create_example_transactions")
@admin_side
@login_required
def create_example_transactions():
    return redirect(url_for("admin_transaction"))

# YL: for transactions -- reading of data and displaying (R in CRUD)
@app.route("/admin/transaction")
@admin_side
@login_required
def admin_transaction():
    restaurant_id = current_user.restaurant_id
    transaction_list = TransactionDao.get_transactions(restaurant_id)

    return render_template("admin/transaction.html",
                           count=len(transaction_list),
                           transaction_list=transaction_list)


@app.route("/admin/transaction/update/<int:transaction_id>", methods=["POST"])
@admin_side
@login_required
def update_transaction_status(transaction_id):
    transaction = TransactionDao.get_transaction(transaction_id)

    if transaction:
        transaction.status = int(request.form.get("transactionStatus", '-1'))

    return redirect(url_for("admin_transaction"))


# YL: for transactions -- soft delete (D in CRUD)
# soft delete -> restaurant can soft delete transactions jic if the transaction is cancelled
@app.route('/admin/transaction/delete/<int:transaction_id>')
@admin_side
@login_required
def delete_transaction(transaction_id):
    TransactionDao.delete_transaction(transaction_id)
    return redirect(url_for('admin_transaction'))


# # certification -- xu yong lin
# @app.route('/admin/cert2')
# @admin_side
# @login_required
# def admin_cert():
#     certification_dict = {}
#     with shelve.open('certification', 'c') as db:
#         try:
#             certification_dict = db["certification"]
#         except Exception as e:
#             logging.error('change_hygiene: certification db has error here (%s)' % e)
#
#         # create new class object
#         cert = Certification()
#         cert.id = current_user.restaurant_id
#
#         certificate_list = []
#         for key in certification_dict:
#             restaurant = certification_dict.get(current_user.restaurant_id)
#             if key == current_user.restaurant_id:
#                 certificate_list = []
#                 certificate_list.append(restaurant)
#                 print(certificate_list)
#
#     return render_template("admin/uploadCertification.html", id=id, certificate_list=certificate_list)
#
#
# @app.route('/admin/cert2Hygiene', methods=['GET', 'POST'])
# @admin_side
# @login_required
# def change_hygiene():
#     cert_dict = {}
#     if request.method == "POST":
#         with shelve.open('certification', 'c') as db:
#             try:
#                 cert_dict = db['certification']
#
#                 restaurant = cert_dict.get(current_user.restaurant_id)
#
#                 hygiene = request.files['hygieneDocument']  # getting the file from the form
#                 hygieneFile = secure_filename(hygiene.filename)
#                 app.config[
#                     'UPLOADED_HYGIENE'] = f'application/static/uploads/restaurantCertification/hygiene/{cert.id}/'
#                 if hygieneFile != '':
#                     os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_HYGIENE'])),
#                                 exist_ok=True)
#                     hygiene.save(os.path.join(os.getcwd(), app.config['UPLOADED_HYGIENE']) + hygieneFile)
#                     logging.info('Hygiene -- file uploaded successfully')
#                     restaurant.hygiene_cert = f"application/static/uploads/restaurantCertification/hygiene/{cert.id}/{hygieneFile}"
#
#             except Exception as e:
#                 logging.error('change_hygiene: certification db has error here (%s)' % e)


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

    def get_current_certifications():
        certification_dict = {}
        with shelve.open('certification', 'c') as handle:
            try:
                if 'certification' in handle:
                    certification_dict = handle['certification']
                else:
                    handle['certification'] = certification_dict
                    print(certification_dict)
                    logging.info(
                        "read_cert: nothing found in database, starting empty")
            except Exception as e:
                logging.error("read_cert: error opening db (%s)" % e)

        return certification_dict



    if request.method == 'POST':
        with shelve.open('certification', 'c') as handle:
            try:
                certification_dict = handle['certification']
            except Exception as e:
                logging.error("uploader: ""certification.db (%s)" % e)

            # create new class object
            cert = Certification()
            orig_cert_obj = get_current_certifications().get(current_user.restaurant_id)
            if orig_cert_obj:
                cert.hygiene_cert = orig_cert_obj.hygiene_cert
                cert.halal_cert = orig_cert_obj.halal_cert
                cert.vegetarian_cert = orig_cert_obj.vegetarian_cert
                cert.vegan_cert = orig_cert_obj.vegan_cert
                cert.noPorknoLard = orig_cert_obj.noPorknoLard
                cert.noBeef = orig_cert_obj.noBeef

            cert.id = current_user.restaurant_id

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
            hygiene = request.files[
                'hygieneDocument']  # getting the file from the form
            if request.files["hygieneDocument"].filename != '':
                hygieneFile = secure_filename(hygiene.filename)
                app.config[
                    'UPLOADED_HYGIENE'] = f'application/static/uploads/restaurantCertification/hygiene/{cert.id}/'
                if hygieneFile != '':
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(
                        app.config['UPLOADED_HYGIENE'])), exist_ok=True)
                    hygiene.save(os.path.join(os.getcwd(), app.config[
                        'UPLOADED_HYGIENE']) + hygieneFile)
                    logging.info('Hygiene -- file uploaded successfully')
                    cert.hygiene_cert = f"application/static/uploads/restaurantCertification/hygiene/{cert.id}/{hygieneFile}"

            # HALAL CERTIFICATE
            halal = request.files['halalDocument']
            if request.files["halalDocument"].filename != '':
                halalFile = secure_filename(halal.filename)
                if halal.filename != "":
                    app.config[
                        'UPLOADED_HALAL'] = f'application/static/uploads/restaurantCertification/halal/{cert.id}/'
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(
                        app.config['UPLOADED_HALAL'])), exist_ok=True)
                    halal.save(os.path.join(os.getcwd(), app.config[
                        'UPLOADED_HALAL']) + halalFile)
                    logging.info('Halal -- file uploaded successfully')
                    cert.halal_cert = f"application/static/uploads/restaurantCertification/halal/{cert.id}/{halalFile}"
                else:
                    cert.halal_cert = ''

            # VEGETARIAN CERTIFICATE
            vegetarian = request.files['vegetarianDocument']
            if request.files["vegetarianDocument"].filename != '':
                vegetarianFile = secure_filename(vegetarian.filename)
                if vegetarian.filename != "":
                    app.config[
                        'UPLOADED_VEGETARIAN'] = f'application/static/uploads/restaurantCertification/vegetarian/{cert.id}/'
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(
                        app.config['UPLOADED_VEGETARIAN'])),
                                exist_ok=True)
                    vegetarian.save(os.path.join(os.getcwd(), app.config[
                        'UPLOADED_VEGETARIAN']) + vegetarianFile)
                    logging.info('Vegetarian -- file uploaded successfully')
                    cert.vegetarian_cert = f"application/static/uploads/restaurantCertification/vegetarian/{cert.id}/{vegetarianFile}"
                else:
                    cert.vegetarian_cert = ''

            # VEGAN CERTIFICATE
            vegan = request.files['veganDocument']
            if request.files["veganDocument"].filename != '':
                veganFile = secure_filename(vegan.filename)
                if vegan.filename != "":
                    app.config[
                        'UPLOADED_VEGAN'] = f'application/static/uploads/restaurantCertification/vegan/{cert.id}/'
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(
                        app.config['UPLOADED_VEGAN'])),
                                exist_ok=True)
                    # save document in app.config['UPLOADED_HALAL']
                    vegan.save(os.path.join(os.getcwd(), app.config[
                        'UPLOADED_VEGAN']) + veganFile)
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
                logging.info(
                    "read_cert: nothing found in database, starting empty")
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

    return render_template('admin/certification2.html', id=id,
                           certificate_list=certificate_list)


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
                os.makedirs(os.path.join(os.getcwd(), os.path.dirname(
                    app.config['UPLOADED_HYGIENE'])), exist_ok=True)
                hygiene.save(os.path.join(os.path.join(os.getcwd(), app.config[
                    'UPLOADED_HYGIENE']) + hygieneFile))
                if cert.hygiene_cert != '':
                    # unlinking existing hygiene doc file
                    if os.path.exists(cert.hygiene_cert):
                        os.remove(cert.hygiene_cert)
                        logging.info(
                            'Successfully removed existing hygiene document')
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
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(
                        app.config['UPLOADED_HALAL'])),
                                exist_ok=True)
                    halal.save(os.path.join(os.path.join(os.getcwd(),
                                                         app.config[
                                                             'UPLOADED_HALAL']) + halalFile))
                    # deleting of existing file
                    if os.path.exists(cert.halal_cert):
                        os.remove(cert.halal_cert)
                        logging.info(
                            'Successfully removed existing halal document')
                    cert.halal_cert = f"application/static/uploads/restaurantCertification/halal/{cert.id}/{halalFile}"

                # VEGETARIAN DOCUMENT
                vegetarian = request.files['vegetarianDocument']
                vegetarianFile = secure_filename(vegetarian.filename)
                if vegetarian.filename != '':
                    app.config[
                        'UPLOADED_VEGETARIAN'] = f'application/static/uploads/restaurantCertification/vegetarian/{cert.id}/'
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(
                        app.config['UPLOADED_VEGETARIAN'])),
                                exist_ok=True)
                    vegetarian.save(
                        os.path.join(os.path.join(os.getcwd(), app.config[
                            'UPLOADED_VEGETARIAN']) + vegetarianFile))
                    # deleting of existing file
                    if os.path.exists(cert.vegetarian_cert):
                        os.remove(cert.vegetarian_cert)
                        logging.info(
                            'Successfully removed existing vegetarian document')
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
                    os.makedirs(os.path.join(os.getcwd(), os.path.dirname(
                        app.config['UPLOADED_VEGAN'])),
                                exist_ok=True)
                    vegan.save(os.path.join(os.path.join(os.getcwd(),
                                                         app.config[
                                                             'UPLOADED_VEGAN']) + veganFile))
                    # deleting of existing file
                    if os.path.exists(cert.vegan_cert):
                        os.remove(cert.vegan_cert)
                        logging.info(
                            'Successfully removed existing vegan document')
                    cert.vegan_cert = f"application/static/uploads/restaurantCertification/vegan/{cert.id}/{veganFile}"
                else:
                    cert.vegan_cert = ''

                # writeback
                db['certification'] = certification_dict
        except Exception as e:
            logging.error(
                "Error in retrieving certificate from ""certification.db (%s)" % e)

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
            logging.error(
                "Error in retrieving certificate from ""certification.db (%s)" % e)

        c = certification_dict.get(id)
        id_list.append(c)
        print(c.hygiene_cert)
        return render_template('admin/updateCertification.html',
                               id_list=id_list)


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
