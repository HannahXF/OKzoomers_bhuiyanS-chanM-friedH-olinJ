# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-19

#=========================================================
# DATABASE FUNCTIONS FOR INTERACTION WITH *cards* TABLE
#=========================================================

# importing the sqlite3 module to interface with sqlite databases
import sqlite3
from .db import _connects
from .players import cache
import random

# Gets a list of the cards owned by a certain user based on ID
# Each card entry will be a tuple in the following format, (<player_id>, rarity)
# Returns the list of cards owned
@_connects
def owned(user_id, db=None):
    try:
        cards = db.execute('''
                            SELECT player_id, rarity
                            FROM cards
                            WHERE user_id=?;
                           ''',
                           (user_id,))
        return [i for i in cards]
    except IndexError as error:
        print(error)
        return list()

# Generates a specified amount of cards owned by a specific given user
# Will cache players generated and store each card in the cards table
# Returns the new cards generated
@_connects
def generate(user_id, num_cards, db=None):
    newCards = list()
    for i in range(num_cards):
        player = random.choice(valid_ids())
        cache(player)
        rarity = random.choices(
                                population = (1  ,2  ,3  ),
                                weights =    (0.6,0.3,0.1)
                               )

        db.execute('''
                    INSERT INTO cards
                    VALUES(?, ?, ?);
                   ''',
                   (player, user_id, rarity))

        cardTuple = tuple((player, rarity))
        newCards.append(cardTuple)
    db.commit()
    return newCards

# Reads the data stored in ids.txt
# Converts items to integers and returns the list of ids
def valid_ids():
    ids = open('utl/api/ids.txt', 'r')
    ids = ids.readlines()
    ids = [int(player_id) for player_id in ids]
    return ids