#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""cleancsv.py
"""
import os
import sys
import numpy as np
import pandas as pd

pd.options.display.width = 180
pd.options.display.max_colwidth = 80
pd.options.display.max_columns = 60
pd.options.display.max_rows = 200

def ensure_uniform_colnames(frame):
    colmap = {
        'ubisoft_id': 'player.ubisoft_id', 
        'username': 'player.username',
        'platform': 'player.platform',
        'stats.ranked.has_played': 'player.ranked.has_played',
        'stats.casual.has_played': 'player.casual.has_played',
        'indexed_at': 'meta.indexed_at',
        'updated_at': 'meta.updated_at'
    }

    frame = frame.rename(columns=colmap)
    frame = frame.loc[:, sorted(frame.columns)]
    return frame

def add_overall_totals(frame):
    for col in ["deaths", "kills", "losses", "playtime", "wins"]:
        ranked_colname = "stats.ranked.{}".format(col)
        casual_colname = "stats.casual.{}".format(col)
        overall_colname = "stats.overall.{}".format(col)
        frame[overall_colname] = frame[ranked_colname].add(frame[casual_colname], fill_value=0.0)
    frame['stats.overall.games_played'] = frame['stats.overall.wins']+frame['stats.overall.losses']
    frame['stats.overall.wlr'] = frame['stats.overall.wins'].fillna(0) / frame['stats.overall.losses'].fillna(0)
    return frame.loc[:, sorted(frame.columns)]

def drop_rows_with_low_playtime(frame, min_playtime_in_sec=86400):
    return frame.drop(frame[frame['stats.overall.playtime']<min_playtime_in_sec].index, axis=0)

def drop_rows_with_negative_stats(frame):
    stats_cols = frame.columns[frame.columns.str.startswith('stats.')]
    n_negs_per_column = frame[stats_cols].lt(0).sum()

    cols_with_negs = n_negs_per_column[n_negs_per_column>0].index

    rows_with_negs = (frame[(frame[cols_with_negs] < 0).any(axis=1)]).index
    frame = frame.drop(rows_with_negs)
    return frame

def drop_duplicate_players(frame):
    order_by = ['player.ubisoft_id', 'stats.overall.playtime']
    frame = frame.sort_values(by=order_by, ascending=[True, False])
    frame = frame.drop_duplicates('player.ubisoft_id')
    return frame

############
infile = sys.argv[1]
outfile = sys.argv[2]

f_name, _ = os.path.splitext(infile)

print("Reading {}".format(infile))
df = pd.read_csv(infile, parse_dates=['indexed_at', 'updated_at'])

print("nrow: {}".format(len(df)))
print("ncol: {}".format(len(df.columns)))

print('renaming columns to common convention')
df = ensure_uniform_colnames(df)
print('summing up player stats')
df = add_overall_totals(df)

print('dropping rows with low playtime')
df = drop_rows_with_low_playtime(df)

print('dropping rows with invalid negatives stats values')
df = drop_rows_with_negative_stats(df)

print('dropping duplicate players')
df = drop_duplicate_players(df)

print("nrow: {}".format(len(df)))
print("ncol: {}".format(len(df.columns)))

print('writing {}'.format(outfile))
df.to_csv(outfile, index=False, encoding='utf-8')

