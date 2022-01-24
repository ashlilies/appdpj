# xu yong lin
import logging
import shelve


class Certification:
    count_id = 1

    def __init__(self, hygiene_cert=None, halal_cert=None, vegetarian_cert=None, vegan_cert=None, noPorknoLard=None,
             noBeef=None):
        with shelve.open('certification', 'c') as db:
            try:
                Certification.count_id = db['certification_id_count']
            except Exception as e:
                logging.info("certification_id_count: error reading from db (%s)" % e)

        self.id = Certification.count_id
        self.hygiene_cert = hygiene_cert
        self.halal_cert = halal_cert
        self.vegetarian_cert = vegetarian_cert
        self.vegan_cert = vegan_cert
        self.noPorknoLard = noPorknoLard
        self.noBeef = noBeef

        Certification.count_id += 1
        with shelve.open('certification', 'c') as db:
            db['certification_id_count'] = Certification.count_id

    def query(self, id):
        with shelve.open('certification', 'c') as handle:
            try:
                certification_dict = handle['certification']
                return certification_dict[str(id)]
            except Exception as e:
                print(e)
                return None
