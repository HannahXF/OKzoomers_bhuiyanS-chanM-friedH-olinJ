# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-19

#============================================================
# DATABASE FUNCTIONS FOR GENERAL INTERACTION WITH DATABASE
#============================================================

# importing the sqlite3 module to interface with sqlite databases
import sqlite3

_DB_FILE = 'sportsball.db'

#===========================================================
# HELPER FUNCTIONS (private)

# Connects to the database file
# Passes the connected object to the wrapped function
# Returns the wrapped function if no SQLite error, otherwise False
def _connects(db_func):
    def establish_connection(*args, **kwargs):
        db = sqlite3.connect(_DB_FILE)
        try:
            return db_func(*args, **kwargs, db = db)
        except sqlite3.Error as error:
            print(error)
            return False
    return establish_connection

#===========================================================

# Creates necessary tables in the database
@_connects
def init(db=None):
    # initializing the users table
    # stores user login data
    db.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER UNIQUE PRIMARY KEY, 
                    username TEXT UNIQUE, 
                    password TEXT
               );''')
    # initializing the cards table
    # stores all cards that exist
    db.execute('''
                CREATE TABLE IF NOT EXISTS cards(
                    player_id INTEGER, 
                    user_id INTEGER,
                    rarity INTEGER
               );''')
    # initializing the cache table
    # stores data accessed from APIs to optimize quota usage
    db.execute('''
                CREATE TABLE IF NOT EXISTS cache(
                    player_id INTEGER UNIQUE PRIMARY KEY, 
                    json_info TEXT, 
                    json_stats TEXT, 
                    image TEXT
               );''')
    db.commit()
