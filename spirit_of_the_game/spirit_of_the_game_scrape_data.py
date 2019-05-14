
# coding: utf-8

# # Scrape data
# This notebook scrapes data from ebuc 2019 tournament and saves them into json file.
# 
# The data is from this page: http://live.ebuc2019.org/results
# 
# Format of the data is dictionary with the form {team name: list of matches of that team}.

import requests as rq
import bs4
import json
from collections import defaultdict

urls=["http://live.ebuc2019.org/results/---201905{:0>2d}----".format(i) for i in [6,7,8,9,10,11]]
pages=[bs4.BeautifulSoup(rq.get(url).content) for url in urls]

team_results=defaultdict(list)
for page in pages:
    table=page.find("tbody")
    rows=table.findAll("tr")
    for r in rows:
        columns=r.findAll("td")
        players=[columns[i].attrs["title"] for i in [2,4]]
        scores= [int(i) for i in [columns[3].text.split()[j] for j in [0,2]]]
        spirit=[[int(j) for j in columns[i].text.split("+")] for i in [7,8]]
        division=columns[1].find(attrs="nomo").text
        #print(players,scores,spirit_strs,division)
        for j in [0,1]:
            team_results[players[j]].append({"score":scores[j],
                                             "oponent_score":scores[0 if j==1 else 1],
                                             "spirit":spirit[j],
                                             "oponent_spirit":spirit[0 if j==1 else 1],
                                             "division":division,
                                             "oponent":players[0 if j==1 else 1]})
            
with open("ebuc_team_results.json", "w") as write_file:
    json.dump(team_results, write_file)
