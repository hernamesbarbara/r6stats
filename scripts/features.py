#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""clean_raw_csv.py - read raw csv data and cast columns to the right types
and save the output to another csv file.
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

pd.options.display.width = 180
pd.options.display.max_colwidth = 80
pd.options.display.max_columns = 60
pd.options.display.max_rows = 200

def scale_series(series):
    series = series.copy().astype(float).fillna(series.mean())
    values_scaled = StandardScaler().fit_transform(series.values.reshape(-1,1))
    name = series.name
    return pd.Series(values_scaled[:,0], name=name+'.scaled')

def normalize_series(series):
    name = series.name
    series = series.copy().astype(float).fillna(series.mean())
    series = preprocessing.normalize(series.values.reshape(1,-1))[0,:]
    return pd.Series(series, name=name+'.normed')

def draw_sample(frame, nrows):
    "return a random sample frame a dataframe"
    return frame.sample(n=nrows, axis=0)

def calc_balance(team_A, team_B):
    team_A_games_played = team_A['stats.overall.games_played']
    team_B_games_played = team_B['stats.overall.games_played']

    team_A_kills = team_A['stats.overall.kills']
    team_B_kills = team_B['stats.overall.kills']
    team_A_sum_avg_kills_per_game = (team_A_kills / team_A_games_played).sum()
    team_B_sum_avg_kills_per_game = (team_B_kills / team_B_games_played).sum()

    delta_kills = team_B_sum_avg_kills_per_game - team_A_sum_avg_kills_per_game 
    max_kills = np.max((team_A_sum_avg_kills_per_game, team_B_sum_avg_kills_per_game))
    balance = delta_kills/max_kills
    return balance


infile = sys.argv[1]
outfile = sys.argv[2]

f_name, _ = os.path.splitext(infile)

print("Reading {}".format(infile))
df = pd.read_csv(infile, parse_dates=['meta.indexed_at', 'meta.updated_at'])
print("nrow: {}".format(len(df)))
print("ncol: {}".format(len(df.columns)))

balances = []

for i in range(10000):
    players_pool = draw_sample(df, 10)
    team_A = players_pool.iloc[:5]
    team_B = players_pool.iloc[5:]
    balance = calc_balance(team_A, team_B)
    balances.append(balance)

balances = pd.Series(balances, name='balance')

balances.hist(bins=75); plt.show()
