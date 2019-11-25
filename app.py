# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-21

import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from utl import db, users, cache
from urllib.request import urlopen
import json


# create instance of class Flask
app = Flask(__name__)
# set up sessions with random secret key
app.secret_key = os.urandom(32)


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
    return render_template("inventory.html")


# trivia page
@app.route("/trivia")
@protected
def trivia():
    list = getQuestion("medium")
    return render_template("trivia.html")


# rewards page
@app.route("/rewards")
@protected
def rewards():
    return render_template("rewards.html")


#=====HELPER=FUNCTIONS=======================================================
# Functions to facilitate API usage:

# Gets info of a given player with their ID
# Only accesses API if the player data is not already cached
# Returns a string of the entire JSON dictionary
def player_info(player_id):
    # if the player id is not already cached, access the API and return the data recieved as a string
    if not in_cache(player_id):
        url = urlopen('https://www.balldontlie.io/api/v1/players/' + player_id)
        # returns the JSON dictionary as a string
        return url.read()
    else:
        return cache.get_info(player_id)

# Gets stats of a given player with their ID
# Only accesses API if the player data is not already cached
# Returns a string of the entire JSON dictionary
def player_stats(player_id):
    # if the player id is not already cached, access the API and return the data recieved as a string
    if not in_cache(player_id):
        url = urlopen('https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]=' + player_id)
        # returns the JSON dictionary as a string
        return url.read()
    else:
        return cache.get_stats(player_id)

def getQuestion(difficulty):
    u = urlopen(
    "https://opentdb.com/api.php?amount=1&category=21&type=multiple&difficulty=" + difficulty
    )

    response = u.read()
    data = json.loads(response)
    return [data[0]["question"],data[0]["correct_answer"],data[0]["incorrect_answer"][0],data[0]["incorrect_answer"][1],data[0]["incorrect_answer"][2]]

def getPPG(playerid):
    u = urlopen(
    "https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]=" + playerid
    )

    response = u.read()
    data = json.loads(response)
    return data[0]["pts"]

def getImage(playedid):
    u = urlopen(
    "https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]=" + playerid"
    )

    response = u.read()
    data = json.loads(response)
    firstname = data[0]["first_name"]
    lastname = data[0]["last_name"]
    return "https://nba-players.herokuapp.com/players/" + lastname + "/" + firstname

#============================================================================


if __name__ == "__main__":
    app.debug = True
    app.run()
