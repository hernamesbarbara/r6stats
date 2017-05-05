#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""io.py
"""
import sys
import os
import numpy as np
import pandas as pd
from pandas.io.json import nested_to_record
try:
    import ujson as json
except ImportError:
    import json

DATE_COLUMNS = ['indexed_at', 'updated_at']
DIMENSION_COLUMNS = ['platform', 'ubisoft_id', 'username', 'stats.ranked.has_played', 'stats.casual.has_played']

def read_jsonl_stream(stream):
    for line in stream:
        try:
            yield json.loads(line)
        except:
            continue

def dump_jsonl_stream(data, stream):
    try:
        json.dump(data, stream)
        stream.write(os.linesep)
    except:
        pass

def read_nested_write_flat(infile, outfile):
    with open(infile, 'r') as infile:
        with open(outfile, 'a') as outfile:
            for record in read_jsonl_stream(infile):
                dump_jsonl_stream(nested_to_record(record), outfile)
    print "saved records to {}".format(outfile.name)

def jsonl_to_csv(infile_jsonl, outfile_csv):
    pd.read_json(infile_jsonl, lines=True).to_csv(outfile_csv, index=False, encoding='utf-8')
    print "saved records to {}".format(outfile_csv)
    
def select_rows_by_platform(frame, platform):
    mask = frame['platform'].astype(str).fillna('NONE') == platform
    return frame[mask]

def select_stats_columns(frame):
    mask1 = frame.columns.str.startswith('stats.')
    mask2 = frame.columns.str.endswith('has_played')==False
    stats_cols = frame.columns[(mask1&mask2)]
    frame = frame.ix[:, stats_cols]
    return frame.astype(np.float64).fillna(0)

def has_playtime(frame, game_mode):
    mask1 = frame['stats.{}.playtime'.format(game_mode)].fillna(0)>0
    mask2 = frame['stats.{}.has_played'.format(game_mode)]==True
    return frame[(mask1&mask2)]

def read_player_csv(filename_or_dataframe, platform, game_mode=None):
    if isinstance(filename_or_dataframe, basestring):
        frame = pd.read_csv(filename_or_dataframe)
    else:
        frame = filename_or_dataframe
    df_platform = select_rows_by_platform(frame, platform)
    df_id_vars = df_platform[DIMENSION_COLUMNS].copy()
    df_dates = df_platform[DATE_COLUMNS].copy()
    df_dates.loc[:, DATE_COLUMNS] = df_dates[DATE_COLUMNS].copy().apply(pd.to_datetime)
    df_stats = select_stats_columns(df_platform)
    df = pd.concat([df_dates, df_id_vars, df_stats], axis=1)
    df['updated_at'] = df[DATE_COLUMNS].max(axis=1)
    df = df.drop(['indexed_at'], axis=1)
    df = df.sort_values(by=['username', 'updated_at'], ascending=[True, False])
    df = df.drop_duplicates(['username'])
    bools = df.columns[df.columns.str.endswith('has_played')]
    df[bools] = df[bools].astype(np.bool)
    if game_mode:
        if game_mode == 'ranked':
            # keep only ranked players with playtime. drop all casual columns.
            df = has_playtime(df, 'ranked')
            df = df.drop(df.columns[df.columns.str.contains("casual")], axis=1)
        else:
            # keep only casual players with playtime. drop all ranked columns.
            df = has_playtime(df, 'casual')
            df = df.drop(df.columns[df.columns.str.contains("ranked")], axis=1)
    return df





