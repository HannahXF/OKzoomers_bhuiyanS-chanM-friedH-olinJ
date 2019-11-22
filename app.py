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
        # if either username or password is blank, flash error
        if request.args["username"] == "" or request.args["password"] == "":
            flash("Please do not leave any fields blank.")
        # else verify login via database function
        else:
            response = db.verify_login(request.args["username"],
                                       request.args["password"])
            # if username and password are verified, session is added and user is sent to home
            if response == "verified":
                session["username"] = request.args["username"]
                return redirect(url_for("home"))
            # else flash the response from database function
            else:
                flash(response)
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
        else:
            # else if the passwords don't match, flash error
            if request.args["password1"] != request.args["password2"]:
                flash("Passwords don't match.")
            else:
            # else if the passwords match, attempt to add to database
                response = db.add_login(request.args["username"],
                                                request.args["password1"])
                # if the username is unique, session is added and user is sent to home
                if response == "valid":
                    session["username"] = request.args["username"]
                    return redirect(url_for("home"))
                # else flash response
                else:
                    flash(response)
    # render register template
    return render_template('register.html')


@app.route("/home")
def home():
    return "Hello World!"


if __name__ == "__main__":
    app.debug = True
    app.run()