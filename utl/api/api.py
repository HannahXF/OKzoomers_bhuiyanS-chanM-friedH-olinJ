# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-19

#=======================================
# FUNCTIONS FOR INTERACTION WITH APIS
#=======================================

from urllib.request import urlopen
import json

# Gets the player info from the BallDontLie API
# Returns the string of the JSON dictionary
def info(player_id):
    return urlopen(f'https://www.balldontlie.io/api/v1/players/{player_id}').read()

# Gets the player stats from the BallDontLie API
# Returns the string of the JSON dictionary
def stats(player_id):
    return urlopen(f'https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]={player_id}').read()

# Gets the player image from the NBA Player API
# Returns the image link
def image(player_id, info):
    info = json.loads(info)
    first_name = info['first_name'].replace(' ', '_')
    last_name = info['last_name'].replace(' ', '_')
    # TODO: test getting the image
    return urlopen(f'https://nba-players.herokuapp.com/players{last_name}/{first_name}').read()

