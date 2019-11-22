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
from utl import db
from urllib.request import urlopen
import json


# create instance of class Flask
app = Flask(__name__)
# set up sessions with random secret key
app.secret_key = os.urandom(32)


@app.route("/")
def root():
    # if user is logged in, redirect to home
    if "username" in session:
        return redirect(url_for("home"))
    # else redirect to login
    return redirect(url_for("login"))


@app.route("/login")
def login():
    # if user is logged in, redirect to home
    if "username" in session:
        return redirect(url_for("home"))
    # if users attempts login
    if len(request.args) == 2:
        # if inputted login info is correct, adds user to session and redirects to home
        if db.auth_user(request.args["username"], request.args["password"]):
            session["username"] = request.args["username"]
            return redirect(url_for("home"))
        # else flashes error message and redirects back to login
        else:
            flash("Incorrect username or password, please check spelling and captilization.")
    # render login template
    return render_template("login.html")


@app.route("/register")
def register():
    # if user is logged in, redirect to home
    if "username" in session:
        return redirect(url_for("home"))
    # if user attempts registration
    if len(request.args) == 3:
         # if any one of the three fields are blank, flash error
        if request.args["username"] == "" or request.args["password1"] == "" or request.args["password2"] == "":
            flash("Please do not leave any fields blank.")
        # else if the passwords don't match, flash error
        elif request.args["password1"] != request.args["password2"]:
            flash("Passwords don't match.")
        # else if adding the user (to the database) is successful, username must be unique
        elif db.add_user(request.args["username"], request.args["password1"]):
            # if the username is unique, session is added and user is redirected to home
            session["username"] = request.args["username"]
            return redirect(url_for("home"))
        # else flash error
        else:
            flash("Username not unique.")
    # render register template
    return render_template('register.html')


@app.route("/home")
def home():
    return "Hello World!"


#=====HELPER=FUNCTIONS=======================================================
# functions to facilitate API usage:

# Gets info of a given player with their ID
# Only accesses API if the player data is not already cached
# Returns a string of the entire JSON dictionary
def player_info(player_id):
    # if the player id is not already cached, access the API and return the data recieved as a string
    if not in_cache(player_id):
        url = urlopen("https://www.balldontlie.io/api/v1/players/" + player_id)
        # returns the JSON dictionary as a string
        return url.read()
    else:
        return db.get_info(player_id)

# Gets stats of a given player with their ID
# Only accesses API if the player data is not already cached
# Returns a string of the entire JSON dictionary
def player_stats(player_id):
    # if the player id is not already cached, access the API and return the data recieved as a string
    if not in_cache(player_id):
        url = urlopen("https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]=" + player_id)
        # returns the JSON dictionary as a string
        return url.read()
    else:
        return db.get_stats(player_id)

#============================================================================


if __name__ == "__main__":
    app.debug = True
    app.run()