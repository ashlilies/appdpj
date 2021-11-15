from flask import Flask, render_template

app = Flask(__name__)


# Global variables
BRAND_NAME = "FoodFinder"  # The name of our app


@app.route('/')
def index():  # put application's code here
    return render_template("index.html", BRAND_NAME=BRAND_NAME)


if __name__ == '__main__':
    app.run(debug=True)
