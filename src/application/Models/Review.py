import shelve
from datetime import datetime

from application.Models.CountId import CountId

REVIEWS_DB = "reviews.db"


class Review:
    count_id = 1
    def __init__(self, title, description, datetime: datetime):
        CountId.load(REVIEWS_DB, Review)
        self.count_id = Review.count_id
        Review.count_id += 1

        self.title = title
        self.description = description
        self.datetime = datetime
        CountId.save(REVIEWS_DB, Review)
