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
from .api import api

# Checks if the info for a player is in the cache
# Returns true if in the cache, otherwise False
@_connects
def _cached(player_id, db=None):
    player = db.execute('''
                         SELECT player_id 
                         FROM cache 
                         WHERE player_id=?;
                        ''', 
                        (player_id,))
    return len([i for i in player]) != 0

# Stores necessary data recieved from APIs
# Optimizes API quota usage by checking if players have already been cached
# Returns True if successful, otherwise False
@_connects
def cache(player_id, db=None):
    if _cached(player_id):
        return False
    data = api.cache_data(player_id)
    db.execute('''
                INSERT INTO cache 
                VALUES(?, ?, ?, ?, ?, ?);
               ''',
               (player_id, 
                data['first_name'], 
                data['last_name'], 
                data['team'], 
                data['avg_pts'], 
                data['image']
               ))
    db.commit()
    return True

# Gets all player information stored in the cache table
# Assures the player is cached so index errors cannot occur
# Returns a dictionary of the data if successful=
@_connects
def data(player_id, db=None):
    cache(player_id)
    player_data = db.execute('''
                              SELECT *
                              FROM cache 
                              WHERE player_id=?;
                             ''', 
                             (player_id,))
    player_data = [i for i in player_data][0]
    
    data = dict()
    data['player_id']  = player_data[0]
    data['first_name'] = player_data[1]
    data['last_name']  = player_data[2]
    data['team']       = player_data[3]
    data['avg_pts']    = player_data[4]
    data['image']      = player_data[5]
    return data
