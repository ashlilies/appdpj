# xu yong lin

class Certification:
    def __init__(self, hygiene_cert, halal, noPork_noLard, vegetarian, vegan, noBeef):
        self.hygiene_cert = hygiene_cert
        self.halal = halal

        self.noPork_noLard = noPork_noLard
        self.vegetarian = vegetarian
        self.vegan = vegan
        self.noBeef = noBeef

    def set_halal_certified(self,halal):
        self.halal = halal

