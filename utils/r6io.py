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

ID_COLUMNS = ['platform', 'ubisoft_id', 'username']

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


def _get_row_mask_for_platform(frame, platform):
    return frame['platform'].astype(str).fillna('NONE') == platform

def _get_col_mask_for_game_mode_stats(frame, game_mode=""):
    mask1 = frame.columns.str.startswith('stats.{}'.format(game_mode))
    mask2 = frame.columns.str.startswith('stats.overall')
    mask3 = frame.columns.str.endswith('has_played')==False
    return frame.columns[ (mask1|mask2) & (mask3)]
    
def select_rows_by_platform(frame, platform):
    return frame[_get_row_mask_for_platform(frame, platform)]

def select_stats_columns_by_game_mode(frame, game_mode=""):
    frame = frame.ix[:,_get_col_mask_for_game_mode_stats(frame, game_mode)]
    return frame.astype(np.float64)

def read_player_csv(filename_or_dataframe, platform, game_mode):

    if isinstance(filename_or_dataframe, basestring):
        df = pd.read_csv(filename_or_dataframe)
    else:
        df = filename_or_dataframe
    df_platform = select_rows_by_platform(df, platform)
    df_id_vars = df_platform[ID_COLUMNS].copy()
    df_dates = df_platform[DATE_COLUMNS].copy()
    df_dates.loc[:, DATE_COLUMNS] = df_dates[DATE_COLUMNS].copy().apply(pd.to_datetime)
    df_stats = select_stats_columns_by_game_mode(df_platform, game_mode)
    return pd.concat([df_dates, df_id_vars, df_stats], axis=1)


