#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""json2csv.py
"""
import sys
import os
import json
import pandas as pd
from pandas.io.json import json_normalize

pd.options.display.width = 200
pd.options.display.max_colwidth = 75

def read_json(filename):
    return json.load(open(filename, 'r'))

all_players = []
for leaderboard in ('casual', 'ranked', 'general'):
    print "*"*80
    print leaderboard.upper()
    print "*"*80
    pages = read_json('data/{}-success.json'.format(leaderboard))
    for i, page in enumerate(pages):
        if i % 10 == 0:
            print "{} of {}".format(i+1, len(pages))
        meta = page['meta']
        players = page['players']
        for player in players:
            player.update(meta)
            all_players.append(player)

df_players = json_normalize(all_players)
outfile = 'data/players.csv'
df_players.to_csv(outfile, sep=',', encoding='utf-8', index=False)

print "Saved {} rows to {}".format(len(df_players), outfile)

