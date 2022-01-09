# xu yong lin

class Certification:
    count_id = 1

    def __init__(self, hygiene_cert=None, halal_cert=None, vegetarian_cert=None, vegan_cert=None):
        self.hygiene_cert = hygiene_cert
        self.halal_cert = halal_cert
        self.vegetarian_cert = vegetarian_cert
        self.vegan_cert = vegan_cert
        Certification.count_id += 1

    def get_hygiene_cert(self):
        return self.hygiene_cert