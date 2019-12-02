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
def _info(player_id):
    return json.loads(urlopen(f'https://www.balldontlie.io/api/v1/players/{player_id}').read())

# Gets the player stats from the BallDontLie API
# Returns the string of the JSON dictionary
def _stats(player_id):
    return json.loads(urlopen(f'https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]={player_id}').read())

# Gets the player image from the NBA Player API
# Returns the image link
def _image(player_id, info):
    first_name = info['first_name'].replace(' ', '_')
    last_name = info['last_name'].replace(' ', '_')
    return (f'https://nba-players.herokuapp.com/players/{last_name}/{first_name}')

# Organizes the cache data needed
# Returns a dictionary of the necessary columns in the cache table
def cache_data(player_id):
    player_info=_info(player_id)
    player_stats=_stats(player_id)
    image=_image(player_id, player_info)

    data = dict()
    data['first_name'] = player_info['first_name']
    data['last_name']  = player_info['last_name']
    data['team']       = player_info['team']['full_name']
    data['avg_pts']    = player_stats['data'][0]['pts']
    data['image']      = image
    return data