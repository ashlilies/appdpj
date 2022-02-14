# Provides easy, error-proof loading and saving of count_id, which is an int.
# Pass in target_class, with a class attribute 'count_id'
# Ashlee

import shelve


class CountId:
    # If id not saved in db, we don't change the target class's id
    @staticmethod
    def load(db_name: str, target_class):
        with shelve.open(db_name, 'c') as db:
            if "count_id" in db:
                target_class.count_id = db["count_id"]

    @staticmethod
    def save(db_name: str, target_class):
        with shelve.open(db_name, 'c') as db:
            db["count_id"] = target_class.count_id
