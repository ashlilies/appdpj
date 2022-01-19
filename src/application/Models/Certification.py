# xu yong lin

class Certification:
    count_id = 1

    def __init__(self, hygiene_cert=None):
        self.id = Certification.count_id
        self.hygiene_cert = hygiene_cert
        # self.halal_cert = halal_cert
        # self.vegetarian_cert = vegetarian_cert
        # self.vegan_cert = vegan_cert
        # self.noPorknoLard = noPorknoLard
        # self.noBeef = noBeef
        Certification.count_id += 1
