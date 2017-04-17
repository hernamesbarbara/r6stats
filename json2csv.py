#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""json2csv.py
"""
import sys
import os
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize, nested_to_record
from bandit import Bandit
try:
    import ujson as json
except ImportError:
    import json

pd.options.display.width = 200
pd.options.display.max_colwidth = 75

def read_jsonl(stream):
    for line in stream:
        try:
            yield json.loads(line)
        except:
            continue

def dump(data, stream):
    try:
        json.dump(data, stream)
        stream.write(os.linesep)
    except:
        pass

def read_nested_write_flat(infile, outfile):
    with open(infile, 'r') as infile:
        with open(outfile, 'a') as outfile:
            for record in read_jsonl(infile):
                dump(nested_to_record(record), outfile)

if __name__ == '__main__':
    infile = 'data/leaderboard-pages.jsonl'
    outfile = 'data/outfile.jsonl'

    # next line
    # CPU times: user 5min 59s, sys: 2.22 s, total: 6min 2s
    # Wall time: 6min 3s
    read_nested_write_flat(infile, outfile)
    
    # next line
    # CPU times: user 1min 14s, sys: 7.69 s, total: 1min 22s
    # Wall time: 1min 23s
    pd.read_json(outfile, lines=True).to_csv('data/outfile.csv', index=False, encoding='utf-8')

