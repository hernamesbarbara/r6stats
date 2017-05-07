#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""features.py
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn import preprocessing

stats = [
    'stats.casual.kpm', 
    'stats.casual.dpm', 
    'stats.casual.wpm', 
    'stats.casual.lpm', 
    'stats.ranked.kpm', 
    'stats.ranked.dpm', 
    'stats.ranked.wpm', 
    'stats.ranked.lpm'
]

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

def calc_total_playtime(frame):
    cols = [col for col in frame.columns if 'playtime' in col]
    return pd.Series(frame[cols].sum(1), name='stats.overall.playtime')

def normalize_for_playtime(value, frame):
    idx = value.index
    if value.name.startswith('stats.overall') or value.name.startswith('stats.progression'):
        playtime = frame.ix[idx, ['stats.casual.playtime', 'stats.ranked.playtime']].sum(1)
    elif value.name.startswith('stats.ranked'):
        playtime = frame.ix[idx, 'stats.ranked.playtime']
    else:
        playtime = frame.ix[idx, 'stats.casual.playtime']
    return (value/playtime).replace(np.inf, 0)
