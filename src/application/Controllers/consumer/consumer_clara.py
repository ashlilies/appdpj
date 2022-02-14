from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from application import app
from flask import request
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# from chatbot import chatbot
# from chatterbot.trainers import ListTrainer


# <------------------------ CLARA ------------------------------>
from application.Controllers.admin.admin_ashlee import admin_side
from application.Controllers.consumer.consumer_ashlee import consumer_side
from application.Models.Food2 import FoodDao
#
# english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")
#
#
# @app.route("/chatbot")
# def bot():
#     return render_template("consumer/chatbot.html")
#
# @app.route("/get")
# def get_bot_response():
#     userText = request.args.get("msg")
#     return str(english_bot.get_response(userText))
#




@app.route("/foodModal/<int:food_id>")
#displaying of food
@consumer_side
@login_required
def consumer_retrieve_food_modal(food_id):
    #retrieve the food created from FoodDao
    #using the currernt users restaurant_id
    food = FoodDao.query(food_id)
    return render_template('consumer/foodModal.html', food=food)


