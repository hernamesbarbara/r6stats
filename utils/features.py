#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""features.py
"""
import os
import sys
import numpy as np
import pandas as pd
from utils import r6io

DATA_TYPES = {
    "ubisoft_id": np.unicode,
    "stats.overall.bullets_hit": np.int64,
    "stats.ranked.deaths": np.int64,
    "stats.progression.level": np.int64,
    "stats.casual.wlr": np.float64,
    "stats.overall.penetration_kills": np.int64,
    "updated_at": pd.to_datetime,
    "stats.ranked.losses": np.int64,
    "stats.overall.melee_kills": np.int64,
    "stats.casual.has_played": np.bool,
    "stats.overall.bullets_fired": np.int64,
    "stats.ranked.wins": np.int64,
    "stats.overall.headshots": np.int64,
    "indexed_at": pd.to_datetime,
    "stats.ranked.kd": np.float64,
    "platform": np.unicode,
    "stats.ranked.wlr": np.float64,
    "username": np.unicode,
    "stats.overall.revives": np.int64,
    "stats.casual.playtime": np.int64,
    "stats.casual.wins": np.float64,
    "stats.progression.xp": np.int64,
    "stats.ranked.playtime": np.int64,
    "stats.overall.assists": np.int64,
    "stats.overall.barricades_built": np.int64,
    "stats.casual.losses": np.int64,
    "stats.casual.kills": np.int64,
    "stats.casual.deaths": np.int64,
    "stats.overall.suicides": np.int64,
    "stats.overall.reinforcements_deployed": np.int64,
    "stats.casual.kd": np.float64,
    "stats.overall.steps_moved": np.int64,
    "stats.ranked.kills": np.int64,
    "stats.ranked.has_played": np.bool
}

def add_overall_totals(frame):
    frame = frame.fillna(0)
    frame = frame.replace(np.inf, 0)
    frame['stats.overall.playtime.hours'] = (frame[['stats.casual.playtime', 'stats.ranked.playtime']].sum(1)) / 60. / 60.
    frame['stats.overall.steps_moved'] = frame['stats.overall.steps_moved'].abs()
    frame['stats.overall.kills'] = frame[['stats.ranked.kills', 'stats.casual.kills']].sum(1).astype(np.int64)
    frame['stats.overall.deaths'] = frame[['stats.ranked.deaths', 'stats.casual.deaths']].sum(1).astype(np.int64)
    frame['stats.overall.wins'] = frame[['stats.ranked.wins', 'stats.casual.wins']].sum(1).astype(np.int64)
    frame['stats.overall.losses'] = frame[['stats.ranked.losses', 'stats.casual.losses']].sum(1).astype(np.int64)
    frame['stats.overall.points'] = frame[['stats.overall.assists', 'stats.overall.kills']].sum(1).astype(np.int64)
    defensive_actions = ['stats.overall.reinforcements_deployed', 'stats.overall.revives', 'stats.overall.barricades_built']
    frame['stats.overall.defensive_actions'] = frame[defensive_actions].sum(1).astype(np.int64)

    frame['stats.overall.engagements'] = frame[['stats.overall.kills', 'stats.overall.deaths']].sum(1)

    frame['stats.normalized.accuracy'] = frame['stats.overall.bullets_hit'] / frame['stats.overall.bullets_fired']
    frame['stats.normalized.points.perhour'] = frame['stats.overall.points'] / frame['stats.overall.playtime.hours']
    frame['stats.normalized.deaths.perhour'] = frame['stats.overall.deaths'] / frame['stats.overall.playtime.hours']
    frame['stats.normalized.kills.perhour'] = frame['stats.overall.kills'] / frame['stats.overall.playtime.hours']
    frame['stats.normalized.wins.perhour'] = frame['stats.overall.wins'] / frame['stats.overall.playtime.hours']
    frame['stats.normalized.losses.perhour'] = frame['stats.overall.losses'] / frame['stats.overall.playtime.hours']

    mask = (frame['stats.overall.kills']>0) & (frame['stats.overall.deaths']==0)
    frame['stats.normalized.kd'] = np.where(mask, 1.0, frame['stats.overall.kills'] / frame['stats.overall.deaths'])

    mask = (frame['stats.overall.wins']>0) & (frame['stats.overall.losses']==0)
    frame['stats.normalized.wlr'] = np.where(mask, 1.0, frame['stats.overall.wins'] / frame['stats.overall.losses'])

    frame['stats.normalized.defensive_actions.perhour'] = \
        frame['stats.overall.defensive_actions'] / frame['stats.overall.playtime.hours']

    frame['stats.normalized.points.perbullet_fired'] = \
        frame['stats.overall.points'] / frame['stats.overall.bullets_fired']

    frame['stats.normalized.aggression'] = \
        frame['stats.overall.points'] / frame['stats.overall.engagements']
    
    frame['stats.normalized.mobility'] = \
        frame['stats.overall.engagements'] / (frame['stats.overall.steps_moved'].abs() / frame['stats.overall.playtime.hours'])
    frame = frame.ix[:,frame.columns.sort_values()]
    return frame

def fillna_and_apply(series, func, na_value=0):
    series = series.fillna(na_value)
    return series.apply(func)

def drop_players_with_low_playtime(frame, min_hours=24.0, copy=True):
    if copy:
        frame = frame.copy()
        return frame[frame['stats.overall.playtime.hours']>=min_hours]
    else:
        frame = frame[frame['stats.overall.playtime.hours']>=min_hours]
        return frame

def get_features_dataframe(frame, verbose=False):
    nrow = len(frame)
    if verbose:
        print "Casting columns to data types"
    for col in frame.columns:
        func = DATA_TYPES[col]
        frame[col] = fillna_and_apply(frame[col], func, na_value=0)
    if verbose:
        print "Adding overall sums for each metric"
    frame = add_overall_totals(frame)
    frame = drop_players_with_low_playtime(frame)
    if verbose:
        print "Dropped {} rows with low playtime".format(nrow-len(frame))
    return frame

if __name__ == '__main__':
    """
    In [3]: %time %run features.py data/leaderboard-pages.csv
    Reading data/leaderboard-pages.csv
    Casting columns to data types
    Adding overall sums for each metric
    Dropped 49155 rows with low playtime
    Saved 723121 rows to data/leaderboard-pages-features.csv
    CPU times: user 3min 17s, sys: 6.14 s, total: 3min 23s
    Wall time: 3min 23s
    """
    infile = sys.argv[1]
    f_name, _ = os.path.splitext(infile)
    outfile = "{}-features.csv".format(f_name)
    print "Reading {}".format(infile)
    df = pd.read_csv(infile)
    df = get_features_dataframe(df, verbose=True)
    # df.to_csv(outfile, index=True, encoding='utf-8')
    # print "Saved {} rows to {}".format(len(df), outfile)
