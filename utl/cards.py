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

#return a list of information to be used in card rendering
@_connects
def generate(user_id, player_ids, num_cards, db=None):
    newCards = list()
    for i in range(num_cards):
        player = random.choice(player_ids)
        cache(player)
        rarity = random.randint(1,3)

        db.execute('''
                    INSERT INTO cards
                    VALUES(?, ?, ?);
                   ''',
                   (player, user_id, rarity))

        cardTuple = tuple((player, rarity))
        newCards.append(cardTuple)
    db.commit()
    return newCards
