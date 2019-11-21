# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-21

from flask import Flask
from flask import render_template
from urllib.request import urlopen
import json

# create instance of class Flask
app = Flask(__name__)


@app.route("/")
def root():
    return "Hello World!"

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')



if __name__ == "__main__":
    app.debug = True
    app.run()