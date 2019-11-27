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
import json
from .api import api

# Checks if the info for a player is in the cache
# Returns true if in the cache, otherwise False
@_connects
def contains(player_id, db=None):
    player = db.execute('''
                         SELECT player_id 
                         FROM cache 
                         WHERE player_id=?;
                        ''', 
                        (player_id,))
    return len(player) != 0

# Stores JSON data recieved from BallDontLie API and NBA Player API
# Optimizes API quota usage
# Returns True if successful, otherwise False
@_connects
def cache(player_id, image, db=None):
    if contains(player_id):
        return False
    json_info = api.info(player_id)
    json_stats = api.stats(player_id)
    image = api.image(player_id, json_info)

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
def info(player_id, db=None):
    cache(player_id)
    player_info = db.execute('''
                              SELECT json_info 
                              RROM cache 
                              WHERE player_id=?;
                             ''', 
                             (player_id,))
    return [i for i in player_info][0][0]

# Gets the player statistics stored in the cache table
# "stats" refers to the average statistics JSON info recieved from BallDontLie API
# Returns the string of the dictionary containing the data if successful, otherwise None
@_connects
def stats(player_id, db=None):
    cache(player_id)
    player_stats = db.execute('''
                               SELECT json_stats 
                               FROM cache 
                               WHERE player_id=?;
                              ''', 
                              (player_id,))
    return [i for i in player_stats][0][0]

# Gets the image of a player given their ID
@_connects
def image(player_id, db=None):
    cache(player_id)
    player_image = db.execute('''
                               SELECT image 
                               FROM cache 
                               WHERE player_id=?;
                              ''', 
                              (player_id,))
    return [i for i in player_image][0][0]



# Gets the name of a player given their ID
def _name(player_id, db=None):
    info = json.loads(info(player_id))
    return info['first_name'] + ' ' + info['last_name']

# Gets the team name of a player given their ID
def _team(player_id, db=None):
    info = json.loads(info(player_id))
    return info['team']['full_name']

# Gets the average points per game in the season of a player given their ID
def _points(player_id, db=None):
    stats = json.loads(stats(player_id))
    return stats['pts']