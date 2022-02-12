# xu yong lin
import logging
import shelve


class Certification:
    def __init__(self, restaurant_id=None,hygiene_cert=None, halal_cert=None, vegetarian_cert=None, vegan_cert=None, noPorknoLard=None,
             noBeef=None):
        self.id = restaurant_id
        self.hygiene_cert = hygiene_cert
        self.halal_cert = halal_cert
        self.vegetarian_cert = vegetarian_cert
        self.vegan_cert = vegan_cert
        self.noPorknoLard = noPorknoLard
        self.noBeef = noBeef
