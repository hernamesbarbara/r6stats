#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""features.py
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn import preprocessing
from utils import r6io

def columns_for_stats(frame, subset=['progression', 'overall', 'casual', 'ranked']):
    cols = []
    columns = frame.columns.copy()
    columns = columns[columns.str.endswith('has_played')==False]
    for stats_type in subset:
        if stats_type == 'overall':
            cols += columns[columns.str.startswith('stats.overall')].tolist()
        if stats_type == 'progression':
            cols += columns[columns.str.startswith('stats.progression')].tolist()
        if stats_type == 'casual':
            cols += columns[columns.str.startswith('stats.casual')].tolist()
        if stats_type == 'ranked':
            cols += columns[columns.str.startswith('stats.ranked')].tolist()
    return columns[columns.isin(cols)]

def normalize_for_playtime(value, frame):
    value = value.copy()
    idx = value.index
    if value.name.startswith('stats.overall') or value.name.startswith('stats.progression'):
        playtime = frame.ix[idx, 'stats.overall.playtime']
    elif value.name.startswith('stats.ranked'):
        playtime = frame.ix[idx, 'stats.ranked.playtime']
    else:
        playtime = frame.ix[idx, 'stats.casual.playtime']
    return value / playtime

def combine_ranked_and_casual(frame, min_playtime=120):
    frame = frame.copy()
    frame['stats.overall.playtime'] = frame[['stats.casual.playtime','stats.ranked.playtime']].sum(1)

    # drop players who have played less than 2 hours
    frame = frame[frame['stats.overall.playtime']>=min_playtime]

    # combine stats from both game modes just to keep it simple
    frame['stats.overall.kills'] = frame[['stats.casual.kills','stats.ranked.kills']].sum(1)
    frame['stats.overall.deaths'] = frame[['stats.casual.deaths','stats.ranked.deaths']].sum(1)

    frame['stats.overall.losses'] = frame[['stats.casual.losses','stats.ranked.losses']].sum(1)
    frame['stats.overall.wins'] = frame[['stats.casual.wins','stats.ranked.wins']].sum(1)

    frame['stats.overall.kd'] = frame['stats.overall.kills'] / frame['stats.overall.deaths']
    frame['stats.overall.wlr'] = frame['stats.overall.wins'] / frame['stats.overall.losses']
    cols = [col for col in frame.columns if col.startswith('stats.overall') or col.startswith('stats.progression')]
    return frame[cols]


for platform in ('ps4', 'xone', 'uplay'):
    outfile = "./data/overall_stats_for_{}.csv".format(platform)

    df = r6io.read_player_csv('./data/leaderboard-pages.csv', platform)
    numbers = columns_for_stats(df)
    df_stats = df[numbers].copy()
    df_stats = df_stats.fillna(0)
    df_overall = combine_ranked_and_casual(df_stats)
    df_overall = df_overall.replace(np.inf,0)    
    df_overall.to_csv(outfile)
    print "saved {} rows to {}".format(len(df_overall), outfile)
