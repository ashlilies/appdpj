# Ashlee
# AI for detecting fake reviews. At least 80% accurate.
# First run will take some time to learn 20k rows of data.

import pickle

# dataset_filename = "application/Models/review-ai/fake-reviews-dataset.csv"
import xgboost

# dataset_filename = "review-ai/fake-reviews-dataset.csv"
# XGB_CLASSIFIER_FILENAME = "xgb_classifier.model"
# TFIDF_VECTORIZER_FILENAME = 'tfidf_vectorizer.pickle'

dataset_filename = "application/Models/review-ai/restaurant_reviews_anonymized.csv"
XGB_CLASSIFIER_FILENAME = "xgb_classifier_model.pickle"
TFIDF_VECTORIZER_FILENAME = 'tfidf_vectorizer.pickle'


def learn():
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC

    from xgboost import XGBClassifier

    from sklearn.metrics import accuracy_score
    from sklearn.metrics import f1_score
    from sklearn.metrics import precision_score
    from sklearn.metrics import recall_score
    from sklearn.metrics import roc_auc_score
    from sklearn.metrics import auc
    from sklearn.metrics import roc_curve
    from sklearn.metrics import plot_confusion_matrix
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import classification_report

    def display_metrics(preds, y_true, display=True):
        accuracy = accuracy_score(y_true, preds)
        precision = precision_score(y_true, preds, average="macro")
        recall = recall_score(y_true, preds, average="macro")
        F1 = f1_score(y_true, preds, average="macro")

        if display:
            print("overall metrics")
            print("=================================")
            print("accuracy score: {}".format(accuracy))
            print("precision score: {}".format(precision))
            print("recall score: {}".format(recall))
            print("F1 score {}".format(F1))
            #     print("auc_roc score: {}".format(auc_roc))
            print("=================================")
            print("")
            print("metrics per class")
            print("=================================")
            print(classification_report(y_true, preds))
            print("=================================")
        else:
            return [accuracy, precision, recall, F1]

    df = pd.read_csv(dataset_filename, engine="python")
    df.head()

    df["Real"].value_counts()

    tfidf = TfidfVectorizer(stop_words="english", strip_accents="unicode")
    X = tfidf.fit_transform(df["Review"])
    Y = df["Real"].map({"0": 0, "1": 1})

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3,
                                                        random_state=101,
                                                        stratify=Y)

    xgb = XGBClassifier(n_jobs=-1, random_state=101)
    xgb.fit(x_train, y_train)
    preds = xgb.predict(x_test)

    display_metrics(preds, y_test)

    # Saving
    # xgb classifier
    xgb.save_model(XGB_CLASSIFIER_FILENAME)

    # Tfidf vectorizer
    outfile = open(TFIDF_VECTORIZER_FILENAME, 'wb')
    pickle.dump(tfidf, outfile)
    outfile.close()


# Returns a score of 0.0 to 1.0, 0 being fake, 1 being real
def predict(text):
    # Load all necessary models
    try:
        xgb = xgboost.Booster({"nthread": 4})
        xgb.load_model(XGB_CLASSIFIER_FILENAME)

        infile = open(TFIDF_VECTORIZER_FILENAME, 'rb')
        tfidf = pickle.load(infile, encoding='bytes')
    except:
        learn()
        return predict(text)

    X = tfidf.transform([text])
    preds = xgb.inplace_predict(X)
    preds = preds[0]
    return preds


if __name__ == "__main__":
    # learn()
    print(predict("We bing shilling"))
    print(predict("Good food."))
