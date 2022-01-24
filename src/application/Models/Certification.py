# xu yong lin
# Consists of: create, read, update, delete of restaurant certifications
import logging
import pickle
import shelve
import uuid

DB_CERT = 'certification'


class Certification:
    def __init__(self, id: str,
                 hygiene_cert=None, halal_cert=None, vegetarian_cert=None, vegan_cert=None,
                 noPorknoLard=None, noBeef=None):
        self.restaurant_id = id
        with shelve.open(DB_CERT, 'c') as db:
            self.restaurant_id = db['restaurant_id']
        self.hygiene_cert = hygiene_cert
        self.halal_cert = halal_cert
        self.vegetarian_cert = vegetarian_cert
        self.vegan_cert = vegan_cert
        self.noPorknoLard = noPorknoLard
        self.noBeef = noBeef
        self.certificates = {}

        with shelve.open(DB_CERT, 'c') as db:
            db['restaurant_id'] = self.restaurant_id
            cert_systems_dict = {}
            if 'cert_systems_dict' in db:
                cert_systems_dict = db['cert_systems_dict']
            cert_systems_dict[self.restaurant_id] = self
            db['cert_systems_dict'] = cert_systems_dict

    def create_res_cert(self, restaurant_id, hygiene_c, halal_c, vegetarian_c, vegan_c,
                        noporknolard, nobeef):
        self.certificates[restaurant_id] = Certification(restaurant_id, hygiene_c, halal_c, vegetarian_c, vegan_c,
                                                         noporknolard, nobeef)
        with shelve.open(DB_CERT, 'c') as cert_db:
            try:
                cert_systems_dict = {}
                if "cert_systems_dict" in cert_db:
                    cert_systems_dict = cert_db["cert_systems_dict"]

                cert_systems_dict[self.restaurant_id] = self
                cert_db["cert_systems_dict"] = cert_systems_dict

                logging.info('create_res_cert: successfully created object')
            except Exception as e:
                logging.error('create_res_cert: fail to access db (%s)' % e)

    # read cert
    def read_res_cert(self, restaurant_id):
        with shelve.open(DB_CERT, 'c') as cert_db:
            try:
                if "cert_systems_dict" in cert_db:
                    certification_dict = cert_db["cert_systems_dict"]
                    print(certification_dict)
                    return certification_dict[restaurant_id]
                logging.info('read_res_cert: reading from db')

            except Exception as e:
                logging.error('read_res_cert: fail to read from db (%s)' % e)
        return None

    def get_certs(self, restaurant_id):
        cert_list = []
        for cert in self.certificates:
            c = self.certificates[cert]
            cert_list.append(c)
        return cert_list

    # todo: update cert
    def update_res_cert(self, restaurant_id, hygiene_c, halal_c, vegetarian_c, vegan_c,
                        noporknolard, nobeef):
        pass

    # todo: delete cert
    def delete_certificate(self ,id):
        # with shelve.open(DB_CERT, 'c') as cert_db:
        #     try:
        #         certification_dict = cert_db["certification"]
        #         if id in certification_dict:
        #             certification_dict.pop(id)
        #         cert_db["certification"] = certification_dict
        #     except Exception as e:
        #         logging.error("delete_cert: error in opening db (%s)" % e)
        pass

    # query db for a cert item by passing in the id
    @staticmethod
    def query(id):
        # 'cert_systems_dict' not id DB_CERT, DB_CERT EMPTY
        with shelve.open(DB_CERT, 'c') as db:
            if 'cert_systems_dict' in db:
                cert_systems_dict = db['cert_systems_dict']
                print(cert_systems_dict)
                return cert_systems_dict.get(id)
            else:
                db['cert_systems_dict']
        return None
            # try:
            #     if 'cert_systems_dict' in db:
            #         cert_systems_dict = db['cert_systems_dict']
            #         return cert_systems_dict.get(id, None)
            # except Exception as e:
            #     print(e)
            #     logging.error(
            #         'Certificate: tried to query id %s but not found' % id)
            #     return None


