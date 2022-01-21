# xu yong lin
# Consists of: create, read, update, delete of restaurant certifications
import logging
import pickle
import shelve
import uuid

DB_CERT = 'certification'


class Certification:
    def __init__(self, id):
        self.restaurant_id = id
        self.hygiene_cert = ''
        self.halal_cert = ''
        self.vegetarian_cert = ''
        self.vegan_cert = ''
        self.noPorknoLard = ''
        self.noBeef = ''

    # query db for a cert item by passing in the id
    def query(self, id):
        with shelve.open('certification', 'c') as handle:
            try:
                certification_dict = handle['certification']
                return certification_dict[str(id)]
            except Exception as e:
                print(e)
                logging.error(
                    'Certificate: tried to query id %s but not found' % id)
                return None


# blogs = shelve.open('blog')
#
# def create_blog(username, title, body):
#     id = str(uuid.uuid4())
#     blog = Blog(id)
#     blog.title = title
#     blog.username = username
#     blog.body = body
#     blog.created = str(date.today())
#     blogs[id] = blog


# create cert
def create_res_cert(restaurant_id, hygiene_c, halal_c, vegetarian_c, vegan_c,
                    noporknolard, nobeef):
    # create new class object
    cert = Certification(restaurant_id)
    cert.hygiene_cert = hygiene_c
    cert.halal_cert = halal_c
    cert.vegetarian_cert = vegetarian_c
    cert.vegan_cert = vegan_c
    cert.noPorknoLard = noporknolard
    cert.noBeef = nobeef

    with shelve.open(DB_CERT, 'c') as cert_db:
        try:
            certification_dict = {}
            if "certification" in cert_db:
                certification_dict = cert_db["certification"]
            certification_dict[cert.restaurant_id] = cert
            cert_db["certification"] = certification_dict

            logging.info('create_res_cert: successfully created object')
        except Exception as e:
            logging.error('create_res_cert: fail to access db (%s)' % e)


# read cert
def read_res_cert(restaurant_id):
    with shelve.open(DB_CERT, 'c') as cert_db:
        try:
            if "certification" in cert_db:
                certification_dict = cert_db["certification"]
                return certification_dict[restaurant_id]

            logging.info('read_res_cert: reading from db')

        except Exception as e:
            logging.error('read_res_cert: fail to read from db (%s)' % e)

    return None

# update cert


# delete cert
