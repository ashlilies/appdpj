class Restaurant_controller():
    def find_user_by_id(self, id):
        db = shelve.open(DB_NAME, 'r')
        for i in db:
            if i.account_id == id:
                return i 