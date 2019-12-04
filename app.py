# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-21

import os
import random
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from utl import db, users, cards, players
from urllib.request import urlopen
import json


# create instance of class Flask
app = Flask(__name__)

# set up sessions with random secret key
app.secret_key = os.urandom(32)     # for deployment
# app.secret_key = "OKZoomers"      # for debugging


db.init()


#=====DECORATOR=FUNCTIONS===================================================
# Decorator functions to eliminate redundancy:

# Login checking
def protected(route_function):
    def login_check(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    login_check.__name__ = route_function.__name__
    return login_check

#============================================================================


# root redirects to login if the user isn't logged in, and home if they are
@app.route("/")
def root():
    # if user is logged in, redirect to home
    if "username" in session:
        return redirect(url_for("home"))
    # else redirect to login
    return redirect(url_for("login"))


# login page and authentication of login
@app.route("/login")
def login():
    # if user is logged in, redirect to home
    if "username" in session:
        return redirect(url_for("home"))
    # if users attempts login
    if len(request.args) >= 2:
        # if inputted login info is correct, adds user to session and redirects to home
        if users.auth(request.args["username"], request.args["password"]):
            session["username"] = request.args["username"]
            return redirect(url_for("home"))
        # else flashes error message and redirects back to login
        else:
            flash("Incorrect username or password, please check spelling and captilization.")
    # render login template
    return render_template("login.html")


# register page and validation
@app.route("/register")
def register():
    # if user is logged in, redirect to home
    if "username" in session:
        return redirect(url_for("home"))
    # if user attempts registration
    if len(request.args) >= 3:
        # if any one of the three fields are blank, flash error
        if request.args["username"] == "" or request.args["password1"] == "" or request.args["password2"] == "":
            flash("Please do not leave any fields blank.")
        # if the passwords don't match, flash error
        if request.args["password1"] != request.args["password2"]:
            flash("Passwords don't match.")
        # else if adding the user (to the database) is successful, username must be unique
        elif users.add(request.args["username"], request.args["password1"]):
            # if the username is unique, session is added and user is redirected to home
            session["username"] = request.args["username"]
            return redirect(url_for("home"))
        # else flash error
        else:
            flash("Username not unique.")
    # render register template
    return render_template('register.html')


# logout will pop username from the session and redirect to login
@app.route("/logout")
@protected
def logout():
    # if user is logged in
    if "username" in session:
        # pop "username" from session
        session.pop("username")
    # redirect user back to login page
    return redirect(url_for("login"))


# information about the project - what? how? etc.
@app.route("/home")
@protected
def home():
    return render_template("home.html")


# logged in user's inventory of cards
@app.route("/inventory")
@protected
def inventory():
    user_id = users.identify(session["username"])
    user_cards = cards.owned(user_id)
    print("User's Inventory: ")
    print(user_cards)
    cards_data = list()
    for card in user_cards:
        player_id = card[0]
        cards_data.append(tuple((players.data(player_id), card[1])))
    return render_template("inventory.html",
                            inventory = cards_data)


# trivia page
@app.route("/trivia")
@protected
def trivia():
    trivia = getTrivia() # list of 10 sets of questions and answer choices
    return render_template("trivia.html",
                            questionSets=trivia)


# rewards page
@app.route("/rewards", methods=["POST"])
@protected
def rewards():
    numCorrect = 0
    # user's answer choices from trivia
    choices = request.form.getlist("choices")
    # for each question
    for question in range(10):
        # if the answer choice is correct
        if choices[question] == "correct":
            # add one to the total number correct
            numCorrect += 1
    playerCards = list()
    if numCorrect > 4:
        # generates numCorrect amount of reward cards
        newCards = cards.generate(users.identify(session["username"]), numCorrect)
        # creates appropriate player cards for the rewards
        for card in newCards:
            player_id = card[0]
            playerCards.append(tuple((players.data(player_id), card[1])))
    return render_template("rewards.html",
                            numCorrect=numCorrect,
                            rewardCards=playerCards)


# test page to give cards
@app.route("/test")
@protected
def test():
    newCards = cards.generate(users.identify(session["username"]), 10)
    print("Generated Test Cards: ")
    print(newCards)
    return "Done?"


#=====HELPER=FUNCTIONS=======================================================
# Functions to facilitate API usage:

# returns 10 trivia questions with all relevant information
def getTrivia():
    api_call = urlopen("https://opentdb.com/api.php?amount=10&category=21&type=multiple")
    response = api_call.read()
    data = json.loads(response)
    data = data["results"]
    trivia = []
    questionNum = 0
    while questionNum < 10:
        questionSet = []
        questionSet.append(data[questionNum]["question"])
        questionSet.append(data[questionNum]["correct_answer"])
        questionSet.append(data[questionNum]["incorrect_answers"][0])
        questionSet.append(data[questionNum]["incorrect_answers"][1])
        questionSet.append(data[questionNum]["incorrect_answers"][2])
        trivia.append(questionSet)
        questionNum += 1
    return trivia

#get photo of a searched player from balldontlie
def getPhoto(idnum):
    api_call = urlopen("https://www.balldontlie.io/api/v1/players/" + idnum)
    response = api_call.read()
    data = json.loads(response)
    firstName = correct(data["first_name"])
    lastName = correct(data["last_name"])

    imgsrc = "https://nba-players.herokuapp.com/players/" + lastName + "/" + first_name
    return imgsrc

#make sure the names of players are easily manipulated
def correct(name):
    while "." in name:
        rem = name.index('.')
        name = name[0:rem] + name[rem+1:len(name)]
    while " " in name:
        rem = name.index(' ')
        name = name[0:rem] + "_"

#create rarity spread for rewards
def createSpread(num):
    list = [1,1,1,1,1]
    i = 0
    while i < num:
        j = random.randint(0,4)
        if list[j] <= 5:
            list[j] +=1
            i += 1
    return list

#============================================================================


if __name__ == "__main__":
    app.debug = True
    app.run()
