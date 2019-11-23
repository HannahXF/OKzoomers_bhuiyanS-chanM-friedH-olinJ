# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-19

# importing the sqlite3 module to interface with sqlite databases
import sqlite3

_DB_FILE = 'sportsball.db'

#===========================================================
# HELPER FUNCTIONS (private)

def _test():
    try:
        db = sqlite3.connect(_DB_FILE)
    except sqlite3.Error as error:
        print(error)

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

# Authenticates login info of a user
# Returns True if correct, False if not (or error)
@_connects
def auth_user(username, password, db=None):
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
def add_user(username, password, db=None):
    #=======================================================
    # TODO: Further testing required for this
    db.execute('''
                INSERT INTO users(username, password) 
                VALUES(?, ?);
               ''',
               (username, password))
    #=======================================================
    db.commit()
    return True

@_connects
def cache(player_id, json_info, json_stats, image, db=None):
    db.execute('''
                INSERT INTO cache 
                VALUES(?, ?, ?, ?);
               ''',
               (player_id, json_info, json_stats, image))
    db.commit()
    return True

@_connects
def get_info(player_id, db=None):
    try:
        player_info = db.execute('''
                                  SELECT json_info 
                                  FROM cache 
                                  WHERE player_id=?;
                                 ''', 
                                 (player_id))
        return [i for i in player_info][0]
    except IndexError as error:
        print(error)
        return None

@_connects
def get_stats(player_id, db=None):
    try:
        player_stats = db.execute('''
                                  SELECT json_stats 
                                  FROM cache 
                                  WHERE player_id=?;
                                 ''', 
                                 (player_id))
        return [i for i in player_stats][0]
    except IndexError as error:
        print(error)
        return None