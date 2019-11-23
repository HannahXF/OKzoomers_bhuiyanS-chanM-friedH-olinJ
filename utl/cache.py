# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-19

# DATABASE FUNCTIONS FOR INTERACTION WITH *cache* TABLE

# importing the sqlite3 module to interface with sqlite databases
import sqlite3
from .db import _connects

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
                                 (player_id,))
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
                                 (player_id,))
        return [i for i in player_stats][0]
    except IndexError as error:
        print(error)
        return None