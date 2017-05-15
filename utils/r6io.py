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
    pd.read_json(infile_jsonl, lines=True)\
        .to_csv(outfile_csv, index=False, encoding='utf-8')
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



