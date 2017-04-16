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
    f = 'http://bandito.yhat.com/api/projects/hernamesbarbara/r6stats/jobs/leaderboards/8/output-files/leaderboard-pages.jsonl'
    o_jsonl = bandit.output_dir+os.path.basename(f).rsplit('.', 1)[0]+'.jsonl'
    o_csv = bandit.output_dir+os.path.basename(f).rsplit('.', 1)[0]+'.csv'
    print "read_nested_write_flat('{}', '{}')".format(f, o_jsonl)
    read_nested_write_flat(f, o_jsonl)
    print "writing csv"
    pd.read_json(o_jsonl, lines=True).to_csv(o_csv, index=False, encoding='utf-8')

