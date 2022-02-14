# Reviews
# Maximum of 5 stars, minimum of 1
# Ashlee (28 Jan 2021)
import logging
import shelve
from datetime import datetime

# from application.Models import ReviewAi
from application.Models import ReviewAi as ReviewAi
from application.Models.Account import Account
from application.Models.CountId import CountId
from application.Models.FileUpload import delete_file
from application.Models.RestaurantSystem import RestaurantSystem

REVIEWS_DB = "reviews.db"


class Review:
    count_id = 1
    TRUSTWORTHINESS_THRESHOLD = 60  # % before a review is considered trusted

    def __init__(self, parent_restaurant_id, reviewer_id, stars: int, title, description,
                 date_time: datetime, media_path: str):
        CountId.load(REVIEWS_DB, Review)
        self.id = Review.count_id
        Review.count_id += 1
        CountId.save(REVIEWS_DB, Review)

        self.parent_restaurant_id = parent_restaurant_id
        self.reviewer_id = reviewer_id
        self.stars = stars  # out of 5
        self.title = title
        self.description = description
        self.datetime = date_time
        self.media_path = media_path
        self.edited = False

    @property
    def reviewer_name(self):
        reviewer = Account.query(self.reviewer_id)
        name = "%s %s" % (reviewer.first_name, reviewer.last_name)
        return name

    # For easy retrieval on consumer my reviews
    @property
    def restaurant_name(self):
        restaurant = RestaurantSystem.find_restaurant_by_id(self.parent_restaurant_id)
        return restaurant.name

    # Returns a trustworthiness score of a review from 0.0 to 1.0.
    # 0 - untrustworthy (fake), 1 - trustworthy
    # Processes the description, or title if it doesn't exist.
    def trustworthiness(self):
        if self.description != "":
            return ReviewAi.predict(self.description)
        return ReviewAi.predict(self.title)

    def delete_untrustworthy(self):
        if self.trustworthiness() * 100 < Review.TRUSTWORTHINESS_THRESHOLD:
            ReviewDao.delete_review(self.id)
            return True
        return False


# Review Data Access Object
class ReviewDao:
    @staticmethod
    def create_review(restaurant_id, reviewer_id, stars: int, title: str, description: str,
                      date_time: datetime, media_path: str):
        review = Review(restaurant_id, reviewer_id, stars, title, description, date_time, media_path)
        ReviewDao.save(review)

    @staticmethod
    def update_review(review_id: int, stars: int, title: str, description: str, date_time: datetime,
                      media_path: str):
        review = ReviewDao.query(review_id)
        if review is None:
            raise ReviewIdNotExistsError

        if review.media_path != media_path:
            delete_file(review.media_path)
            review.media_path = media_path

        review.stars = stars
        review.title = title
        review.description = description
        review.datetime = date_time
        review.edited = True

        ReviewDao.save(review)

    @staticmethod
    def delete_review(review_id):
        review = ReviewDao.query(review_id)
        delete_file(review.media_path)

        try:
            with shelve.open(REVIEWS_DB, 'c') as db:
                review_dict = db["review"]
                review_dict.pop(review_id)
                db["review"] = review_dict
        except KeyError:
            logging.error("ReviewDao: Failed to delete food item")

    @staticmethod
    def get_reviews(restaurant_id):
        # Linear search and retun a list of review objects with matching restaurant ID
        review_list = []
        review_dict = {}

        with shelve.open(REVIEWS_DB, 'c') as db:
            if "review" in db:
                review_dict = db["review"]

        for k in review_dict:
            review = review_dict[k]
            if review.parent_restaurant_id == restaurant_id:
                review_list.append(review)

        return review_list

    @staticmethod
    def get_top_reviews(restaurant_id, count=None):
        # Linear search and retun the [count] most trustworthy reviews
        review_list = []
        review_dict = {}

        with shelve.open(REVIEWS_DB, 'c') as db:
            if "review" in db:
                review_dict = db["review"]

        for k in review_dict:
            review = review_dict[k]
            if review.parent_restaurant_id == restaurant_id:
                review_list.append(review)

        review_list.sort(key=lambda x: x.trustworthiness(), reverse=True)

        if count is not None:
            review_list = review_list[:count]
        return review_list

    @staticmethod
    def get_user_reviews(user_id):
        # Linear search and retun list of review objects with matching user ID
        review_list = []
        review_dict = {}

        with shelve.open(REVIEWS_DB, 'c') as db:
            if "review" in db:
                review_dict = db["review"]

        for k in review_dict:
            review = review_dict[k]
            if review.reviewer_id == user_id:
                review_list.append(review)

        return review_list

    @staticmethod
    def get_average_rating(restaurant_id):
        list_of_reviews = ReviewDao.get_reviews(restaurant_id)
        total_review_score = 0
        for review in list_of_reviews:
            total_review_score += review.stars

        if len(list_of_reviews) == 0:
            return 0
        return total_review_score / len(list_of_reviews)

    @staticmethod
    def save(review: Review):
        try:
            with shelve.open(REVIEWS_DB, 'c') as db:
                review_dict = {}
                if "review" in db:
                    review_dict = db["review"]
                review_dict[review.id] = review
                db["review"] = review_dict
        except KeyError:
            logging.error("ReviewDao: failed to save review dict")

    @staticmethod
    def query(review_id: int) -> "Review":
        try:
            with shelve.open(REVIEWS_DB, 'c') as db:
                if "review" in db:
                    review_dict = db["review"]
                    return review_dict[review_id]

        except KeyError:
            logging.error("Food: tried to query review_id %s but not found" % review_id)


class ReviewIdNotExistsError(Exception):
    pass
