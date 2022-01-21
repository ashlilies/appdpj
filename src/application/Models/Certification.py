# xu yong lin
# Consists of: create, read, update, delete of restaurant certifications
import logging
import pickle
import shelve
import uuid

DB_CERT = 'certification'


class Certification:
    def __init__(self, id):
        # with shelve.open('certification', 'c') as db:
        #     try:
        #         Certification.count_id = db['certification_id_count']
        #     except Exception as e:
        #         logging.error("certification_id_count: error reading from db (%s)" % e)
        self.restaurant_id = id
        self.hygiene_cert = ''
        self.halal_cert = ''
        self.vegetarian_cert = ''
        self.vegan_cert = ''
        self.noPorknoLard = ''
        self.noBeef = ''

        # #  database access in Models not Controller
        # with shelve.open('certification', 'c') as handle:
        #     handle['certification_id_count'] = Certification.count_id

    # query db for a cert item by passing in the id
    def query(self, id):
        with shelve.open('certification', 'c') as handle:
            try:
                certification_dict = handle['certification']
                return certification_dict[str(id)]
            except Exception as e:
                print(e)
                logging.error('Certificate: tried to query id %s but not found' % id)
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
def create_res_cert(restaurant_id, hygiene_c, halal_c, vegetarian_c, vegan_c, noporknolard, nobeef):
    # create new class object
    res = Certification(restaurant_id)
    res.hygiene_cert = hygiene_c
    res.halal_cert = halal_c
    res.vegetarian_cert = vegetarian_c
    res.vegan_cert = vegan_c
    res.noPorknoLard = noporknolard
    res.noBeef = nobeef
    with shelve.open(DB_CERT, 'c') as res_db:
        try:
            res_db['certification'] = res
            logging.info('create_res_cert: successfully created object')
        except Exception as e:
            logging.error('create_res_cert: fail to access db (%s)' % e)


# read cert
def read_res_cert():
    cert_array = []
    with shelve.open(DB_CERT, 'c') as res_db:
        try:
            cert_array = res_db['certification']
            print('existing:', cert_array)
            logging.info('read_res_cert: reading from db')
            # if 'certification' in res_db:
            #     cert_dict = res_db[restaurant_id]
            #     print('existing', cert_dict)
            # else:
            #     res_db[restaurant_id] = cert_dict
            #     logging.info('read_res_cert: nothing found in db, starting empty')
        except Exception as e:
            logging.error('read_res_cert: fail to read from db (%s)' % e)

    return cert_array

# update cert


# delete cert
