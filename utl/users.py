# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-19

#=========================================================
# DATABASE FUNCTIONS FOR INTERACTION WITH *users* TABLE
#=========================================================

# importing the sqlite3 module to interface with sqlite databases
import sqlite3
from .db import _connects

# Authenticates login info of a user
# Returns True if correct, False if not (or error)
@_connects
def auth(username, password, db=None):
    try:
        userData = db.execute('''
                               SELECT password 
                               FROM users 
                               WHERE username=?;
                              ''', 
                              (username,))
        return password == [i for i in userData][0][0]
    except IndexError as error:
        print(error)
        return False

# Adds login info for a new user
# Checks if username is unique
# Returns True if successful, otherwise False
@_connects
def add(username, password, db=None):
    db.execute('''
                INSERT INTO users(username, password) 
                VALUES(?, ?);
               ''',
               (username, password))
    db.commit()
    return True

# Authenticates login info of a user
# Returns True if correct, False if not (or error)
@_connects
def identify(username, db=None):
    try:
        userData = db.execute('''
                               SELECT user_id 
                               FROM users 
                               WHERE username=?;
                              ''', 
                              (username,))
        return [i for i in userData][0][0]
    except IndexError as error:
        print(error)
        return None