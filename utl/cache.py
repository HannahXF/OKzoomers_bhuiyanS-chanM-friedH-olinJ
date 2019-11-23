# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-19

#=========================================================
# DATABASE FUNCTIONS FOR INTERACTION WITH *cache* TABLE
#=========================================================

# importing the sqlite3 module to interface with sqlite databases
import sqlite3
from .db import _connects

# Stores JSON data recieved from BallDontLie API and NBA Player API
# Optimizes API quota usage
# Returns True if successful, otherwise False
@_connects
def cache(player_id, json_info, json_stats, image, db=None):
    db.execute('''
                INSERT INTO cache 
                VALUES(?, ?, ?, ?);
               ''',
               (player_id, json_info, json_stats, image))
    db.commit()
    return True

# Gets the player information stored in the cache table
# "info" refers to the general player JSON info recieved from BallDontLie API
# Returns the string of the dictionary containing the data if successful, otherwise None
@_connects
def get_info(player_id, db=None):
    try:
        player_info = db.execute('''
                                  SELECT json_info 
                                  FROM cache 
                                  WHERE player_id=?;
                                 ''', 
                                 (player_id,))
        return [i for i in player_info][0]
    except IndexError as error:
        print(error)
        return None

# Gets the player statistics stored in the cache table
# "stats" refers to the average statistics JSON info recieved from BallDontLie API
# Returns the string of the dictionary containing the data if successful, otherwise None
@_connects
def get_stats(player_id, db=None):
    try:
        player_stats = db.execute('''
                                  SELECT json_stats 
                                  FROM cache 
                                  WHERE player_id=?;
                                 ''', 
                                 (player_id,))
        return [i for i in player_stats][0]
    except IndexError as error:
        print(error)
        return None