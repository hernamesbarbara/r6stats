#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""json2csv.py
"""
import sys
import os
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize, nested_to_record
try:
    import ujson as json
except ImportError:
    import json

pd.options.display.width = 200
pd.options.display.max_colwidth = 75

def read_jsonl(filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            try:
                yield json.loads(line)
            except:
                continue

def write_flat_jsonl(data, outfile):
    with open(outfile, 'a') as o:
        try:
            json.dump(nested_to_record(data), o)
            o.write(os.linesep)
        except:
            pass

def read_nested_write_flat(infile, outfile):
    for i, rec in enumerate(read_jsonl(infile)):
        if i % 10000 == 0:
            print "{} done".format(i)
        write_flat_jsonl(rec, outfile)

if __name__ == '__main__':
    f = sys.argv[1]
    o = sys.argv[2]
    read_nested_write_flat(f, o)
    pd.read_json(o, lines=True).to_csv('data/outfile.csv', index=False, encoding='utf-8')



# %%time 
# %run json2csv.py data/leaderboard-pages.jsonl data/leaderboard-pages2.jsonl
