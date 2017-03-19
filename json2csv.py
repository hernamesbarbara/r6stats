#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""json2csv.py
"""
import sys
import os
import json
import pandas as pd
from pandas.io.json import json_normaliz

pd.options.display.width = 200
pd.options.display.max_colwidth = 75

def read_json(filename):
    return json.load(open(filename, 'r'))

pages = read_json('pages.json')
all_players = []

for i, page in enumerate(pages):
    if i % 10 == 0:
        print "{} of {}".format(i+1, len(pages))
    meta = page['meta']
    players = page['players']
    for player in players:
        player.update(meta)
        all_players.append(player)

df_players = json_normalize(all_players)
df_players.to_csv('players.csv', sep=',', encoding='utf-8', index=False)


