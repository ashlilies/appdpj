# Ruri
from application.Models.Account import save_db

class Restaurant:
    def __init__(self, name, contact, open, close, add1, add2, postc, desc, bank, del1, del2, del3, del4, del5, tags=None):
        self.name = name
        self.contact = contact
        self.open = open
        self.close = close
        self.add1 = add1
        self.add2 = add2
        self.postc = postc
        self.bank = bank
        self.desc = desc
        self.del1 = del1
        self.del2 = del2
        self.del3 = del3
        self.del4 = del4
        self.del5 = del5
        self.tags = tags

        save_db()

    # def get_name(self):
    #     return self.name
    # 
    # def set_name(self,name):
    #     self.name = name
