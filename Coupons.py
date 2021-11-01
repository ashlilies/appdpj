class Coupons:
    def __init__(self, code, validity_period, quantity_left, valid_products):
        self.code = code
        self.validity_period = validity_period
        self.quantity_left = quantity_left
        self.valid_products = valid_products

    def set_code(self, code):
        self.code = code
