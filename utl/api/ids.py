# Team OKzoomers -- Saad Bhuiyan, Matthew Chan, Hannah Fried, Jacob Olin
# SoftDev1 pd2
# P01 -- ArRESTed Development
# 2019-11-19

#=====================================================================
# A SCRIPT TO DETERMINE THE LIST OF VALID PLAYER IDS IN 2017 SEASON
# ONLY RAN ONCE TO GENERATE ids.txt
#=====================================================================

from urllib.request import urlopen
import json
import time

totalPages = json.loads(urlopen('https://www.balldontlie.io/api/v1/players?per_page=100&page=1000').read())['meta']['total_pages']

for currentPage in range(1,totalPages+1):
    print("Current Page: " + str(currentPage))
    # https://www.balldontlie.io/api/v1/players?per_page=100&page=1
    # https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]={237,1,2,3,4,5}
    players = json.loads(urlopen(f'https://www.balldontlie.io/api/v1/players?per_page=100&page={currentPage}').read())
    ids = '{'
    for player in players['data']:
        ids += str(player['id']) + ','
    ids = ids[:-1] + '}'
    
    print(f'https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]={ids}')
    file = open('ids.txt', 'a+')
    players2017 = json.loads(urlopen(f'https://www.balldontlie.io/api/v1/season_averages?season=2017&player_ids[]={ids}').read())
    for validPlayer in players2017['data']:
        file.write(str(validPlayer['player_id']) + '\n')
    
    
file.close()